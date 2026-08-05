# Goaldenway

Operational toolkit for the Boat House (Cape Coral, FL) Instagram marketing campaign — built from
the campaign brief to run the 7-day hook/format test and the 30-day rollout that follows it.

Brand: **Goaldenway** — your goal + the golden moment + the way to get there. Golden-hour light,
before/after transformation, Ryan Reynolds–style self-aware tone.

## Campaign Hub (mobile)

**[Open the campaign hub](https://claude.ai/code/artifact/31d47080-873c-4742-90af-e4295aeb0c8e)** —
a phone-first web app for daily use: today's plan, the full Hook Bank (copy-to-clipboard), ready
captions, and a posting checklist that resets each day. This is what you'd actually pull up dockside;
the xlsx tracker stays the system of record for the numbers.

## Contents

- `campaign/Goaldenway_Boathouse_Tracker.xlsx` — the working tracker. Fill in daily; everything
  else (Hook Bank aggregates, Format Comparison, Boss Presentation Summary) is a formula.
  Golden-hour color theme, with green/amber/red conditional formatting so hook and format status
  is readable at a glance.
  - **Instructions** tab — how to use it, legend, and assumptions made while building it
  - **Hook Bank** — 23 hooks (10 Value + 13 Reynolds-style, 8 of them new — see below),
    pre-loaded, with auto-rolled-up performance
  - **Daily Log** — one row per day for 30 days; Days 1-6 pre-planned from the brief, Day 7
    auto-picks the strongest performer, Days 8-30 are open for the Week 2+ pivot
  - **Format Comparison** — Format A vs. B vs. C, auto-averaged from the Daily Log
  - **Boss Presentation Summary** — the numbers (and an auto-written pitch line) for when the
    boss is back
- `campaign/CONTENT_CALENDAR.md` — the 7-day plan at a glance (format, hook, time, CTA per day)
- `campaign/CAPTIONS.md` — ready-to-post captions for Days 1-3, hook options for Days 4-7, and the
  8 new Reynolds-style hooks (R6-R13) with the ad technique behind each one
- `campaign/POSTING_CHECKLIST.md` — before/after-posting checklist from the brief
- `campaign/BOSS_PITCH_TEMPLATE.md` — how to present the results, pulling from the tracker

## New Reynolds-style hooks

The brief's 5 Reynolds-style hooks are all the same move (self-aware roast, then pivot). After
studying how Maximum Effort actually writes for Reynolds — Mint Mobile, Aviation Gin — 8 new hooks
(R6-R13) were added, each built on a distinct technique from those real campaigns: breaking the
fourth wall, self-deprecation redirected onto the product, roasting industry jargon, a sincere
setup with a comedic turn, absurd comparisons, mock-authority undercut by honesty, escalating
social guilt, and a deadpan low-pressure close. Full writeup with sourcing is in
`campaign/CAPTIONS.md`; all 13 are live in the tracker's Hook Bank and the campaign hub.

## Workflow

1. Check `campaign/CONTENT_CALENDAR.md` for the day's format/hook/time.
2. Grab the caption from `campaign/CAPTIONS.md`, post it.
3. Run through `campaign/POSTING_CHECKLIST.md` before and after posting.
4. 24 hours later, log the real numbers in the tracker's **Daily Log** tab.
5. At Day 6-7, use **Format Comparison** / **Hook Bank** to decide the pivot for Week 2+.
6. When the boss is back, present from `campaign/BOSS_PITCH_TEMPLATE.md` + the
   **Boss Presentation Summary** tab.

One thing worth flagging: the source brief has a minor internal inconsistency (1 post/day rotating
formats vs. a "3 posts per day" line) — this toolkit follows the detailed day-by-day rotation
since it's the specific, unambiguous version. See the tracker's Instructions tab for the full note.
