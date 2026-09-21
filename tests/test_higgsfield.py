#!/usr/bin/env python3
"""Checks for the Higgsfield integration. Run: python3 tests/test_higgsfield.py

Stdlib only, no test runner, and no network: every case here is about local
behavior — schema validation, cost math, directive expansion, ledger state.
"""

from __future__ import annotations

import json
import math
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from higgsfield import ledger, schemas, specs  # noqa: E402

T25 = "bytedance/seedance-2.5/text-to-video"
T20 = "bytedance/seedance-2.0/text-to-video"

passed = failed = 0


def check(label: str, condition: bool) -> None:
    global passed, failed
    print(f"  {'PASS' if condition else 'FAIL'}  {label}")
    passed += bool(condition)
    failed += not condition


def rejects(model: str, payload: dict) -> bool:
    try:
        schemas.validate(model, payload)
        return False
    except schemas.ValidationError:
        return True


def test_validation() -> None:
    print("schema validation:")
    check("2.5 rejects 1080p", rejects(T25, {"prompt": "x", "resolution": "1080p"}))
    check("2.0 accepts 1080p", not rejects(T20, {"prompt": "x", "resolution": "1080p"}))
    check("2.0 rejects 16s (max 15)", rejects(T20, {"prompt": "x", "duration": 16}))
    check("2.5 accepts 16s (max 30)", not rejects(T25, {"prompt": "x", "duration": 16}))
    check("2.0 rejects bitrate_mode", rejects(T20, {"prompt": "x", "bitrate_mode": "high"}))
    check("2.5 accepts bitrate_mode", not rejects(T25, {"prompt": "x", "bitrate_mode": "high"}))
    check("duration below minimum", rejects(T25, {"prompt": "x", "duration": 2}))
    check("negative_prompt refused", rejects(T25, {"prompt": "x", "negative_prompt": "y"}))
    check("empty prompt refused", rejects(T25, {"prompt": ""}))
    check("missing prompt refused", rejects(T25, {"duration": 5}))
    check("bool is not an integer", rejects(T25, {"prompt": "x", "duration": True}))
    check("unlisted aspect ratio refused", rejects(T25, {"prompt": "x", "aspect_ratio": "5:2"}))
    check(
        "fully populated payload accepted",
        not rejects(
            T25,
            {
                "prompt": "x",
                "duration": 30,
                "resolution": "480p",
                "aspect_ratio": "9:16",
                "bitrate_mode": "standard",
                "output_format": "mov",
                "generate_audio": False,
            },
        ),
    )
    try:
        schemas.get("bytedance/seedance-2.5/image-to-video")
        check("unknown model raises UnknownModel", False)
    except schemas.UnknownModel:
        check("unknown model raises UnknownModel", True)


def test_cost() -> None:
    print("dimensions and cost:")
    check("720p 9:16 is portrait", schemas.dimensions("720p", "9:16") == (720, 1280))
    check("720p 16:9 is landscape", schemas.dimensions("720p", "16:9") == (1280, 720))
    check("1080p 1:1 is square", schemas.dimensions("1080p", "1:1") == (1080, 1080))
    check("4k 21:9 long side", schemas.dimensions("4k", "21:9") == (5040, 2160))

    shot = {"prompt": "x", "duration": 4, "resolution": "720p", "aspect_ratio": "9:16"}
    tokens_25, usd_25 = schemas.estimate_cost(T25, shot)
    tokens_20, usd_20 = schemas.estimate_cost(T20, shot)
    check("token formula matches the docs", tokens_25 == math.ceil(4 * 720 * 1280 * 24 / 1024) == 86_400)
    check("2.5 rate applied", abs(usd_25 - 86.4 * 0.0214) < 1e-6)
    check("2.0 is cheaper at the same size", tokens_20 == tokens_25 and usd_20 < usd_25)
    check("schema defaults fill the gaps", schemas.estimate_cost(T20, {"prompt": "x"})[0] == math.ceil(5 * 1280 * 720 * 24 / 1024))


def test_specs() -> None:
    print("shot specs:")
    shot = specs.load(ROOT / "shots" / "shot_2_carl_illegal.json")
    check("the real shot loads", shot["model"] == T25)
    check("the real shot validates", not rejects(shot["model"], shot["input"]))

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "spec.json"
        path.write_text(json.dumps({"model": "m", "input": {"image_url": {"$image": "assets/shot_2_balcony_reference.png"}}}))
        expanded = specs.load(path, root=ROOT)["input"]["image_url"]
        check("$image becomes a data uri", expanded.startswith("data:image/png;base64,") and len(expanded) > 10_000)

        path.write_text(json.dumps({"model": "m", "input": {"i": {"$image": "missing.png"}}}))
        try:
            specs.load(path, root=ROOT)
            check("$image on a missing file raises", False)
        except specs.SpecError:
            check("$image on a missing file raises", True)

        path.write_text('{"input": {}}')
        try:
            specs.load(path)
            check("a spec without a model raises", False)
        except specs.SpecError:
            check("a spec without a model raises", True)

    check("fingerprint ignores key order", specs.fingerprint("m", {"a": 1, "b": 2}) == specs.fingerprint("m", {"b": 2, "a": 1}))
    check("fingerprint tracks the model", specs.fingerprint("m", {"a": 1}) != specs.fingerprint("m2", {"a": 1}))
    check("summarize shortens long values", "chars)" in specs.summarize({"p": "x" * 500})["p"])


def test_ledger() -> None:
    print("ledger:")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "ledger.json"
        ledger.record(request_id="r1", fingerprint="fp", shot="s", model="m", status="queued", path=path)
        ledger.record(request_id="r1", fingerprint="fp", shot="s", model="m", status="in_progress", path=path)
        check("re-recording updates in place", len(ledger.load(path)) == 1)
        check("status is updated", ledger.load(path)[0]["status"] == "in_progress")
        check("an in-flight request is reusable", ledger.is_reusable(ledger.find_by_fingerprint("fp", path)))

        output = Path(tmp) / "video.mp4"
        ledger.record(request_id="r1", fingerprint="fp", shot="s", model="m", status="completed", output=str(output), path=path)
        check("completed but file gone is not reusable", not ledger.is_reusable(ledger.find_by_fingerprint("fp", path)))
        output.write_text("video")
        check("completed with the file present is reusable", ledger.is_reusable(ledger.find_by_fingerprint("fp", path)))

        check("an unknown fingerprint finds nothing", ledger.find_by_fingerprint("nope", path) is None)
        check("request ids are searchable", ledger.find_by_request_id("r1", path)["shot"] == "s")

        path.write_text("{ corrupt")
        check("a corrupt ledger degrades to empty", ledger.load(path) == [])


def main() -> int:
    for suite in (test_validation, test_cost, test_specs, test_ledger):
        suite()
    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
