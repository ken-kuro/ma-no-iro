# Brief: the Ma no Iro ports (for Claude Code)

Run this in the repository root. `CLAUDE.md` has the working rules; `SPEC.md` sections 4, 6 and 8 are the contract every port meets.

## Prompt to paste

> Build the port generator and the first ports for Ma no Iro (slug `ma-no-iro`). Read `CLAUDE.md`, `SPEC.md` (especially sections 4, 6 and 8) and `briefs/claude-code-ports.md` first. Every colour must come from `palette.json` through templates. Start with the generator and the VS Code, Neovim and Ghostty ports, show me screenshots of both flavors using `samples/palette.ts`, and only then continue down the list.

## Generator

- One command builds every port for both flavors: `python3 tools/build.py`, or `python3 tools/build.py vscode` for one.
- Packages and extensions are published as `ma-no-iro` (for example `ma-no-iro.nvim`, the VS Code extension `ma-no-iro`), with flavors `Ma no Iro Kuromurasaki` and `Ma no Iro Byakuroku`.
- Each port lives in `ports/<target>/` with a `port.json` (name, target, homepage, install summary, output paths), one or more templates, a `README.md`, an `INSTALL.md`, and its generated output committed.
- Templates receive one flavor object from `palette.json` plus helpers: `hex` with and without `#`, `rgb`, `rgba`, `hex8` for alpha equivalents, and the aliases `home`, `on_accent` and `cursor_text`.
- Jinja2 is a reasonable template engine. Keep dependencies to that.
- The generator fails if a template contains a literal hex colour.

## Samples

`samples/` holds one file per language and format; `samples/README.md` lists which rows of `SPEC.md` section 6 each covers. Check every port against all of them, and run `samples/terminal.sh` inside every terminal port. When the role map gains a row, extend the sample that fits.

## Order

1. **VS Code** (also covers Cursor, VSCodium and Open VSX). Full workbench colours plus TextMate token colours and semantic token rules. Use `alpha.hex8` for every background that sits over code: selection, word and find highlights, and the diff backgrounds.
2. **Neovim.** A Lua colorscheme with the built-in groups, tree-sitter captures (`@keyword`, `@function`, `@string`, `@type`, `@number`, `@constant`, `@string.escape`, `@variable.parameter`, `@variable.builtin`, `@attribute`, `@markup.*` and the rest), LSP semantic tokens and diagnostics, and integrations for gitsigns, telescope, nvim-cmp and blink.cmp, lualine and which-key. `CurSearch` uses a `seed` background with `base` text, since Neovim cannot draw a border on a match; `Search` uses `search`; `Visual` uses `hl_high`.
3. **Terminals:** Ghostty, Kitty, Alacritty, WezTerm, iTerm2, Windows Terminal, foot. ANSI 16, cursor and cursor text, selection, and pane or tab colours where supported.
4. **Editors:** Zed (also needs translucent highlights), Helix, JetBrains IDEs.
5. **Tools:** tmux, bat and delta (tmTheme), fzf, lazygit, btop, Starship, Yazi.
6. **Beyond code:** Obsidian, Firefox, Slack sidebar, Raycast. Ask before starting these.

## Per port

- Map every role in `SPEC.md` section 6 that the target supports, and list what could not be mapped in the port's README.
- Keep the scene rules: code only in `keyword`, `function`, `string`, `type`, `special` and the neutrals; `red` and `yellow` only for errors, deletions, warnings and search; highlights only in the grey `hl_*` tokens; green only for functions and additions.
- Apply the styling modifiers: italic for comments, parameters, instance words, type parameters and decorators; bold for Markdown headings and conflict markers; underline for links; strikethrough for deprecated.
- Follow the fallbacks in `SPEC.md` section 6.9.
- Screenshots: `samples/palette.ts`, both flavors, IBM Plex Mono at 14 px, the same window size for every port, framed with the template from the design system.
- Install instructions a new user can follow without guessing.

## Checks in CI

- `python3 tools/derive.py --check`
- `python3 tools/build.py` followed by `git diff --exit-code`, so generated files are always current.
- A scan that fails if any file under `ports/` contains a hex colour not present in `palette.json`.

## Publishing

Marketplace releases (VS Code Marketplace, Open VSX, JetBrains Marketplace) need the owner's accounts and tokens. Prepare the manifests and a release checklist; do not publish.
