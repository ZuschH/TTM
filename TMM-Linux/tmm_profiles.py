"""Built-in read-only register profiles for Toshiba Modbus Monitor."""

from __future__ import annotations

from copy import deepcopy


COMMON_MONITORS = [
    {"key": "output_frequency", "address": "0xFD00", "scale": 0.01, "unit": "Hz", "sampling": "fast"},
    {"key": "frequency_setpoint", "address": "0xFD02", "scale": 0.01, "unit": "Hz", "sampling": "fast"},
    {"key": "operating_status", "address": "0xFD01", "scale": 1, "unit": "raw", "sampling": "fast"},
    {"key": "output_current", "address": "0xFD03", "scale": 0.01, "unit": "%", "sampling": "fast"},
    {"key": "dc_input_voltage", "address": "0xFD04", "scale": 0.01, "unit": "%", "sampling": "normal"},
    {"key": "output_voltage", "address": "0xFD05", "scale": 0.01, "unit": "%", "sampling": "normal"},
    {"key": "trip_code", "address": "0xFC90", "scale": 1, "unit": "raw", "sampling": "normal"},
    {"key": "alarm_information_1", "address": "0xFC91", "scale": 1, "unit": "raw", "sampling": "normal"},
    {"key": "alarm_information_2", "address": "0xFC92", "scale": 1, "unit": "raw", "sampling": "normal"},
]

VF_S11_MONITORS = [
    {"key": "output_frequency", "address": "0xFD00", "scale": 0.01, "unit": "Hz", "sampling": "fast"},
    {"key": "frequency_setpoint", "address": "0xFE02", "scale": 0.01, "unit": "Hz", "sampling": "fast"},
    {"key": "operating_status", "address": "0xFD01", "scale": 1, "unit": "raw", "sampling": "fast"},
    {"key": "output_current", "address": "0xFE03", "scale": 0.01, "unit": "%", "sampling": "fast"},
    {"key": "dc_input_voltage", "address": "0xFE04", "scale": 0.01, "unit": "%"},
    {"key": "output_voltage", "address": "0xFE05", "scale": 0.01, "unit": "%"},
    {"key": "trip_code", "address": "0xFC90", "scale": 1, "unit": "raw"},
    {"key": "alarm_information_1", "address": "0xFC91", "scale": 1, "unit": "raw"},
]

BRAKING_MONITOR = [
    {"key": "braking_resistor_load", "address": "0xFD28", "scale": 1, "unit": "%", "sampling": "normal"},
]

VF_AS1_IO_MONITORS = [
    {"key": "input_terminal_status", "address": "0xFD06", "scale": 1, "unit": "raw", "sampling": "fast"},
    {"key": "fm_analog_output", "address": "0xFE40", "scale": 0.0488519785, "unit": "%"},
]

# Additional live diagnostics confirmed on the VF-AS1 family.  They are kept
# separate so that the more conservative profiles remain unchanged.
VF_AS1_EXTENDED_MONITORS = [
    {"key": "speed_feedback", "address": "0xFD16", "scale": 0.01, "unit": "Hz", "sampling": "diagnostic"},
    {"key": "speed_feedback_filtered", "address": "0xFD17", "scale": 0.01, "unit": "Hz", "sampling": "diagnostic"},
    {"key": "torque", "address": "0xFD18", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "torque_command", "address": "0xFD19", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "torque_current", "address": "0xFD20", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "exciting_current", "address": "0xFD21", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "motor_overload_factor", "address": "0xFD23", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "inverter_overload_factor", "address": "0xFD24", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "motor_load_factor", "address": "0xFD26", "scale": 1, "unit": "%", "sampling": "diagnostic"},
    {"key": "inverter_load_factor", "address": "0xFD27", "scale": 1, "unit": "%", "sampling": "diagnostic"},
    {"key": "input_power", "address": "0xFD29", "scale": 0.01, "unit": "kW", "sampling": "diagnostic"},
    {"key": "output_power", "address": "0xFD30", "scale": 0.01, "unit": "kW", "sampling": "diagnostic"},
    {"key": "calculated_motor_speed", "address": "0xFE90", "scale": 1, "unit": "rpm", "sampling": "diagnostic"},
]

SMALL_DRIVE_IO_MONITORS = [
    {"key": "input_terminal_status", "address": "0xFD06", "scale": 1, "unit": "raw", "sampling": "fast"},
]

MODERN_DRIVE_IO_MONITORS = SMALL_DRIVE_IO_MONITORS + [
    {"key": "fm_analog_output", "address": "0xFE40", "scale": 0.01, "unit": "%"},
]

VF_AS1_DIAGNOSTIC_MONITORS = [
    {"key": "trip_output_frequency", "address": "0xFE00", "scale": 0.01, "unit": "Hz", "sampling": "diagnostic"},
    {"key": "trip_operating_status", "address": "0xFE01", "scale": 1, "unit": "raw", "sampling": "diagnostic"},
    {"key": "trip_output_current", "address": "0xFE03", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "trip_dc_input_voltage", "address": "0xFE04", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "trip_output_voltage", "address": "0xFE05", "scale": 0.01, "unit": "%", "sampling": "diagnostic"},
    {"key": "past_trip_1", "address": "0xFE10", "scale": 1, "unit": "raw", "sampling": "diagnostic"},
    {"key": "past_trip_2", "address": "0xFE11", "scale": 1, "unit": "raw", "sampling": "diagnostic"},
    {"key": "past_trip_3", "address": "0xFE12", "scale": 1, "unit": "raw", "sampling": "diagnostic"},
    {"key": "past_trip_4", "address": "0xFE13", "scale": 1, "unit": "raw", "sampling": "diagnostic"},
]

COMMON_DEVICE_INFORMATION = [
    {"key": "inverter_capacity_code", "address": "0xFB05", "scale": 1, "unit": "raw", "sampling": "information"},
    {"key": "inverter_series_code", "address": "0xFB07", "scale": 1, "unit": "raw", "sampling": "information"},
    {"key": "cpu_version", "address": "0xFE08", "scale": 1, "unit": "raw", "sampling": "information"},
]

VF_AS3_TEMPERATURE_MONITORS = [
    {"key": "inverter_internal_temperature", "address": "0xFD83", "scale": 1, "unit": "°C", "sampling": "diagnostic"},
    {"key": "power_board_temperature", "address": "0xFD78", "scale": 1, "unit": "°C", "sampling": "diagnostic"},
]

VF_S11_DEVICE_INFORMATION = [
    {"key": "inverter_capacity_code", "address": "0xFB05", "scale": 1, "unit": "raw", "sampling": "information"},
    {"key": "cpu_version", "address": "0xFE08", "scale": 1, "unit": "raw", "sampling": "information"},
    {"key": "eeprom_version", "address": "0xFE09", "scale": 1, "unit": "raw", "sampling": "information"},
    {"key": "cpu2_version", "address": "0xFE73", "scale": 1, "unit": "raw", "sampling": "information"},
]

PROFILES = {
    "VF-AS1": {
        "registers": COMMON_MONITORS + BRAKING_MONITOR + VF_AS1_IO_MONITORS + VF_AS1_EXTENDED_MONITORS + VF_AS1_DIAGNOSTIC_MONITORS + COMMON_DEVICE_INFORMATION,
        "decoder": "VF-AS1",
        "max_read_words": 1,
    },
    "VF-S11": {
        "registers": VF_S11_MONITORS + SMALL_DRIVE_IO_MONITORS + VF_AS1_DIAGNOSTIC_MONITORS + VF_S11_DEVICE_INFORMATION,
        "decoder": "VF-S11",
        "max_read_words": 1,
    },
    "VF-S15": {
        "registers": COMMON_MONITORS + BRAKING_MONITOR + MODERN_DRIVE_IO_MONITORS + VF_AS1_DIAGNOSTIC_MONITORS + COMMON_DEVICE_INFORMATION,
        "decoder": "VF-S15",
        "max_read_words": 8,
    },
    "VF-AS3J": {
        "registers": COMMON_MONITORS + BRAKING_MONITOR + MODERN_DRIVE_IO_MONITORS + VF_AS1_DIAGNOSTIC_MONITORS + COMMON_DEVICE_INFORMATION + VF_AS3_TEMPERATURE_MONITORS,
        "decoder": "VF-AS3J",
        "max_read_words": 8,
    },
}

ALIASES = {
    "VFAS1": "VF-AS1",
    "VF-S11": "VF-S11",
    "VFS11": "VF-S11",
    "VF-S15": "VF-S15",
    "VFS15": "VF-S15",
    "VF-AS3": "VF-AS3J",
    "VFAS3": "VF-AS3J",
    "VF-AS3J": "VF-AS3J",
}


def canonical_model(model: str) -> str:
    normalized = model.strip().upper()
    result = ALIASES.get(normalized, normalized)
    if result not in PROFILES:
        raise ValueError(f"unknown inverter profile: {model}")
    return result


def profile(model: str) -> dict:
    name = canonical_model(model)
    result = deepcopy(PROFILES[name])
    result["model"] = name
    return result
