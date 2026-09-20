import json
import tempfile
import unittest
from pathlib import Path

from tmm_installer_config import main


class InstallerConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.template = self.root / "template.json"
        self.config = self.root / "config.json"
        self.template.write_text(json.dumps({
            "serial": {"device": "COM3", "baudrate": 19200},
            "inverters": [],
            "storage": {"database": "old.sqlite3"},
            "web": {"port": 8080},
        }), encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def arguments(self):
        return [
            "--config", str(self.config), "--template", str(self.template),
            "--device", "com7", "--baudrate", "38400", "--model", "VF-S15",
            "--name", "Drive 1", "--slave-id", "3",
            "--database", r"D:\TMM\measurements.sqlite3", "--web-port", "8090",
            "--machine-speed-factor", "0.1", "--machine-speed-unit", "spm",
            "--rated-output-current-a", "8.2", "--rated-output-voltage-v", "400",
            "--motor-rated-power-kw", "3.7", "--motor-rated-speed-rpm", "1450",
        ]

    def test_creates_valid_initial_configuration(self):
        self.assertEqual(main(self.arguments()), 0)
        data = json.loads(self.config.read_text(encoding="utf-8"))
        self.assertEqual(data["serial"], {"device": "COM7", "baudrate": 38400})
        self.assertEqual(data["inverters"][0]["model"], "VF-S15")
        self.assertEqual(data["inverters"][0]["slave_id"], 3)
        self.assertEqual(data["inverters"][0]["engineering"]["machine_speed_factor"], 0.1)
        self.assertEqual(data["inverters"][0]["engineering"]["motor_rated_speed_rpm"], 1450.0)
        self.assertEqual(data["web"]["port"], 8090)

    def test_existing_configuration_is_never_replaced(self):
        self.config.write_text('{"preserved": true}', encoding="utf-8")
        self.assertEqual(main(self.arguments()), 0)
        self.assertEqual(json.loads(self.config.read_text()), {"preserved": True})

    def test_invalid_modbus_address_is_rejected(self):
        arguments = self.arguments()
        arguments[arguments.index("--slave-id") + 1] = "248"
        with self.assertRaisesRegex(ValueError, "between 1 and 247"):
            main(arguments)
