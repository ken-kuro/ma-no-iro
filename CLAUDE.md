# Ma no Iro 間の色: working notes for Claude

Ma no Iro (Ma for short, slug `ma-no-iro`) is an open-source colour palette with two flavors, Kuromurasaki (night) and Byakuroku (day). Its eight colours are four complementary pairs, each anchored by one spectrum and all crossing at one grey, the in-between: the leaf (green and purple, 555 nm), the sky (blue and yellow, λ⁻⁴), the water (cyan and red, 700 nm) and the ink (black and white). This repository holds the palette, its specification, the ports that apply it to software, and the website.

## Sources of truth

1. `palette.json` is the only place colours live. It is generated; never edit it by hand.
2. `tools/derive.py` generates `palette.json` plus the generated regions in `SPEC.md`, `README.md` and `docs/showcase.html`, and enforces the accessibility policy. `tools/cie1931.py` holds the CIE 1931 standard observer table it uses.
3. `SPEC.md` is normative: the rules (section 4), the role map (section 6), the accessibility policy (section 7) and port requirements (section 8).
4. `docs/story.md` is the explanatory voice. `docs/showcase.html` is the story told scene by scene and the visual reference for how the palette looks in use.

If a request conflicts with `SPEC.md`, say so and ask before doing it.

## Commands

```sh
python3 tools/derive.py            # summary and accessibility report
python3 tools/derive.py --write    # regenerate palette.json and every generated region
python3 tools/derive.py --check    # must pass before any commit that touches colour
```

This repository is the base for the Ma no Iro design system, which reads tokens from `palette.json` by name. Any change to a token value, a token name or the ANSI map bumps `VERSION` in `tools/derive.py` and gets a `CHANGELOG.md` entry listing old → new hex.

## Rules that are easy to break

- Never introduce a hex value that is not in `palette.json`. Ports read colours through templates.
- Never raise chroma or tint a neutral or a highlight. See SPEC R5 and R7.
- Ports are flat. Elsewhere a gradient is only a two-stop mix of partners (one pair, or two inks) in linear light. See SPEC R9.
- Code uses `keyword`, `function`, `string`, `type`, `special` and the neutrals. `red` and `yellow` never colour code; they are for errors, deletions, warnings and search. See SPEC R4.
- Green colours only functions and added lines. See SPEC R6.
- Selection, current line and word highlights are the grey `hl_*` tokens, never an accent.
- The seed (`seed`) is only for the cursor, the current search match and focus.
- `home` is `keyword` in Kuromurasaki and `function` in Byakuroku. It marks chrome, not code.
- Use `yellow` for signals and the search wash, and `yellow_text` for anything read as text, including ANSI yellow.
- Where a target needs translucent highlights, use `alpha.hex8`; the opaque `hex` otherwise.
- Every port ships both flavors, named `Ma no Iro Kuromurasaki` and `Ma no Iro Byakuroku`, ids `ma-no-iro-kuromurasaki` and `ma-no-iro-byakuroku`.
- Unknown tokens fall back to `text`. Missing italics drop the style, never swap in a colour.

## Layout

```
palette.json            generated palette, both flavors
LICENSE                 MIT
CHANGELOG.md            what changed per palette version, old → new hex
SPEC.md                 specification
tools/derive.py         derivation and policy check
tools/cie1931.py        CIE 1931 standard observer, 1 nm
samples/                files every port is checked against
docs/story.md           long-form explanation: the four exchanges
docs/showcase.html      the story as a scene-by-scene page
briefs/                 briefs for Claude Design and Claude Code
design/                 the design system, built on palette.json (to be built)
ports/<target>/         one directory per port (to be built)
site/                   the website (to be built)
```

## Writing

Keep the two flavors in balance. Any story, image or correspondence added about one flavor needs its counterpart in the other; if Byakuroku has no honest counterpart, leave it out for Kuromurasaki too.


Sentence case. Plain verbs. Lead with the exchange (the leaf, the sky, the water, the ink), then the number, then the limit. Never present a model as nature, a correspondence as a proof, or a design choice as a law; SPEC section 2 lists the limits of every claim. Say "purple", "green", "blue", "yellow", "cyan" and "red", not "violet", "lavender", "lime" or "teal". Ma no Iro is four pairs around a grey, not a purple theme. Use the full name on first mention and in titles; Ma is fine after that. Japanese names keep their characters on first use: 間の色 Ma no Iro, 黒紫 Kuromurasaki, 白緑 Byakuroku.

## Open decisions (ask before assuming)

- Claiming the `ma-no-iro` names. As of 2026-09-29 none was taken: the GitHub org, the npm package and scope, the VS Code Marketplace publisher, the Open VSX namespace, the JetBrains Marketplace, PyPI, crates.io, ma-no-iro.com and manoiro.com.
- Hosting for the website.
