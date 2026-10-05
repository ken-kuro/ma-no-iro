# Brief: the Ma no Iro design system (for Claude Design)

Attach `palette.json`, `SPEC.md`, `docs/story.md` and `docs/showcase.html` alongside this brief.

## Prompt to paste

> I'm building Ma no Iro (間の色, "the colour of the in-between", Ma for short), an open-source colour palette with two flavors: 黒紫 Kuromurasaki (night) and 白緑 Byakuroku (day). Its eight colours are four complementary pairs, each a scene where something takes a colour away (the leaf, the sky, the water, the ink), and all four cross at one grey. It is also a short guide to colour theory, so accuracy matters as much as looks. The palette is final and lives in `palette.json`; the rules are in `SPEC.md`. Please design the visual system for the project's identity and website: a wordmark and mark, a type scale, layout and spacing, the core components, and page designs for the home, palette, ports, port detail, specification and story pages, each in both flavors. Use only colours from `palette.json`, following SPEC sections 4 and 6.4. `docs/showcase.html` tells the story scene by scene today; keep its narrative order and its one big moment, the colour cube turning into the hexagon, but design the pages properly rather than copying its layout. Start with the identity and the home page, then show me the component set before designing the rest.

## What Ma no Iro is, in one paragraph

Every colour comes with the colour it takes away. A leaf takes the blue and red ends of sunlight, which together look purple, and returns green; the sky scatters blue out of sunlight and leaves the sun yellower; water absorbs red, so deep water looks cyan; ink takes almost all light and paper gives it back. Those eight colours are the corners of the colour cube and the terminal's eight. Opposite corners are complements, and the four lines between them cross at one grey: the in-between, 間, which is the palette's ground. Each pair has one physical anchor (555 nm, λ⁻⁴, 700 nm), its partner is solved on the far side of white, and no hue is chosen by eye. Green is at home in the day flavor and purple at night, and each flavor keeps a dot of the other's colour as its seed, spent only on the cursor, the current match and focus.

## Deliverables

1. **Identity.** A wordmark for "Ma no Iro" with 間の色, a short form "Ma" with 間, and a mark. The starting point is the cube seen down its grey axis: six colours in a hexagon around a grey centre. It must work at favicon size and in both flavors.
2. **Type.** A type scale for display, body, UI labels and code. Latin must support Vietnamese diacritics; CJK must cover 間の色, 黒紫, 白緑, 正色, 間色, 綠, 紫 and 碧. Suggested families: IBM Plex Sans with IBM Plex Sans JP, and IBM Plex Mono for code. Any change needs a reason. Do not use Inter.
3. **Layout.** Grid, spacing scale, and breakpoints down to a 360 px phone.
4. **Components.** Flavor switch (with a system option), scene index, the strictly-speaking note that closes every scene, swatch, token table row with copy action, spectrum figure (white light split into two complementary parts, drawn on a night panel), the colour cube with its turn control, the chromaticity diagram with the three anchors, code block, editor frame, diff frame, terminal frame, ANSI grid, callout, navigation, footer, port card, install instructions block.
5. **Pages.** Home, palette, ports index, a single port, specification, story. Each in both flavors, desktop and phone.
6. **Assets.** A README hero that shows both flavors side by side, or the hexagon, never one flavor alone (a night-only image reads as a purple theme); README banner for each flavor, social card (1200 × 630), favicon set, and a screenshot frame template that every port uses.
7. **Tokens.** The website's design tokens, named after `palette.json` roles (for example `--ma-base`, `--ma-home`, `--ma-seed`), so Claude Code can wire them to generated values.

## Rules the design must follow

- **Colours only from `palette.json`.** No new hex values, no tints made by eye. If a design needs a colour that is not there, flag it rather than inventing it.
- **The website wears the palette.** In dark mode the site is Kuromurasaki; in light mode it is Byakuroku.
- **Home and seed.** The home colour (`keyword` at night, `function` in the day) is for chrome and quiet emphasis: active navigation, buttons, badges. The seed is only for focus rings and the one thing the eye should land on. Do not use the seed decoratively.
- **Each colour where its scene puts it.** Illustrations of the leaf use the leaf's pair, the sky the sky's, and so on. Schematic figures are labelled schematic. Red and yellow appear in the interface only as errors, warnings and highlights.
- **Light is seen best in the dark.** Figures that show light (spectra, the cube, the diagram) sit on a night panel in both flavors.
- **Dose.** Large areas are grey. Accents appear in small areas. The bigger the shape, the lower its chroma.
- **Flat, except a mix.** No glows or colour shadows. A gradient is allowed only as SPEC R9 defines it: two stops that are partners (one pair, or two inks), interpolated in linear light, so a pair's mix passes through its grey.
- **Both flavors are first-class.** The day flavor gets the same care as the night.
- **Accessibility.** Body text at 4.5:1 or better. Focus is always visible. Nothing is conveyed by colour alone.

## Tone

Calm, precise and a little astonished by the physics. The design should feel observed, not decorated: numbers stated plainly, generous space, one bold moment per page. On the home page the bold moment is the cube turning into the mark.

Avoid: multi-hue gradient washes, identical rounded cards with soft shadows, all-caps labels over every heading, and neon-on-black styling, which is the obvious reading of purple and green and the one Ma no Iro exists to move away from.

## Content to design with

Use real content from `docs/story.md` and `SPEC.md`, not placeholder text, and keep every strictly-speaking note; do not shorten a claim in a way that drops its limit. The home page's thesis: "Every colour comes with the colour it takes away."

## Handoff

When the system is agreed, export tokens, component specifications and page designs in a form Claude Code can build from: token names mapped to `palette.json` roles, spacing and type values in rem, and each component's states (default, hover, active, focus, disabled) in both flavors.
