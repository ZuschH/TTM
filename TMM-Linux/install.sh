#!/bin/sh
set -eu

if [ "$(id -u)" -ne 0 ]; then
    echo "Bitte mit sudo ausführen: sudo ./install.sh" >&2
    exit 1
fi

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if ! getent group dialout >/dev/null; then
    groupadd --system dialout
fi
if ! id tmm >/dev/null 2>&1; then
    useradd --system --home-dir /var/lib/tmm --shell /usr/sbin/nologin --groups dialout tmm
else
    usermod -aG dialout tmm
fi

apt-get update
apt-get install -y python3 python3-venv

install -d -o root -g root -m 0755 /opt/tmm
install -d -o root -g tmm -m 0750 /etc/tmm
install -d -o tmm -g tmm -m 0750 /var/lib/tmm
install -o root -g root -m 0755 "$PROJECT_DIR/tmm_monitor.py" /opt/tmm/tmm_monitor.py
install -o root -g root -m 0755 "$PROJECT_DIR/tmm_web.py" /opt/tmm/tmm_web.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_web_data.py" /opt/tmm/tmm_web_data.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_decode.py" /opt/tmm/tmm_decode.py
install -o root -g root -m 0644 "$PROJECT_DIR/tmm_profiles.py" /opt/tmm/tmm_profiles.py
install -o root -g root -m 0644 "$PROJECT_DIR/requirements.txt" /opt/tmm/requirements.txt
install -o root -g root -m 0644 "$PROJECT_DIR/VERSION" /opt/tmm/VERSION
install -o root -g root -m 0644 "$PROJECT_DIR/README.md" /opt/tmm/README.md
install -o root -g root -m 0755 "$PROJECT_DIR/setup.sh" /opt/tmm/setup.sh
install -d -o root -g root -m 0755 /opt/tmm/static
install -o root -g root -m 0644 "$PROJECT_DIR/static/index.html" /opt/tmm/static/index.html
install -o root -g root -m 0644 "$PROJECT_DIR/static/style.css" /opt/tmm/static/style.css
install -o root -g root -m 0644 "$PROJECT_DIR/static/app.js" /opt/tmm/static/app.js
install -o root -g root -m 0644 "$PROJECT_DIR/static/tmm-product-mark.png" /opt/tmm/static/tmm-product-mark.png

python3 -m venv /opt/tmm/.venv
/opt/tmm/.venv/bin/pip install --disable-pip-version-check -r /opt/tmm/requirements.txt

if [ ! -e /etc/tmm/config.json ]; then
    install -o root -g tmm -m 0640 "$PROJECT_DIR/config.example.json" /etc/tmm/config.json
else
    echo "Bestehende Konfiguration bleibt unverändert: /etc/tmm/config.json"
fi

install -o root -g root -m 0644 "$PROJECT_DIR/tmm.service" /etc/systemd/system/tmm.service
install -o root -g root -m 0644 "$PROJECT_DIR/tmm-web.service" /etc/systemd/system/tmm-web.service
systemctl daemon-reload
systemctl enable tmm.service tmm-web.service
systemctl restart tmm.service
systemctl restart tmm-web.service

echo "Toshiba Modbus Monitor V1.0 wurde installiert."
echo "Status: systemctl status tmm tmm-web"
echo "Log:    journalctl -u tmm -f"
echo "Web:    http://<HOST-IP-ADDRESS>:8080/"
