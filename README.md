# Goaldenway

## Carl the alligator butler — shot renders

`scripts/higgsfield_render.py` submits a Higgsfield shot from a JSON spec, polls
the request to a terminal state and downloads the result. Stdlib only, no
`pip install`.

### Credentials

Auth is one header, `Authorization: Key KEY_ID:KEY_SECRET`. **Both halves are
required** — a bare key id returns 401.

```sh
export HF_KEY="KEY_ID:KEY_SECRET"
```

If you hold the halves separately, set `HIGGSFIELD_API_KEY` and
`HIGGSFIELD_API_SECRET` and the script joins them.

### Render

```sh
python3 scripts/higgsfield_render.py shots/shot_2_carl_illegal.json
# -> out/shot_2_carl_illegal.mp4
```

| Flag | Purpose |
| --- | --- |
| `--dry-run` | Print the endpoint and request body, then exit (no network, no credentials) |
| `-o/--out` | Output path |
| `--timeout` / `--interval` | Render wait budget and poll cadence |

`HIGGSFIELD_API_BASE` overrides the API host. On any API error the server's raw
response body is printed verbatim.

### Shots

| Shot | Line | Spec |
| --- | --- | --- |
| Shot 2 — Carl drops into frame | "That's illegal in Southwest Florida." | [`shots/shot_2_carl_illegal.json`](shots/shot_2_carl_illegal.json) |

A spec is `{name, model, input}`; everything under `input` is passed to the API
verbatim, so other models' fields work without touching the script. Reference
frames live in `assets/`.

### Working within the seedance-2.5 schema

The input schema is `additionalProperties: false`, so unknown keys are rejected.
Three consequences worth knowing:

- **No `negative_prompt` field.** Anything the shot must avoid has to be written
  into the prompt text itself.
- **Minimum duration is 4s.** For a 2s cut, render 4s and trim:
  `ffmpeg -i out/shot_2_carl_illegal.mp4 -t 2 -c copy out/shot_2_2s.mp4`
- **`.../text-to-video` takes no image.** The reference frame can't be attached
  to this model id; swap in an image-to-video model id to use one.

Cost is metered on `ceil(seconds × width × height × 24 / 1024)` tokens at
$0.0214/1k for 480p and 720p — about **$1.85** for 4s of 720p 9:16.

### Note on sandboxed sessions

Claude Code web sessions reach the network through a policy-enforcing egress
proxy. If every Higgsfield host returns `403 Forbidden` on CONNECT, the domain
is not on the environment's allowlist — add `higgsfield.ai` to the environment's
network policy, or run the script from a machine with direct network access.
