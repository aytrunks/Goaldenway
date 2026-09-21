# Goaldenway

## Carl the alligator butler — shot renders

`scripts/higgsfield_i2v.py` renders a Higgsfield image-to-video shot from a JSON
spec, polls the job to completion and downloads the `.mp4`.

### Credentials

Higgsfield authenticates with a **pair** of values — a key on its own returns 401:

```sh
export HIGGSFIELD_API_KEY=...     # sent as the hf-api-key header
export HIGGSFIELD_API_SECRET=...  # sent as the hf-secret header
```

### Render

```sh
python3 scripts/higgsfield_i2v.py shots/shot_2_carl_illegal.json -o out/shot_2.mp4
```

Stdlib only — no `pip install`. Useful flags:

| Flag | Purpose |
| --- | --- |
| `--print-payload` | Dump the request body and exit (no network, no credentials needed) |
| `-i/--image` | Override the shot's reference frame |
| `--timeout` / `--interval` | Render wait budget and poll cadence |

If Higgsfield changes its routes, override them without touching the script:
`HIGGSFIELD_API_BASE`, `HIGGSFIELD_I2V_PATH`, `HIGGSFIELD_JOBSET_PATH`. On any
API error the server's raw response body is printed verbatim — that body is the
authority on what the API expects.

### Shots

| Shot | Line | Spec |
| --- | --- | --- |
| Shot 2 — Carl drops into frame | "That's illegal in Southwest Florida." | [`shots/shot_2_carl_illegal.json`](shots/shot_2_carl_illegal.json) |

Each spec carries the prompt, negative prompt, reference frame, model
(`seedance-2.5`), duration, resolution and aspect ratio. Reference frames live
in `assets/`.

### Note on sandboxed sessions

Claude Code web sessions reach the network through a policy-enforcing egress
proxy. If every Higgsfield host returns `403 Forbidden` on CONNECT, the domain
is not on the environment's allowlist — add `higgsfield.ai` to the environment's
network policy, or run the script from a machine with direct network access.
