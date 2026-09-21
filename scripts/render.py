#!/usr/bin/env python3
"""Render Higgsfield shots from JSON specs.

    python3 scripts/render.py render shots/shot_2_carl_illegal.json
    python3 scripts/render.py status <request_id>
    python3 scripts/render.py list
    python3 scripts/render.py models

Credentials come from the environment and never from a spec file:

    export HF_API_KEY_ID=...
    export HF_API_KEY_SECRET=...
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from higgsfield import client, ledger, schemas, specs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _out_path(spec: dict, override: Path | None) -> Path:
    if override:
        return override
    ext = spec["input"].get("output_format", "mp4")
    return ROOT / "out" / f"{spec['name']}.{ext}"


def _finish(state: dict, dest: Path, entry: dict | None = None) -> int:
    """Download a completed request and update the ledger."""
    field, url = client.asset_url(state)
    print(f"  downloading {field}...", flush=True)
    path = client.download(url, dest)
    if entry:
        ledger.record(
            request_id=state["request_id"],
            fingerprint=entry.get("fingerprint", ""),
            shot=entry.get("shot", ""),
            model=entry.get("model", ""),
            status="completed",
            output=str(path),
        )
    print(f"saved: {path} ({path.stat().st_size / 1_000_000:.1f} MB)")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    spec = specs.load(args.shot)
    model, payload = spec["model"], spec["input"]

    # Validate locally before spending anything on a round trip.
    try:
        schemas.validate(model, payload)
        tokens, usd = schemas.estimate_cost(model, payload)
        cost = f"~${usd:.2f}" if usd is not None else "unknown (no rate on file)"
    except schemas.UnknownModel as exc:
        if not args.allow_unverified:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(f"WARNING: no verified schema for {model}; submitting unvalidated.", file=sys.stderr)
        tokens, cost = 0, "unknown (unverified model)"
    except schemas.ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    fingerprint = specs.fingerprint(model, payload)
    dest = _out_path(spec, args.out)

    if args.dry_run:
        print(f"POST {client.API_BASE}/{model.strip('/')}")
        print(json.dumps(specs.summarize(payload), indent=2))
        print(f"\nfingerprint {fingerprint} | {tokens:,} tokens | {cost} | -> {dest}")
        return 0

    # An identical payload already submitted is either in flight or on disk.
    prior = ledger.find_by_fingerprint(fingerprint)
    if prior and ledger.is_reusable(prior) and not args.force:
        if prior["status"] == "completed":
            print(f"already rendered: {prior['output']}\n(--force to render it again)")
            return 0
        print(f"resuming in-flight request {prior['request_id']} (--force to submit a new one)")
        submission = {"request_id": prior["request_id"], "status": prior["status"]}
    else:
        print(f"{spec['name']} -> {model}")
        print(f"  {tokens:,} video tokens, {cost}")
        if not args.yes and sys.stdin.isatty():
            if input("  submit? [y/N] ").strip().lower() not in ("y", "yes"):
                print("cancelled")
                return 1
        submission = client.submit(model, payload)
        print(f"  request_id {submission['request_id']}")
        ledger.record(
            request_id=submission["request_id"],
            fingerprint=fingerprint,
            shot=spec["name"],
            model=model,
            status=submission.get("status", "queued"),
            input_summary=specs.summarize(payload),
        )

    def on_status(current: str) -> None:
        print(f"  {current}", flush=True)
        ledger.record(
            request_id=submission["request_id"],
            fingerprint=fingerprint,
            shot=spec["name"],
            model=model,
            status=current,
        )

    entry = ledger.find_by_request_id(submission["request_id"])
    state = client.poll(submission, timeout=args.timeout, on_status=on_status)
    return _finish(state, dest, entry or {"fingerprint": fingerprint, "shot": spec["name"], "model": model})


def cmd_status(args: argparse.Namespace) -> int:
    entry = ledger.find_by_request_id(args.request_id)
    state = client.status(args.request_id)
    current = str(state.get("status", "unknown")).lower()
    print(f"{args.request_id}: {current}")

    if entry:
        ledger.record(
            request_id=args.request_id,
            fingerprint=entry.get("fingerprint", ""),
            shot=entry.get("shot", ""),
            model=entry.get("model", ""),
            status=current,
        )
    if current != client.COMPLETED:
        if current in client.FAILED:
            print(f"  {state.get('error') or 'no detail given'}", file=sys.stderr)
            return 1
        return 0

    if args.out:
        dest = args.out
    elif entry and entry.get("output"):
        dest = Path(entry["output"])
    else:
        dest = ROOT / "out" / f"{(entry or {}).get('shot') or args.request_id}.mp4"
    return _finish(state, Path(dest), entry)


def cmd_list(args: argparse.Namespace) -> int:
    records = ledger.load()
    if not records:
        print("no requests recorded yet")
        return 0
    for entry in records[-args.limit :]:
        line = f"{entry['created_at']}  {entry['request_id']}  {entry['status']:<12} {entry['shot']}"
        if entry.get("output"):
            line += f"  -> {entry['output']}"
        print(line)
    return 0


def cmd_models(args: argparse.Namespace) -> int:
    known = schemas.registry()
    if not known:
        print(f"no schemas in {schemas.SCHEMA_DIR}")
        return 0
    for model, doc in sorted(known.items()):
        props = doc["schema"].get("properties", {})
        duration = props.get("duration", {})
        span = f"{duration.get('minimum', '?')}-{duration.get('maximum', '?')}s" if duration else "n/a"
        print(f"{model}\n  duration {span} | resolutions {props.get('resolution', {}).get('enum', [])}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    render = sub.add_parser("render", help="submit a shot spec, poll it, download the result")
    render.add_argument("shot", type=Path)
    render.add_argument("-o", "--out", type=Path, help="output path")
    render.add_argument("--dry-run", action="store_true", help="print the request and cost, send nothing")
    render.add_argument("--force", action="store_true", help="resubmit even if an identical render exists")
    render.add_argument("--allow-unverified", action="store_true", help="submit a model with no local schema")
    render.add_argument("-y", "--yes", action="store_true", help="skip the cost confirmation")
    render.add_argument("--timeout", type=int, default=1800, help="seconds to wait (default 1800)")
    render.set_defaults(func=cmd_render)

    status = sub.add_parser("status", help="check or resume a request by id")
    status.add_argument("request_id")
    status.add_argument("-o", "--out", type=Path, help="download here if it is complete")
    status.set_defaults(func=cmd_status)

    listing = sub.add_parser("list", help="show recorded requests")
    listing.add_argument("-n", "--limit", type=int, default=20)
    listing.set_defaults(func=cmd_list)

    models = sub.add_parser("models", help="show models with a verified schema")
    models.set_defaults(func=cmd_models)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (client.HiggsfieldError, specs.SpecError, schemas.SchemaError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\ninterrupted; resume with:  status <request_id>", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
