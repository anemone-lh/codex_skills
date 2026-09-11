#!/usr/bin/env python3
"""Validate local paths for the internship application skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FIELDS = {"tracker_csv", "resume_template", "resume_output_root"}


def load_config(path: str | Path) -> dict[str, Path]:
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(
            f"config.local.json not found at {config_path.parent}; "
            "copy config.example.json and fill in absolute local paths"
        )
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("configuration must be a JSON object")
    missing = FIELDS - set(raw)
    unknown = set(raw) - FIELDS
    if missing:
        raise ValueError(f"missing configuration fields: {', '.join(sorted(missing))}")
    if unknown:
        raise ValueError(f"unknown configuration fields: {', '.join(sorted(unknown))}")

    result: dict[str, Path] = {}
    for field in sorted(FIELDS):
        value = raw[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        resolved = Path(value).expanduser()
        if not resolved.is_absolute():
            raise ValueError(f"{field} must be an absolute path")
        result[field] = resolved
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    load_config(args.config)
    print(json.dumps({"result": "valid"}))


if __name__ == "__main__":
    main()
