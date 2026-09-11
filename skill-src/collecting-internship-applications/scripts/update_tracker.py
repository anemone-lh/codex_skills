#!/usr/bin/env python3
"""Create and update the internship CSV tracker safely."""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


FIELDS = [
    "company_name",
    "job_title",
    "location",
    "salary",
    "application_url",
    "referral_code",
    "job_requirements",
    "source_url",
    "collected_at",
    "generate_resume",
    "resume_status",
    "resume_docx",
    "resume_pdf",
    "notes",
]
STATUSES = {"not_requested", "pending", "completed", "failed"}
TRACKING_PARAMS = {"gclid", "fbclid", "mc_cid", "mc_eid"}


def normalize_bool(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value in (1, "1"):
        return "true"
    if value in (0, "0", None, ""):
        return "false"
    normalized = str(value).strip().lower()
    if normalized in {"true", "yes", "y", "on"}:
        return "true"
    if normalized in {"false", "no", "n", "off"}:
        return "false"
    raise ValueError(f"invalid boolean value: {value!r}")


def normalize_url(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    parts = urlsplit(text)
    host = (parts.hostname or "").lower()
    if parts.port:
        host = f"{host}:{parts.port}"
    query = [
        (key, val)
        for key, val in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_PARAMS
    ]
    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), host, path, urlencode(sorted(query)), ""))


def _normalize_record(record: dict[str, object]) -> dict[str, str]:
    unknown = set(record) - set(FIELDS)
    if unknown:
        raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
    normalized = {field: str(record.get(field, "") or "") for field in FIELDS}
    normalized["generate_resume"] = normalize_bool(record.get("generate_resume", False))
    normalized["resume_status"] = normalized["resume_status"] or "not_requested"
    if normalized["resume_status"] not in STATUSES:
        raise ValueError(f"invalid resume_status: {normalized['resume_status']}")
    return normalized


def _record_key(record: dict[str, str]) -> tuple[str, ...]:
    application = normalize_url(record.get("application_url"))
    if application:
        return ("application_url", application)
    return (
        "fallback",
        normalize_url(record.get("source_url")),
        record.get("company_name", "").strip().casefold(),
        record.get("job_title", "").strip().casefold(),
    )


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError("CSV header does not match the required tracker schema")
        return [dict(row) for row in reader]


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="raise")
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(path)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise


def upsert_record(path: str | Path, record: dict[str, object]) -> str:
    csv_path = Path(path)
    supplied_fields = set(record)
    incoming = _normalize_record(record)
    rows = _read_rows(csv_path)
    incoming_key = _record_key(incoming)
    for index, existing in enumerate(rows):
        if _record_key(existing) == incoming_key:
            rows[index] = {
                field: incoming[field]
                if field in supplied_fields and incoming[field]
                else existing.get(field, "")
                for field in FIELDS
            }
            _write_rows(csv_path, rows)
            return "updated"
    rows.append(incoming)
    _write_rows(csv_path, rows)
    return "inserted"


def set_status(path: str | Path, key: str, status: str, **updates: object) -> None:
    if status not in STATUSES:
        raise ValueError(f"invalid resume_status: {status}")
    allowed_updates = {"generate_resume", "resume_docx", "resume_pdf", "notes"}
    unknown = set(updates) - allowed_updates
    if unknown:
        raise ValueError(f"invalid status update fields: {', '.join(sorted(unknown))}")
    csv_path = Path(path)
    rows = _read_rows(csv_path)
    normalized_key = normalize_url(key)
    for row in rows:
        if normalize_url(row.get("application_url")) == normalized_key:
            row["resume_status"] = status
            for field, value in updates.items():
                row[field] = normalize_bool(value) if field == "generate_resume" else str(value or "")
            _write_rows(csv_path, rows)
            return
    raise KeyError(f"tracker record not found: {key}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    upsert = subparsers.add_parser("upsert", help="insert or enrich one tracker row")
    upsert.add_argument("--csv", required=True)
    upsert.add_argument("--record-json", required=True)
    status = subparsers.add_parser("set-status", help="update resume state for an application URL")
    status.add_argument("--csv", required=True)
    status.add_argument("--key", required=True)
    status.add_argument("--status", required=True, choices=sorted(STATUSES))
    status.add_argument("--updates-json", default="{}")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.command == "upsert":
        result = upsert_record(args.csv, json.loads(args.record_json))
        print(json.dumps({"result": result}, ensure_ascii=False))
    else:
        updates = json.loads(args.updates_json)
        set_status(args.csv, args.key, args.status, **updates)
        print(json.dumps({"result": "updated"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
