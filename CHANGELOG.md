# Changelog

All notable changes to Ma no Iro 間の色 are recorded here. The version is the palette version in `palette.json` and `SPEC.md`.

Ports and the design system read colours from `palette.json` by token name, so every entry lists changed token values as old → new. Until 1.0, a minor version may change token values; a patch version never does. `SPEC.md` section 10 keeps the reasoning behind each decision.

## [0.4.1] - 2026-09-30

No token value changed.

### Changed

- **Showcase, as the base for the landing page.**
  - A new "At a glance" scene after the title shows both flavors in an editor.
  - The anchors scene is headed "Three anchors, and the ink" and says what each anchor is: the peak of daylight vision, the law of scattering, the end of the visible spectrum.
  - A footer states the version, the licence and where the values live.
- SPEC section 3: the c540 and c550 hues in the anchor table are corrected from 332.4 and 326.4 to 332.5 and 326.5, as `derive.py` solves them.
- Licence holder: ken-kuro.

### Removed

- **The anchor slider.** It moved the green anchor and re-solved the purple, which made a fixed palette look adjustable and made 555 nm, a measured peak of vision, look like an arbitrary pick. The chart is now static.

## [0.4.0] - 2026-09-29

### Changed

- **Day-flavor types stand apart from comments.** For protanopes, `type` was ΔE 0.009 from `muted` (comments), effectively one colour. The sRGB gamut caps dark cyan near chroma 0.076, so the fix is lightness: the pair is now 0.039 apart, and the day flavor's weak pairs fall from five to two.
  - Byakuroku `type`: `#016b66` → `#07625e` (L 0.475 → 0.45)
  - Byakuroku `subtle`: `#525252` → `#424242` (L 0.44 → 0.38)
- **Only the seed is vivid (R7).** Night red had the seed's chroma.
  - Kuromurasaki `red`: `#fa5573` → `#ed647a` (C 0.20 → 0.17), and ANSI 1 red with it
  - Derived from it: `diff_delete` `#321f20` → `#302021`, `diff_delete_strong` `#4d282c` → `#4a2a2e`, `error_bg` `#2c1d1e` → `#2a1d1e`
- **ANSI brights are a visible step.** The bright rung grew from 0.06 to 0.08 lightness; most pairs were only ΔE 0.06 apart and are now 0.078 or more.
  - Kuromurasaki brights: red `#ff7b8c` → `#fe8897`, green `#b6eda6` → `#bdf3ac`, yellow `#fff4ad` → `#fff7c3`, blue `#98b5fe` → `#a1bcff`, magenta `#df8ced` → `#e692f4`, cyan `#7df6ee` → `#84fcf4`
  - Byakuroku brights: red `#860029` → `#7d0025`, green `#1a4301` → `#173d01`, blue `#0d4da8` → `#0446a2`, magenta `#63006f` → `#5c0166`, cyan `#036460` → `#045e5a`
  - Byakuroku ANSI 7 white: `#dfdfdf` (`overlay`) → `#a4a4a4` (`dim`); ANSI 15 bright white: `#ededed` (`mantle`) → `#dfdfdf` (`overlay`). Text printed in white was 1.23:1 on the ground and is now 2.31:1.

### Added

- Policy check: every ANSI bright must be at least 0.07 from its normal in Oklab.
- Policy check: no colour may have as much chroma as `seed` (R7).
- `samples/`: one file per language and format that ports are checked against.
- MIT licence.

## [0.3.0] - 2026-09-29

### Changed

- **Selection is a clear grey step.** `hl_high` was 0.03 OKLCH lightness from the border grey (`overlay`) in Kuromurasaki and 0.01 in Byakuroku, so a selection was easy to miss. It stays pure grey.
  - Kuromurasaki `hl_high`: `#2e2e2e` → `#383838` (L 0.30 → 0.34)
  - Byakuroku `hl_high`: `#dcdcdc` → `#d1d1d1` (L 0.895 → 0.86)
  - Their `alpha.hex8` equivalents change to match.
- **The seed is no longer an ANSI colour.** Bright green in Kuromurasaki and bright magenta in Byakuroku used to be the seed, so programs printed the cursor colour everywhere. Both now step one rung like the other brights.
  - Kuromurasaki ANSI 10 bright green: `#98fc70` (`seed`) → `#b6eda6` (`function` +1 rung, chroma capped at 0.11)
  - Byakuroku ANSI 13 bright magenta: `#90039f` (`seed`) → `#63006f` (`keyword` +1 rung)
- **Anchors are described as reference points.** The README, SPEC section 3 and `tools/derive.py` no longer say each pair has a physical anchor. 555 nm and 700 nm belong to the eye and the standard observer and were chosen for the leaf and the water; only λ⁻⁴ is the physics of its own scene. No colour changed.
- **Lead with both flavors.** The README and the design brief say to open with both flavors side by side, or the hexagon, never Kuromurasaki alone, whose purple chrome would read as a purple theme.

### Added

- Policy check: every ANSI colour must be at least 0.07 from `seed` in Oklab (SPEC section 7).
- Policy check: `hl_high` must differ from `overlay` and `hl_med` by at least 0.04 in OKLCH lightness (SPEC section 7).
- This changelog.

## [0.2.0]

Recorded before the repository existed; undated.

### Changed

- **Four pairs.** Every colour is one half of a complementary pair, and the eight are the terminal's eight. Red and cyan are anchored at 700 nm, blue and yellow at λ⁻⁴.
- **Selection is grey.** Highlights moved from the home colour to grey steps of the ground, so code under them keeps its colour and diffs have only one green.
- **The ink, not the night.** The fourth scene became the ink; the flavors are still night and day.
- **Home colour is chrome.** Syntax is identical in both flavors; the flip lives in the chrome and the seed.
- **Name.** Ma became Ma no Iro.

## [0.1.0]

Recorded before the repository existed; undated.

### Added

- One pair: green at 557.7 nm, then 555 nm, and its complementary purple. Red, yellow, blue and cyan were hand-set conventions.
- The official 1 nm CIE 1931 standard observer table, replacing an analytic approximation.
- Two flavors, Kuromurasaki and Byakuroku.
