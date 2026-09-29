# Changelog

All notable changes to Ma no Iro 間の色 are recorded here. The version is the palette version in `palette.json` and `SPEC.md`.

Ports and the design system read colours from `palette.json` by token name, so every entry lists changed token values as old → new. Until 1.0, a minor version may change token values; a patch version never does. `SPEC.md` section 10 keeps the reasoning behind each decision.

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
