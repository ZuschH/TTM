# Raspberry Pi GPIO offline documentation

`raspberry-pi-gpio-input-schematic.pdf` is the locally installed service and
wiring reference linked by the TMM web interface. It uses physical header pin
numbers and BCM GPIO identities side by side and documents TMM's input-only
connection patterns.

Regenerate it with the bundled Python runtime and ReportLab:

```sh
python3 static/docs/gpio/generate_gpio_schematic.py
```

The document is a TMM project aid, not a replacement for the Raspberry Pi
hardware documentation or an electrical safety assessment.
