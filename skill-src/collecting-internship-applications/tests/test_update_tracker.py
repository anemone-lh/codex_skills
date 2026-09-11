import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "update_tracker.py"


def load_module():
    spec = importlib.util.spec_from_file_location("update_tracker", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TrackerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tracker = load_module()

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.path = Path(self.tempdir.name) / "Intership_Information.csv"

    def record(self, **updates):
        data = {
            "company_name": "示例科技",
            "job_title": "数据科学实习生",
            "location": "深圳",
            "salary": "",
            "application_url": "https://jobs.example.com/role?id=7&utm_source=feed",
            "referral_code": "",
            "job_requirements": "Python, SQL",
            "source_url": "https://example.com/post/7",
            "collected_at": "2026-09-11T10:00:00+08:00",
            "generate_resume": False,
            "resume_status": "not_requested",
            "resume_docx": "",
            "resume_pdf": "",
            "notes": "第一行,含逗号\n第二行",
        }
        data.update(updates)
        return data

    def read_rows(self):
        with self.path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_first_upsert_creates_bom_csv_and_preserves_chinese_newlines(self):
        result = self.tracker.upsert_record(self.path, self.record())
        self.assertEqual(result, "inserted")
        self.assertTrue(self.path.read_bytes().startswith(b"\xef\xbb\xbf"))
        rows = self.read_rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["company_name"], "示例科技")
        self.assertEqual(rows[0]["notes"], "第一行,含逗号\n第二行")
        self.assertEqual(rows[0]["generate_resume"], "false")

    def test_duplicate_normalized_url_enriches_without_erasing_values(self):
        self.tracker.upsert_record(self.path, self.record(salary="200/天"))
        result = self.tracker.upsert_record(
            self.path,
            self.record(
                salary="",
                application_url="https://JOBS.example.com/role?utm_medium=email&id=7#apply",
                referral_code="REF88",
            ),
        )
        self.assertEqual(result, "updated")
        rows = self.read_rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["salary"], "200/天")
        self.assertEqual(rows[0]["referral_code"], "REF88")

    def test_duplicate_without_toggle_preserves_enabled_resume_request(self):
        self.tracker.upsert_record(self.path, self.record(generate_resume=True))
        incoming = self.record(referral_code="REF99")
        del incoming["generate_resume"]
        self.tracker.upsert_record(self.path, incoming)
        self.assertEqual(self.read_rows()[0]["generate_resume"], "true")

    def test_boolean_and_url_normalization(self):
        self.assertEqual(self.tracker.normalize_bool("YES"), "true")
        self.assertEqual(self.tracker.normalize_bool(0), "false")
        self.assertEqual(
            self.tracker.normalize_url("HTTPS://Example.COM/a/?b=2&utm_campaign=x&a=1#top"),
            "https://example.com/a?a=1&b=2",
        )
        with self.assertRaises(ValueError):
            self.tracker.normalize_bool("later")

    def test_status_update_sets_paths_and_rejects_invalid_status(self):
        self.tracker.upsert_record(self.path, self.record())
        key = self.tracker.normalize_url(self.record()["application_url"])
        self.tracker.set_status(
            self.path,
            key,
            "completed",
            resume_docx="/tmp/custom.docx",
            resume_pdf="/tmp/custom.pdf",
        )
        row = self.read_rows()[0]
        self.assertEqual(row["resume_status"], "completed")
        self.assertEqual(row["resume_pdf"], "/tmp/custom.pdf")
        with self.assertRaises(ValueError):
            self.tracker.set_status(self.path, key, "running")

    def test_malformed_header_is_rejected(self):
        self.path.write_text("company,role\nA,B\n", encoding="utf-8-sig")
        with self.assertRaisesRegex(ValueError, "header"):
            self.tracker.upsert_record(self.path, self.record())

    def test_replace_failure_preserves_original_file(self):
        self.tracker.upsert_record(self.path, self.record())
        original = self.path.read_bytes()
        with mock.patch.object(Path, "replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                self.tracker.upsert_record(self.path, self.record(referral_code="NEW"))
        self.assertEqual(self.path.read_bytes(), original)

    def test_cli_prints_machine_readable_result(self):
        payload = json.dumps(self.record(), ensure_ascii=False)
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "upsert", "--csv", str(self.path), "--record-json", payload],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(completed.stdout)["result"], "inserted")


if __name__ == "__main__":
    unittest.main()
