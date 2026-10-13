# Sunny Pawn videos

Vertical (1080×1920) social videos for Facebook and Instagram, built with [Remotion](https://www.remotion.dev).

## Templates

| ID | Length | What it shows |
|---|---|---|
| `DealOfTheDay` | 8s | Logo, item, details, old price struck through, new price |
| `GuessThePrice` | 9s | Item, 3-2-1 countdown, price rolls up, "comment your guess" |

Sample data lives in `src/Root.tsx`. Put product photos in `public/` and pass the file name as `image`.

## Commands

```bash
npm install
npm run studio                      # live preview in the browser
npm run render -- DealOfTheDay out/deal.mp4 \
  --props='{"item":"Gold Chain","detail":"22 inch","price":899,"wasPrice":1200,"image":"chain.jpg","footer":"In store now · Sunny Pawn"}'
```

In Claude Code cloud sessions, add `--browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.

Fonts (Oswald, Inter) are bundled in `public/fonts` so renders work offline. Remotion is free for individuals and companies with up to 3 employees; larger companies need a company license.
