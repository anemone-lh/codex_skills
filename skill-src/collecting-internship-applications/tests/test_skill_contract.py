import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
SCHEMA = (ROOT / "references" / "tracker-schema.md").read_text(encoding="utf-8")
TAILORING = (ROOT / "references" / "resume-tailoring.md").read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    def test_frontmatter_and_portable_configuration(self):
        self.assertRegex(SKILL, r"(?s)^---\nname: collecting-internship-applications\ndescription: Use when ")
        self.assertIn("config.local.json", SKILL)
        self.assertIn("scripts/validate_config.py", SKILL)
        self.assertIn("tracker_csv", SKILL)
        self.assertIn("resume_template", SKILL)
        self.assertIn("resume_output_root", SKILL)
        self.assertNotRegex(SKILL, r"/(?:Users|home)/[^/]+/")

    def test_schema_contains_exact_columns_and_states(self):
        columns = [
            "company_name", "job_title", "location", "salary", "application_url",
            "referral_code", "job_requirements", "source_url", "collected_at",
            "generate_resume", "resume_status", "resume_docx", "resume_pdf", "notes",
        ]
        positions = [SCHEMA.index(f"`{column}`") for column in columns]
        self.assertEqual(positions, sorted(positions))
        for value in ("true", "false", "not_requested", "pending", "completed", "failed"):
            self.assertIn(f"`{value}`", SKILL + SCHEMA)

    def test_references_and_boundaries_are_discoverable(self):
        self.assertIn("references/tracker-schema.md", SKILL)
        self.assertIn("references/resume-tailoring.md", SKILL)
        self.assertRegex(SKILL.lower(), r"never (apply|submit)")
        self.assertIn("Never invent", TAILORING)
        self.assertIn("Render the DOCX and every PDF page", TAILORING)
        self.assertIn("selectable text", TAILORING)
        self.assertIn("documents", SKILL)
        self.assertIn("pdf", SKILL)

    def test_example_config_is_generic(self):
        example = (ROOT / "config.example.json").read_text(encoding="utf-8")
        self.assertIn("/absolute/path/to/", example)
        self.assertNotRegex(example, r"/(?:Users|home)/[^/]+/")

    def test_all_local_links_resolve(self):
        links = re.findall(r"\[[^]]+\]\(([^)]+)\)", SKILL)
        self.assertGreaterEqual(len(links), 2)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)


if __name__ == "__main__":
    unittest.main()
