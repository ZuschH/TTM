import json
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import tmm_monitor
from tmm_monitor import Collector, Database, Device, PollStats, PortRecoveryRequired, ProtocolError, Register, add_derived_samples, configured_devices, configured_registers, crc16, parameter_backup_files, parameter_safety_class, parse_pcm_template, parse_read_response, parse_read_responses, parse_write_response, pcm_display_value, pcm_template_matches_model, process_channels_request, process_engineering_request, process_parameter_backup_request, process_parameter_preflight_request, process_parameter_write_request, process_recording_request, read_request, write_request
from tmm_decode import decode_metric, enrich_sample
from tmm_web_data import MonitorRepository


class ProtocolTests(unittest.TestCase):
    def test_manual_word_write_request_and_response(self):
        request = write_request(1, 0x0014, 6000)
        self.assertEqual(request[:6], bytes.fromhex("01 06 00 14 17 70"))
        parse_write_response(request, 1, 0x0014, 6000)
    def test_manual_fd00_request(self):
        self.assertEqual(read_request(1, 0xFD00), bytes.fromhex("01 03 FD 00 00 01 B5 A6"))

    def test_manual_60_hz_response(self):
        response = bytes.fromhex("01 03 02 17 70 B6 50")
        self.assertEqual(parse_read_response(response, 1), 6000)

    def test_multi_register_request_and_response(self):
        request = read_request(1, 0xFD00, 2)
        self.assertEqual(request[:6], bytes.fromhex("01 03 FD 00 00 02"))
        payload = bytes.fromhex("01 03 04 17 70 04 00")
        response = payload + crc16(payload).to_bytes(2, "little")
        self.assertEqual(parse_read_responses(response, 1, 2), [6000, 1024])

    def test_bad_crc_is_rejected(self):
        with self.assertRaisesRegex(ProtocolError, "CRC"):
            parse_read_response(bytes.fromhex("01 03 02 17 70 00 00"), 1)

    def test_exception_is_reported(self):
        payload = bytes.fromhex("01 83 02")
        response = payload + crc16(payload).to_bytes(2, "little")
        with self.assertRaisesRegex(ProtocolError, "0x02"):
            parse_read_response(response, 1)

    def test_collector_groups_nearby_registers(self):
        class FakeSerial:
            def __init__(self, **_kwargs):
                self.is_open = True
                self.requests = []
                self.response = b""

            def reset_input_buffer(self):
                pass

            def write(self, request):
                self.requests.append(request)
                count = int.from_bytes(request[4:6], "big")
                payload = bytes((1, 3, count * 2)) + b"".join(value.to_bytes(2, "big") for value in range(100, 100 + count))
                self.response = payload + crc16(payload).to_bytes(2, "little")

            def flush(self):
                pass

            def read(self, _count):
                return self.response

            def close(self):
                self.is_open = False

        ports = []

        def factory(**kwargs):
            port = FakeSerial(**kwargs)
            ports.append(port)
            return port

        collector = Collector({"serial": {"device": "fake", "baudrate": 38400}, "polling": {}}, factory)
        registers = [Register("a", 0xFD00, 1, "raw", "fast"), Register("b", 0xFD03, 1, "raw", "fast")]
        samples, errors, stats = collector.poll(Device("test", "VF-AS3J", 1, registers, max_read_words=8), registers)
        self.assertEqual(errors, [])
        self.assertEqual([raw for _register, raw in samples], [100, 103])
        self.assertEqual(len(ports[0].requests), 1)
        self.assertEqual(ports[0].requests[0][4:6], b"\x00\x04")
        self.assertEqual(stats.transactions, 1)
        self.assertEqual(stats.retries, 0)
        self.assertGreater(stats.estimated_bus_ms, 0)

    def test_modbus_exception_keeps_serial_port_open_for_next_group(self):
        class FakeSerial:
            def __init__(self, **_kwargs):
                self.is_open = True
                self.response = b""
                self.requests = 0

            def reset_input_buffer(self):
                pass

            def write(self, request):
                self.requests += 1
                if self.requests == 1:
                    payload = bytes((1, 0x83, 0x03))
                else:
                    payload = bytes((1, 0x03, 0x02, 0x12, 0x34))
                self.response = payload + crc16(payload).to_bytes(2, "little")

            def flush(self):
                pass

            def read(self, _count):
                return self.response

            def close(self):
                self.is_open = False

        ports = []

        def factory(**kwargs):
            port = FakeSerial(**kwargs)
            ports.append(port)
            return port

        collector = Collector({"serial": {"device": "COM3", "baudrate": 19200}, "polling": {"retries": 2}}, factory)
        registers = [Register("unsupported", 0xFC90, 1, "raw"), Register("supported", 0xFD00, 1, "raw")]
        samples, errors, stats = collector.poll(Device("test", "VF-AS1", 1, registers), registers)

        self.assertEqual(len(ports), 1)
        self.assertTrue(ports[0].is_open)
        self.assertEqual([(register.key, raw) for register, raw in samples], [("supported", 0x1234)])
        self.assertIn("Modbus exception 0x03", errors[0])
        self.assertEqual(stats.retries, 0)

    def test_repeated_windows_access_denied_requests_service_restart(self):
        def denied_factory(**_kwargs):
            raise Exception("could not open port 'COM3': Access is denied")

        collector = Collector({
            "serial": {"device": "COM3", "baudrate": 19200},
            "polling": {"windows_access_denied_restart_after": 2},
        }, denied_factory)
        with patch.object(tmm_monitor.os, "name", "nt"):
            with self.assertRaisesRegex(Exception, "Access is denied"):
                collector.connect()
            with self.assertRaisesRegex(PortRecoveryRequired, "requesting service restart"):
                collector.connect()


class ConfigurationTests(unittest.TestCase):
    def test_parameter_import_safety_classes(self):
        self.assertEqual(parameter_safety_class(0x0014, 1, "VF-AS1"), "candidate")
        self.assertEqual(parameter_safety_class(0x0800, 0, "VF-AS1"), "communication")
        self.assertEqual(parameter_safety_class(0x0792, 0, "VF-AS1"), "special")
        self.assertEqual(parameter_safety_class(0xFD00, 1, "VF-AS1"), "monitor")
        self.assertEqual(parameter_safety_class(0x0257, 1, "VF-AS1"), "unsupported")
    def test_pcm002z_template_parser(self):
        content = "###\r\nVFAS1\r\n-4037PL\r\nV170\r\nEnglish\r\nNo Comments.\r\n0\r\n17\r\n0000,0,0,1\r\nF792,10,0,0\r\n"
        header, records = parse_pcm_template(content)
        self.assertEqual(header[1:4], ["VFAS1", "-4037PL", "V170"])
        self.assertEqual(records, [(0x0000, 0, 0, 1), (0xF792, 10, 0, 0)])

    def test_pcm_template_model_family_must_match(self):
        header = ["###", "VFAS1", "-4037PL", "V170", "English", "No Comments.", "0", "17"]
        self.assertTrue(pcm_template_matches_model(header, "VF-AS1"))
        self.assertFalse(pcm_template_matches_model(header, "VF-S15"))

    def test_parameter_backups_are_scoped_to_one_inverter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "drive-20260101-000001.pcm").write_text("x")
            (root / "drive-20260102-000001.pcm").write_text("x")
            (root / "drive-2-20260103-000001.pcm").write_text("x")
            self.assertEqual([item.name for item in parameter_backup_files(root, "drive")], [
                "drive-20260102-000001.pcm", "drive-20260101-000001.pcm",
            ])

    def test_pcm002z_signed_decimal_convention_is_preserved(self):
        self.assertEqual(pcm_display_value(-15, 0xFFF1), -15)
        self.assertEqual(pcm_display_value(0, 0xFFF1), 0xFFF1)

    def test_parameter_backup_preserves_pcm_flags_and_uses_fresh_values(self):
        class FakeCollector:
            def poll(self, _device, registers):
                return [(register, register.address + 1) for register in registers], [], PollStats()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); request = root / "parameter-backup-request.json"; output = root / "backups"
            content = "###\r\nVFAS1\r\n-4037PL\r\nV170\r\nEnglish\r\nNo Comments.\r\n0\r\n17\r\n0000,0,0,1\r\nF792,10,0,0\r\n"
            request.write_text(json.dumps({"inverter": "drive", "content": content}), encoding="utf-8")
            device = Device("drive", "VF-AS1", 1, [])
            process_parameter_backup_request(FakeCollector(), [device], request, output)
            result = json.loads((root / "parameter-backup-result.json").read_text(encoding="utf-8"))
            saved = (output / result["file"]).read_bytes()
            self.assertIn(b"0000,1,0,1\r\n", saved)
            self.assertIn(b"F792,63379,0,0\r\n", saved)

    def test_parameter_backup_retains_template_value_for_unsupported_register(self):
        class PartialCollector:
            def poll(self, _device, registers):
                return [(registers[0], 7)], ["parameter_F792 (0xF792-0xF792): Modbus exception 0x02"], PollStats()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); request = root / "parameter-backup-request.json"; output = root / "backups"
            content = "###\r\nVFAS1\r\n-4037PL\r\nV170\r\nEnglish\r\nNo Comments.\r\n0\r\n17\r\n0000,0,0,1\r\nF792,10,0,0\r\n"
            request.write_text(json.dumps({"inverter": "drive", "content": content}), encoding="utf-8")
            process_parameter_backup_request(PartialCollector(), [Device("drive", "VF-AS1", 1, [])], request, output)
            result = json.loads((root / "parameter-backup-result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "complete_with_warnings")
            self.assertEqual((result["refreshed_records"], result["retained_records"]), (1, 1))
            self.assertIn(b"F792,10,0,0\r\n", (output / result["file"]).read_bytes())
            self.assertTrue((output / result["report"]).is_file())
    def test_channel_modes_disable_polling_or_history(self):
        device = configured_devices({"inverters": [{
            "name": "drive", "model": "VF-AS1", "slave_id": 1,
            "channels": {"output_voltage": "off", "output_current": "live", "operating_status": "off"},
        }]})[0]
        registers = {register.key: register for register in device.registers}
        self.assertNotIn("output_voltage", registers)
        self.assertFalse(registers["output_current"].record_history)
        self.assertTrue(registers["operating_status"].record_history)

    def test_hidden_live_card_keeps_recording_enabled(self):
        device = configured_devices({"inverters": [{
            "name": "drive", "model": "VF-AS1", "slave_id": 1,
            "hidden_live_cards": ["output_current"],
        }]})[0]
        registers = {register.key: register for register in device.registers}
        self.assertIn("output_current", registers)
        self.assertTrue(registers["output_current"].record_history)

    def test_alert_monitors_remain_polled_when_channel_is_off(self):
        device = configured_devices({"inverters": [{
            "name": "drive", "model": "VF-AS1", "slave_id": 1,
            "channels": {"alarm_information_1": "off", "output_current": "off"},
        }]})[0]
        registers = {register.key: register for register in device.registers}
        self.assertIn("alarm_information_1", registers)
        self.assertIn("output_current", registers)
        self.assertFalse(registers["alarm_information_1"].record_history)
        self.assertFalse(registers["output_current"].record_history)

    def test_invalid_channel_mode_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid channel mode"):
            configured_devices({"inverters": [{
                "name": "drive", "model": "VF-AS1", "slave_id": 1,
                "channels": {"output_voltage": "sometimes"},
            }]})
    def test_hex_register_address(self):
        registers = configured_registers({"registers": [{"key": "frequency", "address": "0xFD00"}]})
        self.assertEqual(registers[0].address, 0xFD00)

    def test_multi_device_profiles(self):
        devices = configured_devices({
            "inverters": [
                {"name": "drive-1", "model": "VF-AS1", "slave_id": 1},
                {"name": "drive-2", "model": "VF-S15", "slave_id": 2},
                {"name": "disabled", "model": "VF-AS3J", "slave_id": 3, "enabled": False},
            ]
        })
        self.assertEqual([(item.name, item.model, item.slave_id) for item in devices], [
            ("drive-1", "VF-AS1", 1), ("drive-2", "VF-S15", 2)
        ])
        self.assertEqual(devices[0].registers[0].address, 0xFD00)
        as1_registers = {register.key: register.address for register in devices[0].registers}
        self.assertEqual(as1_registers["input_terminal_status"], 0xFD06)
        self.assertEqual(as1_registers["frequency_setpoint"], 0xFD02)
        self.assertEqual(as1_registers["fm_analog_output"], 0xFE40)
        self.assertEqual(as1_registers["past_trip_1"], 0xFE10)
        self.assertEqual(as1_registers["past_trip_4"], 0xFE13)
        self.assertEqual(as1_registers["trip_output_frequency"], 0xFE00)
        self.assertEqual(as1_registers["braking_resistor_load"], 0xFD28)
        self.assertEqual(as1_registers["inverter_capacity_code"], 0xFB05)
        self.assertEqual(as1_registers["inverter_series_code"], 0xFB07)
        self.assertEqual(as1_registers["cpu_version"], 0xFE08)
        self.assertEqual(as1_registers["speed_feedback"], 0xFD16)
        self.assertEqual(as1_registers["torque"], 0xFD18)
        self.assertEqual(as1_registers["input_power"], 0xFD29)
        self.assertEqual(as1_registers["output_power"], 0xFD30)
        self.assertEqual(as1_registers["calculated_motor_speed"], 0xFE90)
        self.assertEqual(devices[0].max_read_words, 1)
        self.assertEqual(devices[1].max_read_words, 8)
        self.assertEqual(next(item for item in devices[0].registers if item.key == "output_frequency").sampling, "fast")
        self.assertEqual(next(item for item in devices[0].registers if item.key == "past_trip_1").sampling, "diagnostic")
        s15_registers = {register.key: register for register in devices[1].registers}
        self.assertEqual(s15_registers["braking_resistor_load"].address, 0xFD28)
        self.assertEqual(s15_registers["fm_analog_output"].scale, 0.01)

        as3 = configured_devices({"inverters": [{"name": "as3", "model": "VF-AS3J", "slave_id": 3}]})[0]
        as3_registers = {register.key: register for register in as3.registers}
        self.assertEqual(as3_registers["inverter_internal_temperature"].address, 0xFD83)
        self.assertEqual(as3_registers["power_board_temperature"].address, 0xFD78)
        self.assertEqual(as3_registers["inverter_internal_temperature"].unit, "°C")
        self.assertNotIn("inverter_internal_temperature", s15_registers)

    def test_machine_speed_engineering_factor(self):
        device = configured_devices({"inverters": [{
            "name": "geared-drive", "model": "VF-AS1", "slave_id": 1,
            "engineering": {"machine_speed_factor": 0.125, "machine_speed_unit": "rpm"},
        }]})[0]
        source = Register("calculated_motor_speed", 0xFE90, 1, "rpm", "diagnostic")
        samples = add_derived_samples(device, [(source, 1440)])
        derived, raw = samples[-1]
        self.assertEqual((derived.key, derived.address, derived.unit, derived.derived, raw),
                         ("machine_speed", 0xFE90, "rpm", True, 1440))
        self.assertEqual(raw * derived.scale, 180.0)

    def test_machine_speed_factor_must_be_positive(self):
        with self.assertRaisesRegex(ValueError, "must be greater than zero"):
            configured_devices({"inverters": [{
                "name": "bad", "model": "VF-AS1", "slave_id": 1,
                "engineering": {"machine_speed_factor": 0},
            }]})

    def test_engineering_current_and_voltage(self):
        device = configured_devices({"inverters": [{
            "name": "drive", "model": "VF-AS1", "slave_id": 1,
            "engineering": {"rated_output_current_a": 12.5, "rated_output_voltage_v": 400},
        }]})[0]
        current = Register("output_current", 0xFD03, 0.01, "%", "normal")
        voltage = Register("output_voltage", 0xFD05, 0.01, "%", "normal")
        samples = add_derived_samples(device, [(current, 5000), (voltage, 7500)])
        values = {register.key: raw * register.scale for register, raw in samples}
        units = {register.key: register.unit for register, _ in samples}
        self.assertEqual(values["actual_output_current"], 6.25)
        self.assertEqual(values["actual_output_voltage"], 300.0)
        self.assertEqual(units["actual_output_current"], "A")
        self.assertEqual(units["actual_output_voltage"], "V")

    def test_engineering_reference_values_must_be_positive(self):
        for key in ("rated_output_current_a", "rated_output_voltage_v"):
            with self.assertRaisesRegex(ValueError, "must be greater than zero"):
                configured_devices({"inverters": [{
                    "name": "bad", "model": "VF-AS1", "slave_id": 1,
                    "engineering": {key: 0},
                }]})

    def test_motor_torque_and_mechanical_power(self):
        device = configured_devices({"inverters": [{
            "name": "motor", "model": "VF-AS1", "slave_id": 1,
            "engineering": {"motor_rated_power_kw": 3.7, "motor_rated_speed_rpm": 1450},
        }]})[0]
        torque = Register("torque", 0xFD18, 0.01, "%", "diagnostic")
        speed = Register("calculated_motor_speed", 0xFE90, 1, "rpm", "diagnostic")
        samples = add_derived_samples(device, [(torque, 5000), (speed, 1450)])
        values = {register.key: raw * register.scale for register, raw in samples}
        self.assertAlmostEqual(values["actual_motor_torque"], 12.184, places=3)
        self.assertAlmostEqual(values["mechanical_power"], 1.85, places=3)

    def test_motor_power_and_speed_must_be_configured_together(self):
        with self.assertRaisesRegex(ValueError, "configured together"):
            configured_devices({"inverters": [{
                "name": "bad", "model": "VF-AS1", "slave_id": 1,
                "engineering": {"motor_rated_power_kw": 3.7},
            }]})

    def test_s11_frequency_setpoint_uses_status_monitor(self):
        device = configured_devices({"inverters": [{"name": "s11", "model": "VF-S11", "slave_id": 1}]})[0]
        registers = {register.key: register for register in device.registers}
        self.assertEqual(registers["frequency_setpoint"].address, 0xFE02)
        self.assertEqual(registers["frequency_setpoint"].scale, 0.01)
        self.assertEqual(registers["frequency_setpoint"].sampling, "fast")
        self.assertEqual(registers["inverter_capacity_code"].address, 0xFB05)
        self.assertEqual(registers["cpu_version"].address, 0xFE08)
        self.assertEqual(registers["eeprom_version"].address, 0xFE09)
        self.assertEqual(registers["cpu2_version"].address, 0xFE73)
        self.assertTrue(all(registers[key].sampling == "information" for key in (
            "inverter_capacity_code", "cpu_version", "eeprom_version", "cpu2_version"
        )))

    def test_example_alert_thresholds_are_ordered(self):
        example = json.loads((Path(__file__).parent.parent / "config.example.json").read_text(encoding="utf-8"))
        for section in example["alerts"].values():
            for threshold in section.values():
                self.assertLess(threshold["warning"], threshold["critical"])

    def test_duplicate_slave_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate slave_id"):
            configured_devices({"inverters": [
                {"name": "one", "model": "VF-AS1", "slave_id": 1},
                {"name": "two", "model": "VF-S11", "slave_id": 1},
            ]})


class DecoderTests(unittest.TestCase):
    def test_communication_status(self):
        self.assertEqual(decode_metric("communication_status", 2)["severity"], "normal")
        self.assertEqual(decode_metric("communication_status", 1)["severity"], "warning")
        self.assertEqual(decode_metric("communication_status", 0)["severity"], "critical")

    def test_running_forward_status(self):
        decoded = decode_metric("operating_status", (1 << 10) | (1 << 14))
        self.assertEqual(decoded["summary"], "Läuft vorwärts")
        self.assertEqual(decoded["severity"], "normal")

    def test_trip_takes_status_priority(self):
        decoded = decode_metric("operating_status", (1 << 1) | (1 << 2))
        self.assertEqual(decoded["summary"], "Trip")
        self.assertEqual(decoded["severity"], "critical")

    def test_alarm_bits_ignore_undefined_bits(self):
        decoded = decode_metric("alarm_information_2", (1 << 2) | (1 << 6))
        self.assertEqual(decoded["summary"], "1 aktiver Alarm")
        self.assertEqual(decoded["active"][0]["bit"], 2)

    def test_known_trip_code(self):
        decoded = decode_metric("trip_code", 0x18)
        self.assertEqual(decoded["code"], "err5")
        self.assertEqual(decoded["severity"], "critical")

    def test_unknown_trip_code_is_preserved(self):
        sample = enrich_sample({"metric": "trip_code", "raw_value": 0xFFFF})
        self.assertEqual(sample["decoded"]["code"], "0xFFFF")
        self.assertEqual(sample["raw_value"], 0xFFFF)

    def test_input_terminal_bits(self):
        decoded = decode_metric("input_terminal_status", (1 << 0) | (1 << 4) | (1 << 6))
        self.assertEqual([item["label"] for item in decoded["active"]], ["F", "S1", "S3"])
        states = {item["label"]: item["active"] for item in decoded["states"]}
        self.assertTrue(states["F"])
        self.assertFalse(states["R"])

    def test_s15_input_terminal_layout(self):
        decoded = decode_metric("input_terminal_status", 1 << 3, "VF-S15")
        self.assertEqual(decoded["active"][0]["label"], "S1")

    def test_as3_input_terminal_layout(self):
        decoded = decode_metric("input_terminal_status", 1 << 7, "VF-AS3J")
        self.assertEqual(decoded["active"][0]["label"], "S5")

    def test_historic_trip_uses_trip_table(self):
        decoded = decode_metric("past_trip_1", 0x01)
        self.assertEqual(decoded["code"], "oc1")
        self.assertEqual(decoded["summary"], "Überstrom während Beschleunigung")

    def test_retained_operating_status(self):
        decoded = decode_metric("trip_operating_status", 1 << 1)
        self.assertEqual(decoded["summary"], "Trip")


class DatabaseTests(unittest.TestCase):
    def test_parameter_preflight_reports_ready_only_after_three_safe_polls(self):
        class FakeCollector:
            def __init__(self): self.polls=0
            def poll(self, _device, registers):
                self.polls += 1
                values={"safe_output_frequency":0,"safe_operating_status":0,"safe_input_terminal_status":0}
                return [(register,values[register.key]) for register in registers], [], PollStats()
        with tempfile.TemporaryDirectory() as directory:
            request=Path(directory)/"parameter-preflight-request.json"
            request.write_text(json.dumps({"inverter":"drive"}),encoding="utf-8")
            collector=FakeCollector(); process_parameter_preflight_request(collector,[Device("drive","VF-AS1",1,[])],request)
            result=json.loads((Path(directory)/"parameter-preflight-result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"],"ready")
            self.assertEqual(collector.polls,3)

    def test_parameter_write_requires_stationary_drive_and_verifies_value(self):
        class FakeCollector:
            def __init__(self): self.writes=[]
            def poll(self, _device, registers):
                values={"safe_output_frequency":0,"safe_operating_status":0,"safe_input_terminal_status":0}
                return [(register,values[register.key]) for register in registers], [], PollStats()
            def read_register(self, register, _slave): return 123 if not self.writes else (456 if register.address == 0x0014 else 789)
            def write_register(self, address, value, slave): self.writes.append((address,value,slave))
        with tempfile.TemporaryDirectory() as directory:
            database=Database(Path(directory)/"measurements.sqlite3")
            request=Path(directory)/"parameter-write-request.json"
            request.write_text(json.dumps({"inverter":"drive","source_backup":"drive-20260919-120000.pcm","target_sha256":"a" * 64,"changes":[{"address":0x0014,"target":456},{"address":0x0015,"target":789}]}),encoding="utf-8")
            collector=FakeCollector(); process_parameter_write_request(database,collector,[Device("drive","VF-AS1",1,[])],request)
            result=json.loads((Path(directory)/"parameter-write-result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"],"complete")
            self.assertEqual(collector.writes,[(0x0014,456,1),(0x0015,789,1)])
            self.assertEqual(len(result["changes"]),2)
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM parameter_changes").fetchone()[0],2)
            self.assertEqual(database.connection.execute("SELECT source_backup,target_sha256 FROM parameter_changes LIMIT 1").fetchone(),("drive-20260919-120000.pcm","a" * 64))
            database.close()

    def test_parameter_write_reports_verified_prefix_when_batch_stops(self):
        class FakeCollector:
            def __init__(self): self.writes=[]
            def poll(self, _device, registers):
                values={"safe_output_frequency":0,"safe_operating_status":0,"safe_input_terminal_status":0}
                return [(register,values[register.key]) for register in registers], [], PollStats()
            def read_register(self, register, _slave):
                if not self.writes: return 10
                return 11 if register.address == 0x0014 else 0
            def write_register(self, address, value, slave): self.writes.append((address,value,slave))
        with tempfile.TemporaryDirectory() as directory:
            database=Database(Path(directory)/"measurements.sqlite3")
            request=Path(directory)/"parameter-write-request.json"
            request.write_text(json.dumps({"inverter":"drive","changes":[{"address":0x0014,"target":11},{"address":0x0015,"target":22}]}),encoding="utf-8")
            collector=FakeCollector(); process_parameter_write_request(database,collector,[Device("drive","VF-AS1",1,[])],request)
            result=json.loads((Path(directory)/"parameter-write-result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"],"partial")
            self.assertEqual(result["changes"],[{"address":"0014","old":10,"new":11}])
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM parameter_changes").fetchone()[0],1)
            database.close()

    def test_parameter_write_rejects_alarm_state(self):
        class FakeCollector:
            def __init__(self): self.writes=[]
            def poll(self, _device, registers):
                values={"safe_output_frequency":0,"safe_operating_status":1 << 2,"safe_input_terminal_status":0}
                return [(register,values[register.key]) for register in registers], [], PollStats()
            def read_register(self, _register, _slave): return 0
            def write_register(self, address, value, slave): self.writes.append((address,value,slave))
        with tempfile.TemporaryDirectory() as directory:
            database=Database(Path(directory)/"measurements.sqlite3")
            request=Path(directory)/"parameter-write-request.json"
            request.write_text(json.dumps({"inverter":"drive","changes":[{"address":0x0014,"target":11}]}),encoding="utf-8")
            collector=FakeCollector(); process_parameter_write_request(database,collector,[Device("drive","VF-AS1",1,[])],request)
            result=json.loads((Path(directory)/"parameter-write-result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"],"error")
            self.assertIn("trip, alarm, or emergency stop",result["detail"])
            self.assertEqual(collector.writes,[])
            database.close()

    def test_live_only_channel_updates_latest_without_history(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "measurements.sqlite3", {"enabled": True})
            live = Register("output_current", 0xFD03, 0.01, "%", record_history=False)
            database.store_cycle("2026-09-19T10:00:00.000+00:00", "drive", 1, [(live, 1234)], [])
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM samples WHERE metric='output_current'").fetchone()[0], 0)
            self.assertEqual(database.connection.execute("SELECT raw_value FROM latest_values WHERE metric='output_current'").fetchone()[0], 1234)
            database.close()

    def test_engineering_request_updates_running_device_and_invalidates_derived_values(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "measurements.sqlite3"
            database = Database(database_path, {"enabled": True})
            device = configured_devices({"inverters": [{
                "name": "drive", "model": "VF-AS1", "slave_id": 1,
                "engineering": {"machine_speed_factor": 1, "machine_speed_unit": "rpm", "rated_output_current_a": 10, "rated_output_voltage_v": 400},
            }]})[0]
            derived = Register("machine_speed", 0xFE90, 1, "rpm", derived=True)
            database.store_cycle("2026-01-01T00:00:00Z", "drive", 1, [(derived, 100)], [])
            request_path = Path(directory) / "engineering-request.json"
            request_path.write_text(json.dumps({"inverter": "drive", "engineering": {
                "machine_speed_factor": 0.5, "machine_speed_unit": "spm",
                "rated_output_current_a": 12.5, "rated_output_voltage_v": 460,
            }}), encoding="utf-8")
            devices = process_engineering_request(database, [device], request_path)
            self.assertEqual((devices[0].machine_speed_factor, devices[0].machine_speed_unit), (0.5, "spm"))
            self.assertEqual((devices[0].rated_output_current_a, devices[0].rated_output_voltage_v), (12.5, 460))
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM latest_values WHERE metric='machine_speed'").fetchone()[0], 0)
            database.close()

    def test_recording_database_is_archived_and_reinitialized(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "measurements.sqlite3"
            database = Database(database_path, {"enabled": True}, "old investigation")
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            request_path = Path(directory) / "recording-request.json"
            request_path.write_text(json.dumps({"action": "archive", "reference": "new investigation"}), encoding="utf-8")
            database = process_recording_request(database, database_path, {"enabled": True}, request_path)
            self.assertEqual(database.connection.execute("SELECT reference FROM recording_info").fetchone()[0], "new investigation")
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0], 0)
            self.assertEqual(len(list((Path(directory) / "archive").glob("*.sqlite3"))), 1)
            database.close()

    def test_permanent_recording_deletion_requires_three_confirmations(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "measurements.sqlite3"
            database = Database(database_path, {"enabled": True}, "old")
            request_path = Path(directory) / "recording-request.json"
            request_path.write_text(json.dumps({"action": "delete", "reference": "new", "confirmation": "DELETE"}), encoding="utf-8")
            same_database = process_recording_request(database, database_path, {"enabled": True}, request_path)
            self.assertIs(same_database, database)
            self.assertTrue(database_path.exists())
            database.close()

    def test_permanent_recording_deletion_clears_without_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "measurements.sqlite3"
            database = Database(database_path, {"enabled": True}, "old")
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            request_path = Path(directory) / "recording-request.json"
            request_path.write_text(json.dumps({
                "action": "delete", "reference": "new",
                "confirmation": "DELETE DELETE DELETE",
            }), encoding="utf-8")
            database = process_recording_request(database, database_path, {"enabled": True}, request_path)
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0], 0)
            self.assertEqual(database.connection.execute("SELECT reference FROM recording_info").fetchone()[0], "new")
            self.assertFalse((Path(directory) / "archive").exists())
            database.close()

    def test_change_only_logging_and_live_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path, {
                "enabled": True, "default_analog_delta": 0.1,
                "successful_cycle_interval_seconds": 60,
                "thresholds": {"output_frequency": 0.05},
            })
            frequency = Register("output_frequency", 0xFD00, 0.01, "Hz")
            terminals = Register("input_terminal_status", 0xFD06, 1, "raw")
            database.store_cycle("2026-01-01T00:00:00.000+00:00", "VFAS1", 1, [(frequency, 5000), (terminals, 1)], [])
            database.store_cycle("2026-01-01T00:00:01.000+00:00", "VFAS1", 1, [(frequency, 5003), (terminals, 1)], [])
            database.store_cycle("2026-01-01T00:00:02.000+00:00", "VFAS1", 1, [(frequency, 5006), (terminals, 3)], [])
            database.close()
            connection = sqlite3.connect(path)
            rows = connection.execute("SELECT metric, raw_value FROM samples ORDER BY id").fetchall()
            self.assertEqual(rows, [
                ("output_frequency", 5000), ("input_terminal_status", 1),
                ("communication_status", 2),
                ("output_frequency", 5006), ("input_terminal_status", 3),
            ])
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM poll_cycles").fetchone()[0], 2)
            latest = {(item["metric"]): item for item in MonitorRepository(path).latest_samples()}
            self.assertEqual(latest["output_frequency"]["raw_value"], 5006)

    def test_change_logging_writes_full_snapshot_after_process_restart(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            settings = {"enabled": True, "initial_snapshot_on_start": True}
            frequency = Register("output_frequency", 0xFD00, 0.01, "Hz")
            terminals = Register("input_terminal_status", 0xFD06, 1, "raw")

            database = Database(path, settings)
            database.store_cycle(
                "2026-01-01T00:00:00.000+00:00", "VFAS1", 1,
                [(frequency, 5000), (terminals, 1)], [],
            )
            database.close()

            database = Database(path, settings)
            database.store_cycle(
                "2026-01-01T01:00:00.000+00:00", "VFAS1", 1,
                [(frequency, 5000), (terminals, 1)], [],
            )
            database.close()

            connection = sqlite3.connect(path)
            rows = connection.execute(
                "SELECT observed_at, metric, raw_value FROM samples ORDER BY id"
            ).fetchall()
            self.assertEqual(rows, [
                ("2026-01-01T00:00:00.000+00:00", "output_frequency", 5000),
                ("2026-01-01T00:00:00.000+00:00", "input_terminal_status", 1),
                ("2026-01-01T00:00:00.000+00:00", "communication_status", 2),
                ("2026-01-01T01:00:00.000+00:00", "output_frequency", 5000),
                ("2026-01-01T01:00:00.000+00:00", "input_terminal_status", 1),
                ("2026-01-01T01:00:00.000+00:00", "communication_status", 2),
            ])

    def test_change_logging_can_reuse_persisted_baseline(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database = Database(path, {"enabled": True, "initial_snapshot_on_start": False})
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            database.close()
            database = Database(path, {"enabled": True, "initial_snapshot_on_start": False})
            database.store_cycle("2026-01-01T01:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            database.close()
            connection = sqlite3.connect(path)
            self.assertEqual(connection.execute(
                "SELECT COUNT(*) FROM samples WHERE metric='output_frequency'"
            ).fetchone()[0], 1)

    def test_communication_state_is_debounced_and_recovers(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            settings = {"enabled": True, "communication_unreachable_after_transport_errors": 3}
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database = Database(path, settings)
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            database.store_cycle("2026-01-01T00:00:01Z", "VFAS1", 1, [], ["timeout"])
            database.store_cycle("2026-01-01T00:00:02Z", "VFAS1", 1, [], ["timeout"])
            database.store_cycle("2026-01-01T00:00:03Z", "VFAS1", 1, [], ["timeout"])
            database.store_cycle("2026-01-01T00:00:04Z", "VFAS1", 1, [(register, 5000)], [])
            database.close()
            connection = sqlite3.connect(path)
            states = connection.execute(
                "SELECT observed_at, raw_value FROM samples "
                "WHERE metric='communication_status' ORDER BY id"
            ).fetchall()
            self.assertEqual(states, [
                ("2026-01-01T00:00:00Z", 2),
                ("2026-01-01T00:00:01Z", 1),
                ("2026-01-01T00:00:03Z", 0),
                ("2026-01-01T00:00:04Z", 2),
            ])
            self.assertEqual(connection.execute(
                "SELECT COUNT(*) FROM samples WHERE metric='output_frequency'"
            ).fetchone()[0], 2)

    def test_partial_late_recovery_does_not_hide_transport_outage(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            settings = {"enabled": True, "communication_unreachable_after_transport_errors": 3}
            database = Database(path, settings)
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            database.store_cycle(
                "2026-01-01T00:00:01Z", "VFAS1", 1, [(register, 0)],
                ["operating_status: received 0", "frequency_setpoint: received 0",
                 "output_current: received 0", "input_terminal_status: received 0"],
            )
            database.store_cycle("2026-01-01T00:00:14Z", "VFAS1", 1, [(register, 0)], [])
            database.close()
            connection = sqlite3.connect(path)
            states = connection.execute(
                "SELECT observed_at, raw_value FROM samples "
                "WHERE metric='communication_status' ORDER BY id"
            ).fetchall()
            self.assertEqual(states, [
                ("2026-01-01T00:00:00Z", 2),
                ("2026-01-01T00:00:01Z", 0),
                ("2026-01-01T00:00:14Z", 2),
            ])

    def test_success_or_modbus_exception_proves_reachability(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database = Database(path, {"enabled": True})
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            database.store_cycle(
                "2026-01-01T00:00:01Z", "VFAS1", 1, [(register, 5000)],
                ["unsupported: Modbus exception 0x03"],
            )
            database.store_cycle(
                "2026-01-01T00:00:02Z", "VFAS1", 1, [],
                ["unsupported: Modbus exception 0x03"],
            )
            database.close()
            connection = sqlite3.connect(path)
            states = connection.execute(
                "SELECT raw_value FROM samples WHERE metric='communication_status' ORDER BY id"
            ).fetchall()
            self.assertEqual(states, [(2,)])

    def test_legacy_database_gains_diagnostic_columns(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            connection = sqlite3.connect(path)
            connection.execute("""CREATE TABLE poll_cycles (
                id INTEGER PRIMARY KEY, observed_at TEXT NOT NULL, inverter TEXT NOT NULL,
                slave_id INTEGER NOT NULL, successful_reads INTEGER NOT NULL,
                failed_reads INTEGER NOT NULL, error TEXT)""")
            connection.commit(); connection.close()
            database = Database(path); database.close()
            connection = sqlite3.connect(path)
            columns = {row[1] for row in connection.execute("PRAGMA table_info(poll_cycles)")}
            self.assertTrue({"duration_ms", "transactions", "retries", "estimated_bus_ms"} <= columns)

    def test_store_cycle(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path)
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 6000)], [])
            database.close()
            connection = sqlite3.connect(path)
            row = connection.execute("SELECT metric, raw_value, value, unit FROM samples").fetchone()
            self.assertEqual(row, ("output_frequency", 6000, 60.0, "Hz"))

    def test_communication_diagnostics(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path)
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            from datetime import datetime, timezone
            database.store_cycle(
                datetime.now(timezone.utc).isoformat(timespec="milliseconds"), "VFAS1", 1,
                [(register, 6000)], [], PollStats(12.5, 1, 0, 4.3),
            )
            database.close()
            diagnostics = MonitorRepository(path).communication_diagnostics(60)
            self.assertEqual(diagnostics["transactions"], 1)
            self.assertEqual(diagnostics["average_cycle_ms"], 12.5)
            self.assertGreater(diagnostics["bus_utilization_percent"], 0)

    def test_storage_growth_estimate_after_five_minutes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path)
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database.store_cycle("2026-01-01T00:00:00.000+00:00", "VFAS1", 1, [(register, 5000)], [])
            database.store_cycle("2026-01-01T01:00:00.000+00:00", "VFAS1", 1, [(register, 6000)], [])
            database.close()
            info = MonitorRepository(path).storage_info()
            self.assertEqual(info["observed_seconds"], 3600)
            self.assertGreater(info["growth_bytes_per_second"], 0)

    def test_read_only_web_queries(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path)
            frequency = Register("output_frequency", 0xFD00, 0.01, "Hz")
            status = Register("operating_status", 0xFD01, 1, "raw")
            database.store_cycle("2026-01-01T00:00:00.000+00:00", "VFAS1", 1, [(frequency, 5000), (status, 3)], [])
            database.store_cycle("2026-01-01T00:00:01.000+00:00", "VFAS1", 1, [(frequency, 6000)], ["status timeout"])
            database.store_cycle("2026-01-01T00:00:02.000+00:00", "VFS15", 2, [(frequency, 4500)], [])
            database.close()

            repository = MonitorRepository(path)
            cycles_by_name = {item["inverter"]: item for item in repository.last_cycles()}
            self.assertEqual(cycles_by_name["VFAS1"]["failed_reads"], 1)
            self.assertEqual(cycles_by_name["VFS15"]["failed_reads"], 0)
            self.assertEqual(repository.metrics(), ["communication_status", "operating_status", "output_frequency"])
            latest = {(item["inverter"], item["metric"]): item for item in repository.latest_samples()}
            self.assertEqual(latest[("VFAS1", "output_frequency")]["value"], 60.0)
            self.assertEqual(latest[("VFAS1", "operating_status")]["raw_value"], 3)
            self.assertEqual(latest[("VFS15", "output_frequency")]["value"], 45.0)
            history = repository.history("output_frequency", "VFAS1", limit=1)
            self.assertEqual([item["value"] for item in history], [60.0])
            self.assertEqual(len(repository.poll_cycles(limit=1)), 1)
            self.assertEqual(len(repository.last_cycles()), 2)
            info = repository.storage_info()
            self.assertEqual(info["sample_count"], 7)
            self.assertGreater(info["bytes"], 0)
            self.assertGreater(info["filesystem_free_bytes"], 0)
            self.assertIsNone(info["growth_bytes_per_second"])
            exported = list(repository.export_rows(metric="output_frequency", inverter="VFAS1", limit=10))
            self.assertEqual([row[6] for row in exported], [50.0, 60.0])

    def test_csv_iterator_can_move_between_streaming_threads(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path)
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            for second in range(3):
                database.store_cycle(
                    f"2026-01-01T00:00:0{second}.000+00:00",
                    "VFAS1",
                    1,
                    [(register, 5000 + second)],
                    [],
                )
            database.close()

            rows = iter(MonitorRepository(path).export_rows(metric="output_frequency", limit=10))
            with ThreadPoolExecutor(max_workers=1) as first, ThreadPoolExecutor(max_workers=1) as second:
                # Keep both workers alive so their thread identities differ.
                received = [
                    first.submit(next, rows).result(),
                    second.submit(next, rows).result(),
                    first.submit(next, rows).result(),
                ]
            self.assertEqual([row[5] for row in received], [5000, 5001, 5002])

    def test_retention_prunes_samples_and_cycles(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path)
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database.store_cycle("2025-01-01T00:00:00.000+00:00", "VFAS1", 1, [(register, 1000)], [])
            database.store_cycle("2026-01-01T00:00:00.000+00:00", "VFAS1", 1, [(register, 2000)], [])
            deleted = database.prune_before("2025-06-01T00:00:00.000+00:00")
            self.assertEqual(deleted, (2, 1))
            database.close()
            connection = sqlite3.connect(path)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0], 1)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM poll_cycles").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
