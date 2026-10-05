# 間の色 Ma no Iro

*The colour of the interval.* Ma for short.

A two-flavor colour palette for code and terminals, and a short guide to how colour works: in light, in the eye, in the models we draw it with, and in the traditions that named it.

<!-- flavors:start -->
| | 黒紫 Kuromurasaki | 白緑 Byakuroku |
| --- | --- | --- |
| Ground | black `#141414` | white `#f7f7f7` |
| Home colour | purple `#cc79d9` | green `#27540f` |
| Seed (cursor, focus, current match) | green `#98fc70` | purple `#90039f` |
<!-- flavors:end -->

<!-- screenshots: assets/kuromurasaki.png and assets/byakuroku.png, side by side in one image, or the hexagon mark. Never lead with one flavor alone: Ma no Iro is four pairs around a grey, not a purple theme. -->

## The idea

Fire, stars and screens make colour by giving light off. Almost everything else makes it by taking light away, and what reaches your eye leans toward the complement of what was taken. Ma no Iro is four of those exchanges:

- **The leaf** takes the blue and red ends of sunlight, which together look purple, and gives back green. Anchored at 555 nm, the peak of daylight vision.
- **The sky** scatters blue out of sunlight and leaves the sun yellower. Anchored at the λ⁻⁴ scattering curve.
- **The water** absorbs red, so deep water looks cyan. Anchored at 700 nm, the end of red.
- **The ink** takes almost all light and paper gives it all back: black and white, the amount of light itself.

Those eight colours are the terminal's eight, named for the corners of the colour cube. They are not the corners themselves: each is solved from its anchor and sits a few degrees of hue from the corner it is named for. Opposite colours are complements, and all four lines between them cross at one grey. That grey is the interval, 間, and it is the ground everything in Ma no Iro sits on.

Each pair is named for its scene and anchored at one reference point: the eye's daylight peak for the leaf, the scattering curve for the sky, the end of red for the water. Only the sky's anchor is the physics of its own scene; the other two are choices, not measurements of a leaf or a lake. From each anchor the partner is solved on the far side of white, and every shade is solved the same way, so once the anchors are set no hue is picked by eye. You can rerun the derivation yourself.

Every explanation comes with its limits. The scenes are real physics told simply, the cube is a model of a screen, and the links to wuxing and yin-yang are correspondences, not proofs. `SPEC.md` section 2 states each one precisely.

## Principles

- **Two flavors.** 黒紫 Kuromurasaki is the night, with purple at home and a green seed. 白緑 Byakuroku is the day, with green at home and a purple seed. The seed marks only the cursor, the current match and focus.
- **Code in three scenes.** Keywords purple and functions green (the leaf), strings blue (the sky), types cyan (the water). Red and yellow are kept for errors, warnings and search.
- **A grey ground.** Neutrals, selections and highlights are pure grey, so code never changes colour under them.
- **One green in code.** An added line is the only green background you will see.
- **Colour by dose.** The larger the area, the lower the chroma. Only the cursor is vivid.
- **Numbers you can check.** Every colour comes out of `tools/derive.py`, which also enforces the contrast policy.

## Ports

Ports are in progress. See `SPEC.md` section 8 for what a port has to meet.

## Using the palette

`palette.json` holds both flavors with hex, RGB, OKLCH, contrast, role and scene for every colour, the 16 ANSI colours, derived diff and diagnostic washes, and translucent equivalents for editors that need them.

```sh
python3 tools/derive.py            # print the palette and the accessibility report
python3 tools/derive.py --write    # regenerate palette.json and every generated region
python3 tools/derive.py --check    # fail if anything is stale or breaks the policy
```

The script is plain Python with no dependencies.

## Documents

- `SPEC.md`: the specification. The idea, derivation, rules, palette, role map, accessibility policy, port requirements.
- `docs/story.md`: the story, written for people rather than ports, with the limits of every claim.
- `docs/showcase.html`: the story told scene by scene, with the palette in use.

## Contributing

Read `SPEC.md` before anything else. Never type a hex value by hand: ports are generated from `palette.json`, and `tools/derive.py --check` must pass.

## Licence

MIT. See `LICENSE`. If you fork Ma no Iro and change its colours, please give the fork a different name.
