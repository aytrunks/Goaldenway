# Video Content Creator Tools

Automated video analysis and caption generation for boat detailing content.

## What These Do

**`video-analyzer.js`** — Analyzes raw boat detail videos and generates an edit plan:
- Extracts frames and uses AI to identify key moments
- Detects before/after transitions automatically
- Suggests cut points and structure
- Outputs a JSON manifest with timestamps and recommendations

**`video-caption-generator.js`** — Generates three ready-to-post captions from the analysis:
- Long-form (1:00–1:35) for Instagram Reels/YouTube Shorts
- Short-form (7–18s) for TikTok/Instagram Reels
- Carousel (3-5 slides) for static posts

Together: **Raw video → Edit plan + timestamps → 3 polished captions → Copy to CapCut/Premiere/DaVinci**

---

## Setup

### Prerequisites

1. **ffmpeg** (for frame extraction)
   ```bash
   # Mac
   brew install ffmpeg

   # Linux
   sudo apt install ffmpeg

   # Windows
   choco install ffmpeg
   ```

2. **Node.js** (v16+)
   ```bash
   node --version  # Should be v16 or higher
   ```

3. **Anthropic API key**
   - Get one free at https://console.anthropic.com
   - Set environment variable: `export ANTHROPIC_API_KEY=sk-ant-...`

### Install Dependencies

```bash
cd /home/user/Goaldenway
npm install @anthropic-ai/sdk
```

---

## Usage

### Step 1: Analyze Video

```bash
node video-analyzer.js boat-detail.mp4
```

**Output:** 
- `boat-detail_edit-plan.json` — Edit timeline with key moments, timestamps, structure
- Prints a summary showing:
  - Detected before/after points
  - Hero moments (best shots)
  - Recommended cuts
  - Suggested hook

### Step 2: Generate Captions

```bash
node video-caption-generator.js boat-detail_edit-plan.json
```

**Output:**
- `boat-detail_captions.json` — Three captions ready to copy
  - Long-form (full detail process)
  - Short-form (7-18s quick cut)
  - Carousel (3-5 slides)

### Step 3: Edit in Your Tool

Open `boat-detail_edit-plan.json` and use timestamps in **CapCut**, **Adobe Premiere**, or **DaVinci Resolve**:

**CapCut:**
1. Import video
2. Use `keyFrames` timestamps to mark cut points
3. Copy caption from `boat-detail_captions.json`
4. Export 3 versions (long/short/carousel)

**Premiere/DaVinci:**
1. Create markers at the timestamps
2. Use `beforeAfterPoints` to find transition moments
3. Paste captions onto text layers

---

## Example Workflow

```bash
# 1. Analyze a video
node video-analyzer.js my-boat-detail.mp4

# 2. Check the timestamps
cat my-boat-detail_edit-plan.json | jq '.editInstructions.keyFrames'

# 3. Generate captions
node video-caption-generator.js my-boat-detail_edit-plan.json

# 4. Copy captions
cat my-boat-detail_captions.json | jq '.formats.shortForm.text'

# 5. Use timestamps in CapCut/Premiere (manual editing)
# 6. Post to Instagram/TikTok/Facebook
```

---

## What the Analyzer Detects

- **Before/After transitions** — Dirty → Clean states
- **Key moments** — Water spray, scrubbing, detail work, finished shine
- **Video structure** — Problem setup, solution showcase, before/after reveal
- **Importance scores** — Which frames matter most for social

## What the Caption Generator Creates

All captions follow your Ryan Reynolds brand:
- Self-aware hook opening
- Description of the transformation
- CTA: "The Boat House Cape Coral. 📍 DM me"
- Optimized for each platform (length, tone, pacing)

---

## Limitations

- Video analysis is sampling-based (checks ~10% of frames to save API cost)
- Requires good lighting in original video (darker videos = less accurate analysis)
- Manual editing in CapCut/Premiere still needed (this gives you the *plan*, not the finished video)
- Each video costs ~$0.03 in API calls (Sonnet 3.5)

---

## Troubleshooting

**ffmpeg not found:**
```bash
which ffmpeg
# If empty, install it (see Setup section)
```

**API key issues:**
```bash
echo $ANTHROPIC_API_KEY
# Should show sk-ant-... (not empty)
```

**Frames not extracted:**
- Check video format (MP4/MOV/WebM supported)
- Check file permissions: `ls -la video.mp4`
- Check disk space: `df -h`

**Caption generation fails:**
- Verify API key is valid
- Check rate limits (free tier: 10 requests/minute)
- Wait 60s and retry

---

## Advanced: Batch Process Multiple Videos

```bash
#!/bin/bash
for video in *.mp4; do
  echo "Processing $video..."
  node video-analyzer.js "$video"
  node video-caption-generator.js "${video%.mp4}_edit-plan.json"
done
```

Save as `batch-process.sh`, then:
```bash
chmod +x batch-process.sh
./batch-process.sh
```

---

## Integration with Campaign Hub

Use captions from these tools in the campaign hub:
1. Generate captions here
2. Copy to campaign hub's manual caption input
3. Or paste into CapCut → export → upload

---

## Next: Full Automation?

These tools handle the *analysis* and *caption* parts. For full automation (video editing + effects + export), you'd need:
- **CapCut API** (not public yet)
- **Runway ML** or **Synthesia** (paid, ~$30-50/month)
- **Descript** (AI editing, ~$20/month)

For now: **Analysis + Captions (free/cheap) → Manual edit in CapCut (free) → Post**

This workflow takes ~15-20 min per video (vs. 45+ min without these tools).

---

## Questions?

Stuck? Check:
- `node video-analyzer.js` (no args) — shows usage
- `echo $ANTHROPIC_API_KEY` — confirms key is set
- `ffmpeg -version` — confirms ffmpeg installed
