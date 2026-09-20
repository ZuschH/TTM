"""Human-readable Toshiba status, alarm, and trip decoding."""

from __future__ import annotations

from typing import Any


STATUS_BITS = {
    0: "Störungsausgang FL aktiv",
    1: "Umrichter ausgelöst (Trip)",
    2: "Alarm aktiv",
    4: "Motorparametersatz 2 aktiv",
    5: "PID-Regelung gesperrt",
    6: "Beschleunigungs-/Verzögerungsmuster 2 aktiv",
    7: "Erzwungene Gleichstrombremsung",
    8: "Tippbetrieb aktiv",
    9: "Rückwärtslauf",
    10: "Motor läuft",
    11: "Freier Auslauf (ST aus)",
    12: "Not-Halt-Zustand",
    13: "Betriebsbereit (ST und RUN ein)",
    14: "Umrichter betriebsbereit",
}

ALARM_1_BITS = {
    0: "Überstrom-Voralarm",
    1: "Umrichter-Überlast-Voralarm",
    2: "Motor-Überlast-Voralarm",
    3: "Übertemperatur-Voralarm",
    4: "Überspannungs-/Bremswiderstands-Voralarm",
    5: "Unterspannung im Hauptkreis erkannt",
    7: "Unterstromalarm",
    8: "Überdrehmoment erkannt",
    9: "Bremswiderstand-Überlast-Voralarm",
    10: "Betriebsstundenalarm",
    11: "Fehler am Kommunikationsmodul",
    12: "RS-485-Kommunikationsalarm",
    13: "Unterspannungsalarm im Hauptkreis",
    14: "Zwangsverzögerung nach Netzausfall",
    15: "Voralarm-Stopp an unterer Frequenzgrenze",
}

ALARM_2_BITS = {
    2: "Lebensdaueralarm",
    3: "Überdrehmoment-Alarm",
    4: "Überlast-Stallalarm",
    5: "Steuerkreis-/Optionsalarm",
    7: "Unterbrechung am VI/II-Eingang",
}

INPUT_TERMINAL_BITS_AS1 = {
    0: "F", 1: "R", 2: "ST", 3: "RES", 4: "S1", 5: "S2", 6: "S3", 7: "S4",
    8: "L1", 9: "L2", 10: "L3", 11: "L4", 12: "L5", 13: "L6", 14: "L7", 15: "L8",
}

INPUT_TERMINAL_BITS_SMALL = {
    0: "F", 1: "R", 2: "RES", 3: "S1", 4: "S2", 5: "S3", 6: "VIB", 7: "VIA",
}

INPUT_TERMINAL_BITS_AS3 = {
    0: "F", 1: "R", 2: "RES", 3: "S1", 4: "S2", 5: "S3", 6: "S4", 7: "S5",
    8: "DI11", 9: "DI12", 10: "DI13", 11: "DI14", 12: "DI15", 13: "DI16",
}

TRIP_CODES = {
    0x00: ("nerr", "Kein Fehler"),
    0x01: ("oc1", "Überstrom während Beschleunigung"),
    0x02: ("oc2", "Überstrom während Verzögerung"),
    0x03: ("oc3", "Überstrom bei konstanter Drehzahl"),
    0x04: ("ocl", "Überstrom der Last beim Start"),
    0x05: ("ocai", "Überstrom im U-Phasen-Leistungszweig"),
    0x06: ("oca2", "Überstrom im V-Phasen-Leistungszweig"),
    0x07: ("oca3", "Überstrom im W-Phasen-Leistungszweig"),
    0x08: ("ephi", "Eingangsphasenausfall"),
    0x09: ("epho", "Ausgangsphasenausfall"),
    0x0A: ("op1", "Überspannung während Beschleunigung"),
    0x0B: ("op2", "Überspannung während Verzögerung"),
    0x0C: ("op3", "Überspannung bei konstanter Drehzahl"),
    0x0D: ("ol1", "Umrichter überlastet"),
    0x0E: ("ol2", "Motor überlastet"),
    0x0F: ("olr", "Bremswiderstand überlastet"),
    0x10: ("oh", "Übertemperatur"),
    0x11: ("e", "Not-Halt"),
    0x12: ("eep1", "EEPROM-Fehler"),
    0x13: ("eep2", "Initialer Lesefehler"),
    0x14: ("eep3", "Initialer Lesefehler"),
    0x15: ("err2", "RAM-Fehler des Umrichters"),
    0x16: ("err3", "ROM-Fehler des Umrichters"),
    0x17: ("err4", "CPU-Fehler"),
    0x18: ("err5", "Kommunikations-Timeout"),
    0x19: ("err6", "Gate-Array-Fehler"),
    0x1A: ("err7", "Fehler der Ausgangsstromerfassung"),
    0x1B: ("err8", "Optionsfehler"),
    0x1D: ("uc", "Unterstrom-Betriebszustand"),
    0x1E: ("up1", "Unterspannung im Hauptkreis"),
    0x20: ("ot", "Überdrehmoment"),
    0x21: ("ef1", "Erdschluss"),
    0x22: ("ef2", "Erdschluss"),
    0x24: ("ocr", "Fehler im dynamischen Bremszweig"),
    0x25: ("oc1p", "Überstrom bei Beschleunigung (Leistungsteil überhitzt)"),
    0x26: ("oc2p", "Überstrom bei Verzögerung (Leistungsteil überhitzt)"),
    0x27: ("oc3p", "Überstrom bei Festdrehzahl (Leistungsteil überhitzt)"),
    0x28: ("etn", "Abstimmfehler"),
    0x29: ("etyp", "Falscher Umrichtertyp"),
    0x2A: ("e-10", "Überspannung am Analogeingang"),
    0x2B: ("e-11", "Fehlerhafte Bremssequenz"),
    0x2C: ("e-12", "Encoder-Unterbrechung"),
    0x2D: ("e-13", "Drehzahlfehler"),
    0x2E: ("oh2", "Externer Thermoschutz ausgelöst"),
    0x2F: ("sout", "Synchronisationsverlust des PM-Motors"),
    0x32: ("e-18", "Klemmeneingangsfehler"),
    0x33: ("e-19", "CPU2-Kommunikationsfehler"),
    0x34: ("e-20", "V/f-Regelungsfehler"),
    0x35: ("e-21", "CPU1-Fehler"),
    0x36: ("e-22", "Fehlerhafte Logikeingangsspannung"),
    0x37: ("e-23", "Option-1-Fehler"),
    0x38: ("e-24", "Option-2-Fehler"),
    0x39: ("e-25", "Fehler der Positionshaltung"),
    0x3A: ("e-26", "CPU2-Fehler"),
    0x54: ("etn1", "Abstimmfehler F410"),
    0x55: ("etn2", "Abstimmfehler F412"),
    0x56: ("etn3", "Fehler der Motorkonstanten"),
}


def _active_bits(raw_value: int, definitions: dict[int, str]) -> list[dict[str, Any]]:
    return [
        {"bit": bit, "label": label}
        for bit, label in definitions.items()
        if raw_value & (1 << bit)
    ]


def decode_metric(metric: str, raw_value: int, model: str = "VF-AS1") -> dict[str, Any] | None:
    if metric == "communication_status":
        if raw_value == 2:
            return {"summary": "Kommunikation online", "severity": "normal", "active": []}
        if raw_value == 1:
            return {"summary": "Kommunikation eingeschränkt", "severity": "warning", "active": []}
        return {
            "summary": "Kommunikation nicht verfügbar",
            "severity": "critical",
            "active": [{"code": "unreachable", "label": "Keine gültige Modbus-Kommunikation"}],
        }
    if metric == "input_terminal_status":
        if model == "VF-AS1":
            definitions = INPUT_TERMINAL_BITS_AS1
        elif model == "VF-AS3J":
            definitions = INPUT_TERMINAL_BITS_AS3
        else:
            definitions = INPUT_TERMINAL_BITS_SMALL
        active = _active_bits(raw_value, definitions)
        return {
            "summary": f"{len(active)} Eingänge aktiv" if active else "Alle Eingänge aus",
            "severity": "normal",
            "active": active,
            "states": [
                {"bit": bit, "label": label, "active": bool(raw_value & (1 << bit))}
                for bit, label in definitions.items()
            ],
        }
    if metric in ("operating_status", "trip_operating_status"):
        active = _active_bits(raw_value, STATUS_BITS)
        if raw_value & (1 << 1):
            summary, severity = "Trip", "critical"
        elif raw_value & (1 << 12):
            summary, severity = "Not-Halt", "critical"
        elif raw_value & (1 << 2):
            summary, severity = "Alarm", "warning"
        elif raw_value & (1 << 10):
            direction = "rückwärts" if raw_value & (1 << 9) else "vorwärts"
            summary, severity = f"Läuft {direction}", "normal"
        elif raw_value & (1 << 14):
            summary, severity = "Bereit / gestoppt", "normal"
        else:
            summary, severity = "Gestoppt / nicht bereit", "neutral"
        return {"summary": summary, "severity": severity, "active": active}

    if metric in ("alarm_information_1", "alarm_information_2"):
        definitions = ALARM_1_BITS if metric.endswith("_1") else ALARM_2_BITS
        active = _active_bits(raw_value, definitions)
        if not active:
            summary = "Keine aktiven Alarme"
        elif len(active) == 1:
            summary = "1 aktiver Alarm"
        else:
            summary = f"{len(active)} aktive Alarme"
        return {
            "summary": summary,
            "severity": "normal" if not active else "warning",
            "active": active,
        }

    if metric == "trip_code" or metric.startswith("past_trip_"):
        code, label = TRIP_CODES.get(raw_value, (f"0x{raw_value:04X}", "Unbekannter Trip-Code"))
        return {
            "summary": label,
            "severity": "normal" if raw_value == 0 else "critical",
            "code": code,
            "active": [] if raw_value == 0 else [{"code": code, "label": label}],
        }
    return None


def enrich_sample(sample: dict[str, Any], model: str = "VF-AS1") -> dict[str, Any]:
    enriched = dict(sample)
    decoded = decode_metric(str(sample["metric"]), int(sample["raw_value"]), model)
    if decoded is not None:
        enriched["decoded"] = decoded
    return enriched
