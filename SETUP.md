# Animated profile cards

Run `python render_cards.py` for animated SVGs or `STATIC=1 python render_cards.py` for still screenshot previews.

Edit `profile.json` for your brand colours, font families, portrait, three linked tiles and featured repositories. The starter palette is an interpretation of the portfolio: near-black, warm white and vivid lime. Exact computed CSS/font data was not exposed by the site reader, so verify exact values in browser DevTools before treating this as pixel-perfect.

For embedded custom fonts, install `python -m pip install fonttools brotli`, add licensed TTF/OTF files, and add entries to `fonts.files`, e.g. `{"path":"assets/font.ttf","family":"Your Font","weight":400}`. The renderer subsets glyphs using pyftsubset, converts to WOFF and embeds base64 data URIs.

The scheduled GitHub Action fetches the GraphQL contribution calendar daily, renders the cards and commits the generated SVGs. Enable Actions and workflow write permissions in the profile repository.

Copy `README.profile-snippet.md` into `D3vi7x7/D3vi7x7/README.md`. Verify the featured repository URLs and descriptions before publishing.
