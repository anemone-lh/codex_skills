---
name: collecting-internship-applications
description: Use when collecting internship or job-posting URLs into the user's application tracker, updating tracked roles, or tailoring a resume for a tracked position.
---

# Collecting Internship Applications

## Overview

Turn job URLs into a reliable CSV tracker, then generate a truthful targeted resume only for rows whose `generate_resume` toggle is `true`. Do not submit applications.

## Local configuration

Before any live operation, locate `config.local.json` beside this `SKILL.md` and run:

```bash
python3 scripts/validate_config.py --config config.local.json
```

Read these validated absolute paths from the file:

- `tracker_csv`
- `resume_template`
- `resume_output_root`

If validation fails, stop and tell the user to copy `config.example.json` to `config.local.json` and fill in local absolute paths. Do not guess paths or create live files without valid configuration. Never print private configuration values unless the user explicitly asks to inspect them.

Create the tracker only immediately before writing its first real record. Never create it during skill installation or testing.

## Collect URLs

1. Open every supplied URL and identify the authoritative job posting. Follow a direct application link if needed, but never apply, sign in, upload, or send data.
2. Extract company, title, location, salary, application URL, referral code, requirements, source URL, and collection time. Leave unknown facts blank. Put any inference and its basis in `notes`.
3. Read [references/tracker-schema.md](references/tracker-schema.md), construct one JSON object per role, and show it before writing only when several roles or conflicting links create material ambiguity.
4. Run `scripts/update_tracker.py upsert` with `--csv` set to the validated `tracker_csv` value and `--record-json` set to the structured role object.
5. Report whether each row was inserted or updated. Never fabricate missing values.

## Process resume toggles

When the user asks to tailor a resume, or to process enabled rows, read `tracker_csv` and select only rows with canonical `generate_resume=true`.

For each selected row:

1. Set `resume_status=pending` with `scripts/update_tracker.py set-status` and the validated tracker path.
2. Read [references/resume-tailoring.md](references/resume-tailoring.md).
3. **REQUIRED SUB-SKILL:** Use `documents` to inspect `resume_template`, edit a copy, and render the DOCX for visual QA.
4. **REQUIRED SUB-SKILL:** Use `pdf` to create or inspect the final PDF and render every page for visual QA.
5. Write both outputs under `resume_output_root/<safe-company>_<safe-role>/`. Never overwrite an existing version; add a timestamp to a collision.
6. After every acceptance check passes, update `resume_status=completed`, `resume_docx`, and `resume_pdf`. If generation fails, set `resume_status=failed`, append an actionable explanation to `notes`, and preserve earlier successful paths.

## Completion contract

Collection is complete only when the tracker row is present and deduplicated. Resume tailoring is complete only when the DOCX and PDF exist, both render correctly, the PDF contains selectable text, tracker paths resolve, and every claim remains supported by the source resume.

## Common mistakes

| Mistake | Required correction |
|---|---|
| Guessing missing local paths | Stop and request a valid `config.local.json` |
| Treating a blank job field as permission to guess | Leave it blank and describe uncertainty in `notes` |
| Replacing a populated field with a blank scrape | Preserve the existing value |
| Treating CSV as an interactive checkbox UI | Use lowercase `true` or `false` in `generate_resume` |
| Adding attractive but unsupported metrics | Rewrite only facts already supported by the template or user |
| Delivering an unrendered PDF | Render and inspect all DOCX and PDF pages first |
