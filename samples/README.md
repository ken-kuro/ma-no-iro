# Samples

Every port is checked against these files in both flavors. Each one covers the rows of `SPEC.md` section 6 that its language or format can express. If a role does not show the colour the role map gives it, the port is wrong. `palette.ts` is also the screenshot file, and `docs/showcase.html` embeds it.

| File | Covers (SPEC section) |
| --- | --- |
| `palette.ts` | Core syntax (6.1): keywords, storage, functions, types, type unions, strings, template interpolation, numbers, constants, regex, escapes, format specifiers, decorators, `this`, comments |
| `derive.py` | Syntax (6.1): docstrings, doc-comment tags, decorators, type parameters, `self`, f-string interpolation and format specifiers, word operators (`in`, `not`), built-ins, `None`, unused names |
| `flavor.rs` | Syntax (6.1): attributes, lifetimes, labels, macros, enum members, traits, `impl`, namespaces, hex numbers, doc comments |
| `scatter.go` | Syntax (6.1): packages, struct tags, `iota` constants, errors, methods, `defer`, `switch` |
| `swatch.tsx` | Markup (6.2): JSX tags, component tags, attributes, entities, embedded expressions; generics and `keyof` |
| `index.html` | Markup (6.2): tags, attributes, attribute values, named and numeric entities, comments, embedded script |
| `style.css` | Markup (6.2): at-rules, element, class, id and pseudo selectors, properties, values, units, custom properties, `!important`, escapes |
| `pairs.json` | Data (6.2): keys, strings, numbers, booleans, `null`, nesting, escapes |
| `port.toml` | Data (6.2): section headers, arrays of tables, inline tables, dates, literal strings |
| `workflow.yaml` | Data (6.2): keys, block scalars, anchors, aliases, `${{ }}` expressions, `~`, booleans |
| `notes.md` | Markdown (6.3): headings, emphasis, links, autolinks, quotes, lists, task lists, tables, strikethrough, code spans and fences, rules, images, footnotes, inline HTML |
| `change.diff` | Diff (6.5): file headers, hunk headers, added, deleted and context lines, a deleted file, the no-newline marker |
| `release.sh` | Syntax (6.1) in shell: variables, expansions, command substitution, ANSI escapes in `printf`, `case`, functions, redirections |
| `terminal.sh` | Terminal (6.7): run it inside the terminal. It prints all 16 ANSI colours as text and background, the SGR styles, and typical `git`, `ls`, test-runner and prompt output |

When the role map gains a row, add it to the sample that fits and to this table.
