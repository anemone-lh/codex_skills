# Resume tailoring

## Evidence boundary

Treat the template and explicit user corrections as the only evidence for personal claims. Preserve identity, contact details, organizations, schools, dates, titles, technologies, credentials, and numbers. Never invent experience, tools, metrics, impact, or qualifications to match a posting.

Before editing, map each important job requirement to supporting resume evidence. Requirements without evidence are gaps; do not convert them into claims.

## STAR rewriting

Use compact accomplishment bullets rather than visible STAR labels:

`[Situation/task context when needed] + [specific action] + [supported result]`

Prefer strong verbs and quantified results already present in the template. If no result is supported, describe the action and concrete deliverable without creating a number. Reorder supported bullets and sections to foreground the strongest requirement matches.

## ATS matching

Reuse exact job terminology only when it accurately describes existing evidence. Prefer conventional headings, readable text, standard bullets, and text-based links. Do not keyword-stuff, hide text, use tables that break reading order, or add a skill solely because it appears in the posting.

## Output rules

- Copy the template; never edit it in place.
- Use filesystem-safe company and role names for the output directory and filenames.
- Produce both `<company>_<role>_Resume.docx` and `<company>_<role>_Resume.pdf`.
- If either target exists, append a local timestamp to both filenames.
- Default to the template page count. Change it only when readability or content integrity requires it.

## Acceptance checks

Render the DOCX and every PDF page. Confirm:

- no clipping, overlap, broken glyphs, orphaned headings, or accidental blank pages;
- contact details and core experience remain present;
- hyperlinks work or appear as valid text;
- the PDF has selectable text and opens normally;
- the final files exist at the absolute paths written to the tracker;
- every changed claim can be traced to the template or a user correction.

