#!/usr/bin/env python3
"""Create the initial TMM configuration without replacing existing data."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path


MODELS = {"VF-AS1", "VF-AS3J", "VF-S11", "VF-S15"}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--config", type=Path, required=True)
    result.add_argument("--template", type=Path, required=True)
    result.add_argument("--device", required=True)
    result.add_argument("--baudrate", type=int, required=True)
    result.add_argument("--model", required=True)
    result.add_argument("--name", required=True)
    result.add_argument("--slave-id", type=int, required=True)
    result.add_argument("--database", required=True)
    result.add_argument("--web-port", type=int, required=True)
    result.add_argument("--machine-speed-factor", default="")
    result.add_argument("--machine-speed-unit", default="rpm")
    result.add_argument("--rated-output-current-a", default="")
    result.add_argument("--rated-output-voltage-v", default="")
    result.add_argument("--motor-rated-power-kw", default="")
    result.add_argument("--motor-rated-speed-rpm", default="")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.config.exists():
        print(f"Existing configuration retained: {args.config}")
        return 0
    device = args.device.strip().upper()
    if not re.fullmatch(r"COM\d+", device):
        raise ValueError("serial device must be COM followed by a number")
    if args.baudrate not in {9600, 19200, 38400}:
        raise ValueError("baudrate must be 9600, 19200, or 38400")
    if args.model not in MODELS:
        raise ValueError(f"unsupported model: {args.model}")
    if not 1 <= args.slave_id <= 247:
        raise ValueError("Modbus address must be between 1 and 247")
    if not 1 <= args.web_port <= 65535:
        raise ValueError("web port must be between 1 and 65535")

    data = json.loads(args.template.read_text(encoding="utf-8"))
    data["serial"]["device"] = device
    data["serial"]["baudrate"] = args.baudrate
    engineering: dict[str, float | str] = {}
    numeric_options = {
        "machine_speed_factor": args.machine_speed_factor,
        "rated_output_current_a": args.rated_output_current_a,
        "rated_output_voltage_v": args.rated_output_voltage_v,
        "motor_rated_power_kw": args.motor_rated_power_kw,
        "motor_rated_speed_rpm": args.motor_rated_speed_rpm,
    }
    for key, value in numeric_options.items():
        if str(value).strip():
            number = float(value)
            if number <= 0:
                raise ValueError(f"{key} must be greater than zero")
            engineering[key] = number
    if ("motor_rated_power_kw" in engineering) != ("motor_rated_speed_rpm" in engineering):
        raise ValueError("motor rated power and speed must be configured together")
    if "machine_speed_factor" in engineering:
        unit = args.machine_speed_unit.strip()
        if not unit or len(unit) > 20:
            raise ValueError("machine speed unit must contain 1 to 20 characters")
        engineering["machine_speed_unit"] = unit
    inverter = {
        "name": args.name.strip() or args.model,
        "model": args.model,
        "slave_id": args.slave_id,
        "enabled": True,
    }
    if engineering:
        inverter["engineering"] = engineering
    data["inverters"] = [inverter]
    data["storage"]["database"] = args.database
    data["web"]["port"] = args.web_port

    args.config.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix="config-", suffix=".json", dir=args.config.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as output:
            json.dump(data, output, indent=2, ensure_ascii=False)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_name, args.config)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    print(f"Created configuration: {args.config}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
