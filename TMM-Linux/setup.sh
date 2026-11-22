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

if [[ ${1:-} == "--edit-config" ]]; then
  command -v nano >/dev/null 2>&1 || { echo "nano is not installed (install it with: sudo apt-get install nano)." >&2; exit 1; }
  exec nano "$CONFIG_PATH"
fi

prompt_default() {
  local variable=$1 prompt=$2 default=$3 answer
  if [[ ${use_dialog:-no} == yes ]]; then
    answer=$(dialog --stdout --title "TMM setup" --inputbox "$prompt" 9 76 "$default") || exit 0
    printf -v "$variable" '%s' "${answer:-$default}"
    return
  fi
  read -r -p "$prompt [$default]: " answer
  printf -v "$variable" '%s' "${answer:-$default}"
}

choose_value() {
  local variable=$1 prompt=$2 default=$3; shift 3
  local -a choices=("$@")
  local index=1 answer choice
  if [[ ${use_dialog:-no} == yes ]]; then
    local -a menu=()
    for choice in "${choices[@]}"; do menu+=("$index" "$choice"); ((index++)); done
    answer=$(dialog --stdout --title "TMM setup" --default-item "$default" --menu "$prompt" 18 76 "${#choices[@]}" "${menu[@]}") || exit 0
    [[ $answer =~ ^[0-9]+$ ]] && (( answer >= 1 && answer <= ${#choices[@]} )) || exit 0
    printf -v "$variable" '%s' "${choices[answer-1]}"
    return
  fi
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

confirm() {
  local prompt=$1 default=${2:-yes} answer
  if [[ ${use_dialog:-no} == yes ]]; then
    if [[ $default == yes ]]; then dialog --title "TMM setup" --yesno "$prompt" 8 76
    else dialog --title "TMM setup" --defaultno --yesno "$prompt" 8 76
    fi
    return $?
  fi
  read -r -p "$prompt [$([[ $default == yes ]] && printf 'Y/n' || printf 'y/N')]: " answer
  [[ ${answer:-$([[ $default == yes ]] && printf Y || printf N)} =~ ^[Yy]$ ]]
}

ensure_i2c_runtime() {
  # All Sequent boards used by TMM communicate via /dev/i2c-1.  The vendor
  # Python modules cannot create that device themselves, so load the standard
  # kernel interface before attempting any driver installation or probe.
  [[ -e /dev/i2c-1 ]] && return 0
  echo "I²C bus /dev/i2c-1 is not available; loading the I²C kernel modules …"
  modprobe i2c-dev 2>/dev/null || true
  modprobe i2c-bcm2835 2>/dev/null || true
  if [[ -e /dev/i2c-1 ]]; then
    install -d -m 0755 /etc/modules-load.d
    printf 'i2c-dev\n' >/etc/modules-load.d/tmm-i2c.conf
    return 0
  fi
  echo "I²C is still unavailable." >&2
  if command -v raspi-config >/dev/null 2>&1 && confirm "Enable I²C now via raspi-config?" yes; then
    raspi-config nonint do_i2c 0 || true
    modprobe i2c-dev 2>/dev/null || true
    modprobe i2c-bcm2835 2>/dev/null || true
  fi
  [[ -e /dev/i2c-1 ]] || echo "Enable I²C and reboot if requested; TMM will keep affected cards unavailable until then." >&2
}

ensure_configured_sequent_drivers() {
  local runtime_python=/opt/tmm/.venv/bin/python
  [[ -x $runtime_python ]] || runtime_python=python3
  # An array declared without an assignment is still considered unset by older
  # Bash releases.  Explicit initialization keeps ${#packages[@]} safe under
  # `set -u` when every required driver is already installed.
  local -a required=() missing=() packages=()
  mapfile -t required < <("$runtime_python" - "$CONFIG_PATH" <<'PY'
import json
import sys

drivers = {
    "sequent_16inpind": ("lib16inpind", "SM16inpind"),
    "sequent_24b8vin": ("SM24b8vin", "SM24b8vin"),
    "sequent_multiio": ("multiio", "SMmultiio"),
    "sequent_super_watchdog": ("wdt", "SMwdt"),
    "sequent_smart_fan": ("sfan", "SMsfan"),
}
for addon in json.load(open(sys.argv[1], encoding="utf-8")).get("addons", []):
    if isinstance(addon, dict) and addon.get("enabled", True) and addon.get("type") in drivers:
        print("\t".join(drivers[addon["type"]]))
PY
  )
  ((${#required[@]})) || return 0
  ensure_i2c_runtime
  for entry in "${required[@]}"; do
    IFS=$'\t' read -r module package <<<"$entry"
    "$runtime_python" -c "import $module" >/dev/null 2>&1 || { missing+=("$module"); packages+=("$package"); }
  done
  ((${#packages[@]})) || { echo "Sequent drivers: all required modules are available."; return 0; }
  echo "Missing Sequent modules: ${missing[*]}"
  if confirm "Install/update the required Sequent Python drivers now (internet required)?" yes; then
    apt-get update
    apt-get install -y i2c-tools python3-smbus
    install_sequent_driver_packages "$runtime_python" "${packages[@]}"
  else
    echo "The configured cards remain unavailable until their driver packages are installed." >&2
  fi
}

# SMsfan 1.2.0 still declares the obsolete RPi.GPIO package although its
# current code uses gpiozero and smbus2 instead.  RPi.GPIO has no modern
# aarch64/Python 3.13 wheel and needlessly falls back to a native build.  Keep
# the real runtime dependencies explicit and install only SMsfan without its
# inaccurate legacy dependency metadata.
install_sequent_driver_packages() {
  local runtime_python=$1 package
  shift
  local -a regular_packages=()
  local smart_fan=no
  for package in "$@"; do
    if [[ $package == SMsfan ]]; then smart_fan=yes; else regular_packages+=("$package"); fi
  done
  ((${#regular_packages[@]})) && "$runtime_python" -m pip install --disable-pip-version-check -U "${regular_packages[@]}"
  if [[ $smart_fan == yes ]]; then
    "$runtime_python" -m pip install --disable-pip-version-check -U 'smbus2>=0.4' 'gpiozero>=2.0.0'
    "$runtime_python" -m pip install --disable-pip-version-check -U --no-deps SMsfan
  fi
}

config_document_count() {
  python3 - "$CONFIG_PATH" <<'PY'
import json, sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
decoder = json.JSONDecoder(); documents = []; position = 0
while True:
    while position < len(text) and text[position].isspace(): position += 1
    if position >= len(text): break
    try: value, position = decoder.raw_decode(text, position)
    except json.JSONDecodeError: print(0); raise SystemExit
    if not isinstance(value, dict): print(0); raise SystemExit
    documents.append(value)
print(len(documents))
PY
}

config_has_only_trailing_closing_braces() {
  python3 - "$CONFIG_PATH" <<'PY'
import json, sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
try:
    json.loads(text)
except json.JSONDecodeError as error:
    try:
        value = json.loads(text[:error.pos])
    except (json.JSONDecodeError, ValueError):
        raise SystemExit(1)
    suffix = text[error.pos:]
    if isinstance(value, dict) and suffix.strip() and all(character == "}" or character.isspace() for character in suffix):
        raise SystemExit(0)
raise SystemExit(1)
PY
}

show_config_json_error() {
  python3 - "$CONFIG_PATH" <<'PY'
import json, sys
from pathlib import Path

path = Path(sys.argv[1]); text = path.read_text(encoding="utf-8")
try:
    value = json.loads(text)
    if not isinstance(value, dict): raise ValueError("top-level JSON value must be an object")
except json.JSONDecodeError as error:
    lines = text.splitlines()
    first=max(0,error.lineno-3); last=min(len(lines),error.lineno+2)
    print(f"Invalid TMM configuration: {path}", file=sys.stderr)
    print(f"{error.msg} at line {error.lineno}, column {error.colno} (character {error.pos})", file=sys.stderr)
    for number in range(first,last):
        marker=">" if number+1 == error.lineno else " "
        print(f"{marker} {number+1:5d}: {lines[number][:180]}", file=sys.stderr)
    raise SystemExit(1)
except (OSError, UnicodeError, ValueError) as error:
    print(f"Invalid TMM configuration: {path}: {error}", file=sys.stderr); raise SystemExit(1)
PY
}

repair_config_document() {
  local selection=$1 backup_path
  backup_path="${CONFIG_PATH}.invalid-$(date +%Y%m%d-%H%M%S)-$$"
  cp --preserve=mode,ownership,timestamps "$CONFIG_PATH" "$backup_path"
  python3 - "$CONFIG_PATH" "$selection" <<'PY'
import json, os, sys
from pathlib import Path

path=Path(sys.argv[1]); selection=sys.argv[2]; text=path.read_text(encoding="utf-8")
decoder=json.JSONDecoder(); documents=[]; position=0
while True:
    while position < len(text) and text[position].isspace(): position += 1
    if position >= len(text): break
    value, position=decoder.raw_decode(text,position)
    if not isinstance(value,dict): raise SystemExit("Every candidate document must be a JSON object")
    documents.append(value)
if len(documents) < 2: raise SystemExit("No complete duplicate JSON documents were found")
selected=documents[0 if selection == "first" else -1]
temporary=path.with_name(f".{path.name}.repair-{os.getpid()}")
metadata=path.stat()
temporary.write_text(json.dumps(selected,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
os.chmod(temporary,metadata.st_mode & 0o7777)
os.chown(temporary,metadata.st_uid,metadata.st_gid)
json.loads(temporary.read_text(encoding="utf-8"))
os.replace(temporary,path)
PY
  echo "Invalid original configuration preserved as: $backup_path"
}

repair_trailing_config_data() {
  local backup_path
  backup_path="${CONFIG_PATH}.invalid-$(date +%Y%m%d-%H%M%S)-$$"
  cp --preserve=mode,ownership,timestamps "$CONFIG_PATH" "$backup_path"
  python3 - "$CONFIG_PATH" <<'PY'
import json, os, sys
from pathlib import Path

path=Path(sys.argv[1]); text=path.read_text(encoding="utf-8")
try:
    json.loads(text)
    raise SystemExit("Configuration is already valid")
except json.JSONDecodeError as error:
    value=json.loads(text[:error.pos]); suffix=text[error.pos:]
if not isinstance(value,dict) or not suffix.strip() or not all(character == "}" or character.isspace() for character in suffix):
    raise SystemExit("Refusing repair: trailing data is not limited to closing braces")
temporary=path.with_name(f".{path.name}.repair-{os.getpid()}")
metadata=path.stat()
temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
os.chmod(temporary,metadata.st_mode & 0o7777)
os.chown(temporary,metadata.st_uid,metadata.st_gid)
json.loads(temporary.read_text(encoding="utf-8"))
os.replace(temporary,path)
PY
  echo "Invalid original configuration preserved as: $backup_path"
}

ensure_valid_config_json() {
  local count repair_action
  while ! show_config_json_error; do
    count=$(config_document_count)
    if config_has_only_trailing_closing_braces; then
      choose_value repair_action "The valid JSON object is followed only by an extra closing brace." 3 \
        "Remove the extra trailing closing brace(s)" \
        "Open config.json in nano" \
        "Exit without changing the file"
      case "$repair_action" in
        "Remove the extra trailing closing brace(s)") repair_trailing_config_data ;;
        "Open config.json in nano") command -v nano >/dev/null 2>&1 || { echo "nano is not installed." >&2; exit 1; }; nano "$CONFIG_PATH" ;;
        *) exit 1 ;;
      esac
    elif [[ $count =~ ^[0-9]+$ ]] && (( count >= 2 )); then
      echo "Detected $count complete JSON documents in a file that must contain exactly one."
      choose_value repair_action "How should the configuration be repaired?" 4 \
        "Keep the first complete document" \
        "Keep the last complete document" \
        "Open config.json in nano" \
        "Exit without changing the file"
      case "$repair_action" in
        "Keep the first complete document") repair_config_document first ;;
        "Keep the last complete document") repair_config_document last ;;
        "Open config.json in nano") command -v nano >/dev/null 2>&1 || { echo "nano is not installed." >&2; exit 1; }; nano "$CONFIG_PATH" ;;
        *) exit 1 ;;
      esac
    else
      choose_value repair_action "The configuration contains a JSON syntax error." 2 \
        "Open config.json in nano" \
        "Exit without changing the file"
      if [[ $repair_action == "Open config.json in nano" ]]; then
        command -v nano >/dev/null 2>&1 || { echo "nano is not installed." >&2; exit 1; }
        nano "$CONFIG_PATH"
      else
        exit 1
      fi
    fi
  done
}

ensure_valid_config_json

mapfile -t serial_candidates < <(
  {
    find /dev/serial/by-id -maxdepth 1 -type l -print 2>/dev/null || true
    printf '%s\n' /dev/ttyUSB* /dev/ttyACM*
  } | while IFS= read -r candidate; do [[ -e $candidate ]] && printf '%s\n' "$candidate"; done | sort -u
)

echo "Toshiba Modbus Monitor — interactive setup"
echo "Configuration: $CONFIG_PATH"
echo
use_dialog=no
if [[ -t 0 && -t 1 ]]; then
  if command -v dialog >/dev/null 2>&1; then
    use_dialog=yes
  elif confirm "Install the optional dialog package for a menu-guided setup?" yes; then
    apt-get update && apt-get install -y dialog && use_dialog=yes
  fi
fi
choose_value setup_action "What would you like to do?" 1 \
  "Configure transparent HMI proxy" \
  "Configure serial buses and inverters" \
  "Configure field I/O sources and channels" \
  "Guided configuration" \
  "Edit config.json directly (nano)" \
  "Exit without changes"
case "$setup_action" in
  "Configure transparent HMI proxy")
    runtime_python=/opt/tmm/.venv/bin/python
    [[ -x $runtime_python ]] || runtime_python=python3
    setup_program=/opt/tmm/tmm_setup.py
    [[ -f $setup_program ]] || setup_program="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/tmm_setup.py"
    "$runtime_python" "$setup_program" --config "$CONFIG_PATH" --proxy
    if confirm "Restart TMM services now?" yes; then
      systemctl restart tmm.service tmm-web.service
      echo "TMM services restarted. HMI forwarding has priority; optional TMM polling uses configured idle windows."
    else
      echo "Restart later with: sudo systemctl restart tmm.service tmm-web.service"
    fi
    exit 0
    ;;
  "Configure serial buses and inverters")
    runtime_python=/opt/tmm/.venv/bin/python
    [[ -x $runtime_python ]] || runtime_python=python3
    setup_program=/opt/tmm/tmm_setup.py
    [[ -f $setup_program ]] || setup_program="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/tmm_setup.py"
    "$runtime_python" "$setup_program" --config "$CONFIG_PATH" --serial
    if confirm "Restart TMM services now?" yes; then
      systemctl restart tmm.service tmm-web.service
      echo "TMM services restarted."
    else
      echo "Restart later with: sudo systemctl restart tmm.service tmm-web.service"
    fi
    exit 0
    ;;
  "Configure field I/O sources and channels")
    runtime_python=/opt/tmm/.venv/bin/python
    [[ -x $runtime_python ]] || runtime_python=python3
    setup_program=/opt/tmm/tmm_setup.py
    [[ -f $setup_program ]] || setup_program="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/tmm_setup.py"
    "$runtime_python" "$setup_program" --config "$CONFIG_PATH"
    ensure_configured_sequent_drivers
    if confirm "Restart TMM services now?" yes; then
      systemctl restart tmm.service tmm-web.service
      echo "TMM services restarted."
    else
      echo "Restart later with: sudo systemctl restart tmm.service tmm-web.service"
    fi
    exit 0
    ;;
  "Edit config.json directly (nano)")
    command -v nano >/dev/null 2>&1 || { echo "nano is not installed (install it with: sudo apt-get install nano)." >&2; exit 1; }
    nano "$CONFIG_PATH"
    echo "Configuration editor closed. Restart when appropriate: sudo systemctl restart tmm.service tmm-web.service"
    exit 0
    ;;
  "Exit without changes") exit 0 ;;
esac
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

# External I/O is optional and intentionally configured here, not in the
# regular Modbus polling questions. It uses the Pi I²C bus exclusively.
choose_value addon_mode "External Sequent I/O add-ons:" 1 "Keep existing configuration" "Configure Sequent cards now" "Disable all external I/O add-ons"
addon_selection=none
di_stack=0; di_id=field_di; di_label="External digital inputs"
ai_stack=1; ai_id=field_ai; ai_label="External analog inputs"; ai_channel=1; ai_channel_label="Analog input 1"; ai_scale=1; ai_offset=0; ai_unit=V
mi_stack=2; mi_id=field_multiio; mi_label="External Multi-IO"
fan_enabled=no; fan_stack=0; fan_id=system_fan; fan_label="System cooling"
ups_enabled=no; ups_id=system_ups; ups_label="System UPS & watchdog"
di_detected=""; ai_detected=""; mi_detected=""; fan_detected=""

has_addon() {
  [[ ",$addon_selection," == *",$1,"* ]]
}

if [[ $addon_mode == "Configure Sequent cards now" ]]; then
  echo
  if [[ ! -e /dev/i2c-1 ]]; then
    echo "I²C bus /dev/i2c-1 was not found. Enable I²C in raspi-config, reboot if requested, then run setup again." >&2
    if command -v raspi-config >/dev/null 2>&1; then
      read -r -p "Open raspi-config now? [y/N]: " open_i2c
      if [[ ${open_i2c:-N} =~ ^[Yy]$ ]]; then raspi-config; fi
    fi
  else
    echo "I²C bus detected: /dev/i2c-1"
    if command -v i2cdetect >/dev/null 2>&1; then
      echo "Detected I²C addresses (a card is only probed; no outputs are changed):"
      i2cdetect -y 1 || true
    else
      echo "Tip: install i2c-tools to display detected I²C addresses."
    fi
  fi
  choose_value addon_selection "Which cards should TMM configure?" 8 "No card" "Sixteen LV Digital Inputs" "Eight 24-Bit Analog Inputs DAQ" "Multi-IO" "Digital + Analog" "Digital + Multi-IO" "Analog + Multi-IO" "All three card types"
  case "$addon_selection" in
    "No card") addon_selection=none ;;
    "Sixteen LV Digital Inputs") addon_selection=digital ;;
    "Eight 24-Bit Analog Inputs DAQ") addon_selection=analog ;;
    "Multi-IO") addon_selection=multiio ;;
    "Digital + Analog") addon_selection=digital,analog ;;
    "Digital + Multi-IO") addon_selection=digital,multiio ;;
    "Analog + Multi-IO") addon_selection=analog,multiio ;;
    "All three card types") addon_selection=digital,analog,multiio ;;
  esac
  confirm "Configure Sequent Smart Fan HAT too?" no && fan_enabled=yes
  confirm "Configure Sequent Super Watchdog & UPS HAT too?" no && ups_enabled=yes
  if [[ $addon_selection != none || $fan_enabled == yes || $ups_enabled == yes ]]; then
    ensure_i2c_runtime
    runtime_python=/opt/tmm/.venv/bin/python
    [[ -x $runtime_python ]] || runtime_python=python3
    driver_modules=(); driver_packages=()
    has_addon digital && { driver_modules+=(lib16inpind); driver_packages+=(SM16inpind); }
    has_addon analog && { driver_modules+=(SM24b8vin); driver_packages+=(SM24b8vin); }
    has_addon multiio && { driver_modules+=(multiio); driver_packages+=(SMmultiio); }
    [[ $fan_enabled == yes ]] && { driver_modules+=(sfan); driver_packages+=(SMsfan); }
    [[ $ups_enabled == yes ]] && { driver_modules+=(wdt); driver_packages+=(SMwdt); }
    drivers_missing=no
    for driver_module in "${driver_modules[@]}"; do "$runtime_python" -c "import $driver_module" >/dev/null 2>&1 || drivers_missing=yes; done
    if [[ $drivers_missing == yes ]]; then
      if confirm "Install/update the required Sequent Python drivers now (internet required)?" yes; then
        apt-get update
        apt-get install -y i2c-tools python3-smbus
        install_sequent_driver_packages "$runtime_python" "${driver_packages[@]}"
      else
        echo "Drivers are not installed. TMM will show the card as unavailable until they are installed." >&2
      fi
    fi
    if [[ -e /dev/i2c-1 ]]; then
      echo "Driver probe (detected stacks only):"
      probe_output=$("$runtime_python" - <<'PY' || true
for kind, module_name, factory, probe_method in (
    ("digital", "lib16inpind", None, "readAll"),
    # A real input read avoids false positives from version-only probes.
    ("analog", "SM24b8vin", "SM24b8vin", "get_u_in"),
    ("multiio", "multiio", "SMmultiio", "get_u_in"),
    ("fan", "sfan", None, "getPower"),
):
    try:
        module = __import__(module_name)
    except Exception as error:
        print(f"  {kind}: driver unavailable ({error})")
        continue
    found = []
    for stack in range(8):
        try:
            if kind == "fan":
                # Smart-Fan revisions use two different address layouts.  Fan
                # power is available on both of them; temperature is not.
                # It is therefore the only reliable non-invasive probe.
                value = getattr(module, probe_method)(stack)
                if value < 0:
                    continue
            elif factory:
                value = getattr(getattr(module, factory)(stack=stack), probe_method)(1)
            else:
                value = module.readAll(stack)
            # Several vendor libraries signal an absent card with -1 instead
            # of raising.  Do not offer that stack as an automatic default.
            if value == -1:
                continue
            found.append(str(stack))
            print(f"    {kind}: stack {stack} responded ({value})")
        except Exception:
            pass
    stacks = ",".join(found)
    print(f"  {kind}: stack " + (stacks.replace(",", ", ") if stacks else "not detected"))
    # Machine-readable companion line: the shell uses the first detected ID
    # as the safe default but still lets the technician choose another stack.
    print(f"TMM_DETECTED_{kind}={stacks}")
PY
      )
      printf '%s\n' "$probe_output"
      di_detected=$(awk -F= '$1 == "TMM_DETECTED_digital" { print $2; exit }' <<<"$probe_output")
      ai_detected=$(awk -F= '$1 == "TMM_DETECTED_analog" { print $2; exit }' <<<"$probe_output")
      mi_detected=$(awk -F= '$1 == "TMM_DETECTED_multiio" { print $2; exit }' <<<"$probe_output")
      fan_detected=$(awk -F= '$1 == "TMM_DETECTED_fan" { print $2; exit }' <<<"$probe_output")
    fi
  fi
  if has_addon digital; then
    di_default=${di_detected%%,*}; [[ -n $di_default ]] || di_default=0
    di_hint=${di_detected:-none}
    prompt_default di_stack "Digital card stack address (0-7; detected: $di_hint)" "$di_default"
    prompt_default di_id "Digital card ID" "$di_id"
    prompt_default di_label "Digital card label" "$di_label"
  fi
  if has_addon analog; then
    ai_default=${ai_detected%%,*}; [[ -n $ai_default ]] || ai_default=1
    ai_hint=${ai_detected:-none}
    prompt_default ai_stack "Analog card stack address (0-7; detected: $ai_hint)" "$ai_default"
    prompt_default ai_id "Analog card ID" "$ai_id"
    prompt_default ai_label "Analog card label" "$ai_label"
    prompt_default ai_channel "First analog channel to configure (1-8)" "1"
    prompt_default ai_channel_label "Analog channel label" "$ai_channel_label"
    prompt_default ai_scale "Scaling multiplier (engineering value = V × multiplier + offset)" "1"
    prompt_default ai_offset "Scaling offset" "0"
    prompt_default ai_unit "Engineering unit" "V"
  fi
  if has_addon multiio; then
    mi_default=${mi_detected%%,*}; [[ -n $mi_default ]] || mi_default=2
    mi_hint=${mi_detected:-none}
    prompt_default mi_stack "Multi-IO card stack address (0-7; detected: $mi_hint)" "$mi_default"
    prompt_default mi_id "Multi-IO card ID" "$mi_id"
    prompt_default mi_label "Multi-IO card label" "$mi_label"
  fi
  if [[ $fan_enabled == yes ]]; then
    fan_default=${fan_detected%%,*}; [[ -n $fan_default ]] || fan_default=0
    fan_hint=${fan_detected:-none}
    prompt_default fan_stack "Smart Fan stack address (0-1; detected: $fan_hint)" "$fan_default"
    prompt_default fan_id "Smart Fan card ID" "$fan_id"
    prompt_default fan_label "Smart Fan label" "$fan_label"
  fi
  if [[ $ups_enabled == yes ]]; then
    echo "The Super Watchdog has a fixed I²C address; TMM will not actively probe it during setup."
    prompt_default ups_id "Super Watchdog & UPS card ID" "$ups_id"
    prompt_default ups_label "Super Watchdog & UPS label" "$ups_label"
  fi
fi

backup_path="${CONFIG_PATH}.before-setup-$(date +%Y%m%d-%H%M%S)"
cp --preserve=mode,ownership,timestamps "$CONFIG_PATH" "$backup_path"

python3 - "$CONFIG_PATH" "$serial_device" "$baudrate" "$parity" "$timeout_seconds" "$inverter_name" "$model" "$slave_id" "$fast_interval" "$normal_interval" "$diagnostic_interval" "$database_path" "$retention_days" "$web_port" "$remote_admin" "$recording_reference" "$contact_name" "$contact_url" "$addon_mode" "$addon_selection" "$di_stack" "$di_id" "$di_label" "$ai_stack" "$ai_id" "$ai_label" "$ai_channel" "$ai_channel_label" "$ai_scale" "$ai_offset" "$ai_unit" "$mi_stack" "$mi_id" "$mi_label" "$fan_enabled" "$fan_stack" "$fan_id" "$fan_label" "$ups_enabled" "$ups_id" "$ups_label" <<'PY'
import json
import math
import os
import sys
from pathlib import Path

(path, device, baud, parity, timeout, name, model, slave, fast, normal, diagnostic,
 database, retention, port, remote_admin, reference, contact_name, contact_url,
 addon_mode, addon_selection, di_stack, di_id, di_label, ai_stack, ai_id, ai_label,
 ai_channel, ai_channel_label, ai_scale, ai_offset, ai_unit, mi_stack, mi_id, mi_label,
 fan_enabled, fan_stack, fan_id, fan_label, ups_enabled, ups_id, ups_label) = sys.argv[1:]

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
config["inverters"] = [{"name": name.strip(), "model": model, "slave_id": slave, "enabled": True, "channels": {}}]
polling = config.setdefault("polling", {}); intervals = polling.setdefault("intervals", {})
intervals.update({"fast": fast, "normal": normal, "diagnostic": diagnostic})
storage = config.setdefault("storage", {}); storage["database"] = database; storage["retention_days"] = retention
web = config.setdefault("web", {}); web["port"] = port; web["allow_remote_administration"] = remote_admin == "yes"
config.setdefault("recording", {})["reference"] = reference.strip()
config.setdefault("product", {}).update({"contact_name": contact_name.strip(), "contact_url": contact_url.strip()})

if addon_mode == "Disable all external I/O add-ons":
    config["addons"] = []
elif addon_mode == "Configure Sequent cards now":
    def addon_number(value, label, low, high, integer=False):
        result = number(value, label, low, integer)
        if result > high:
            raise SystemExit(f"{label} must not exceed {high}")
        return result
    # System cards are configured independently of the field I/O selection.
    # Retain them when setup is re-run to add or re-address an I/O HAT.
    addons = [dict(item) for item in config.get("addons", []) if isinstance(item, dict) and (
        (item.get("type") == "sequent_super_watchdog" and ups_enabled != "yes") or
        (item.get("type") == "sequent_smart_fan" and fan_enabled != "yes")
    )]
    selected = set(addon_selection.split(","))
    if "digital" in selected:
        stack = addon_number(di_stack, "Digital stack", 0, 7, True)
        if not di_id.replace("_", "").replace("-", "").isalnum():
            raise SystemExit("Digital card ID may contain only letters, numbers, _ or -")
        addons.append({"id": di_id, "type": "sequent_16inpind", "label": di_label.strip() or di_id,
                       "stack": stack, "interval_seconds": 0.02, "enabled": True, "channels": []})
    if "analog" in selected:
        stack = addon_number(ai_stack, "Analog stack", 0, 7, True)
        channel = addon_number(ai_channel, "Analog channel", 1, 8, True)
        if not ai_id.replace("_", "").replace("-", "").isalnum():
            raise SystemExit("Analog card ID may contain only letters, numbers, _ or -")
        # Older Super-Watchdog entries deliberately have no stack field.  They
        # are retained above, so collision detection must only inspect cards
        # which actually declare one.
        if any(item.get("stack") == stack and item.get("type") == "sequent_24b8vin" for item in addons):
            raise SystemExit("Only one analog card may use the same stack address")
        addons.append({"id": ai_id, "type": "sequent_24b8vin", "label": ai_label.strip() or ai_id,
                       "stack": stack, "interval_seconds": 0.05, "enabled": True,
                       "channels": [{"channel": channel, "label": ai_channel_label.strip() or f"AI {channel}",
                                     "gain": 1, "scale": number(ai_scale, "Analog scaling", -math.inf),
                                     "offset": number(ai_offset, "Analog offset", -math.inf), "unit": ai_unit.strip() or "V", "enabled": False, "record": False, "live": False}]})
    if "multiio" in selected:
        stack = addon_number(mi_stack, "Multi-IO stack", 0, 7, True)
        if not mi_id.replace("_", "").replace("-", "").isalnum():
            raise SystemExit("Multi-IO card ID may contain only letters, numbers, _ or -")
        addons.append({"id": mi_id, "type": "sequent_multiio", "label": mi_label.strip() or mi_id,
                       "stack": stack, "interval_seconds": 0.05, "enabled": True, "channels": [
                           {"signal": "digital", "channel": channel, "label": f"Digital input {channel}", "enabled": False, "record": False, "live": False}
                           for channel in range(1, 5)
                       ] + [
                           {"signal": "voltage", "channel": channel, "label": f"Voltage input {channel}", "unit": "V", "enabled": False, "record": False, "live": False}
                           for channel in range(1, 3)
                       ] + [
                           {"signal": "current", "channel": channel, "label": f"Current input {channel}", "unit": "mA", "enabled": False, "record": False, "live": False}
                           for channel in range(1, 3)
                       ] + [
                           {"signal": "temperature", "channel": channel, "label": f"PT100 input {channel}", "unit": "°C", "enabled": False, "record": False, "live": False}
                           for channel in range(1, 3)
                       ]})
    if fan_enabled == "yes":
        stack = addon_number(fan_stack, "Smart Fan stack", 0, 1, True)
        if not fan_id.replace("_", "").replace("-", "").isalnum():
            raise SystemExit("Smart Fan card ID may contain only letters, numbers, _ or -")
        addons.append({"id": fan_id, "type": "sequent_smart_fan", "label": fan_label.strip() or fan_id,
                       "stack": stack, "interval_seconds": 2.0, "enabled": True, "channels": [
                           {"metric": metric, "enabled": False, "live": False, "record": False}
                           for metric in ("fan_power", "stop_interval", "processor_temperature", "target_power")
                       ]})
    if ups_enabled == "yes":
        if not ups_id.replace("_", "").replace("-", "").isalnum():
            raise SystemExit("Super Watchdog & UPS card ID may contain only letters, numbers, _ or -")
        addons.append({"id": ups_id, "type": "sequent_super_watchdog", "label": ups_label.strip() or ups_id,
                       "stack": 0, "interval_seconds": 1.0, "enabled": True, "channels": [
                           {"metric": metric, "enabled": False, "live": False, "record": False}
                           for metric in ("input_voltage", "raspberry_voltage", "battery_voltage", "board_temperature", "charge_status", "reset_count")
                       ]})
    if len({item["id"] for item in addons}) != len(addons):
        raise SystemExit("Digital and analog card IDs must be different")
    config["addons"] = addons

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

# A re-run of setup may keep an already configured Smart Fan or UPS card.
# Reconcile against the resulting config, not only this run's answers, so a
# missing vendor module is repaired before the collector is restarted.
ensure_configured_sequent_drivers

echo
echo "Configuration written successfully. Backup: $backup_path"
read -r -p "Restart TMM services now? [Y/n]: " restart
if [[ ${restart:-Y} =~ ^[Yy]$ ]]; then
  systemctl restart tmm.service tmm-web.service
  echo "TMM services restarted."
else
  echo "Restart later with: sudo systemctl restart tmm.service tmm-web.service"
fi
