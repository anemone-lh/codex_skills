# Tracker schema

Use UTF-8 with BOM and these columns in this exact order:

| Column | Meaning | Normalization |
|---|---|---|
| `company_name` | Employer shown by the posting | Preserve official display name |
| `job_title` | Specific role title | Preserve meaningful level/team text |
| `location` | City, region, remote/hybrid status | Blank if not stated |
| `salary` | Stated pay and period/currency | Keep source wording; blank if absent |
| `application_url` | Direct authoritative application link | Normalize for deduplication |
| `referral_code` | Referral/invite code explicitly supplied | Never infer |
| `job_requirements` | Concise duties and qualifications | Preserve keywords and minimum criteria |
| `source_url` | URL originally supplied | Normalize for fallback matching |
| `collected_at` | Collection timestamp | ISO 8601 with timezone |
| `generate_resume` | Resume-generation toggle | Lowercase `true` or `false`; default `false` |
| `resume_status` | Generation state | `not_requested`, `pending`, `completed`, `failed` |
| `resume_docx` | Editable output | Absolute path or blank |
| `resume_pdf` | Submission output | Absolute path or blank |
| `notes` | Ambiguity, inference basis, or errors | Concise free text |

## Identity and merge rules

Use normalized `application_url` as the primary identity. If it is blank, use normalized `source_url` plus case-folded company and job title. URL normalization lowercases scheme/host, removes fragments, sorts query parameters, trims a non-root trailing slash, and removes common tracking parameters including `utm_*`, `gclid`, and `fbclid`.

On a match, fill missing fields and accept richer non-empty incoming values. Never replace a non-empty field with blank input. Preserve prior successful resume paths during a failed retry.

## Helper input

Pass exactly one JSON object containing the 14 fields to `scripts/update_tracker.py upsert`. The helper rejects unknown fields, malformed existing headers, invalid booleans, and invalid status values. It writes through a sibling temporary file before atomic replacement.

