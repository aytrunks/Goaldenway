# Inventory: sunnypawnandjewelry.com

Source: 12 iPhone screenshots (1320×2868, mobile layout) supplied on 2026-10-06. The live site is blocked by this environment's network policy, so nothing here comes from the DOM or CSS. Copy is in `copy.json`.

## Colours (median of 5×5 px samples from the screenshots)

| Token | Hex | Where sampled |
|---|---|---|
| sun-yellow | `#FFD42A` | Shop Now pill, yellow service cards, stat cards, Read Reviews pill, About underline |
| nav-icon-yellow | `#FFD52B` | Bottom nav icons (same colour, within rounding) |
| review-yellow | `#FDDF67` | Testimonial card |
| review-ink | `#3D3619` | Stars, avatar circle |
| ink | `#1C1C1C` | Learn More buttons, bottom nav bar |
| black | `#000000` | Header, About section, footer |
| footer-card | `#0F0F0F` | Hours card |
| services-bg | `#EFF4D2` | Pale green page background behind cards |
| steps-bg | `#FDFCE5` → `#FEE165` | "How to Pay" section background (vertical fade) |
| white | `#FFFFFF` | White service cards |
| light-bg | `#F9F9F9` | Brands / stats / testimonials background |

## Fonts
- Headings and UI: a geometric sans that **visually matches Plus Jakarta Sans** (bold headings, medium buttons). Not confirmed, because the CSS isn't reachable.
- Testimonial widget: a separate system/Roboto-style sans (Google reviews embed).
- Logo: custom artwork (condensed "PAWN" with a sun). I'll crop it from the screenshot rather than redraw it.

## Components

| # | Component | Specs (approx., mobile px ÷ 1.43) | Real copy | Interaction seen | How the shape becomes it |
|---|---|---|---|---|---|
| 1 | Hero CTA pill | ~350×90, fully rounded, sun-yellow, ink text | Shop Now | Tap target | The shape at rest: a pill |
| 2 | White service card | ~750×410, radius ~70, white, line icon with yellow accent | Cash Loans / Sell To Us / Buy From Us | None visible (static) | Pill grows, radius drops, yellow → white |
| 3 | Yellow service card | ~670×410, radius ~40, sun-yellow, dark pill button inside | What We Buy, Pawn Loans Made Easy, Get a Free Online Quote, Layaway, Why Choose Us? | Learn More / Get A Quote / Read Reviews buttons | Card recolours; the inner dark button is a second element |
| 4 | Stat card | ~810×360, radius ~50, sun-yellow, huge number | 300+ / 5-star Google reviews; 100% / Satisfaction guaranteed | None | Card with big digits: digits can roll 300+ → 100% |
| 5 | Testimonial card | ~790×400, radius ~25, review-yellow | 5 ★★★★★, Jul 08, 2026, quote, Ms87Dodge | Carousel with pagination (page 9 of 9 shown), "More" link | Card lightens; stars carry over from "5-star" |
| 6 | Read Reviews pill | ~405×90, fully rounded, sun-yellow | Read Reviews | Tap target | Card collapses back into a pill |
| 7 | Section underline | ~200×12 bar, ink (Brands/Testimonies) or yellow (About) | none | **Animates**: grows from a small square to a bar when scrolled into view (screens 06 vs 07) | Real site motion: a good bridge element |
| 8 | Bottom nav bar | full width ×190, ink, 5 yellow icons + white labels | Our Services, Shop Online, Home, About Us, Contact Us | Tap targets | Pill stretches to full width and goes ink |
| 9 | Brand logo carousel | Logos slide horizontally (screens 06→07 shifted ~60px) | HUBLOT, BVLGARI (third logo cut off) | Auto-scroll | Not used (third-party trademarks) |
| 10 | Hours card | ~835×410, radius ~20, #0F0F0F with border | Phone, Facebook, hours | None | Possible end card |
| 11 | Hamburger menu | Yellow icon, top right | not captured | Opens a menu (state not screenshotted) | Not used: open state missing |

## Flags
- **Numbers kept:** "300+", "100%", "20% down", "4 months" are business claims printed on the site, not sample data. They appear as written.
- **Possible site bug:** the footer's About Us column lists "About Us" twice. I won't show that column.
- **Missing:** the hamburger menu's open state, the full "How to Pay Your Loan or…" heading and its first step, the content under "Want A Faster Way?", the third brand logo, and the full review text behind "More". None of these will be shown.
- **Firearms** are mentioned in several cards. They're kept out of the video, per the earlier advice to keep guns off the main social account.
- **Hero background** is a photo only available at screenshot resolution (~1320 px wide). It works as a dimmed backdrop but may look soft at 1440×1440 zoom.
- **Mobile layout only.** Desktop sizes aren't known, so components are built at the mobile proportions shown and scaled up by the camera.
