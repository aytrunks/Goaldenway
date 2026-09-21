"""Minimal client for the Higgsfield API.

Layers, so a new model is a data change rather than a code change:
    client  - auth, submit, polling lifecycle, retries, downloads
    schemas - published model schemas from schemas/, validation, cost estimates
    specs   - shot specs from shots/, directive expansion, fingerprinting
    ledger  - request ids on disk, for resuming and deduplicating

Stdlib only; no install step.
"""

from . import client, ledger, schemas, specs

__all__ = ["client", "ledger", "schemas", "specs"]
