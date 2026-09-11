# Codex Skills

Personal Codex skills maintained as portable, testable packages. The repository currently includes `collecting-internship-applications`, which extracts job information from supplied URLs and can produce a role-targeted resume from a local template.

## Collecting Internship Applications

Source: [`skill-src/collecting-internship-applications`](skill-src/collecting-internship-applications)

Features:

- Extracts company, role, location, compensation, application link, referral code, and requirements.
- Writes a UTF-8 BOM CSV application tracker with URL normalization and duplicate merging.
- Uses the CSV `generate_resume` field as a portable toggle: `false` records the role; `true` requests a targeted resume.
- Rewrites only evidence already supported by the source resume, using concise STAR-style bullets and truthful ATS terminology.
- Produces editable DOCX and submission-ready PDF files after render-based quality checks.
- Never submits an application, enters credentials, or invents candidate claims.

## Install and configure

Copy the skill into your Codex skills directory:

```bash
cp -R skill-src/collecting-internship-applications /absolute/path/to/codex/skills/
```

Create a private local configuration beside the installed `SKILL.md`:

```bash
cp /absolute/path/to/codex/skills/collecting-internship-applications/config.example.json \
  /absolute/path/to/codex/skills/collecting-internship-applications/config.local.json
```

Edit `config.local.json` with three absolute paths:

```json
{
  "tracker_csv": "/absolute/path/to/job-search/Intership_Information.csv",
  "resume_template": "/absolute/path/to/resume/editable-template.docx",
  "resume_output_root": "/absolute/path/to/job-search/tailored-resumes"
}
```

`config.local.json` is ignored by Git. Do not commit application trackers, resumes, generated documents, or private path values.

Validate the configuration without printing its values:

```bash
python3 /absolute/path/to/codex/skills/collecting-internship-applications/scripts/validate_config.py \
  --config /absolute/path/to/codex/skills/collecting-internship-applications/config.local.json
```

## Usage

Example prompts:

```text
Collect this internship posting in my application tracker: https://example.com/job/123
```

```text
Process tracked roles whose generate_resume toggle is true.
```

See [`tracker-schema.md`](skill-src/collecting-internship-applications/references/tracker-schema.md) for the CSV contract and [`resume-tailoring.md`](skill-src/collecting-internship-applications/references/resume-tailoring.md) for truthfulness and rendering requirements.

## Test

```bash
python3 -m unittest discover \
  -s skill-src/collecting-internship-applications/tests \
  -v
```

Run the validator bundled with your Codex installation against the skill directory. The validator requires `PyYAML`.

All repository tests use temporary directories and never write to live trackers or resume locations.
