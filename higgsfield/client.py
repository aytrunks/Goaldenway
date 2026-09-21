"""HTTP client for the Higgsfield API.

Everything here follows the documented request lifecycle: submit to
``{base}/{model_id}``, receive a ``request_id`` plus a ``status_url``, poll that
url until a terminal status, then read the asset url off the completed body.

Credentials are read from the server environment only and are never written to
disk, logged, or embedded in a shot spec.
"""

from __future__ import annotations

import json
import os
import random
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

API_BASE = os.environ.get("HIGGSFIELD_API_BASE", "https://api.higgsfield.ai").rstrip("/")

# Documented request statuses.
PENDING = {"queued", "in_progress"}
FAILED = {"failed", "nsfw", "canceled", "cancelled"}
COMPLETED = "completed"

# Asset fields a completed request may carry, in the order we prefer them.
ASSET_FIELDS = ("video", "mov", "zip", "jsx", "fbx", "ply")

RETRY_STATUSES = {429, 500, 502, 503, 504}
MAX_HTTP_ATTEMPTS = 5


class HiggsfieldError(RuntimeError):
    """Base class for every failure this module raises."""


class CredentialsError(HiggsfieldError):
    pass


class ApiError(HiggsfieldError):
    def __init__(self, message: str, status: int | None = None, body: str = "") -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class RequestFailed(HiggsfieldError):
    """The generation request reached a terminal non-success status."""


class PollTimeout(HiggsfieldError):
    pass


def credentials() -> str:
    """Return ``KEY_ID:KEY_SECRET`` for the Authorization header.

    Accepts either the combined form (HF_KEY / HF_CREDENTIALS) or the split
    halves (HF_API_KEY_ID + HF_API_KEY_SECRET). A key id on its own is rejected
    here rather than spending a round trip to be told 401.
    """
    combined = os.environ.get("HF_KEY") or os.environ.get("HF_CREDENTIALS") or ""
    if ":" in combined:
        return combined

    key_id = combined or os.environ.get("HF_API_KEY_ID") or os.environ.get("HIGGSFIELD_API_KEY") or ""
    secret = os.environ.get("HF_API_KEY_SECRET") or os.environ.get("HIGGSFIELD_API_SECRET") or ""
    if not key_id and not secret:
        raise CredentialsError(
            "No Higgsfield credentials found. Set HF_API_KEY_ID and HF_API_KEY_SECRET "
            "(or the combined HF_KEY='KEY_ID:KEY_SECRET'). See .env.example."
        )
    if not secret:
        raise CredentialsError(
            f"Incomplete credentials: found a key id ({key_id[:8]}...) but no secret. "
            "Higgsfield authenticates with both halves; set HF_API_KEY_SECRET."
        )
    if not key_id:
        raise CredentialsError("Incomplete credentials: found a secret but no HF_API_KEY_ID.")
    return f"{key_id}:{secret}"


def _sleep_for(attempt: int, base: float, cap: float) -> float:
    """Exponential backoff with full jitter, so retries don't synchronize."""
    return random.uniform(0, min(cap, base * (2**attempt)))


def request(method: str, url: str, payload: dict | None = None, timeout: int = 120) -> dict:
    """Make one authenticated call, retrying rate limits and transient 5xx."""
    body = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Key {credentials()}", "Content-Type": "application/json"}

    last: ApiError | None = None
    for attempt in range(MAX_HTTP_ATTEMPTS):
        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode() or "{}")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            if exc.code == 401:
                raise ApiError(
                    "401 Unauthorized - check HF_API_KEY_ID and HF_API_KEY_SECRET.", exc.code, detail
                ) from None
            if exc.code not in RETRY_STATUSES:
                raise ApiError(f"{method} {url} -> HTTP {exc.code}\n{detail}", exc.code, detail) from None
            last = ApiError(f"{method} {url} -> HTTP {exc.code}\n{detail}", exc.code, detail)
            # A Retry-After from the server beats our own guess.
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            delay = float(retry_after) if retry_after and retry_after.isdigit() else _sleep_for(attempt, 1.0, 30.0)
        except urllib.error.URLError as exc:
            last = ApiError(f"{method} {url} -> unreachable: {exc.reason}")
            delay = _sleep_for(attempt, 1.0, 30.0)

        if attempt == MAX_HTTP_ATTEMPTS - 1:
            break
        time.sleep(delay)

    raise last or ApiError(f"{method} {url} failed")


def submit(model: str, payload: dict) -> dict:
    """Start a generation. Returns the pending status body (has request_id)."""
    data = request("POST", f"{API_BASE}/{model.strip('/')}", payload)
    if not data.get("request_id"):
        raise ApiError(f"no request_id in submit response:\n{json.dumps(data, indent=2)[:2000]}")
    return data


def status(request_id: str, status_url: str | None = None) -> dict:
    return request("GET", status_url or f"{API_BASE}/requests/{request_id}")


def poll(
    submission: dict,
    timeout: int = 1800,
    initial_interval: float = 3.0,
    max_interval: float = 20.0,
    on_status: Callable[[str], None] | None = None,
) -> dict:
    """Poll to a terminal status, backing off between checks.

    Returns the completed body. Raises RequestFailed on a terminal failure and
    PollTimeout if the deadline passes while still pending.
    """
    request_id = submission["request_id"]
    status_url = submission.get("status_url")
    deadline = time.time() + timeout
    state = submission
    seen: str | None = None
    attempt = 0

    while True:
        current = str(state.get("status", "")).lower()
        if current != seen:
            if on_status:
                on_status(current)
            seen = current
            attempt = 0  # progress: restart the backoff ramp

        if current == COMPLETED:
            return state
        if current in FAILED:
            raise RequestFailed(f"request {request_id} {current}: {state.get('error') or 'no detail given'}")

        remaining = deadline - time.time()
        if remaining <= 0:
            raise PollTimeout(
                f"timed out after {timeout}s; request {request_id} last status {current!r}. "
                f"It may still finish - resume with: status {request_id}"
            )

        time.sleep(min(max_interval, initial_interval * (1.5**attempt), max(remaining, 0.1)))
        attempt += 1
        state = status(request_id, status_url)


def asset_url(state: dict) -> tuple[str, str]:
    """Return (field, url) for the first asset a completed request carries."""
    for field in ASSET_FIELDS:
        entry = state.get(field)
        if isinstance(entry, dict) and entry.get("url"):
            return field, entry["url"]
    raise ApiError(f"completed request carries no asset url:\n{json.dumps(state, indent=2)[:2000]}")


def download(url: str, dest: Path) -> Path:
    """Stream an asset to disk, writing to a temp file so a failure leaves no
    half-written result behind."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        with urllib.request.urlopen(url, timeout=300) as resp, tmp.open("wb") as fh:
            while chunk := resp.read(1 << 16):
                fh.write(chunk)
        tmp.replace(dest)
    finally:
        tmp.unlink(missing_ok=True)
    return dest
