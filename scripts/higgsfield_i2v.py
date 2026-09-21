#!/usr/bin/env python3
"""Render a Higgsfield image-to-video shot from a JSON shot spec.

Usage:
    export HIGGSFIELD_API_KEY=...
    export HIGGSFIELD_API_SECRET=...
    python3 scripts/higgsfield_i2v.py shots/shot_2_carl_illegal.json -o out/shot_2.mp4

The Higgsfield API needs BOTH halves of the credential pair: the key goes in
the `hf-api-key` header, the secret in `hf-secret`. A key on its own gets a 401.

Endpoint, model slug and payload field names can all be overridden from the
environment (see ENV OVERRIDES below) so a change on Higgsfield's side can be
worked around without editing this file. On any API error the server's raw
response body is printed verbatim — that body, not this script, is the
authority on what the API expects.

ENV OVERRIDES
    HIGGSFIELD_API_BASE   default https://platform.higgsfield.ai
    HIGGSFIELD_I2V_PATH   default /v1/image2video/{model}
    HIGGSFIELD_JOBSET_PATH default /v1/job-sets/{id}
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = os.environ.get("HIGGSFIELD_API_BASE", "https://platform.higgsfield.ai").rstrip("/")
I2V_PATH = os.environ.get("HIGGSFIELD_I2V_PATH", "/v1/image2video/{model}")
JOBSET_PATH = os.environ.get("HIGGSFIELD_JOBSET_PATH", "/v1/job-sets/{id}")

TERMINAL_OK = {"completed", "succeeded", "success", "done"}
TERMINAL_BAD = {"failed", "error", "canceled", "cancelled", "nsfw", "rejected"}


class ApiError(RuntimeError):
    pass


def auth_headers() -> dict[str, str]:
    key = os.environ.get("HIGGSFIELD_API_KEY")
    secret = os.environ.get("HIGGSFIELD_API_SECRET") or os.environ.get("HIGGSFIELD_SECRET")
    missing = [n for n, v in (("HIGGSFIELD_API_KEY", key), ("HIGGSFIELD_API_SECRET", secret)) if not v]
    if missing:
        raise SystemExit(
            "Missing credential(s): "
            + ", ".join(missing)
            + "\nThe Higgsfield API authenticates with the key AND its paired secret."
        )
    return {"hf-api-key": key, "hf-secret": secret, "Content-Type": "application/json"}


def request(method: str, url: str, payload: dict | None = None, timeout: int = 120) -> dict:
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, headers=auth_headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise ApiError(f"{method} {url} -> HTTP {exc.code}\n{detail}") from None
    except urllib.error.URLError as exc:
        raise ApiError(f"{method} {url} -> unreachable: {exc.reason}") from None


def data_uri(path: Path) -> str:
    """Inline the reference frame; avoids needing a public URL for the image."""
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def build_payload(shot: dict, image: Path) -> dict:
    params = {
        "prompt": shot["prompt"],
        "input_images": [{"type": "image_url", "image_url": data_uri(image)}],
        "duration": shot.get("duration", 2),
        "resolution": shot.get("resolution", "720p"),
        "aspect_ratio": shot.get("aspect_ratio", "9:16"),
    }
    if shot.get("negative_prompt"):
        params["negative_prompt"] = shot["negative_prompt"]
    if shot.get("seed") is not None:
        params["seed"] = shot["seed"]
    return {"params": params}


def submit(shot: dict, image: Path) -> str:
    model = shot.get("model", "seedance-2.5")
    url = API_BASE + I2V_PATH.format(model=model)
    print(f"submitting {shot.get('name', 'shot')} -> {model} ({url})", flush=True)
    data = request("POST", url, build_payload(shot, image))
    job_set_id = data.get("id") or data.get("job_set_id")
    if not job_set_id:
        raise ApiError(f"no job-set id in response:\n{json.dumps(data, indent=2)}")
    return job_set_id


def iter_jobs(job_set: dict) -> list[dict]:
    jobs = job_set.get("jobs")
    return jobs if isinstance(jobs, list) and jobs else [job_set]


def result_url(job: dict) -> str | None:
    results = job.get("results") or {}
    for key in ("raw", "min", "video", "output"):
        entry = results.get(key)
        if isinstance(entry, dict) and entry.get("url"):
            return entry["url"]
        if isinstance(entry, str) and entry.startswith("http"):
            return entry
    return job.get("url") or job.get("video_url")


def poll(job_set_id: str, timeout: int, interval: int) -> str:
    url = API_BASE + JOBSET_PATH.format(id=job_set_id)
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        job_set = request("GET", url)
        for job in iter_jobs(job_set):
            status = str(job.get("status", "unknown")).lower()
            if status != last:
                print(f"  status: {status}", flush=True)
                last = status
            if status in TERMINAL_OK:
                link = result_url(job)
                if not link:
                    raise ApiError(f"job completed without a video url:\n{json.dumps(job, indent=2)}")
                return link
            if status in TERMINAL_BAD:
                raise ApiError(f"job {status}:\n{json.dumps(job, indent=2)}")
        time.sleep(interval)
    raise ApiError(f"timed out after {timeout}s waiting on job set {job_set_id}")


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as resp, dest.open("wb") as fh:
        while chunk := resp.read(1 << 16):
            fh.write(chunk)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("shot", type=Path, help="path to the shot JSON spec")
    parser.add_argument("-o", "--out", type=Path, help="output .mp4 (default out/<shot name>.mp4)")
    parser.add_argument("-i", "--image", type=Path, help="override the shot's reference image")
    parser.add_argument("--timeout", type=int, default=900, help="seconds to wait for the render")
    parser.add_argument("--interval", type=int, default=5, help="seconds between status polls")
    parser.add_argument("--print-payload", action="store_true", help="dump the request payload and exit")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    shot = json.loads(args.shot.read_text())
    image = args.image or (root / shot["reference_image"])
    if not image.is_file():
        raise SystemExit(f"reference image not found: {image}")

    if args.print_payload:
        payload = build_payload(shot, image)
        payload["params"]["input_images"] = ["<base64 data uri omitted>"]
        print(json.dumps(payload, indent=2))
        return 0

    out = args.out or root / "out" / f"{shot.get('name', args.shot.stem)}.mp4"
    try:
        link = poll(submit(shot, image), args.timeout, args.interval)
        print(f"rendered: {link}", flush=True)
        path = download(link, out)
    except ApiError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1
    print(f"saved: {path} ({path.stat().st_size / 1_000_000:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
