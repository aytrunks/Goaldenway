"""Shot specs: the JSON files under ``shots/`` that describe one generation.

A spec is ``{name, model, input}``. Everything under ``input`` is sent to the
API verbatim, so a model's fields are never hard-coded here.

One directive is expanded before sending. ``{"$image": "assets/frame.png"}``
becomes a base64 data URI, which lets an image-driven model take a local file
without the project needing to host it publicly. You choose the field name it
sits under, so adding image-to-video support never means guessing at one:

    "input": {
      "prompt": "...",
      "image_url": {"$image": "assets/shot_2_balcony_reference.png"}
    }
"""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class SpecError(Exception):
    pass


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def _expand(value, root: Path):
    """Recursively resolve $image directives against the project root."""
    if isinstance(value, dict):
        if set(value) == {"$image"}:
            path = Path(value["$image"])
            path = path if path.is_absolute() else root / path
            if not path.is_file():
                raise SpecError(f"$image file not found: {path}")
            return data_uri(path)
        return {k: _expand(v, root) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand(v, root) for v in value]
    return value


def load(path: Path, root: Path = ROOT) -> dict:
    """Read a shot spec and expand its directives."""
    try:
        spec = json.loads(Path(path).read_text())
    except json.JSONDecodeError as exc:
        raise SpecError(f"{path} is not valid JSON: {exc}") from None
    for key in ("model", "input"):
        if key not in spec:
            raise SpecError(f"{path} is missing required key {key!r}")
    if not isinstance(spec["input"], dict):
        raise SpecError(f"{path}: 'input' must be an object")
    spec.setdefault("name", Path(path).stem)
    spec["input"] = _expand(spec["input"], root)
    return spec


def fingerprint(model: str, payload: dict) -> str:
    """Stable hash of a submission, used to recognize a repeat of it."""
    blob = json.dumps({"model": model, "input": payload}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def summarize(payload: dict, limit: int = 96) -> dict:
    """Payload with long values shortened, safe to print or store."""
    out = {}
    for key, value in payload.items():
        if isinstance(value, str) and len(value) > limit:
            out[key] = f"{value[:limit]}... ({len(value)} chars)"
        else:
            out[key] = value
    return out
