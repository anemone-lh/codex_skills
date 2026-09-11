# Public Repository Sanitization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove personal workstation data from the repository and its public history while preserving a privately configured, working local installation of the skill.

**Architecture:** Convert the tracked skill to a portable configuration contract with a safe example file, while keeping real values only in an ignored installed `config.local.json`. Validate a sanitized candidate tree in an isolated worktree, then create a new one-commit public history and replace remote `main` only after remote-state and privacy checks.

**Tech Stack:** Markdown, JSON, Python 3 standard library, `unittest`, Git, GitHub SSH, Codex skill validator.

**Spec:** `docs/superpowers/specs/2026-09-11-public-repository-sanitization-design.md`

## Global Constraints

- The installed local skill must retain its current tracker, template, and output paths without committing those values.
- The public tree and every commit reachable from public `main` must contain no personal name, local account name, institution-specific path, machine-local email, or macOS home-directory absolute path.
- The GitHub account name and repository URL remain public identifiers.
- Keep the repository private until all remote-history checks pass.
- Never push the local private backup branch or tags that reach the old history.

---

### Task 1: Portable configuration contract

**Files:**
- Create: `skill-src/collecting-internship-applications/config.example.json`
- Create: `skill-src/collecting-internship-applications/scripts/validate_config.py`
- Create: `skill-src/collecting-internship-applications/tests/test_validate_config.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `config.local.json` with `tracker_csv`, `resume_template`, and `resume_output_root` string fields.
- Produces: `load_config(path: Path) -> dict[str, Path]`; CLI emits JSON with `result=valid` without echoing private values.

- [ ] Write tests for valid configuration, missing file, missing fields, unknown fields, relative paths, and non-string values.
- [ ] Run the focused tests and verify they fail because `validate_config.py` is absent.
- [ ] Implement strict JSON validation using only the Python standard library.
- [ ] Add a generic `config.example.json` and ignore `config.local.json` at any depth.
- [ ] Run the focused tests and require all to pass.
- [ ] Commit as `feat: add portable local configuration`.

### Task 2: Sanitize skill and documentation

**Files:**
- Modify: `README.md`
- Modify: `skill-src/collecting-internship-applications/SKILL.md`
- Modify: `skill-src/collecting-internship-applications/tests/test_skill_contract.py`
- Modify or remove: older files under `docs/superpowers/` that contain private values

**Interfaces:**
- Consumes: validated paths from `config.local.json`.
- Produces: the same tracker and resume workflow without tracked personal defaults.

- [ ] Replace fixed-path contract assertions with configuration-loading, missing-config stop behavior, and generic-path assertions; verify the changed tests fail first.
- [ ] Rewrite `SKILL.md` so every live operation validates and reads `config.local.json`, then substitutes the returned paths into existing helper and document workflows.
- [ ] Rewrite README installation/setup examples with generic paths and explicitly exclude real resumes, trackers, and local configuration.
- [ ] Remove old private planning/specification documents; retain the generic sanitization specification and plan.
- [ ] Run all unit and contract tests and the official skill validator.
- [ ] Run a tracked-tree privacy scan and require zero matches for the private patterns.
- [ ] Commit as `refactor: make internship skill portable`.

### Task 3: Preserve the private local installation

**Files:**
- Create outside Git: installed skill `config.local.json`
- Replace outside Git: installed public skill files while preserving the local configuration

**Interfaces:**
- Consumes: the user's existing three private paths.
- Produces: a validated installed skill with private configuration excluded from source-control comparisons.

- [ ] Write `config.local.json` directly into the installed skill with owner-only permissions.
- [ ] Replace installed tracked files from the sanitized source without deleting the private configuration.
- [ ] Validate installed configuration without printing values.
- [ ] Run installed skill validation and compare staged/installed hashes excluding `config.local.json`, caches, and tests when appropriate.
- [ ] Confirm the existing template and destination parent directories resolve, without creating the tracker.

### Task 4: Rebuild and publish sanitized history

**Files:**
- Git references only; no new product files.

**Interfaces:**
- Consumes: sanitized, tested working tree and the currently advertised remote `main` hash.
- Produces: one clean public root commit on local and remote `main`, plus a local-only private backup branch.

- [ ] Record the expected remote `main` hash and confirm it matches the pre-cleanup local lineage.
- [ ] Create local branch `private/pre-public-sanitization` at the old-history tip and confirm it has no upstream.
- [ ] Materialize the sanitized tree on an orphan branch and commit it with the noreply identity.
- [ ] Scan the new tree and every commit reachable from the new root; require zero private-pattern matches.
- [ ] Run all tests and the official validator from the new root.
- [ ] Replace local `main` with the new root while preserving the local backup branch.
- [ ] Force-push using `--force-with-lease=<expected-old-hash>`; never use an unguarded force push.
- [ ] Verify remote `main`, remote branch inventory, reachable history, repository tests, and privacy scans.

### Task 5: Change repository visibility

**Files:**
- GitHub repository setting only.

**Interfaces:**
- Consumes: verified sanitized remote repository.
- Produces: repository visibility set to Public.

- [ ] Open repository visibility settings and inspect the current value.
- [ ] Ask for action-time confirmation immediately before the final Public visibility submission.
- [ ] Change visibility and complete any GitHub confirmation challenge through user handoff when credentials are required.
- [ ] Verify the repository page visibly reports Public and report the final URL and audit evidence.
