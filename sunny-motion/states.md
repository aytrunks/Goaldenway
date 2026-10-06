# Motion plan: Sunny Pawn & Jewelry, 14 s loop, 1440×1440

Grid: 120 BPM, one beat every 0.5 s, 28 beats (7 bars). Beat numbers are b0–b27; bN = N × 0.5 s.
The shape is one element throughout. It changes size, radius and colour, and its content swaps with a short blur.
Text readable in frame ≥ 30 px tall (the camera zooms per state).

| # | State | Beats (time) | Shape | Content (verbatim) | Cursor | Hand-off to next (shared element) |
|---|---|---|---|---|---|---|
| 1 | **Shop Now pill** on the dark hero | b0–b2 (0.0–1.5 s) | Pill, sun-yellow `#FFD42A`, full radius | Above the pill: "BRIGHT DEALS. / HONEST SERVICE. / ALWAYS SUNNY." Pill: "Shop Now" | Glides in from bottom right; hovers at b1; presses at 1.42 s, releases on **b3** | The word **"Shop"** stays put while the pill grows: "Shop Now" → "Shop quality pre-owned…" |
| 2 | **Buy From Us** white card | b3–b10 (1.5–5.5 s), **4 s hold** (paragraph) | Card, white, radius ~70 | Cart icon, "Buy From Us", "Shop quality pre-owned items in-store or online. Every item is tested, ready to use, and new arrivals are posted daily." | Rests near the card; on b6 and b8, hover-nudges the icon (the yellow cart accent ticks on the beat); grabs the card at b9 and drags left; releases on **b11** | Card frame: white → yellow as it springs back from the drag |
| 3 | **300+** stat card | b11–b12 (5.5–6.5 s) | Card, sun-yellow, radius ~50 | "300+", "5-star / Google reviews" | Taps the number on **b13** | The big **digits** roll vertically: 300+ → 100% |
| 4 | **100%** stat card | b13–b14 (6.5–7.5 s) | Same card | "100%", "Satisfaction / guaranteed" | Moves toward where the stars will appear; taps on **b15** | The label shrinks into the **5 stars** row (the "5-star" idea carries over); yellow lightens to `#FDDF67` |
| 5 | **Testimonial** card | b15–b22 (7.5–11.5 s), **4 s hold** (quote) | Card, review-yellow, radius ~25 | "5 ★★★★★", "Jul 08, 2026", "The ONLY pawn shop I return to again and again. The customer service is outstanding and they have the best rates for pawns and purchases. I highly rec... More", avatar "M", "Ms87Dodge", Google G | Stars fill one per beat b15–b19; cursor hovers the author on b20; presses below the card and releases on **b23** | The card collapses into the **Read Reviews** pill (the real button under the carousel) |
| 6 | **Read Reviews** pill | b23 (11.5–12.0 s) | Pill, sun-yellow | "Read Reviews" | Click lands on b23 | The pill **stretches to full width** and goes ink `#1C1C1C` |
| 7 | **Bottom nav bar** | b24–b25 (12.0–13.0 s) | Bar, ink, small radius | 5 yellow icons + labels: Our Services, Shop Online, Home, About Us, Contact Us. Liquid indicator under the active icon slides Our Services → Home (leading edge on the stiffer spring) | Taps **Home**; press at 12.92 s, release on **b26** | Home icon tap: bar contracts back into the yellow pill |
| 8 | **Back to Shop Now** | b26–b27 (13.0–14.0 s) | Pill, sun-yellow | "Shop Now" + hero headline | Drifts back to its frame-0 position | Last frame = first frame (springs wrapped across the loop) |

## Background
- States 1 and 8: dimmed hero photo cropped from the screenshot, as on the site, or flat black `#000` if it looks soft at zoom. I'll decide from the contact sheet.
- States 2–7: the section backgrounds sampled from the site: `#EFF4D2` behind the service card, `#F9F9F9` behind the stats and testimonial, crossfading by beat. No gradients on UI chrome.

## Sound (no song)
Dry UI clicks only: presses, releases, a soft tick for each star and each digit roll. Mastered to −14 LUFS, true peak ≤ −1.5 dBTP.

## Left out
- Firearms cards (FFL Firearm Transfers, and firearms mentioned in What We Buy / Cash Loans)
- Brand logos (third-party trademarks; third logo also cut off)
- Hamburger menu (open state not captured)
- "How to Pay" and "Want A Faster Way?" (incomplete in the screenshots)
- Layaway and other yellow cards: no room in 14 s with 4 s paragraph holds. A 42 s version could include Layaway, Sell To Us, the About checklist and the hours card.
