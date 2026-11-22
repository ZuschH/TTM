#!/usr/bin/env bash
# Build an offline installation bundle on a Pi with internet access.
set -euo pipefail

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
  cat <<'EOF'
Usage: sudo ./prepare-offline-bundle.sh [destination]

Downloads all Debian and Python packages required for an offline TMM
installation. Build it on the same Raspberry Pi OS release and CPU architecture
as the intended target.
EOF
  exit 0
fi

if [[ ${EUID} -ne 0 ]]; then
  echo "Please run with sudo: sudo ./prepare-offline-bundle.sh [destination]" >&2
  exit 1
fi

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DESTINATION=${1:-"$PROJECT_DIR/tmm-offline-bundle"}
if [[ $# -gt 1 ]]; then
  echo "Usage: sudo ./prepare-offline-bundle.sh [destination]" >&2
  exit 2
fi
if [[ -e $DESTINATION && -n $(find "$DESTINATION" -mindepth 1 -maxdepth 1 -print -quit) ]]; then
  echo "Destination is not empty: $DESTINATION" >&2
  exit 1
fi

mkdir -p "$DESTINATION/debs/partial" "$DESTINATION/wheels" "$DESTINATION/docs/sequent"
echo "Downloading Debian packages and their dependencies …"
apt-get update
apt-get -y --download-only --reinstall \
  -o "Dir::Cache::archives=$DESTINATION/debs" \
  install python3 python3-venv python3-smbus i2c-tools dialog nano curl

echo "Downloading Python distributions for this Pi architecture …"
python3 -m pip download --disable-pip-version-check --dest "$DESTINATION/wheels" \
  -r "$PROJECT_DIR/requirements.txt" \
  SM16inpind SM24b8vin SMmultiio SMwdt 'smbus2>=0.4' 'gpiozero>=2.0.0' pip setuptools wheel
# The current SMsfan code uses gpiozero/smbus2, while its package metadata
# still pulls the obsolete RPi.GPIO C extension.  Store the fan wheel itself;
# its actual dependencies were downloaded explicitly above.
python3 -m pip download --disable-pip-version-check --no-deps --dest "$DESTINATION/wheels" SMsfan

echo "Downloading and verifying optional Sequent documentation …"
"$PROJECT_DIR/fetch-sequent-docs.sh" "$DESTINATION/docs/sequent"

cat >"$DESTINATION/manifest.txt" <<EOF
TMM offline bundle
version=$(cat "$PROJECT_DIR/VERSION")
architecture=$(dpkg --print-architecture)
python=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
created_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF
(cd "$DESTINATION" && find debs wheels docs -type f -print0 | sort -z | xargs -0 sha256sum >SHA256SUMS)

echo "Offline bundle created: $DESTINATION"
echo "Copy the complete project directory and this bundle to the target Pi."
echo "Install there with: sudo ./install.sh --offline-bundle $DESTINATION"
