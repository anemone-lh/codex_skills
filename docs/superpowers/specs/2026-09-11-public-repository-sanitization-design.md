# Public Repository Sanitization Design

## Goal

Publish the repository without exposing a person's name, local username, institution-specific directory structure, resume filename, machine-local email address, or other private workstation details, while preserving a fully configured local installation of the internship application skill.

## Separation model

The repository contains portable behavior and an example configuration. Personal values live only in an ignored local configuration file inside the installed skill directory.

The public skill reads `config.local.json` from its own directory before collecting jobs or tailoring resumes. The file has three required absolute-path fields:

- `tracker_csv`
- `resume_template`
- `resume_output_root`

The repository includes `config.example.json` using generic placeholder paths. `.gitignore` excludes `config.local.json` at any depth. If the local configuration is absent or invalid, the skill stops with an actionable setup message and does not guess paths or create files.

The CSV helper remains path-parameterized and contains no personal defaults. The installed skill receives a private `config.local.json` populated with the current working paths, preserving local behavior.

## Public documentation

Rewrite `README.md`, `SKILL.md`, tests, specifications, and implementation plans so that they contain only generic examples. Public documentation explains how to copy `config.example.json` to the installed skill directory and fill in local absolute paths.

Historic planning documents may remain only after sanitization. Any document whose value is purely historical and whose examples are difficult to make portable may be removed from the clean public snapshot.

## Tests

Add deterministic configuration tests covering:

- valid three-path configuration;
- missing configuration;
- missing required fields;
- relative paths rejected;
- repository example contains no personal values;
- ignored `config.local.json` remains outside the tracked file set;
- installed local configuration resolves to the intended existing template and destination directories without printing its values.

Existing tracker and contract tests remain green after replacing fixed-path assertions with configuration-contract assertions.

## Privacy audit

Before publishing, scan the candidate public tree and every commit reachable from the candidate public `main` for:

- personal name and local account name;
- macOS home-directory absolute paths;
- institution-specific path names;
- machine-local email domains;
- private configuration filenames containing tracked values;
- private resume or job-output artifacts.

The GitHub account name and repository URL are public identifiers required to identify the repository and are not treated as removable workstation data.

## History replacement

Preserve the existing history only in a local backup branch named `private/pre-public-sanitization`; never push that branch or any tag pointing to the private commits.

Create a new orphan public-history branch from the sanitized working tree. Commit it as a single root commit using the repository-local identity `anemone-lh <anemone-lh@users.noreply.github.com>`. Replace local `main` with this branch and force-push only after confirming the remote still points to the previously inspected private history.

After the push, verify that:

- remote `main` equals the sanitized local root commit;
- only the intended remote branch is advertised;
- privacy scans pass against the tree and all reachable public commits;
- tests and skill validation pass from the rewritten `main`.

## GitHub visibility

Keep the repository private throughout cleanup. Change visibility to Public only after remote verification. Because this exposes the repository to everyone, request confirmation immediately before the final visibility-control action. Verify the repository page visibly reports Public afterward.

## Recovery

The local backup branch permits recovery of the original private development history. It must remain local and clearly named. The installed skill's private configuration remains untracked and is not altered by future public-repository pulls unless the user explicitly requests it.
