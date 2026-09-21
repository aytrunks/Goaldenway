# Goaldenway

Higgsfield video generation, driven by JSON shot specs.

## Setup

```sh
cp .env.example .env     # then fill in your key halves
set -a && . ./.env && set +a
```

Auth is one header, `Authorization: Key KEY_ID:KEY_SECRET`. **Both halves are
required** — a key id alone returns 401. Credentials are read from the
environment only: never from a spec file, never written to the ledger, never
committed. `.env` is gitignored.

| Variable | Purpose |
| --- | --- |
| `HF_API_KEY_ID` | Key id |
| `HF_API_KEY_SECRET` | Key secret |
| `HF_KEY` / `HF_CREDENTIALS` | Combined `KEY_ID:KEY_SECRET`, as the official SDKs take it |
| `HIGGSFIELD_API_BASE` | Override the API host (default `https://api.higgsfield.ai`) |
| `HIGGSFIELD_LEDGER` | Override the request ledger path |

No install step — stdlib only, Python 3.10+.

## Use

```sh
python3 scripts/render.py models                              # models with a verified schema
python3 scripts/render.py render shots/shot_2_carl_illegal.json --dry-run
python3 scripts/render.py render shots/shot_2_carl_illegal.json
python3 scripts/render.py list                                # every request made
python3 scripts/render.py status <request_id>                 # check or resume one
python3 tests/test_higgsfield.py                              # 38 checks, no network
```

`render` validates the payload locally, prints the token count and dollar cost,
asks before spending, submits, polls with backoff, and downloads the result to
`out/`.

| Flag | Effect |
| --- | --- |
| `--dry-run` | Print the request and cost, send nothing |
| `-y/--yes` | Skip the cost confirmation |
| `--force` | Resubmit even if an identical render exists |
| `--allow-unverified` | Submit a model that has no local schema |
| `--timeout` | Seconds to wait (default 1800) |

## How it fits together

| Module | Responsibility |
| --- | --- |
| `higgsfield/client.py` | Auth, submit, polling lifecycle, retries, downloads |
| `higgsfield/schemas.py` | Schema registry, validation, cost estimation |
| `higgsfield/specs.py` | Shot specs, `$image` expansion, fingerprinting |
| `higgsfield/ledger.py` | Request ids on disk, for resuming and deduplicating |
| `scripts/render.py` | CLI |

**Generation is asynchronous.** A submit returns a `request_id`; the video
arrives later. Every submission is written to `.higgsfield/ledger.json` with its
request id, model, status and output path, so an interrupted render resumes
instead of being paid for twice. Before submitting, the payload is fingerprinted
and checked against that ledger: an identical request already in flight is
resumed, and one already downloaded is reused. `--force` overrides both.

Polling backs off (3s → 20s, resetting on a status change) until a documented
terminal status — `completed`, `failed`, `nsfw`, or `canceled`. Rate limits
(429, honoring `Retry-After`) and transient 5xx are retried with jittered
backoff; other 4xx fail immediately with the server's response body.

## Adding a model

Schemas are data, not code. To support another Higgsfield model, save its
published Input JSON Schema to `schemas/`:

```json
{
  "model": "<model id>",
  "source": "<the llms.txt url it came from>",
  "pricing": { "per_1k_tokens": { "720p": 0.014 } },
  "schema": { "...": "the model's Input JSON Schema, verbatim" }
}
```

That's the whole change — validation, cost estimates and `models` pick it up
automatically. Verified so far:

| Model | Duration | Resolutions | Per 1k tokens |
| --- | --- | --- | --- |
| `bytedance/seedance-2.0/text-to-video` | 4–15s | 480p, 720p, 1080p, 4k | $0.014 (4k $0.008) |
| `bytedance/seedance-2.5/text-to-video` | 4–30s | 480p, 720p | $0.0214 |

A model with no schema on file is refused unless you pass `--allow-unverified`,
rather than being submitted against guessed field names.

### Image-to-video

Not yet wired up — that model's schema has not been verified, so no field names
for it are invented here. When you have its `llms.txt`, drop the schema in
`schemas/` as above and point a spec at it. The image itself is already handled:
`{"$image": "assets/frame.png"}` anywhere in a spec's `input` expands to a
base64 data URI at submit time, under whatever field name that model documents.

```json
"input": {
  "prompt": "...",
  "image_url": { "$image": "assets/shot_2_balcony_reference.png" }
}
```

## Shots

A spec is `{name, model, input}`; `input` goes to the API verbatim.

| Shot | Line | Spec |
| --- | --- | --- |
| Shot 2 — Carl drops into frame | "That's illegal in Southwest Florida." | [`shots/shot_2_carl_illegal.json`](shots/shot_2_carl_illegal.json) |

Two constraints shape shot 2, both from the published schema:

- **No `negative_prompt` field** (`additionalProperties: false`), so the
  don't-list — not scary, no roaring, no sharp teeth, no extra limbs or
  characters, no text, logos or UI, no layout changes — is written into the
  prompt itself.
- **Minimum duration is 4s**, over the 2s the brief asked for. Render 4 and trim:
  `ffmpeg -i out/shot_2_carl_illegal.mp4 -t 2 -c copy out/shot_2_2s.mp4`

## Note on sandboxed sessions

Claude Code web sessions reach the network through a policy-enforcing egress
proxy. If every Higgsfield host returns `403 Forbidden` on CONNECT, the domain
is not on the environment's allowlist — add `higgsfield.ai` to the environment's
network policy, or run from a machine with direct network access.
