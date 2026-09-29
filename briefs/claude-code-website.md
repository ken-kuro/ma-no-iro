# Brief: the Ma no Iro website (for Claude Code)

Run this in the repository root, after the design system from Claude Design is in `design/`. `CLAUDE.md` in the root has the working rules.

## Prompt to paste

> Build the Ma no Iro website in `site/`. Read `CLAUDE.md`, `SPEC.md` and `briefs/claude-code-website.md` first, and follow the design system in `design/`. Colours must come from `palette.json` at build time; do not type hex values. Start by proposing the stack and page structure, then build the home page and the palette page before the rest.

## Goal

A fast static site, published as `ma-no-iro`, that tells the story of the four exchanges, lets people inspect every colour, and gets them to a port for their tools.

## Stack

A static site generator that renders Markdown and ships no JavaScript by default, with small islands for the interactive parts. Astro fits this well. Propose an alternative if there is a good reason.

## Pages

- **Home.** The story in the order `docs/showcase.html` uses: the exchange, the leaf, the sky, the water, the ink, the eye, the interval, traditions, three anchors, two flavors, the palette in use. Every scene keeps its strictly-speaking note. Each scene links onward to the palette and ports.
- **Palette.** Both flavors as tables generated from `palette.json`, grouped by scene: token, role, hex, RGB, OKLCH, contrast, and the alpha equivalent where one exists. Copy buttons for each format. The ANSI table and derived washes.
- **Specification.** `SPEC.md` rendered, with a table of contents.
- **Story.** `docs/story.md` rendered.
- **Ports.** An index generated from `ports/*/port.json`, and one page per port built from that port's README, install instructions and screenshots.
- **Downloads.** `palette.json`, plus CSS custom properties, SCSS variables and a Tailwind preset generated from it.

## Interactive pieces

`docs/showcase.html` already implements rough versions of all of these; reuse its logic, not its markup.

- **Flavor switch.** System, Kuromurasaki, Byakuroku. It follows `prefers-color-scheme` by default and remembers the choice.
- **The cube.** The colour cube standing on its black corner, with the four complementary diagonals through the grey centre, and a control that turns it until you look straight down the grey axis and see the hexagon. Respect `prefers-reduced-motion`.
- **The three anchors.** The chromaticity diagram with 555 nm, 700 nm and λ⁻⁴, the D65 white point, and each complement on the far side of white. The diagram is static, with no slider: the anchors are fixed by the eye and by physics, and a control that moves them would suggest otherwise. Port the maths from `tools/derive.py` to TypeScript. At 555 nm it must reproduce `palette.json` exactly for every accent: purples and greens from 555 nm, cyans and reds from 700 nm, blues and yellows from λ⁻⁴.
- **Spectra.** White light split into the two parts of each exchange, drawn on a night panel. Label the leaf, water and ink figures as schematic; the sky's λ⁻⁴ is exact.
- **The eye.** The Stockman and Sharpe cone fundamentals with the CIE daylight luminosity curve and its 555 nm peak. Embed the data table; do not redraw the curves by hand.
- **Scene index.** A small index of scenes on the home page with keyboard movement between them.

## Requirements

- **Colour.** Generate CSS custom properties from `palette.json` at build time. A build step fails if any source file other than generated output contains a hex colour.
- **Rules.** Follow `SPEC.md` section 4 on the site itself: home colour for chrome, seed only for focus and the point of attention, grey grounds and highlights, no gradients.
- **Accessibility.** WCAG 2.2 AA. Visible focus everywhere. Full keyboard use of every interactive piece.
- **Performance.** No layout shift from fonts. Subset CJK fonts to the characters used.
- **Tests.** A parity test that runs `tools/derive.py` and compares the TypeScript derivation against it for every accent. Link checking. `python3 tools/derive.py --check` in CI.

## Out of scope for now

Hosting and domain (ask), analytics (none unless asked), a blog.
