#!/usr/bin/env bash
# Interactive first-run configuration helper for Toshiba Modbus Monitor.
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Please run with sudo: sudo ./setup.sh" >&2
  exit 1
fi

CONFIG_PATH=${TMM_CONFIG_PATH:-/etc/tmm/config.json}
if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "Configuration not found: $CONFIG_PATH" >&2
  echo "Install TMM first, or set TMM_CONFIG_PATH to an existing config.json." >&2
  exit 1
fi

prompt_default() {
  local variable=$1 prompt=$2 default=$3 answer
  read -r -p "$prompt [$default]: " answer
  printf -v "$variable" '%s' "${answer:-$default}"
}

choose_value() {
  local variable=$1 prompt=$2 default=$3; shift 3
  local -a choices=("$@")
  local index=1 answer choice
  echo
  echo "$prompt"
  for choice in "${choices[@]}"; do
    echo "  $index) $choice"
    ((index++))
  done
  read -r -p "Selection [$default]: " answer
  answer=${answer:-$default}
  [[ $answer =~ ^[0-9]+$ ]] && (( answer >= 1 && answer <= ${#choices[@]} )) || { echo "Invalid selection." >&2; exit 1; }
  printf -v "$variable" '%s' "${choices[answer-1]}"
}

mapfile -t serial_candidates < <(
  {
    find -L /dev/serial/by-id -maxdepth 1 -type l -print 2>/dev/null || true
    printf '%s\n' /dev/ttyUSB* /dev/ttyACM*
  } | while IFS= read -r candidate; do [[ -e $candidate ]] && printf '%s\n' "$candidate"; done | sort -u
)

echo "Toshiba Modbus Monitor — interactive setup"
echo "Configuration: $CONFIG_PATH"
echo
if ((${#serial_candidates[@]})); then
  serial_candidates+=("Enter a device path manually")
  choose_value serial_device "Detected serial adapters:" 1 "${serial_candidates[@]}"
  if [[ $serial_device == "Enter a device path manually" ]]; then
    prompt_default serial_device "Serial device path" "/dev/ttyUSB0"
  fi
else
  echo "No USB serial adapter was detected. It may not yet be connected."
  prompt_default serial_device "Serial device path" "/dev/ttyUSB0"
fi

choose_value baudrate "Baud rate:" 2 9600 19200 38400
choose_value parity "Parity:" 1 E N O
prompt_default timeout_seconds "Response timeout in seconds" "0.75"
choose_value model "Inverter model:" 1 VF-AS1 VF-AS3J VF-S11 VF-S15
prompt_default inverter_name "Inverter name" "$model"
prompt_default slave_id "Modbus slave address" "1"
prompt_default fast_interval "Fast polling interval in seconds" "0.2"
prompt_default normal_interval "Normal polling interval in seconds" "0.5"
prompt_default diagnostic_interval "Diagnostic polling interval in seconds" "5.0"
prompt_default database_path "SQLite database path" "/var/lib/tmm/measurements.sqlite3"
prompt_default retention_days "Retention in days (0 = unlimited)" "365"
prompt_default web_port "Web interface port" "8080"
choose_value remote_admin "Allow administration from remote hosts?" 2 yes no
prompt_default recording_reference "Initial investigation reference (optional)" ""
prompt_default contact_name "Contact name (optional)" ""
prompt_default contact_url "Contact URL or e-mail (optional)" ""

backup_path="${CONFIG_PATH}.before-setup-$(date +%Y%m%d-%H%M%S)"
cp --preserve=mode,ownership,timestamps "$CONFIG_PATH" "$backup_path"

python3 - "$CONFIG_PATH" "$serial_device" "$baudrate" "$parity" "$timeout_seconds" "$inverter_name" "$model" "$slave_id" "$fast_interval" "$normal_interval" "$diagnostic_interval" "$database_path" "$retention_days" "$web_port" "$remote_admin" "$recording_reference" "$contact_name" "$contact_url" <<'PY'
import json
import math
import os
import sys
from pathlib import Path

(path, device, baud, parity, timeout, name, model, slave, fast, normal, diagnostic,
 database, retention, port, remote_admin, reference, contact_name, contact_url) = sys.argv[1:]

def number(value, label, minimum=0, integer=False):
    try:
        result = int(value) if integer else float(value)
    except ValueError as error:
        raise SystemExit(f"{label} must be numeric") from error
    if not math.isfinite(result) or result < minimum:
        raise SystemExit(f"{label} must be at least {minimum}")
    return result

if not device.startswith("/dev/"):
    raise SystemExit("Serial device must be an absolute /dev/ path")
if parity not in {"E", "N", "O"}:
    raise SystemExit("Parity must be E, N, or O")
if model not in {"VF-AS1", "VF-AS3J", "VF-S11", "VF-S15"}:
    raise SystemExit("Unsupported inverter model")
if not name.strip() or len(name) > 120:
    raise SystemExit("Inverter name must contain 1 to 120 characters")

timeout = number(timeout, "Timeout", 0.05)
slave = number(slave, "Slave address", 1, True)
if slave > 247:
    raise SystemExit("Slave address must not exceed 247")
fast = number(fast, "Fast interval", 0.05)
normal = number(normal, "Normal interval", 0.05)
diagnostic = number(diagnostic, "Diagnostic interval", 0.05)
retention = number(retention, "Retention", 0, True)
port = number(port, "Web port", 1, True)
if port > 65535:
    raise SystemExit("Web port must not exceed 65535")

config_path = Path(path)
with config_path.open(encoding="utf-8") as source:
    config = json.load(source)
serial = config.setdefault("serial", {})
serial.update({"device": device, "baudrate": int(baud), "parity": parity, "stopbits": 1, "bytesize": 8, "timeout_seconds": timeout})
config["inverters"] = [{"name": name.strip(), "model": model, "slave_id": slave, "enabled": True}]
polling = config.setdefault("polling", {}); intervals = polling.setdefault("intervals", {})
intervals.update({"fast": fast, "normal": normal, "diagnostic": diagnostic})
storage = config.setdefault("storage", {}); storage["database"] = database; storage["retention_days"] = retention
web = config.setdefault("web", {}); web["port"] = port; web["allow_remote_administration"] = remote_admin == "yes"
config.setdefault("recording", {})["reference"] = reference.strip()
config.setdefault("product", {}).update({"contact_name": contact_name.strip(), "contact_url": contact_url.strip()})

temporary = config_path.with_suffix(".setup.tmp")
temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
json.loads(temporary.read_text(encoding="utf-8"))
# Keep the service-readable permission and ownership of /etc/tmm/config.json.
# A plain atomic replacement would otherwise create a root:root, world-readable
# configuration file according to the process umask.
original_stat = config_path.stat()
os.chmod(temporary, original_stat.st_mode)
try:
    os.chown(temporary, original_stat.st_uid, original_stat.st_gid)
except PermissionError:
    pass
os.replace(temporary, config_path)
PY

echo
echo "Configuration written successfully. Backup: $backup_path"
read -r -p "Restart TMM services now? [Y/n]: " restart
if [[ ${restart:-Y} =~ ^[Yy]$ ]]; then
  systemctl restart tmm.service tmm-web.service
  echo "TMM services restarted."
else
  echo "Restart later with: sudo systemctl restart tmm.service tmm-web.service"
fi
