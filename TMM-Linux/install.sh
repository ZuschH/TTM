#!/bin/sh
set -eu

OFFLINE_BUNDLE=${TMM_OFFLINE_BUNDLE:-}
while [ "$#" -gt 0 ]; do
    case "$1" in
        --offline-bundle)
            [ "$#" -ge 2 ] || { echo "--offline-bundle requires a directory" >&2; exit 2; }
            OFFLINE_BUNDLE=$2
            shift 2
            ;;
        --help|-h)
            cat <<'EOF'
Usage: sudo ./install.sh [--offline-bundle DIRECTORY]

Without an offline bundle, packages are downloaded from the configured APT and
Python package repositories.  With --offline-bundle, only the supplied local
Debian packages and Python distributions are used.
EOF
            exit 0
            ;;
        *) echo "Unknown option: $1 (use --help)" >&2; exit 2 ;;
    esac
done

if [ "$(id -u)" -ne 0 ]; then
    echo "Bitte mit sudo ausführen: sudo ./install.sh" >&2
    exit 1
fi

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

# Refuse an incomplete release before touching an existing installation. This
# prevents a new entry point from importing a companion module that was absent
# from a partial archive or selective file update.
REQUIRED_RELEASE_FILES="
tmm_monitor.py
tmm_proxy.py
tmm_addons.py
tmm_conditions.py
tmm_ups_guard.py
tmm_web.py
tmm_web_data.py
tmm_decode.py
tmm_profiles.py
tmm_setup.py
requirements.txt
VERSION
README.md
CHANGELOG.md
RELEASE_POLICY.md
ROADMAP.md
LICENSE
THIRD_PARTY_NOTICES.md
fetch-sequent-docs.sh
setup.sh
uninstall.sh
tmm.service
tmm-web.service
tmm-ups-guard.service
config.example.json
static/index.html
static/style.css
static/app.js
static/tmm-product-mark.png
static/docs/sequent/README.md
static/docs/sequent/availability.js
static/docs/gpio/raspberry-pi-gpio-input-schematic.pdf
"
for required_file in $REQUIRED_RELEASE_FILES; do
    if [ ! -f "$PROJECT_DIR/$required_file" ]; then
        echo "Incomplete TMM release: missing $required_file" >&2
        echo "No installed application files have been changed." >&2
        exit 1
    fi
done

python3 -m py_compile \
    "$PROJECT_DIR/tmm_monitor.py" "$PROJECT_DIR/tmm_addons.py" \
    "$PROJECT_DIR/tmm_conditions.py" "$PROJECT_DIR/tmm_ups_guard.py" \
    "$PROJECT_DIR/tmm_web.py" "$PROJECT_DIR/tmm_web_data.py" \
    "$PROJECT_DIR/tmm_decode.py" "$PROJECT_DIR/tmm_profiles.py" \
    "$PROJECT_DIR/tmm_setup.py"
python3 -m py_compile "$PROJECT_DIR/tmm_proxy.py"

if ! getent group dialout >/dev/null; then
    groupadd --system dialout
fi
if ! getent group i2c >/dev/null; then
    groupadd --system i2c
fi
if ! getent group gpio >/dev/null; then
    groupadd --system gpio
fi
if ! id tmm >/dev/null 2>&1; then
    useradd --system --home-dir /var/lib/tmm --shell /usr/sbin/nologin --groups dialout,i2c,gpio tmm
else
    usermod -aG dialout,i2c,gpio tmm
fi

if [ -n "$OFFLINE_BUNDLE" ]; then
    [ -d "$OFFLINE_BUNDLE/debs" ] && [ -d "$OFFLINE_BUNDLE/wheels" ] || {
        echo "Invalid offline bundle: expected debs/ and wheels/ below $OFFLINE_BUNDLE" >&2; exit 1;
    }
    [ -f "$OFFLINE_BUNDLE/manifest.txt" ] || { echo "Invalid offline bundle: manifest.txt is missing" >&2; exit 1; }
    [ -f "$OFFLINE_BUNDLE/SHA256SUMS" ] || { echo "Invalid offline bundle: SHA256SUMS is missing" >&2; exit 1; }
    BUNDLE_ARCH=$(sed -n 's/^architecture=//p' "$OFFLINE_BUNDLE/manifest.txt" | head -n 1)
    HOST_ARCH=$(dpkg --print-architecture)
    [ -n "$BUNDLE_ARCH" ] && [ "$BUNDLE_ARCH" = "$HOST_ARCH" ] || {
        echo "Offline bundle architecture ($BUNDLE_ARCH) does not match this Pi ($HOST_ARCH)." >&2; exit 1;
    }
    echo "Verifying offline bundle checksums …"
    (cd "$OFFLINE_BUNDLE" && sha256sum -c SHA256SUMS)
    set -- "$OFFLINE_BUNDLE"/debs/*.deb
    [ -f "$1" ] || { echo "Offline bundle contains no Debian packages." >&2; exit 1; }
    echo "Installing required Debian packages from the offline bundle …"
    apt-get --no-download install -y "$@"
else
    apt-get update
    apt-get install -y python3 python3-venv curl
fi

install -d -o root -g root -m 0755 /opt/tmm
install -d -o root -g tmm -m 0770 /etc/tmm
install -d -o tmm -g tmm -m 0750 /var/lib/tmm
install -o root -g root -m 0755 "$PROJECT_DIR/tmm_monitor.py" /opt/tmm/tmm_monitor.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_proxy.py" /opt/tmm/tmm_proxy.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_addons.py" /opt/tmm/tmm_addons.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_conditions.py" /opt/tmm/tmm_conditions.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_ups_guard.py" /opt/tmm/tmm_ups_guard.py
install -o root -g root -m 0755 "$PROJECT_DIR/tmm_web.py" /opt/tmm/tmm_web.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_web_data.py" /opt/tmm/tmm_web_data.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_decode.py" /opt/tmm/tmm_decode.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_profiles.py" /opt/tmm/tmm_profiles.py
install -o root -g root -m 0644 "$PROJECT_DIR/requirements.txt" /opt/tmm/requirements.txt
install -o root -g root -m 0644 "$PROJECT_DIR/VERSION" /opt/tmm/VERSION
install -o root -g root -m 0644 "$PROJECT_DIR/README.md" /opt/tmm/README.md
install -o root -g root -m 0644 "$PROJECT_DIR/CHANGELOG.md" /opt/tmm/CHANGELOG.md
install -o root -g root -m 0644 "$PROJECT_DIR/RELEASE_POLICY.md" /opt/tmm/RELEASE_POLICY.md
install -o root -g root -m 0644 "$PROJECT_DIR/ROADMAP.md" /opt/tmm/ROADMAP.md
install -o root -g root -m 0644 "$PROJECT_DIR/LICENSE" /opt/tmm/LICENSE
install -o root -g root -m 0644 "$PROJECT_DIR/THIRD_PARTY_NOTICES.md" /opt/tmm/THIRD_PARTY_NOTICES.md
install -o root -g root -m 0755 "$PROJECT_DIR/fetch-sequent-docs.sh" /opt/tmm/fetch-sequent-docs.sh
install -o root -g root -m 0755 "$PROJECT_DIR/setup.sh" /opt/tmm/setup.sh
install -o root -g root -m 0755 "$PROJECT_DIR/tmm_setup.py" /opt/tmm/tmm_setup.py
install -o root -g root -m 0755 "$PROJECT_DIR/uninstall.sh" /opt/tmm/uninstall.sh
install -d -o root -g root -m 0755 /opt/tmm/static
install -o root -g root -m 0644 "$PROJECT_DIR/static/index.html" /opt/tmm/static/index.html
install -o root -g root -m 0644 "$PROJECT_DIR/static/style.css" /opt/tmm/static/style.css
install -o root -g root -m 0644 "$PROJECT_DIR/static/app.js" /opt/tmm/static/app.js
install -o root -g root -m 0644 "$PROJECT_DIR/static/tmm-product-mark.png" /opt/tmm/static/tmm-product-mark.png
install -d -o root -g root -m 0755 /opt/tmm/static/docs/sequent
install -o root -g root -m 0644 "$PROJECT_DIR/static/docs/sequent/README.md" /opt/tmm/static/docs/sequent/README.md
install -o root -g root -m 0644 "$PROJECT_DIR/static/docs/sequent/availability.js" /opt/tmm/static/docs/sequent/availability.js
if [ -n "$OFFLINE_BUNDLE" ] && [ -d "$OFFLINE_BUNDLE/docs/sequent" ]; then
    for document in "$OFFLINE_BUNDLE"/docs/sequent/*.pdf; do
        [ -f "$document" ] || continue
        install -o root -g root -m 0644 "$document" /opt/tmm/static/docs/sequent/
    done
    printf 'window.TMM_SEQUENT_DOCS_LOCAL = true;\n' >/opt/tmm/static/docs/sequent/availability.js
elif ! "$PROJECT_DIR/fetch-sequent-docs.sh" /opt/tmm/static/docs/sequent; then
    echo "Warning: Sequent documents could not be downloaded; official publisher links remain active." >&2
fi
install -d -o root -g root -m 0755 /opt/tmm/static/docs/gpio
install -o root -g root -m 0644 "$PROJECT_DIR/static/docs/gpio/raspberry-pi-gpio-input-schematic.pdf" /opt/tmm/static/docs/gpio/
install -o root -g root -m 0644 "$PROJECT_DIR/static/docs/gpio/README.md" /opt/tmm/static/docs/gpio/README.md

python3 -m venv /opt/tmm/.venv
if [ -n "$OFFLINE_BUNDLE" ]; then
    echo "Installing Python packages from the offline bundle …"
    /opt/tmm/.venv/bin/pip install --disable-pip-version-check --no-index --find-links "$OFFLINE_BUNDLE/wheels" \
        -r /opt/tmm/requirements.txt SM16inpind SM24b8vin SMmultiio SMwdt 'smbus2>=0.4' 'gpiozero>=2.0.0'
    # SMsfan's current implementation uses gpiozero and smbus2, but its wheel
    # still declares the obsolete RPi.GPIO package.  Avoid compiling that
    # unused C extension on modern Python (notably aarch64 Python 3.13).
    /opt/tmm/.venv/bin/pip install --disable-pip-version-check --no-index --find-links "$OFFLINE_BUNDLE/wheels" \
        --no-deps SMsfan
else
    /opt/tmm/.venv/bin/pip install --disable-pip-version-check -r /opt/tmm/requirements.txt
fi

# Detect a missing companion module or broken import before restarting a
# currently working service. PYTHONPATH is explicit because this check is not
# launched through one of the scripts located in /opt/tmm.
PYTHONPATH=/opt/tmm /opt/tmm/.venv/bin/python -c \
    'import tmm_addons, tmm_conditions, tmm_decode, tmm_profiles, tmm_web_data, tmm_monitor, tmm_proxy, tmm_web'

if [ ! -e /etc/tmm/config.json ]; then
    install -o tmm -g tmm -m 0660 "$PROJECT_DIR/config.example.json" /etc/tmm/config.json
else
    echo "Bestehende Konfiguration bleibt unverändert: /etc/tmm/config.json"
    # The web UI performs narrowly scoped, local configuration updates using
    # an atomic replacement.  Keep existing installations compatible.
    chown tmm:tmm /etc/tmm/config.json
    chmod 0660 /etc/tmm/config.json
fi

install -o root -g root -m 0644 "$PROJECT_DIR/tmm.service" /etc/systemd/system/tmm.service
install -o root -g root -m 0644 "$PROJECT_DIR/tmm-web.service" /etc/systemd/system/tmm-web.service
install -o root -g root -m 0644 "$PROJECT_DIR/tmm-ups-guard.service" /etc/systemd/system/tmm-ups-guard.service
systemctl daemon-reload
systemctl enable tmm.service tmm-web.service tmm-ups-guard.service
systemctl restart tmm.service
systemctl restart tmm-web.service
systemctl restart tmm-ups-guard.service

echo "Toshiba Modbus Monitor $(cat /opt/tmm/VERSION) wurde installiert."
echo "Status: systemctl status tmm tmm-web"
echo "Log:    journalctl -u tmm -f"
echo "Web:    http://<HOST-IP-ADDRESS>:8080/"
