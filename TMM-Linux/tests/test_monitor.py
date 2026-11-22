import ast
import json
import re
import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import tmm_monitor
from tmm_monitor import Collector, Database, Device, PollStats, PortRecoveryRequired, ProtocolError, Register, add_derived_samples, configured_devices, configured_registers, configured_serial_buses, crc16, load_config, parameter_backup_files, parameter_safety_class, parse_pcm_template, parse_read_response, parse_read_responses, parse_write_response, pcm_display_value, pcm_template_matches_model, process_channels_request, process_engineering_request, process_parameter_backup_request, process_parameter_preflight_request, process_parameter_write_request, process_recording_request, read_request, start_addon_collectors, write_request
from tmm_decode import decode_metric, enrich_sample, terminal_history_items
from tmm_web_data import MonitorRepository
from tmm_setup import complete_channels, default_channels, new_card, set_mode, validate_config
from tmm_conditions import condition_rules, rule_matches
from tmm_proxy import ModbusProxy, ProxyLog, ProxyPersistenceWorker, ScheduledProxyPoller, adapter_serial, configured_endpoint_status, crc16 as proxy_crc16, looks_like_modbus_request, validate_proxy_config


class SetupAssistantTests(unittest.TestCase):
    def test_live_addon_cards_refresh_independently_with_bounded_requests(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("async function getJSON(url, timeoutMs=8000)", source)
        self.assertIn('getJSON("/api/v1/addons",2500)', source)
        self.assertIn('getJSON("/api/v1/metrics/latest",2500)', source)
        self.assertIn("renderCards(state.latest,state.metadata?.alert_thresholds?.metrics,addons)", source)
        self.assertIn("renderCards(latest.items,state.metadata?.alert_thresholds?.metrics,state.addons)", source)
        self.assertIn('data.storage_capacity_stable ? t("storage.stable")', source)

    def test_addons_and_proxy_follow_persistent_recording_generation(self):
        monitor = (Path(__file__).parents[1] / "tmm_monitor.py").read_text(encoding="utf-8")
        proxy = (Path(__file__).parents[1] / "tmm_proxy.py").read_text(encoding="utf-8")
        self.assertIn("current_identity = database.recording_identity()", monitor)
        self.assertIn("runtime.reset_recording_baseline()", monitor)
        self.assertIn("add-on discarded pre-reset sample", monitor)
        self.assertIn("observer.database.recording_identity", proxy)
        self.assertIn("observer.database.reset_runtime_state()", proxy)

    def test_proxy_administration_worker_recovers_instead_of_exiting(self):
        monitor = (Path(__file__).parents[1] / "tmm_monitor.py").read_text(encoding="utf-8")
        self.assertIn("proxy administration worker recovering after error", monitor)
        self.assertIn("database = None", monitor)
        self.assertIn("while not stop.is_set():", monitor)

    def test_proxy_mode_has_an_independent_recording_administration_worker(self):
        monitor = (Path(__file__).parents[1] / "tmm_monitor.py").read_text(encoding="utf-8")
        self.assertIn("def run_proxy_administration(", monitor)
        self.assertIn('name="tmm-proxy-administration"', monitor)
        self.assertIn("database = process_recording_request(", monitor)
        self.assertIn('"modbus_proxy_transactions",', monitor)
        self.assertLess(monitor.index("administration_thread.start()"), monitor.index("return run_proxy(settings, stop, once=args.once)"))

    def test_recording_reinitialization_is_tracked_until_collector_confirmation(self):
        web = (Path(__file__).parents[1] / "tmm_web.py").read_text(encoding="utf-8")
        monitor = (Path(__file__).parents[1] / "tmm_monitor.py").read_text(encoding="utf-8")
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn('operation_id = uuid.uuid4().hex', web)
        self.assertIn('info["pending_operation"]', web)
        self.assertIn('"operation_id": operation_id', monitor)
        self.assertIn('refreshRecording(accepted.operation_id)', source)
        self.assertIn('for(let attempt=0;attempt<120&&!complete;attempt++)', source)

    def test_setup_safely_repairs_extra_trailing_closing_braces(self):
        setup = (Path(__file__).parents[1] / "setup.sh").read_text(encoding="utf-8")
        self.assertIn("config_has_only_trailing_closing_braces()", setup)
        self.assertIn("repair_trailing_config_data()", setup)
        self.assertIn('all(character == "}" or character.isspace() for character in suffix)', setup)
        self.assertIn('"Remove the extra trailing closing brace(s)"', setup)
        self.assertIn("Refusing repair: trailing data is not limited to closing braces", setup)

    def test_setup_detects_and_safely_repairs_concatenated_json_documents(self):
        setup = (Path(__file__).parents[1] / "setup.sh").read_text(encoding="utf-8")
        self.assertIn("config_document_count()", setup)
        self.assertIn("show_config_json_error()", setup)
        self.assertIn("repair_config_document()", setup)
        self.assertIn('cp --preserve=mode,ownership,timestamps "$CONFIG_PATH" "$backup_path"', setup)
        self.assertIn('"Keep the first complete document"', setup)
        self.assertIn('"Keep the last complete document"', setup)
        self.assertIn("os.replace(temporary,path)", setup)
        self.assertLess(setup.index("ensure_valid_config_json\n"), setup.index("mapfile -t serial_candidates"))

    def test_recording_can_be_stopped_per_source_or_globally(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        html = (Path(__file__).parents[1] / "static" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="history-stop-source-recording"', html)
        self.assertIn('id="history-stop-all-recording"', html)
        self.assertIn('const withoutRecording = mode => mode === "record" ? "live" : mode === "hide" ? "off" : mode', source)
        self.assertIn("async function stopAllRecording()", source)
        self.assertIn('state.addons=await getJSON("/api/v1/addons")', source)

    def test_configured_system_sources_exist_before_their_first_sample(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("for (const addon of state.addons?.items || [])", source)
        self.assertIn('const metric=`addon.${addon.id}.${leaf}`', source)
        self.assertIn("configuredAddonSources", source)
        self.assertIn("function addonChannelMode(channel)", source)
        self.assertIn('channel.enabled === false) return "off"', source)

    def test_system_card_measurements_remain_configurable(self):
        web = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        backend = (Path(__file__).parents[1] / "tmm_web.py").read_text(encoding="utf-8")
        self.assertIn("appendSystemChannelConfiguration(device, addon, health)", web)
        self.assertIn('select.dataset.metric', web)
        self.assertIn('metric:select.dataset.metric,mode:select.value', web)
        self.assertIn('"metric_label": label', backend)
        self.assertIn('for metric, (label, unit) in SYSTEM_ADDON_METRICS', backend)

    def test_unselected_addon_channels_do_not_raise_stale_data_alerts(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn('else if (hasActiveChannel && stale)', source)
        self.assertIn('t("addons.verified")', source)
        self.assertNotIn('sourceObserved && stale', source)

    def test_remote_administration_error_is_actionable_in_the_dashboard(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn('detail === "administration is restricted to localhost"', source)
        self.assertIn('t("admin.remoteDisabled")', source)
        self.assertIn("/etc/tmm/config.json web.allow_remote_administration", source)
        self.assertIn("throw await responseError(response)", source)

    def test_addon_health_is_confirmed_even_without_selected_channels(self):
        source = (Path(__file__).parents[1] / "tmm_monitor.py").read_text(encoding="utf-8")
        self.assertIn("if registers or not health_confirmed:", source)
        self.assertIn('LOG.info("add-on communication verified: %s"', source)

        with tempfile.TemporaryDirectory() as temporary_directory:
            database = Database(
                Path(temporary_directory) / "measurements.sqlite3",
                {"enabled": False, "successful_cycle_interval_seconds": 60.0},
                "utc",
            )
            database.store_cycle(
                "2026-11-17T16:57:47+00:00", "addon:field_di", -2, [], ["old driver error"]
            )
            database.store_cycle(
                "2026-11-17T18:14:02+00:00", "addon:field_di", -2, [], []
            )
            health = database.connection.execute(
                "SELECT observed_at, failed_reads, error FROM latest_poll_cycles "
                "WHERE inverter=? AND slave_id=?",
                ("addon:field_di", -2),
            ).fetchone()
            database.close()
        self.assertEqual(tuple(health), ("2026-11-17T18:14:02+00:00", 0, None))

    def test_smart_fan_install_avoids_obsolete_rpi_gpio_build(self):
        setup = (Path(__file__).parents[1] / "setup.sh").read_text(encoding="utf-8")
        installer = (Path(__file__).parents[1] / "install.sh").read_text(encoding="utf-8")
        bundle = (Path(__file__).parents[1] / "prepare-offline-bundle.sh").read_text(encoding="utf-8")
        self.assertIn("install_sequent_driver_packages", setup)
        self.assertIn("--no-deps SMsfan", setup)
        self.assertIn("--no-deps SMsfan", installer)
        self.assertIn("--no-deps --dest", bundle)
        self.assertIn("'gpiozero>=2.0.0'", setup)

    def test_gpio_source_has_runtime_permissions_and_web_configuration(self):
        installer = (Path(__file__).parents[1] / "install.sh").read_text(encoding="utf-8")
        service = (Path(__file__).parents[1] / "tmm.service").read_text(encoding="utf-8")
        web = (Path(__file__).parents[1] / "tmm_web.py").read_text(encoding="utf-8")
        frontend = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("--groups dialout,i2c,gpio", installer)
        self.assertIn("SupplementaryGroups=dialout i2c gpio", service)
        self.assertIn('kind == "raspberry_pi_gpio"', web)
        self.assertIn('addon.type === "raspberry_pi_gpio"', frontend)
        self.assertIn('invert.dataset.field="active_low"', frontend)

    def test_gpio_electrical_warning_is_permanent_and_explicit(self):
        frontend = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        styles = (Path(__file__).parents[1] / "static" / "style.css").read_text(encoding="utf-8")
        self.assertIn('addon.type === "raspberry_pi_gpio"', frontend)
        self.assertIn('warning.className="gpio-safety-warning"', frontend)
        self.assertIn("Niemals 5 V, 24 V oder Maschinensignale direkt anschließen", frontend)
        self.assertIn("weder galvanische Trennung noch Überspannungsschutz", frontend)
        self.assertIn(".gpio-safety-warning", styles)

    def test_gpio_offline_schematic_is_linked_and_installed(self):
        root = Path(__file__).parents[1]
        frontend = (root / "static" / "app.js").read_text(encoding="utf-8")
        installer = (root / "install.sh").read_text(encoding="utf-8")
        schematic = root / "static" / "docs" / "gpio" / "raspberry-pi-gpio-input-schematic.pdf"
        self.assertIn('raspberry_pi_gpio: { base: "gpio", schematic: "raspberry-pi-gpio-input-schematic.pdf" }', frontend)
        self.assertIn('`/static/docs/${documents.base}/${filename}`', frontend)
        self.assertIn("static/docs/gpio/raspberry-pi-gpio-input-schematic.pdf", installer)
        self.assertTrue(schematic.is_file())
        self.assertEqual(schematic.read_bytes()[:5], b"%PDF-")

    def test_sequent_documents_are_linked_or_checksum_verified_but_not_redistributed(self):
        root = Path(__file__).parents[1]
        frontend = (root / "static" / "app.js").read_text(encoding="utf-8")
        installer = (root / "install.sh").read_text(encoding="utf-8")
        downloader = (root / "fetch-sequent-docs.sh").read_text(encoding="utf-8")
        bundle = (root / "prepare-offline-bundle.sh").read_text(encoding="utf-8")
        self.assertEqual(list((root / "static" / "docs" / "sequent").glob("*.pdf")), [])
        self.assertIn("window.TMM_SEQUENT_DOCS_LOCAL", frontend)
        self.assertIn("cdn.shopify.com", frontend)
        self.assertIn("sha256sum --check --status", downloader)
        self.assertIn("cdn.shopify.com", downloader)
        self.assertIn("fetch-sequent-docs.sh", installer)
        self.assertIn('fetch-sequent-docs.sh" "$DESTINATION/docs/sequent', bundle)
        self.assertIn("THIRD_PARTY_NOTICES.md", installer)

    def test_release_130_version_is_consistent_across_runtime_and_ui(self):
        root = Path(__file__).parents[1]
        self.assertEqual((root / "VERSION").read_text(encoding="utf-8").strip(), "1.3.0")
        web = (root / "tmm_web.py").read_text(encoding="utf-8")
        page = (root / "static" / "index.html").read_text(encoding="utf-8")
        app = (root / "static" / "app.js").read_text(encoding="utf-8")
        services = "\n".join((root / name).read_text(encoding="utf-8") for name in ("tmm.service", "tmm-web.service", "tmm-ups-guard.service"))
        self.assertIn("version=APP_VERSION", web)
        self.assertIn('"version": APP_VERSION', web)
        self.assertIn("Version 1.3.0", page)
        self.assertNotIn("1.3.0-dev", page)
        self.assertNotIn("Version 1.1", app)
        self.assertNotIn("V1.0", services)

    def test_feature_freeze_and_parameter_interchange_roadmap_are_packaged(self):
        root = Path(__file__).parents[1]
        policy = (root / "RELEASE_POLICY.md").read_text(encoding="utf-8")
        roadmap = (root / "ROADMAP.md").read_text(encoding="utf-8")
        installer = (root / "install.sh").read_text(encoding="utf-8")
        self.assertIn("Every later change to the 1.3 line is classified and published as a **Bugfix**", policy)
        self.assertIn("Primary objective: tested Toshiba parameter-set import and export", roadmap)
        self.assertIn("TMM Linux Master 1.4 roadmap", roadmap)
        self.assertIn("Explicit 1.4 objective: Condition Monitoring Milestones", roadmap)
        self.assertIn("second explicit and mandatory 1.4 product goal", roadmap)
        self.assertIn("Windows CSV Viewer alignment", roadmap)
        self.assertIn("RELEASE_POLICY.md", installer)
        self.assertIn("ROADMAP.md", installer)

    def test_unconfigured_hardware_remains_visible_as_inert_support_reference(self):
        backend = (Path(__file__).parents[1] / "tmm_web.py").read_text(encoding="utf-8")
        frontend = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        styles = (Path(__file__).parents[1] / "static" / "style.css").read_text(encoding="utf-8")
        for kind in ("raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin", "sequent_multiio", "sequent_smart_fan", "sequent_super_watchdog"):
            self.assertIn(f'("{kind}"', backend)
        self.assertIn('"configured": False', backend)
        self.assertIn('addon.configured === false ? "hardware-reference"', frontend)
        self.assertIn('if (addon.configured === false) continue;', frontend)
        self.assertIn('t("addons.reference")', frontend)
        self.assertIn(".addon-device.hardware-reference", styles)

    def test_proxy_setup_enforces_hmi_priority_without_offering_scheduled_polling(self):
        source = (Path(__file__).parents[1] / "tmm_setup.py").read_text(encoding="utf-8")
        self.assertIn("scheduled_enabled = False", source)
        self.assertNotIn("Enable independent TMM monitoring in verified HMI idle windows?", source)

    def test_terminal_history_is_reconstructed_from_the_authoritative_status_word(self):
        source = [
            {"observed_at": "2026-01-01T00:00:00+00:00", "metric": "input_terminal_status", "raw_value": 0, "value": 0.0, "unit": "raw"},
            {"observed_at": "2026-01-01T00:00:01+00:00", "metric": "input_terminal_status", "raw_value": (1 << 0) | (1 << 3), "value": 9.0, "unit": "raw"},
        ]
        f_items = terminal_history_items(source, "terminal_f", "VF-AS3J")
        s1_items = terminal_history_items(source, "terminal_s1", "VF-AS3J")
        s2_items = terminal_history_items(source, "terminal_s2", "VF-AS3J")
        self.assertEqual([item["raw_value"] for item in f_items], [0, 1])
        self.assertEqual([item["value"] for item in s1_items], [0.0, 1.0])
        self.assertEqual([item["raw_value"] for item in s2_items], [0, 0])
        self.assertTrue(all(item["unit"] == "on/off" for item in f_items))

    def test_zoomed_history_curves_are_clipped_to_the_plot_area(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("context.rect(pad.left,pad.top,width,plotHeight); context.clip()", source)
        self.assertIn("context.rect(pad.left,pad.top+plotHeight,width,digitalHeight); context.clip()", source)

    def test_history_markers_use_right_click_without_conflicting_with_fullscreen(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn('addEventListener("contextmenu", event=>{ event.preventDefault(); addHistoryMarker(event); })', source)
        self.assertIn('addEventListener("pointerdown", event=>{ if(event.button!==0)return;', source)
        self.assertNotIn('if(pan && !pan.moved)addHistoryMarker(event)', source)

    def test_change_based_analogue_history_holds_the_last_value_to_view_end(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function historyRowsForViewport(entry, start, end, holdLastValue=false)", source)
        self.assertIn("historyRowsForViewport(entry,start,end,true)", source)
        self.assertIn("observed_at:new Date(end).toISOString()", source)

    def test_history_tooltip_flips_left_before_overlapping_the_ruler(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("const gap=28, edge=8, tooltipWidth=tooltip.offsetWidth", source)
        self.assertIn("const fitsRight=event.offsetX+gap+tooltipWidth+edge<=rect.width", source)
        self.assertIn("Math.max(edge,event.offsetX-gap-tooltipWidth)", source)

    def test_installer_preflights_condition_monitoring_module(self):
        installer = (Path(__file__).parents[1] / "install.sh").read_text(encoding="utf-8")
        preflight = installer.index("REQUIRED_RELEASE_FILES=")
        first_install = installer.index('install -d -o root -g root -m 0755 /opt/tmm')
        self.assertLess(preflight, first_install)
        self.assertIn("tmm_conditions.py", installer[preflight:first_install])

    def test_condition_editor_builds_compound_logic_expressions(self):
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        page = (Path(__file__).parents[1] / "static" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="condition-logic"', page)
        self.assertIn('<option>AND</option><option>OR</option><option>XOR</option>', page)
        self.assertIn("function conditionFormExpression()", source)
        self.assertIn('expression};', source)
        self.assertIn("conditionExpressionTree(item.snapshot.logic)", source)

    def test_every_field_card_has_a_complete_disabled_channel_template(self):
        self.assertGreaterEqual(len(default_channels("raspberry_pi_gpio")), 10)
        self.assertEqual(len(default_channels("sequent_16inpind")), 16)
        self.assertEqual(len(default_channels("sequent_24b8vin")), 8)
        self.assertGreater(len(default_channels("sequent_multiio")), 10)
        self.assertTrue(all(not item["enabled"] for item in default_channels("sequent_16inpind")))

    def test_every_new_card_starts_without_selected_channels(self):
        for kind in ("raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin", "sequent_multiio", "sequent_smart_fan", "sequent_super_watchdog"):
            channels = new_card(kind)["channels"]
            self.assertTrue(channels)
            self.assertTrue(all(not item["enabled"] and not item["live"] and not item["record"] for item in channels))

    def test_existing_channel_settings_survive_template_completion(self):
        card = new_card("sequent_24b8vin")
        card["channels"] = [{"channel": 3, "label": "Pressure", "enabled": True, "live": True, "record": True, "scale": 25.0}]
        channels = complete_channels(card)
        self.assertEqual(len(channels), 8)
        self.assertEqual(channels[2]["label"], "Pressure")
        self.assertEqual(channels[2]["scale"], 25.0)

    def test_live_and_record_modes_are_independent(self):
        channel = {}
        set_mode(channel, "live")
        self.assertEqual(channel, {"enabled": True, "live": True, "record": False})
        set_mode(channel, "record")
        self.assertTrue(channel["record"])
        set_mode(channel, "off")
        self.assertFalse(channel["enabled"])

    def test_generated_cards_pass_runtime_validation(self):
        config = {"addons": [new_card(kind) for kind in ("raspberry_pi_gpio", "sequent_16inpind", "sequent_24b8vin", "sequent_multiio", "sequent_smart_fan", "sequent_super_watchdog")]}
        validate_config(config)
from tmm_addons import AddonConfigurationError, SequentAddon, configured_addons


class AddonTests(unittest.TestCase):
    def test_raspberry_pi_gpio_is_read_only_and_uses_bcm_identity(self):
        definition = configured_addons({"addons": [{
            "id": "pi_gpio", "type": "raspberry_pi_gpio", "stack": 0,
            "channels": [
                {"channel": 17, "label": "Machine ready", "pull": "down", "enabled": True},
                {"channel": 27, "label": "Safety", "pull": "up", "active_low": True, "enabled": True},
            ],
        }]})[0]

        class FakeDevice:
            def __init__(self, pin, **settings):
                self.pin = SimpleNamespace(state=pin == 17)
                self.value = int(self.pin.state)
                self.settings = settings
                self.closed = False
            def close(self): self.closed = True
        fake_module = SimpleNamespace(DigitalInputDevice=FakeDevice)
        addon = SequentAddon(definition, lambda name: fake_module if name == "gpiozero" else None)
        samples = addon.changes(now=1.0)
        self.assertEqual([(item.metric, item.value) for item in samples], [
            ("addon.pi_gpio.gpio_17", 1.0),
            ("addon.pi_gpio.gpio_27", 1.0),
        ])
        devices = list(addon.driver.values())
        self.assertEqual(devices[0].settings["pull_up"], False)
        self.assertEqual(devices[1].settings["pull_up"], True)
        addon.close()
        self.assertTrue(all(device.closed for device in devices))

    def test_raspberry_pi_gpio_rejects_invalid_pin_and_pull(self):
        for channel in ({"channel": 1}, {"channel": 17, "pull": "sideways"}):
            with self.assertRaises(AddonConfigurationError):
                configured_addons({"addons": [{"id": "gpio", "type": "raspberry_pi_gpio", "channels": [channel]}]})

    def test_proxy_mode_starts_one_independent_worker_per_sequent_card(self):
        definitions = [SimpleNamespace(identifier="inputs"), SimpleNamespace(identifier="fan")]
        started = []
        class FakeThread:
            def __init__(self, **settings): self.settings=settings
            def start(self): started.append(self)
        config={"storage":{"change_logging":{"enabled":True}},"_config_path":"/etc/tmm/config.json"}
        with patch("tmm_monitor.configured_addons",return_value=definitions), patch("tmm_monitor.threading.Thread",FakeThread):
            threads=start_addon_collectors(config,Path("/var/lib/tmm/measurements.sqlite3"),SimpleNamespace())
        self.assertEqual(len(threads),2)
        self.assertEqual([item.settings["name"] for item in started],["tmm-addon-inputs","tmm-addon-fan"])
        self.assertEqual(started[0].settings["target"],tmm_monitor.run_addon_collector)

    def test_digital_addon_uses_one_bitmap_read_and_stable_channel_names(self):
        definitions = configured_addons({"addons": [{
            "id": "field_di", "type": "sequent_16inpind", "stack": 1,
            "channels": [{"channel": 2, "label": "Safety circuit", "enabled": True}],
        }]})

        class FakeDigital:
            def __init__(self): self.calls = []
            def readAll(self, stack): self.calls.append(stack); return 0b10
        fake = FakeDigital()
        addon = SequentAddon(definitions[0], lambda _name: fake)
        samples = addon.changes(now=1.0)
        self.assertEqual(fake.calls, [1])
        active = next(sample for sample in samples if sample.metric.endswith("input_02"))
        self.assertEqual(active.value, 1)
        self.assertEqual(active.label, "Safety circuit")

    def test_analog_addon_scales_voltage_to_engineering_value(self):
        definitions = configured_addons({"addons": [{
            "id": "field_ai", "type": "sequent_24b8vin", "stack": 0,
            "channels": [{"channel": 1, "label": "Pressure", "scale": 25, "offset": 0, "unit": "bar", "enabled": True}],
        }]})

        class FakeBoard:
            def __init__(self): self.gains = []
            def set_gain(self, channel, gain): self.gains.append((channel, gain))
            def get_u_in(self, channel): return 4.0 if channel == 1 else 0.0
        class FakeModule:
            @staticmethod
            def SM24b8vin(stack):
                self.assertEqual(stack, 0); return FakeBoard()
        addon = SequentAddon(definitions[0], lambda _name: FakeModule)
        sample = next(item for item in addon.changes(now=1.0) if item.metric.endswith("input_01"))
        self.assertEqual(sample.value, 100.0)
        self.assertEqual(sample.unit, "bar")

    def test_addon_channel_can_record_without_a_live_card(self):
        definition = configured_addons({"addons": [{
            "id": "field_ai", "type": "sequent_24b8vin", "stack": 0,
            "channels": [{"channel": 1, "enabled": True, "record": True, "live": False}],
        }]} )[0]
        channel = definition.channels[0]
        self.assertTrue(channel["enabled"])
        self.assertTrue(channel["record"])
        self.assertFalse(channel["live"])

    def test_unconfigured_field_inputs_are_off_by_default(self):
        definition = configured_addons({"addons": [{
            "id": "field_di", "type": "sequent_16inpind", "stack": 0,
        }]} )[0]

        class FakeDigital:
            @staticmethod
            def readAll(_stack): return 0xFFFF

        self.assertEqual(SequentAddon(definition, lambda _name: FakeDigital).changes(now=1.0), [])

    def test_digital_addon_restarts_with_a_complete_state_baseline(self):
        definition = configured_addons({"addons": [{
            "id": "field_di", "type": "sequent_16inpind", "stack": 0,
            "channels": [{"channel": 1, "enabled": True, "record": True}],
        }]} )[0]

        class FakeDigital:
            @staticmethod
            def readAll(_stack): return 0b1

        addon = SequentAddon(definition, lambda _name: FakeDigital)
        first = next(sample for sample in addon.changes(now=1.0) if sample.metric.endswith("input_01"))
        self.assertTrue(first.record_history)
        addon.reset_recording_baseline()
        reset = next(sample for sample in addon.changes(now=2.0) if sample.metric.endswith("input_01"))
        self.assertEqual(reset.value, 1)
        self.assertTrue(reset.record_history)

    def test_addons_reject_duplicate_card_stack(self):
        with self.assertRaises(AddonConfigurationError):
            configured_addons({"addons": [
                {"id": "a", "type": "sequent_16inpind", "stack": 0},
                {"id": "b", "type": "sequent_16inpind", "stack": 0},
            ]})

    def test_addon_channel_label_is_retained_in_csv_database_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            database = Database(Path(folder) / "measurements.sqlite3")
            database.store_cycle(
                "2026-09-20T12:00:00+00:00", "addon:field_ai", -1,
                [(Register("addon.field_ai.input_01", 0xE000, 0.001, "bar", "fast", label="Hydraulic pressure"), 123_400)], [],
            )
            database.close()
            exported = list(MonitorRepository(Path(folder) / "measurements.sqlite3").export_rows())
            self.assertEqual(exported[0][-1], "Hydraulic pressure")


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
    def test_multiple_serial_buses_allow_repeated_slave_addresses(self):
        config = {
            "serial_buses": [
                {"id": "line_a", "device": "/dev/serial/by-id/usb-a", "baudrate": 19200},
                {"id": "line_b", "device": "/dev/serial/by-id/usb-b", "baudrate": 38400},
            ],
            "inverters": [
                {"name": "drive-a", "model": "VF-AS3J", "bus_id": "line_a", "slave_id": 1},
                {"name": "drive-b", "model": "VF-AS1", "bus_id": "line_b", "slave_id": 1},
            ],
        }
        buses = configured_serial_buses(config)
        devices = configured_devices(config)
        self.assertEqual(list(buses), ["line_a", "line_b"])
        self.assertEqual([(item.name, item.bus_id, item.slave_id) for item in devices], [
            ("drive-a", "line_a", 1), ("drive-b", "line_b", 1),
        ])

    def test_multiple_serial_buses_require_stable_unique_paths(self):
        with self.assertRaisesRegex(ValueError, "/dev/serial/by-id"):
            configured_serial_buses({"serial_buses": [{"id": "line", "device": "/dev/ttyUSB0"}]})
        with self.assertRaisesRegex(ValueError, "more than one bus"):
            configured_serial_buses({"serial_buses": [
                {"id": "a", "device": "/dev/serial/by-id/usb-a"},
                {"id": "b", "device": "/dev/serial/by-id/usb-a"},
            ]})

    def test_load_config_accepts_named_buses_without_legacy_serial_object(self):
        config = {
            "serial_buses": [{"id": "line", "device": "/dev/serial/by-id/usb-test"}],
            "polling": {}, "storage": {}, "addons": [],
            "inverters": [{"name": "Drive", "model": "VF-AS3J", "bus_id": "line", "slave_id": 1}],
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "config.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            loaded = load_config(path)
        self.assertEqual(loaded["serial_buses"][0]["id"], "line")

    def test_dashboard_section_ids_match_the_web_interface(self):
        project = Path(__file__).resolve().parents[1]
        markup = (project / "static" / "index.html").read_text(encoding="utf-8")
        section_ids = re.findall(r'<section\b[^>]*aria-labelledby="([^"]+)"', markup)
        module = ast.parse((project / "tmm_web.py").read_text(encoding="utf-8"))
        assignment = next(node for node in module.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "DASHBOARD_SECTION_IDS" for target in node.targets))
        self.assertEqual(section_ids, list(ast.literal_eval(assignment.value)))

    def test_bridge_template_is_safe_and_uses_two_unassigned_ports(self):
        project = Path(__file__).resolve().parents[1]
        config = json.loads((project / "config.example.json").read_text(encoding="utf-8"))
        bridge = config["communication_bridge"]
        self.assertEqual(bridge["mode"], "transparent_proxy")
        self.assertNotIn("hardware_bypass_declared", bridge)
        self.assertEqual(bridge["hmi_port"]["device"], "")
        self.assertEqual(bridge["drive_port"]["device"], "")

    def test_bridge_status_identifies_the_missing_adapter_role(self):
        config = {"communication_bridge": {
            "enabled": True,
            "hmi_port": {"device": "/dev/serial/by-id/usb-hmi"},
            "drive_port": {"device": "/dev/serial/by-id/usb-drive"},
        }}
        with patch.object(Path, "exists", autospec=True, side_effect=lambda path: str(path).endswith("usb-hmi")):
            endpoints, missing_adapters, checks = configured_endpoint_status(config["communication_bridge"])
        self.assertTrue(endpoints[0]["present"])
        self.assertFalse(endpoints[1]["present"])
        self.assertFalse(checks["devices_present"])
        self.assertEqual(missing_adapters[0]["id"], "drive")

    def test_adapter_role_uses_short_ftdi_serial(self):
        device = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_BG041YSU-if00-port0"
        self.assertEqual(adapter_serial(device), "BG041YSU")

    def test_reversal_detector_accepts_requests_but_not_read_responses(self):
        request_body = bytes.fromhex("01 03 fd 00 00 01")
        request = request_body + proxy_crc16(request_body).to_bytes(2, "little")
        response_body = bytes.fromhex("01 03 02 13 88")
        response = response_body + proxy_crc16(response_body).to_bytes(2, "little")
        self.assertTrue(looks_like_modbus_request(request))
        self.assertFalse(looks_like_modbus_request(response))

    def test_reversal_detector_requires_repeated_drive_side_requests(self):
        body = bytes.fromhex("01 03 fd 00 00 01")
        frame = body + proxy_crc16(body).to_bytes(2, "little")

        class FakePort:
            def __init__(self, payload): self.payload = bytearray(payload); self.timeout = 0.1
            @property
            def in_waiting(self): return len(self.payload)
            def read(self, size):
                chunk = bytes(self.payload[:size]); del self.payload[:size]; return chunk

        proxy = object.__new__(ModbusProxy)
        proxy.settings = {"drive_port": {"baudrate": 19200, "bytesize": 8, "parity": "E", "stopbits": 1}}
        proxy.upstream_requests_seen = 0
        proxy.unexpected_drive_bursts = 0
        proxy.reversed_request_candidates = 0
        proxy.reversed_candidate_started = 0.0
        proxy.drive = FakePort(frame)
        self.assertEqual(proxy.observe_drive_side_request(), frame)
        self.assertEqual(proxy.reversed_request_candidates, 1)
        proxy.drive = FakePort(frame)
        self.assertEqual(proxy.observe_drive_side_request(), frame)
        self.assertEqual(proxy.reversed_request_candidates, 2)
        self.assertTrue(proxy.reversal_suspected())

    def test_reversal_detector_uses_repeated_wrong_side_activity_as_fallback(self):
        class FakePort:
            def __init__(self, payload): self.payload = bytearray(payload); self.timeout = 0.1
            @property
            def in_waiting(self): return len(self.payload)
            def read(self, size):
                chunk = bytes(self.payload[:size]); del self.payload[:size]; return chunk

        proxy = object.__new__(ModbusProxy)
        proxy.settings = {"drive_port": {"baudrate": 19200, "bytesize": 8, "parity": "E", "stopbits": 1}}
        proxy.upstream_requests_seen = 0
        proxy.unexpected_drive_bursts = 0
        proxy.reversed_request_candidates = 0
        proxy.reversed_candidate_started = 0.0
        for payload in (b"\x01\x7f\x10\x20", b"\x01\x7f\x11\x21", b"\x01\x7f\x12\x22"):
            proxy.drive = FakePort(payload)
            self.assertEqual(proxy.observe_drive_side_request(), payload)
        self.assertEqual(proxy.reversed_request_candidates, 0)
        self.assertEqual(proxy.unexpected_drive_bursts, 3)
        self.assertTrue(proxy.reversal_suspected())

    def test_proxy_does_not_forward_a_crc_invalid_hmi_request(self):
        class FakePort:
            def __init__(self, payload=b""): self.payload=bytearray(payload); self.timeout=0.1; self.written=[]
            def read(self, size):
                chunk=bytes(self.payload[:size]); del self.payload[:size]; return chunk
            def write(self, payload): self.written.append(payload)
            def flush(self): pass

        request=bytes.fromhex("fd f2 07 fb fe fd aa 96")
        proxy=object.__new__(ModbusProxy)
        proxy.settings={
            "idle_read_timeout_seconds":0.1,
            "response_timeout_seconds":0.75,
            "hmi_port":{"baudrate":19200,"bytesize":8,"parity":"E","stopbits":1},
            "drive_port":{"baudrate":19200,"bytesize":8,"parity":"E","stopbits":1},
        }
        proxy.hmi=FakePort(request); proxy.drive=FakePort(); proxy.last_request_at=None; proxy.upstream_requests_seen=0
        result=proxy.forward_once()
        self.assertEqual(result[3], "request_crc_error")
        self.assertEqual(proxy.drive.written, [])

    def test_scheduled_proxy_poll_uses_idle_window_and_stores_value(self):
        response_body=bytes.fromhex("01 03 02 00 7b")
        response=response_body+proxy_crc16(response_body).to_bytes(2,"little")

        class FakePort:
            def __init__(self,payload=b""): self.payload=bytearray(payload); self.timeout=0.75; self.written=[]
            @property
            def in_waiting(self): return len(self.payload)
            def read(self,size): chunk=bytes(self.payload[:size]); del self.payload[:size]; return chunk
            def write(self,payload): self.written.append(payload)
            def flush(self): pass
        class FakeDrive(FakePort):
            def __init__(self,reply): super().__init__(); self.reply=reply
            def write(self,payload): super().write(payload); self.payload.extend(self.reply)
        class FakeDatabase:
            def __init__(self): self.cycles=[]
            def store_cycle(self,*args): self.cycles.append(args)
        class FakeLog:
            def __init__(self): self.items=[]
            def store(self,*args,**kwargs): self.items.append((args,kwargs))

        register=Register("output_frequency",0xFD00,0.01,"Hz")
        device=SimpleNamespace(name="drive",slave_id=1)
        scheduled=object.__new__(ScheduledProxyPoller)
        scheduled.enabled=True; scheduled.idle_guard=.5; scheduled.response_timeout=.1; scheduled.minimum_gap=.2
        scheduled.next_allowed=0; scheduled.entries=[{"device":device,"register":register,"interval":1.0,"due":0}]
        scheduled.database=FakeDatabase(); scheduled.successes=0; scheduled.errors=0
        scheduled.monitor=SimpleNamespace(read_request=read_request,parse_read_responses=parse_read_responses,PollStats=PollStats)
        proxy=SimpleNamespace(hmi=FakePort(),drive=FakeDrive(response),last_upstream_activity=0,
                              settings={"drive_port":{"baudrate":19200,"bytesize":8,"parity":"E","stopbits":1}},
                              _gap=lambda _settings:.002)
        log=FakeLog()
        self.assertTrue(scheduled.poll_once(proxy,log))
        self.assertEqual(scheduled.successes,1)
        self.assertEqual(scheduled.database.cycles[0][3][0][1],123)
        self.assertEqual(log.items[0][1]["origin"],"tmm")

    def test_scheduled_proxy_poll_never_preempts_recent_hmi_activity(self):
        scheduled=object.__new__(ScheduledProxyPoller)
        scheduled.enabled=True; scheduled.entries=[{"due":0}]; scheduled.next_allowed=0
        scheduled.idle_guard=.5; scheduled.response_timeout=.1; scheduled.minimum_gap=.2
        proxy=SimpleNamespace(hmi=SimpleNamespace(in_waiting=0),drive=SimpleNamespace(in_waiting=0),last_upstream_activity=__import__("time").monotonic())
        self.assertFalse(scheduled.poll_once(proxy,SimpleNamespace()))

    def test_valid_hmi_read_is_passively_stored_without_a_serial_write(self):
        class FakeDatabase:
            def __init__(self): self.cycles=[]
            def store_cycle(self,*args): self.cycles.append(args)

        register=Register("output_frequency",0xFD00,0.01,"Hz")
        device=SimpleNamespace(name="VF-AS3J",slave_id=1,registers=[register])
        scheduled=object.__new__(ScheduledProxyPoller)
        scheduled.passive_decode=True; scheduled.devices=[device]
        scheduled.database=FakeDatabase(); scheduled.passive_transactions=0; scheduled.passive_samples=0
        scheduled.monitor=SimpleNamespace(add_derived_samples=lambda _device,samples:samples,PollStats=PollStats)
        request_body=bytes.fromhex("01 03 fd 00 00 01")
        response_body=bytes.fromhex("01 03 02 13 88")
        request=request_body+proxy_crc16(request_body).to_bytes(2,"little")
        response=response_body+proxy_crc16(response_body).to_bytes(2,"little")

        count=scheduled.observe_hmi_read("2026-11-10T10:00:00+00:00",request,response,27.0,"ok")

        self.assertEqual(count,1)
        self.assertEqual(scheduled.passive_transactions,1)
        self.assertEqual(scheduled.database.cycles[0][3],[(register,5000)])
        self.assertEqual(scheduled.database.cycles[0][5].transactions,0)

    def test_proxy_log_migrates_origin_and_marks_tmm_transactions(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path=Path(temporary_directory)/"proxy.sqlite3"
            connection=sqlite3.connect(path)
            connection.execute("""CREATE TABLE modbus_proxy_transactions (
                id INTEGER PRIMARY KEY,request_at TEXT NOT NULL,response_at TEXT,slave_id INTEGER,function_code INTEGER,
                request_hex TEXT NOT NULL,response_hex TEXT,request_crc_valid INTEGER NOT NULL,response_crc_valid INTEGER,
                latency_ms REAL,outcome TEXT NOT NULL)""")
            connection.commit(); connection.close()
            log=ProxyLog(path)
            body=bytes.fromhex("01 03 fd 00 00 01"); frame=body+proxy_crc16(body).to_bytes(2,"little")
            log.store("2026-01-01T00:00:00+00:00",None,frame,b"",1.0,"tmm_poll_timeout",origin="tmm"); log.close()
            connection=sqlite3.connect(path)
            self.assertEqual(connection.execute(
                "SELECT origin,observed_samples FROM modbus_proxy_transactions"
            ).fetchone(),("tmm",0))
            connection.close()

    def test_proxy_persistence_queue_never_blocks_when_full(self):
        worker = object.__new__(ProxyPersistenceWorker)
        worker.queue = __import__("queue").Queue(maxsize=1)
        worker.enqueued = 0; worker.processed = 0; worker.dropped = 0; worker.failed = 0; worker.lock_retries = 0
        worker.maximum_depth = 0; worker.last_error = ""; worker.last_error_at = ""; worker.last_success_at = ""
        args = ("2026-01-01T00:00:00+00:00", None, b"\x01\x03", b"", 1.0, "test")
        self.assertTrue(worker.submit(*args))
        self.assertFalse(worker.submit(*args))
        self.assertEqual((worker.enqueued, worker.dropped, worker.maximum_depth), (1, 1, 1))
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn('t("bridge.hmiPriority")', source)
        self.assertIn("data.runtime_diagnostics?.persistence", source)

    def test_proxy_persistence_retries_sqlite_maintenance_locks(self):
        worker = object.__new__(ProxyPersistenceWorker)
        worker.lock_retries = 0; worker.last_error = ""; worker.last_error_at = ""
        attempts = {"count": 0}
        def temporarily_locked():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise sqlite3.OperationalError("database is locked")
            return "stored"
        with patch("tmm_proxy.time.sleep"):
            self.assertEqual(worker._retry_database_lock(temporarily_locked), "stored")
        self.assertEqual((attempts["count"], worker.lock_retries), (3, 2))
        source = (Path(__file__).parents[1] / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn('bridge.persistenceRecovered', source)
        self.assertIn('persistence.capacity', source)

    def test_proxy_retention_cleanup_is_bounded(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "proxy.sqlite3"
            log = ProxyLog(path)
            body = bytes.fromhex("01 03 fd 00 00 01")
            frame = body + proxy_crc16(body).to_bytes(2, "little")
            for second in range(5):
                log.store(f"2026-01-01T00:00:0{second}+00:00", None, frame, b"", 1.0, "test")
            self.assertEqual(log.prune_before("2027-01-01T00:00:00+00:00", limit=2), 2)
            self.assertEqual(log.connection.execute("SELECT COUNT(*) FROM modbus_proxy_transactions").fetchone()[0], 3)
            log.close()

    def test_scheduled_proxy_polling_rejects_an_unbounded_timeout(self):
        config={"communication_bridge":{"enabled":True,"mode":"transparent_proxy",
            "hmi_port":{"device":"/dev/serial/by-id/hmi","baudrate":19200,"parity":"E","stopbits":1,"bytesize":8},
            "drive_port":{"device":"/dev/serial/by-id/drive","baudrate":19200,"parity":"E","stopbits":1,"bytesize":8},
            "scheduled_polling":{"enabled":True,"response_timeout_seconds":.5}}}
        with self.assertRaisesRegex(ValueError,"scheduled proxy polling"):
            validate_proxy_config(config)

    def test_short_proxy_idle_window_is_accepted_and_observable(self):
        config={"communication_bridge":{"enabled":True,"mode":"transparent_proxy",
            "idle_read_timeout_seconds":.1,
            "hmi_port":{"device":"/dev/serial/by-id/hmi","baudrate":19200,"parity":"E","stopbits":1,"bytesize":8},
            "drive_port":{"device":"/dev/serial/by-id/drive","baudrate":19200,"parity":"E","stopbits":1,"bytesize":8},
            "scheduled_polling":{"enabled":True,"idle_guard_seconds":.005,"minimum_gap_seconds":.005}}}
        validated=validate_proxy_config(config)
        self.assertEqual(validated["idle_read_timeout_seconds"],.005)
        config["communication_bridge"]["scheduled_polling"]["idle_guard_seconds"]=.004
        with self.assertRaisesRegex(ValueError,"idle guard >= 0.005"):
            validate_proxy_config(config)

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

    def test_smart_fan_is_read_only_and_uses_stack_zero(self):
        definitions = configured_addons({"addons": [{
            "id": "system_fan", "type": "sequent_smart_fan", "stack": 0,
            "channels": [
                {"metric": "fan_power", "enabled": True, "live": True, "record": True},
                {"metric": "processor_temperature", "enabled": True, "live": True, "record": True},
            ],
        }]})

        class FakeFan:
            @staticmethod
            def getPower(stack): return 42 if stack == 0 else -1
            @staticmethod
            def getSafetyTemp(stack): return 65
            @staticmethod
            def getProcTemp(stack): return 48
            @staticmethod
            def getStopInt(stack): return 0
        addon = SequentAddon(definitions[0], lambda _name: FakeFan)
        samples = {sample.metric: sample for sample in addon.changes(now=1.0)}
        self.assertEqual(samples["addon.system_fan.fan_power"].value, 42)
        self.assertEqual(samples["addon.system_fan.processor_temperature"].unit, "°C")

    def test_steady_smart_fan_retains_a_sparse_history_heartbeat(self):
        definition = configured_addons({"addons": [{
            "id": "system_fan", "type": "sequent_smart_fan", "stack": 0,
            "channels": [{"metric": "fan_power", "enabled": True, "live": True, "record": True}],
        }]} )[0]

        class FakeFan:
            @staticmethod
            def getPower(_stack): return 42
            @staticmethod
            def getStopInt(_stack): return 0

        addon = SequentAddon(definition, lambda _name: FakeFan)
        first = {sample.metric: sample for sample in addon.changes(now=1.0)}
        after_minute = {sample.metric: sample for sample in addon.changes(now=61.0)}
        self.assertTrue(first["addon.system_fan.fan_power"].record_history)
        self.assertTrue(after_minute["addon.system_fan.fan_power"].record_history)

    def test_reduced_smart_fan_keeps_supported_measurements_online(self):
        definition = configured_addons({"addons": [{
            "id": "system_fan", "type": "sequent_smart_fan", "stack": 0,
            "channels": [
                {"metric": "fan_power", "enabled": True, "live": True, "record": True},
                {"metric": "processor_temperature", "enabled": True, "live": True, "record": True},
            ],
        }]} )[0]

        class ReducedFan:
            @staticmethod
            def getPower(stack): return 55
            @staticmethod
            def getProcTemp(stack): return 43
        samples = SequentAddon(definition, lambda _name: ReducedFan).changes(now=1.0)
        self.assertEqual({item.metric.rsplit(".", 1)[-1] for item in samples}, {"fan_power", "processor_temperature"})

    def test_smart_fan_with_no_selected_channels_is_idle_not_failed(self):
        definition = configured_addons({"addons": [new_card("sequent_smart_fan") | {"enabled": True}]})[0]
        self.assertEqual(SequentAddon(definition, lambda _name: object()).changes(now=1.0), [])

    def test_failed_vendor_probe_closes_partially_open_bus(self):
        definitions = configured_addons({"addons": [{
            "id": "field_ai", "type": "sequent_24b8vin", "stack": 0,
        }]})

        class Bus:
            closed = False
            def close(self): self.closed = True
        bus = Bus()
        class BrokenBoard:
            def __init__(self, stack):
                self.bus = bus
                raise OSError("no card")
        class FakeModule:
            SM24b8vin = BrokenBoard
        with self.assertRaises(OSError):
            SequentAddon(definitions[0], lambda _name: FakeModule).poll()
        self.assertTrue(bus.closed)

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
        self.assertFalse(registers["operating_status"].record_history)

    def test_unselected_inverter_channels_do_not_record_by_default(self):
        device = configured_devices({"inverters": [{"name": "drive", "model": "VF-AS1", "slave_id": 1, "channels": {}}]})[0]
        self.assertTrue(device.registers)
        self.assertTrue(all(not register.record_history for register in device.registers))
        self.assertIn("operating_status", {register.key for register in device.registers})

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
                {"name": "drive-1", "model": "VF-AS1", "slave_id": 1, "channels": {key: "live" for key in ("output_frequency", "input_terminal_status", "frequency_setpoint", "fm_analog_output", "past_trip_1", "past_trip_4", "trip_output_frequency", "braking_resistor_load", "inverter_capacity_code", "inverter_series_code", "cpu_version", "speed_feedback", "torque", "input_power", "output_power", "calculated_motor_speed")}},
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
        self.assertEqual(devices[1].max_read_words, 1)
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
        self.assertEqual(as3.max_read_words, 1)
        self.assertIn("trip_code", as3_registers)
        self.assertIn("alarm_information_1", as3_registers)
        self.assertIn("alarm_information_2", as3_registers)
        self.assertIn("dc_input_voltage", as3_registers)
        self.assertIn("output_voltage", as3_registers)
        self.assertIn("braking_resistor_load", as3_registers)
        self.assertIn("fm_analog_output", as3_registers)
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
        device = configured_devices({"inverters": [{"name": "s11", "model": "VF-S11", "slave_id": 1, "channels": {key: "live" for key in ("frequency_setpoint", "inverter_capacity_code", "cpu_version", "eeprom_version", "cpu2_version")}}]})[0]
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

    def test_web_alert_configuration_supports_lower_limit_pairs(self):
        source = (Path(__file__).resolve().parents[1] / "tmm_web.py").read_text(encoding="utf-8")
        self.assertIn('"warning_low": warning_low, "critical_low": critical_low', source)
        self.assertIn("critical_low >= warning_low", source)

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
    def test_condition_rule_creates_persistent_enter_and_exit_milestones(self):
        with tempfile.TemporaryDirectory() as directory:
            rules = condition_rules({"condition_monitoring": {"rules": [{
                "id": "hot", "name": "Temperature high", "source": "drive", "metric": "temperature",
                "operator": ">", "value": 10, "duration_seconds": 5, "hysteresis": 2,
                "tolerance": 0, "severity": "warning", "enabled": True,
            }]}})
            database = Database(Path(directory) / "monitor.sqlite3", {"enabled": False}, conditions=rules)
            register = Register("temperature", 1, 1, "°C", record_history=False)
            database.store_cycle("2026-01-01T00:00:00+00:00", "drive", 1, [(register, 11)], [])
            database.store_cycle("2026-01-01T00:00:06+00:00", "drive", 1, [(register, 11)], [])
            database.store_cycle("2026-01-01T00:00:07+00:00", "drive", 1, [(register, 9)], [])
            database.store_cycle("2026-01-01T00:00:08+00:00", "drive", 1, [(register, 7)], [])
            events = database.connection.execute("SELECT event_type,value FROM milestones ORDER BY id").fetchall()
            self.assertEqual(events, [("enter", 11.0), ("exit", 7.0)])
            database.close()

    def test_condition_not_and_equality_tolerance(self):
        not_rule, equal_rule = condition_rules({"condition_monitoring": {"rules": [
            {"id": "off", "name": "Input off", "source": "drive", "metric": "input", "operator": "NOT"},
            {"id": "target", "name": "At target", "source": "drive", "metric": "speed", "operator": "=", "value": 50, "tolerance": .5},
        ]}})
        self.assertTrue(rule_matches(not_rule, 0)); self.assertFalse(rule_matches(not_rule, 1))
        self.assertTrue(rule_matches(equal_rule, 50.4)); self.assertFalse(rule_matches(equal_rule, 50.6))

    def test_compound_condition_and_creates_one_milestone_after_all_operands_match(self):
        with tempfile.TemporaryDirectory() as directory:
            rules = condition_rules({"condition_monitoring": {"rules": [{
                "id": "hot-loaded", "name": "Hot and loaded", "duration_seconds": 0,
                "severity": "critical", "expression": {"logic": "AND", "conditions": [
                    {"source": "drive", "metric": "temperature", "operator": ">", "value": 70, "hysteresis": 2},
                    {"source": "drive", "metric": "current", "operator": ">=", "value": 80, "hysteresis": 5},
                ]},
            }]}})
            database = Database(Path(directory) / "monitor.sqlite3", {"enabled": False}, conditions=rules)
            temperature = Register("temperature", 1, 1, "°C", record_history=False)
            current = Register("current", 2, 1, "%", record_history=False)
            database.store_cycle("2026-01-01T00:00:00+00:00", "drive", 1, [(temperature, 75)], [])
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM milestones").fetchone()[0], 0)
            database.store_cycle("2026-01-01T00:00:01+00:00", "drive", 1, [(current, 85)], [])
            row = database.connection.execute("SELECT event_type,snapshot_json FROM milestones").fetchone()
            self.assertEqual(row[0], "enter")
            snapshot = json.loads(row[1])
            self.assertEqual(len(snapshot["operands"]), 2)
            self.assertTrue(all(item["matches"] for item in snapshot["operands"]))
            database.close()

    def test_compound_condition_or_xor_and_group_not(self):
        base = lambda logic: condition_rules({"condition_monitoring": {"rules": [{
            "id": logic.lower(), "name": logic, "expression": {"logic": logic, "conditions": [
                {"source": "drive", "metric": "a", "operator": ">", "value": 0},
                {"source": "drive", "metric": "b", "operator": ">", "value": 0},
            ]},
        }]}})[0]
        self.assertEqual(base("OR").expression["logic"], "OR")
        self.assertEqual(base("XOR").expression["logic"], "XOR")
        not_rule = condition_rules({"condition_monitoring": {"rules": [{
            "id": "not-group", "name": "Neither running", "expression": {"logic": "NOT", "conditions": [
                {"logic": "OR", "conditions": [
                    {"source": "drive", "metric": "f", "operator": "NOT"},
                    {"source": "drive", "metric": "r", "operator": "NOT"},
                ]}
            ]}
        }]}})[0]
        self.assertEqual(not_rule.expression["conditions"][0]["logic"], "OR")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            condition_rules({"condition_monitoring": {"rules": [{
                "id": "bad-not", "name": "Bad", "expression": {"logic": "NOT", "conditions": [
                    {"source": "drive", "metric": "a", "operator": "NOT"},
                    {"source": "drive", "metric": "b", "operator": "NOT"},
                ]}
            }]}})

    def test_xor_condition_is_true_for_exactly_one_matching_operand(self):
        with tempfile.TemporaryDirectory() as directory:
            rule = condition_rules({"condition_monitoring": {"rules": [{
                "id": "xor", "name": "Exactly one", "expression": {"logic": "XOR", "conditions": [
                    {"source": "drive", "metric": "a", "operator": ">", "value": 0},
                    {"source": "drive", "metric": "b", "operator": ">", "value": 0},
                ]}
            }]}})
            database = Database(Path(directory) / "monitor.sqlite3", {"enabled": False}, conditions=rule)
            a = Register("a", 1, 1, "raw", record_history=False)
            b = Register("b", 2, 1, "raw", record_history=False)
            database.store_cycle("2026-01-01T00:00:00+00:00", "drive", 1, [(a, 1), (b, 0)], [])
            database.store_cycle("2026-01-01T00:00:01+00:00", "drive", 1, [(b, 1)], [])
            self.assertEqual(database.connection.execute("SELECT event_type FROM milestones ORDER BY id").fetchall(), [("enter",), ("exit",)])
            database.close()

    def test_condition_pending_state_survives_collector_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "monitor.sqlite3"
            rules = condition_rules({"condition_monitoring": {"rules": [{
                "id": "delay", "name": "Delayed", "source": "drive", "metric": "load",
                "operator": ">=", "value": 80, "duration_seconds": 10,
            }]}})
            register = Register("load", 1, 1, "%", record_history=False)
            first = Database(path, {"enabled": False}, conditions=rules)
            first.store_cycle("2026-01-01T00:00:00+00:00", "drive", 1, [(register, 90)], [])
            first.close()
            second = Database(path, {"enabled": False}, conditions=rules)
            second.store_cycle("2026-01-01T00:00:11+00:00", "drive", 1, [(register, 90)], [])
            self.assertEqual(second.connection.execute("SELECT COUNT(*) FROM milestones").fetchone()[0], 1)
            second.close()

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
            database.connection.execute("CREATE TABLE modbus_proxy_transactions (id INTEGER PRIMARY KEY, request_at TEXT)")
            database.connection.execute("INSERT INTO modbus_proxy_transactions(request_at) VALUES ('2026-01-01T00:00:00Z')")
            database.connection.commit()
            request_path = Path(directory) / "recording-request.json"
            request_path.write_text(json.dumps({"action": "archive", "reference": "new investigation"}), encoding="utf-8")
            database = process_recording_request(database, database_path, {"enabled": True}, request_path)
            self.assertEqual(database.connection.execute("SELECT reference FROM recording_info").fetchone()[0], "new investigation")
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0], 0)
            self.assertEqual(database.connection.execute("SELECT COUNT(*) FROM modbus_proxy_transactions").fetchone()[0], 0)
            archives = list((Path(directory) / "archive").glob("*.sqlite3"))
            self.assertEqual(len(archives), 1)
            with sqlite3.connect(archives[0]) as archive:
                self.assertEqual(archive.execute("SELECT COUNT(*) FROM modbus_proxy_transactions").fetchone()[0], 1)
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
                # The unlogged predecessor retains the true step shape.
                ("output_frequency", 5003),
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

    def test_sparse_analog_history_keeps_preceding_cycle_as_support_point(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path, {"enabled": True, "default_analog_delta": 0.1})
            register = Register("output_frequency", 0xFD00, 0.01, "Hz")
            database.store_cycle("2026-01-01T00:00:00Z", "VFAS1", 1, [(register, 5000)], [])
            # This physical cycle is deliberately not persisted by the delta
            # filter, but becomes the support point of the later change.
            database.store_cycle("2026-01-01T00:00:10Z", "VFAS1", 1, [(register, 5000)], [])
            database.store_cycle("2026-01-01T00:00:20Z", "VFAS1", 1, [(register, 6000)], [])
            database.close()
            connection = sqlite3.connect(path)
            rows = connection.execute(
                "SELECT observed_at, raw_value FROM samples WHERE metric='output_frequency' ORDER BY id"
            ).fetchall()
            self.assertEqual(rows, [
                ("2026-01-01T00:00:00Z", 5000),
                ("2026-01-01T00:00:10Z", 5000),
                ("2026-01-01T00:00:20Z", 6000),
            ])

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
            with database.connection:
                database.connection.execute(
                    "UPDATE recording_info SET created_at='2026-01-01T00:00:00.000+00:00' WHERE singleton=1"
                )
                database.connection.execute("DELETE FROM storage_growth_samples")
                database.connection.executemany(
                    """INSERT INTO storage_growth_samples
                       (observed_at,database_bytes,allocated_bytes,used_bytes,reusable_bytes)
                       VALUES (?,?,?,?,?)""",
                    [
                        ("2026-01-01T00:00:00.000+00:00", 2_000_000, 2_000_000, 1_000_000, 1_000_000),
                        ("2026-01-01T01:00:00.000+00:00", 2_000_000, 2_000_000, 1_360_000, 640_000),
                    ],
                )
            database.close()
            info = MonitorRepository(path).storage_info()
            self.assertEqual(info["observed_seconds"], 3600)
            self.assertEqual(info["growth_observed_seconds"], 3600)
            self.assertEqual(info["growth_bytes_per_second"], 100)
            self.assertEqual(info["sqlite_reusable_bytes"], 640_000)

    def test_storage_fixed_overhead_is_not_reported_as_growth(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            database = Database(path)
            with database.connection:
                database.connection.execute(
                    "UPDATE recording_info SET created_at='2026-01-01T00:00:00.000+00:00' WHERE singleton=1"
                )
                database.connection.execute("DELETE FROM storage_growth_samples")
                database.connection.executemany(
                    "INSERT INTO storage_growth_samples(observed_at, database_bytes) VALUES (?, ?)",
                    [
                        ("2026-01-01T00:00:00.000+00:00", 2_000_000),
                        ("2026-01-01T00:10:00.000+00:00", 2_000_000),
                    ],
                )
            database.close()
            info = MonitorRepository(path).storage_info()
            self.assertEqual(info["growth_observed_seconds"], 600)
            self.assertEqual(info["growth_bytes_per_second"], 0)

    def test_recording_generation_is_visible_to_existing_database_connections(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            first = Database(path, recording_reference="first")
            second = Database(path, recording_reference="first")
            before = second.recording_identity()
            first.reinitialize("second")
            self.assertNotEqual(second.recording_identity(), before)
            self.assertEqual(second.recording_identity()[0], "second")
            first.close(); second.close()

    def test_existing_addon_connection_can_write_zero_baseline_after_reinitialize(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            administrator = Database(path, recording_reference="first")
            addon = Database(path, {"enabled": False}, recording_reference="first")
            digital = Register("addon.field_di.input_01", 0xE000, 1.0, "on/off", record_history=True)
            addon.store_cycle("2026-01-01T00:00:00.000+00:00", "addon:field_di", -2, [(digital, 1)], [])
            administrator.reinitialize("second")
            addon.reset_runtime_state()
            addon.store_cycle("2026-01-01T00:00:01.000+00:00", "addon:field_di", -2, [(digital, 0)], [])
            self.assertEqual(addon.connection.execute(
                "SELECT raw_value FROM latest_values WHERE inverter='addon:field_di' AND metric='addon.field_di.input_01'"
            ).fetchone()[0], 0)
            self.assertEqual(addon.connection.execute(
                "SELECT raw_value FROM samples WHERE inverter='addon:field_di' AND metric='addon.field_di.input_01'"
            ).fetchone()[0], 0)
            administrator.close(); addon.close()

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

    def test_proxy_evidence_log_returns_recent_raw_transactions(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "measurements.sqlite3"
            connection = sqlite3.connect(path)
            connection.execute("""CREATE TABLE modbus_proxy_transactions (
                id INTEGER PRIMARY KEY, request_at TEXT, response_at TEXT,
                request_hex TEXT, response_hex TEXT, request_crc_valid INTEGER,
                response_crc_valid INTEGER, latency_ms REAL, outcome TEXT,
                origin TEXT NOT NULL DEFAULT 'hmi')""")
            connection.execute("""INSERT INTO modbus_proxy_transactions
                (request_at,response_at,request_hex,response_hex,request_crc_valid,response_crc_valid,latency_ms,outcome)
                VALUES (?,?,?,?,?,?,?,?)""",
                ("2026-01-01T00:00:00+00:00", None, "01 03 00 00", None, 0, None, 750.0, "response_timeout"))
            connection.commit(); connection.close()
            items = MonitorRepository(path).proxy_transactions(10)
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0]["request_hex"], "01 03 00 00")
            self.assertEqual(items[0]["outcome"], "response_timeout")

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
