#!/usr/bin/env python3
"""Fail-safe shutdown guard for Sequent Super Watchdog UPS.

This intentionally runs as a small root-owned system service, separate from
the TMM web/collector accounts.  It is inert unless explicitly enabled in the
``ups_shutdown`` configuration block.
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import time
from pathlib import Path


LOG = logging.getLogger("tmm-ups-guard")


def load_policy(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        settings = json.load(handle)
    policy = dict(settings.get("ups_shutdown", {}))
    override_path = Path(settings["storage"]["database"]).parent / "ups-shutdown-policy.json"
    try:
        override = json.loads(override_path.read_text(encoding="utf-8"))
        if isinstance(override, dict):
            policy.update(override)
    except (OSError, json.JSONDecodeError):
        pass
    enabled = bool(policy.get("enabled", False))
    threshold = float(policy.get("input_voltage_threshold_v", 4.5))
    delay = float(policy.get("input_loss_delay_seconds", 30))
    handoff = int(policy.get("watchdog_handoff_seconds", 15))
    dry_run = bool(policy.get("dry_run", True))
    if threshold <= 0 or delay < 1 or not 11 <= handoff <= 65000:
        raise ValueError("invalid ups_shutdown policy")
    return {"enabled": enabled, "threshold": threshold, "delay": delay, "handoff": handoff, "dry_run": dry_run}


def run(path: Path) -> None:
    last_policy: dict | None = None
    policy: dict = {"enabled": False}
    outage_started: float | None = None
    outage_confirmed = False
    while True:
        try:
            updated = load_policy(path)
            if updated != last_policy:
                policy = updated; last_policy = dict(updated)
                outage_started = None; outage_confirmed = False
                LOG.info("UPS shutdown guard %s%s", "armed" if policy["enabled"] else "disabled", " (test mode)" if policy.get("dry_run") else "")
            if not policy["enabled"]:
                time.sleep(1); continue
            import wdt  # optional vendor driver, required only when armed
            vin = float(wdt.getVin())
            if vin >= policy["threshold"]:
                if outage_confirmed:
                    LOG.info("UPS input restored; shutdown guard re-armed")
                outage_started = None; outage_confirmed = False
            elif outage_confirmed:
                pass
            elif outage_started is None:
                outage_started = time.monotonic()
                LOG.warning("UPS input %.3f V below %.3f V; confirmation started", vin, policy["threshold"])
            elif time.monotonic() - outage_started >= policy["delay"]:
                LOG.critical("confirmed input power loss; initiating %sshutdown", "test " if policy["dry_run"] else "")
                if policy["dry_run"]:
                    outage_confirmed = True
                else:
                    # The board independently cuts power when the now-unfed
                    # watchdog expires.  This prevents a battery-powered boot
                    # loop after systemctl has completed the clean shutdown.
                    wdt.setRepowerOnBattery(0)
                    wdt.setPeriod(policy["handoff"])
                    wdt.reload()
                    subprocess.run(["sync"], check=False)
                    subprocess.run(["systemctl", "poweroff"], check=False)
                    return
        except Exception as error:
            LOG.warning("UPS guard read/policy error: %s", error)
        time.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    run(args.config)


if __name__ == "__main__":
    main()
