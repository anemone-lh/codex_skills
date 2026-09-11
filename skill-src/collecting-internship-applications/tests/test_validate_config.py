import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "validate_config.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_config", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_module()

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.path = self.root / "config.local.json"

    def write(self, value):
        self.path.write_text(json.dumps(value), encoding="utf-8")

    def valid(self):
        return {
            "tracker_csv": str(self.root / "applications.csv"),
            "resume_template": str(self.root / "resume.docx"),
            "resume_output_root": str(self.root / "tailored"),
        }

    def test_valid_config_returns_paths(self):
        self.write(self.valid())
        result = self.config.load_config(self.path)
        self.assertEqual(set(result), set(self.valid()))
        self.assertTrue(all(isinstance(value, Path) for value in result.values()))

    def test_missing_file_is_actionable(self):
        with self.assertRaisesRegex(FileNotFoundError, "config.local.json"):
            self.config.load_config(self.path)

    def test_missing_unknown_and_non_string_fields_are_rejected(self):
        value = self.valid()
        del value["tracker_csv"]
        self.write(value)
        with self.assertRaisesRegex(ValueError, "missing"):
            self.config.load_config(self.path)

        value = self.valid() | {"secret": "unexpected"}
        self.write(value)
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.config.load_config(self.path)

        value = self.valid() | {"tracker_csv": 42}
        self.write(value)
        with self.assertRaisesRegex(ValueError, "string"):
            self.config.load_config(self.path)

    def test_relative_paths_are_rejected(self):
        self.write(self.valid() | {"resume_output_root": "relative/output"})
        with self.assertRaisesRegex(ValueError, "absolute"):
            self.config.load_config(self.path)

    def test_cli_does_not_echo_private_values(self):
        values = self.valid()
        self.write(values)
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--config", str(self.path)],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(completed.stdout), {"result": "valid"})
        for value in values.values():
            self.assertNotIn(value, completed.stdout)


if __name__ == "__main__":
    unittest.main()
