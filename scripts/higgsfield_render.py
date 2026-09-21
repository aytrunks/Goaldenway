#!/usr/bin/env python3
"""Render a Higgsfield shot from a JSON spec: submit, poll, download.

Usage:
    export HF_KEY="KEY_ID:KEY_SECRET"
    python3 scripts/higgsfield_render.py shots/shot_2_carl_illegal.json

Auth is a single header, `Authorization: Key KEY_ID:KEY_SECRET`. Both halves are
required; a bare KEY_ID returns 401. If you hold the halves separately, set
HIGGSFIELD_API_KEY and HIGGSFIELD_API_SECRET and this script joins them.

The seedance-2.5 input schema is `additionalProperties: false`, so unknown keys
are rejected outright — notably there is no `negative_prompt` field, and the
text-to-video model takes no image. Anything the model must avoid belongs in the
prompt text itself. Keys in a shot spec's "input" are passed through verbatim,
so a different model's fields work without editing this file.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = os.environ.get("HIGGSFIELD_API_BASE", "https://api.higgsfield.ai").rstrip("/")

PENDING = {"queued", "in_progress"}
FAILED = {"failed", "nsfw", "canceled", "cancelled"}


class ApiError(RuntimeError):
    pass


def credentials() -> str:
    """Return the KEY_ID:KEY_SECRET pair the Authorization header needs."""
    key = os.environ.get("HF_KEY") or os.environ.get("HF_CREDENTIALS") or ""
    if ":" not in key:
        key_id = key or os.environ.get("HIGGSFIELD_API_KEY", "")
        secret = os.environ.get("HIGGSFIELD_API_SECRET") or os.environ.get("HIGGSFIELD_SECRET", "")
        if not key_id:
            raise SystemExit("No credentials. Set HF_KEY='KEY_ID:KEY_SECRET'.")
        if not secret:
            raise SystemExit(
                f"Incomplete credentials: have a key id ({key_id[:8]}...) but no secret.\n"
                "Higgsfield needs both halves: export HF_KEY='KEY_ID:KEY_SECRET'"
            )
        key = f"{key_id}:{secret}"
    return key


def request(method: str, url: str, payload: dict | None = None, timeout: int = 120) -> dict:
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Authorization": f"Key {credentials()}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        raise ApiError(f"{method} {url} -> HTTP {exc.code}\n{exc.read().decode(errors='replace')}") from None
    except urllib.error.URLError as exc:
        raise ApiError(f"{method} {url} -> unreachable: {exc.reason}") from None


def submit(shot: dict) -> dict:
    model = shot["model"]
    url = f"{API_BASE}/{model.strip('/')}"
    print(f"submitting {shot.get('name', 'shot')} -> {model}", flush=True)
    data = request("POST", url, shot["input"])
    if not data.get("request_id"):
        raise ApiError(f"no request_id in response:\n{json.dumps(data, indent=2)}")
    return data


def poll(submission: dict, timeout: int, interval: int) -> dict:
    request_id = submission["request_id"]
    url = submission.get("status_url") or f"{API_BASE}/requests/{request_id}"
    deadline = time.time() + timeout
    last = None
    state = submission
    while True:
        status = str(state.get("status", "")).lower()
        if status and status != last:
            print(f"  {status}", flush=True)
            last = status
        if status == "completed":
            return state
        if status in FAILED:
            raise ApiError(f"request {status}: {state.get('error', json.dumps(state, indent=2))}")
        if status not in PENDING:
            print(f"  (unrecognized status {status!r}, still polling)", flush=True)
        if time.time() >= deadline:
            raise ApiError(f"timed out after {timeout}s; request {request_id} last status {status!r}")
        time.sleep(interval)
        state = request("GET", url)


def download(state: dict, dest: Path) -> Path:
    for key in ("video", "mov", "zip"):
        entry = state.get(key)
        if isinstance(entry, dict) and entry.get("url"):
            url = entry["url"]
            break
    else:
        raise ApiError(f"completed but no video url:\n{json.dumps(state, indent=2)}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as resp, dest.open("wb") as fh:
        while chunk := resp.read(1 << 16):
            fh.write(chunk)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("shot", type=Path, help="path to the shot JSON spec")
    parser.add_argument("-o", "--out", type=Path, help="output file (default out/<shot name>.<format>)")
    parser.add_argument("--timeout", type=int, default=1800, help="seconds to wait for the render")
    parser.add_argument("--interval", type=int, default=5, help="seconds between status polls")
    parser.add_argument("--dry-run", action="store_true", help="print the request and exit, no network")
    args = parser.parse_args()

    shot = json.loads(args.shot.read_text())
    if args.dry_run:
        print(f"POST {API_BASE}/{shot['model'].strip('/')}")
        print(json.dumps(shot["input"], indent=2))
        return 0

    ext = shot["input"].get("output_format", "mp4")
    out = args.out or Path(__file__).resolve().parent.parent / "out" / f"{shot.get('name', args.shot.stem)}.{ext}"
    try:
        state = poll(submit(shot), args.timeout, args.interval)
        path = download(state, out)
    except ApiError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1
    print(f"saved: {path} ({path.stat().st_size / 1_000_000:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
