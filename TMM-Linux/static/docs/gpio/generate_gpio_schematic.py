#!/usr/bin/env python3
"""Generate TMM's offline Raspberry Pi GPIO connection schematic."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


OUTPUT = Path(__file__).with_name("raspberry-pi-gpio-input-schematic.pdf")
PAGE_W, PAGE_H = landscape(A4)

BG = colors.HexColor("#101817")
PANEL = colors.HexColor("#172321")
GRID = colors.HexColor("#38504b")
TEXT = colors.HexColor("#eef4f1")
MUTED = colors.HexColor("#a7b8b3")
GREEN = colors.HexColor("#70e2b4")
YELLOW = colors.HexColor("#ffd166")
RED = colors.HexColor("#ff806f")
BLUE = colors.HexColor("#74c7ec")
PURPLE = colors.HexColor("#cba6f7")


def system_font(filename):
    candidates = (
        Path("/usr/share/fonts/truetype/dejavu") / filename,
        Path("/usr/share/fonts/TTF") / filename,
        Path("/usr/local/share/fonts") / filename,
    )
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(f"Required DejaVu font not found: {filename}")


pdfmetrics.registerFont(TTFont("TMMRegular", system_font("DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("TMMBold", system_font("DejaVuSans-Bold.ttf")))

SAFE_BCM = {4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27}
PINS = {
    1: ("3.3 V", None), 2: ("5 V", None),
    3: ("GPIO 2 / SDA", 2), 4: ("5 V", None),
    5: ("GPIO 3 / SCL", 3), 6: ("GND", None),
    7: ("GPIO 4", 4), 8: ("GPIO 14 / TX", 14),
    9: ("GND", None), 10: ("GPIO 15 / RX", 15),
    11: ("GPIO 17", 17), 12: ("GPIO 18", 18),
    13: ("GPIO 27", 27), 14: ("GND", None),
    15: ("GPIO 22", 22), 16: ("GPIO 23", 23),
    17: ("3.3 V", None), 18: ("GPIO 24", 24),
    19: ("GPIO 10 / MOSI", 10), 20: ("GND", None),
    21: ("GPIO 9 / MISO", 9), 22: ("GPIO 25", 25),
    23: ("GPIO 11 / SCLK", 11), 24: ("GPIO 8 / CE0", 8),
    25: ("GND", None), 26: ("GPIO 7 / CE1", 7),
    27: ("GPIO 0 / ID_SD", 0), 28: ("GPIO 1 / ID_SC", 1),
    29: ("GPIO 5", 5), 30: ("GND", None),
    31: ("GPIO 6", 6), 32: ("GPIO 12", 12),
    33: ("GPIO 13", 13), 34: ("GND", None),
    35: ("GPIO 19", 19), 36: ("GPIO 16", 16),
    37: ("GPIO 26", 26), 38: ("GPIO 20", 20),
    39: ("GND", None), 40: ("GPIO 21", 21),
}


def text(c, x, y, value, size=8, color=TEXT, font="TMMRegular", align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "right":
        x -= stringWidth(value, font, size)
    elif align == "center":
        x -= stringWidth(value, font, size) / 2
    c.drawString(x, y, value)


def wrapped(c, x, y, value, width, size=8, color=MUTED, leading=None, font="TMMRegular"):
    leading = leading or size * 1.35
    words, lines, line = value.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and stringWidth(candidate, font, size) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    for item in lines:
        text(c, x, y, item, size, color, font)
        y -= leading
    return y


def panel(c, x, y, w, h, title, accent=GREEN):
    c.setFillColor(PANEL)
    c.setStrokeColor(GRID)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    text(c, x + 14, y + h - 22, title, 11, accent, "TMMBold")


def terminal(c, x, y, label, color=GREEN):
    c.setFillColor(BG)
    c.setStrokeColor(color)
    c.roundRect(x, y, 60, 24, 4, fill=1, stroke=1)
    text(c, x + 30, y + 8, label, 8, TEXT, "TMMBold", "center")


def wire(c, points, color=GREEN, width=2):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    path = c.beginPath()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    c.drawPath(path)


def draw_pinout(c):
    x, y, w, h = 24, 105, 390, 425
    panel(c, x, y, w, h, "40-PIN-HEADER: PHYSISCHER PIN UND BCM-NUMMER")
    text(c, x + 14, y + h - 40, "Ansicht auf die Stiftleiste des Raspberry Pi (USB/Ethernet unten)", 7.5, MUTED)
    top = y + h - 62
    row_h = 16.4
    for row in range(20):
        left_pin, right_pin = row * 2 + 1, row * 2 + 2
        yy = top - row * row_h
        for pin, pin_x, label_x, align in (
            (left_pin, x + 177, x + 159, "right"),
            (right_pin, x + 213, x + 231, "left"),
        ):
            label, bcm = PINS[pin]
            safe = bcm in SAFE_BCM
            is_power = label in {"3.3 V", "5 V"}
            color = GREEN if safe else (RED if is_power else MUTED)
            c.setFillColor(color)
            c.setStrokeColor(BG)
            c.circle(pin_x, yy, 5, fill=1, stroke=1)
            text(c, pin_x, yy - 2.4, str(pin), 5.2, BG, "TMMBold", "center")
            text(c, label_x, yy - 2.8, label, 7, color, "TMMBold" if safe else "TMMRegular", align)
    text(c, x + 14, y + 20, "GRÜN = in TMM-Setup angeboten", 8, GREEN, "TMMBold")
    text(c, x + 180, y + 20, "GRAU = reserviert / Schnittstelle", 8, MUTED)
    text(c, x + 14, y + 8, "ROT = Versorgung - niemals als Eingang verwenden", 7.5, RED)
    text(c, x + 390 - 14, y + 8, "BCM-Nummerierung verwenden", 7.5, YELLOW, "TMMBold", "right")


def draw_wiring(c):
    x, w = 430, 387
    panel(c, x, 382, w, 148, "A  POTENTIALFREIER KONTAKT", GREEN)
    text(c, x + 14, 486, "Empfohlene TMM-Konfiguration: Pull-up, active LOW", 8, MUTED)
    terminal(c, x + 18, 440, "GPIO / BCM")
    terminal(c, x + 290, 440, "GND", BLUE)
    wire(c, [(x + 78, 452), (x + 157, 452)], GREEN)
    wire(c, [(x + 230, 452), (x + 290, 452)], BLUE)
    c.setStrokeColor(TEXT); c.setLineWidth(2)
    c.line(x + 157, 452, x + 193, 468)
    c.line(x + 201, 452, x + 230, 452)
    text(c, x + 194, 428, "Schließer", 8, TEXT, "TMMBold", "center")
    wrapped(c, x + 14, 410, "Kontakt offen = 0, Kontakt geschlossen = 1. Keine externe Spannung einspeisen.", w - 28, 7.5)

    panel(c, x, 225, w, 143, "B  3,3-V-LOGIKSIGNAL", BLUE)
    text(c, x + 14, 329, "Empfohlene TMM-Konfiguration: Pull-down, active HIGH", 8, MUTED)
    terminal(c, x + 18, 282, "GPIO / BCM")
    terminal(c, x + 290, 270, "GND", BLUE)
    c.setFillColor(BG); c.setStrokeColor(YELLOW); c.roundRect(x + 139, 270, 91, 48, 5, fill=1, stroke=1)
    text(c, x + 184, 299, "3,3-V-QUELLE", 7.5, YELLOW, "TMMBold", "center")
    text(c, x + 184, 282, "OUT       GND", 7, TEXT, align="center")
    wire(c, [(x + 78, 294), (x + 139, 294)], GREEN)
    wire(c, [(x + 230, 282), (x + 290, 282)], BLUE)
    wrapped(c, x + 14, 253, "Gemeinsame Masse erforderlich. Signalpegel muss sicher auf 0...3,3 V begrenzt sein.", w - 28, 7.5)

    panel(c, x, 105, w, 106, "C  MASCHINENSIGNAL 5 V / 24 V", RED)
    c.setFillColor(colors.HexColor("#3a211e")); c.setStrokeColor(RED)
    c.roundRect(x + 14, 123, w - 28, 56, 5, fill=1, stroke=1)
    text(c, x + 28, 156, "NICHT DIREKT AN GPIO ANSCHLIESSEN", 11, RED, "TMMBold")
    wrapped(c, x + 28, 138, "Nur über geeignetes galvanisch getrenntes Eingangsmodul / Optokoppler mit 3,3-V-Ausgang.", w - 56, 7.5, color=TEXT)


def build():
    c = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("TMM - Raspberry Pi GPIO Eingangsschema")
    c.setAuthor("Toshiba Modbus Monitor")
    c.setSubject("Offline-Anschluss- und Sicherheitsschema für passive GPIO-Klemmen-HATs")
    c.setFillColor(BG); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    text(c, 24, PAGE_H - 28, "TMM · SERVICE-SCHEMA", 9, GREEN, "TMMBold")
    text(c, 24, PAGE_H - 55, "Raspberry Pi GPIO als digitaler Eingang", 21, TEXT, "TMMBold")
    text(c, PAGE_W - 24, PAGE_H - 46, "Nur 3,3-V-Logik · Eingangsbetrieb · BCM-Nummerierung", 9, YELLOW, "TMMBold", "right")
    c.setStrokeColor(GRID); c.line(24, PAGE_H - 68, PAGE_W - 24, PAGE_H - 68)
    draw_pinout(c)
    draw_wiring(c)
    c.setFillColor(colors.HexColor("#3a211e")); c.setStrokeColor(RED)
    c.roundRect(24, 28, PAGE_W - 48, 58, 7, fill=1, stroke=1)
    text(c, 38, 64, "ELEKTRISCHE SICHERHEIT", 10, RED, "TMMBold")
    wrapped(c, 38, 48, "Der GPIO-Header ist keine industrielle I/O. Ein passiver Schraubklemmen-HAT bietet weder galvanische Trennung noch Überspannungsschutz. Vor dem Anschließen spannungsfrei schalten und Signalpegel prüfen.", PAGE_W - 76, 8, TEXT, 11)
    text(c, 24, 12, "TMM Version 1.3 · Release-Baseline r133 · Offline-Unterlage für Service und Installation", 7, MUTED)
    text(c, PAGE_W - 24, 12, "Anschlussprüfung durch qualifiziertes Fachpersonal", 7, MUTED, align="right")
    c.showPage()
    c.save()


if __name__ == "__main__":
    build()
    print(OUTPUT)
