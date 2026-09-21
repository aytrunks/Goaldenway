"""A local record of every submission.

The API is asynchronous: a submit returns a ``request_id`` and the result shows
up later. The ledger is what makes that survivable from a CLI — it remembers
which request belongs to which shot, so an interrupted render can be resumed
instead of paid for twice, and a repeat of an identical submission is caught
before it reaches the API.

Stored at ``.higgsfield/ledger.json`` (gitignored). Records carry no
credentials; the ``$image`` data URIs in a payload are summarized, not stored.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = Path(os.environ.get("HIGGSFIELD_LEDGER", ROOT / ".higgsfield" / "ledger.json"))

OPEN_STATUSES = {"queued", "in_progress"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(path: Path = LEDGER_PATH) -> list[dict]:
    if not path.is_file():
        return []
    try:
        records = json.loads(path.read_text())
    except json.JSONDecodeError:
        return []
    return records if isinstance(records, list) else []


def _save(records: list[dict], path: Path = LEDGER_PATH) -> None:
    """Write atomically; a half-written ledger would lose request ids."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(records, fh, indent=2)
        Path(tmp).replace(path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def record(
    *,
    request_id: str,
    fingerprint: str,
    shot: str,
    model: str,
    status: str,
    input_summary: dict | None = None,
    output: str | None = None,
    path: Path = LEDGER_PATH,
) -> dict:
    """Insert or update the record for a request id."""
    records = load(path)
    for entry in records:
        if entry.get("request_id") == request_id:
            entry.update(status=status, updated_at=_now())
            if output:
                entry["output"] = output
            _save(records, path)
            return entry

    entry = {
        "request_id": request_id,
        "fingerprint": fingerprint,
        "shot": shot,
        "model": model,
        "status": status,
        "created_at": _now(),
        "updated_at": _now(),
        "input": input_summary or {},
    }
    if output:
        entry["output"] = output
    records.append(entry)
    _save(records, path)
    return entry


def find_by_fingerprint(fingerprint: str, path: Path = LEDGER_PATH) -> dict | None:
    """Most recent submission of an identical payload, if there is one."""
    matches = [e for e in load(path) if e.get("fingerprint") == fingerprint]
    return matches[-1] if matches else None


def find_by_request_id(request_id: str, path: Path = LEDGER_PATH) -> dict | None:
    for entry in load(path):
        if entry.get("request_id") == request_id:
            return entry
    return None


def is_reusable(entry: dict) -> bool:
    """True when a prior submission can be resumed or its output reused."""
    if entry.get("status") in OPEN_STATUSES:
        return True
    return entry.get("status") == "completed" and bool(entry.get("output")) and Path(entry["output"]).is_file()
