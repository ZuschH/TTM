#!/usr/bin/env bash
# Safe uninstaller for Toshiba Modbus Monitor (TMM).
set -euo pipefail

purge=no
assume_yes=no
for argument in "$@"; do
  case "$argument" in
    --purge) purge=yes ;;
    --yes) assume_yes=yes ;;
    --help|-h)
      cat <<'EOF'
Usage: sudo ./uninstall.sh [--purge] [--yes]

Without options, TMM services and program files are removed while /etc/tmm
and /var/lib/tmm (configuration, measurements, exports and archives) remain.

--purge  Also remove /etc/tmm and /var/lib/tmm after an explicit confirmation.
--yes    Accept the confirmation; only valid together with --purge.
EOF
      exit 0
      ;;
    *) echo "Unknown option: $argument (use --help)" >&2; exit 2 ;;
  esac
done

if [[ ${EUID} -ne 0 ]]; then
  echo "Please run with sudo: sudo ./uninstall.sh" >&2
  exit 1
fi

if [[ $assume_yes == yes && $purge != yes ]]; then
  echo "--yes is only valid together with --purge." >&2
  exit 2
fi

if [[ $purge == yes && $assume_yes != yes ]]; then
  echo "WARNING: this also permanently removes /etc/tmm and /var/lib/tmm."
  echo "That includes config.json, the SQLite database, CSV exports, backups and archives."
  read -r -p "Type PURGE TMM to continue: " confirmation
  [[ $confirmation == "PURGE TMM" ]] || { echo "Nothing was removed."; exit 0; }
fi

echo "Stopping and disabling TMM services …"
for service in tmm.service tmm-web.service tmm-ups-guard.service; do
  systemctl disable --now "$service" 2>/dev/null || true
  rm -f "/etc/systemd/system/$service"
done
systemctl daemon-reload
systemctl reset-failed tmm.service tmm-web.service tmm-ups-guard.service 2>/dev/null || true

# Exact, fixed paths only: never derive a deletion target from configuration.
rm -rf -- /opt/tmm
rm -f -- /etc/modules-load.d/tmm-i2c.conf

if [[ $purge == yes ]]; then
  rm -rf -- /etc/tmm /var/lib/tmm
  echo "TMM program, services, configuration and local data were removed."
else
  echo "TMM program and services were removed."
  echo "Configuration and data were retained: /etc/tmm and /var/lib/tmm"
  echo "For complete removal, run: sudo ./uninstall.sh --purge"
fi

echo "Shared system packages (Python, i2c-tools, dialog) and the tmm system user were retained deliberately."
