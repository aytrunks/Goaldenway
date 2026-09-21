"""Model schemas, input validation, and cost estimation.

Schemas live as JSON files in ``schemas/`` rather than in code, so supporting a
new Higgsfield model is a matter of dropping in its published schema — no edits
here. Each file is ``{model, category, source, pricing, schema}``.

Validation is deliberately strict about ``additionalProperties: false``: these
models reject unknown keys outright, and catching that locally is free whereas
catching it at the API costs a round trip.
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"

# Short side in pixels for each documented resolution label.
SHORT_SIDE = {"480p": 480, "720p": 720, "1080p": 1080, "4k": 2160}


class SchemaError(Exception):
    pass


class UnknownModel(SchemaError):
    """No verified schema on disk for this model id."""


class ValidationError(SchemaError):
    def __init__(self, model: str, errors: list[str]) -> None:
        super().__init__(f"input does not match the schema for {model}:\n  - " + "\n  - ".join(errors))
        self.errors = errors


@lru_cache(maxsize=1)
def registry() -> dict[str, dict]:
    """Every schema file on disk, keyed by model id."""
    found = {}
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        doc = json.loads(path.read_text())
        if model := doc.get("model"):
            doc["_path"] = str(path)
            found[model] = doc
    return found


def get(model: str) -> dict:
    try:
        return registry()[model]
    except KeyError:
        known = "\n  ".join(sorted(registry())) or "(none)"
        raise UnknownModel(
            f"No verified schema for {model!r}.\n"
            f"Known models:\n  {known}\n"
            f"Add one by saving that model's published schema to {SCHEMA_DIR}/ as\n"
            '  {"model": "<model id>", "schema": {<its Input JSON Schema>}}\n'
            "Or pass --allow-unverified to submit without local validation."
        ) from None


def validate(model: str, payload: dict) -> None:
    """Check a payload against a model's published Input JSON Schema.

    Supports the subset those schemas actually use: type, required, enum,
    minimum/maximum, minLength, and additionalProperties.
    """
    schema = get(model)["schema"]
    props = schema.get("properties", {})
    errors: list[str] = []

    for key in schema.get("required", []):
        if payload.get(key) in (None, ""):
            errors.append(f"{key!r} is required")

    if schema.get("additionalProperties") is False:
        for key in sorted(set(payload) - set(props)):
            errors.append(f"{key!r} is not accepted by this model (additionalProperties: false)")

    types = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "object": dict, "array": list}
    for key, value in payload.items():
        rule = props.get(key)
        if rule is None or value is None:
            continue
        expected = types.get(rule.get("type", ""))
        # bool is a subclass of int; an integer field must not accept True.
        if expected and (not isinstance(value, expected) or (rule.get("type") == "integer" and isinstance(value, bool))):
            errors.append(f"{key!r} must be {rule['type']}, got {type(value).__name__}")
            continue
        if (allowed := rule.get("enum")) and value not in allowed:
            errors.append(f"{key}={value!r} is not one of {allowed}")
        if (lo := rule.get("minimum")) is not None and value < lo:
            errors.append(f"{key}={value} is below the minimum of {lo}")
        if (hi := rule.get("maximum")) is not None and value > hi:
            errors.append(f"{key}={value} is above the maximum of {hi}")
        if (ml := rule.get("minLength")) is not None and len(value) < ml:
            errors.append(f"{key!r} is shorter than the minimum length of {ml}")

    if errors:
        raise ValidationError(model, errors)


def defaults(model: str) -> dict:
    """Schema defaults, so cost estimates reflect what the API will actually do."""
    return {k: v["default"] for k, v in get(model)["schema"].get("properties", {}).items() if "default" in v}


def dimensions(resolution: str, aspect_ratio: str) -> tuple[int, int]:
    """Pixel dimensions for a resolution label and aspect ratio."""
    short = SHORT_SIDE.get(resolution.lower())
    if short is None:
        raise SchemaError(f"unknown resolution {resolution!r}")
    try:
        a, b = (float(n) for n in aspect_ratio.split(":"))
    except ValueError:
        raise SchemaError(f"unknown aspect ratio {aspect_ratio!r}") from None
    long = round(short * max(a, b) / min(a, b))
    return (long, short) if a >= b else (short, long)


def estimate_cost(model: str, payload: dict) -> tuple[int, float | None]:
    """Return (billable video tokens, estimated USD) for a payload.

    USD is None when the model's schema file carries no rate for that
    resolution, rather than guessing a price.
    """
    merged = defaults(model) | payload
    width, height = dimensions(merged.get("resolution", "720p"), merged.get("aspect_ratio", "16:9"))
    seconds = merged.get("duration", 5)
    tokens = math.ceil(seconds * width * height * 24 / 1024)
    rate = get(model).get("pricing", {}).get("per_1k_tokens", {}).get(merged.get("resolution", "720p"))
    return tokens, (tokens / 1000 * rate if rate is not None else None)
