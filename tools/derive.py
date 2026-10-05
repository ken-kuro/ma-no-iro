#!/usr/bin/env python3
"""
Ma no Iro (間の色) palette derivation.

Every colour in palette.json is produced by this file from a handful of
parameters. Nothing in the palette is hand-picked hex.

    python3 tools/derive.py            print a summary and the accessibility report
    python3 tools/derive.py --write    regenerate palette.json
    python3 tools/derive.py --check    fail if palette.json is stale or breaks policy

Pure Python 3.8+, no dependencies.

The story: every colour comes with the colour it takes away.

  A terminal has eight colours, the corners of the RGB cube. Opposite corners
  are complements, and all four lines between them cross at one grey: the
  in-between, 間, which is Ma no Iro's ground. Each pair is one scene in which
  something takes a colour away. The scene names the pair; the anchor is a
  reference spectrum chosen for it, not a measurement of the scene:

    leaf   green  dominant wavelength 555 nm, the peak of daylight vision
           purple its complement: the blue and red ends a leaf absorbs, seen together
    water  red    700 nm, the end of red (every longer wavelength looks the same)
           cyan   its complement: water absorbs red, so deep water looks cyan
    sky    blue   the lambda^-4 curve of scattering, also the glow of infinite heat
           yellow its complement: the sunlight the sky leaves behind
    ink    black and white: ink takes all of the light, paper gives it all back

  Every accent is solved the same way: at its lightness and chroma, the colour
  whose CIE xy chromaticity lies on the ray from D65 toward its anchor, or
  directly away from it for the complement. Once the anchors are chosen, no
  hue is set by eye.
  Lightness and chroma per role are the design parameters below; ANSI brights,
  washes and alpha equivalents follow by rule.
"""
import json
import math
import os
import sys
from itertools import combinations

VERSION = "0.4.1"
GREEN_NM = 555.0
BRIGHT_STEP = 0.08      # one ANSI rung of lightness, toward the text colour
BRIGHT_GREEN_C = 0.11   # dark bright green, softened so it never reads as the seed
D65 = (0.3127, 0.3290)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "palette.json")
SPEC = os.path.join(HERE, "..", "SPEC.md")
SHOWCASE = os.path.join(HERE, "..", "docs", "showcase.html")
SAMPLE = os.path.join(HERE, "..", "samples", "palette.ts")
README = os.path.join(HERE, "..", "README.md")

# ---------------------------------------------------------------- math

def mat(m, v):
    return [m[i][0] * v[0] + m[i][1] * v[1] + m[i][2] * v[2] for i in range(3)]

def inv3(m):
    a, b, c = m[0]; d, e, f = m[1]; g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]

def cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)

# Oklab (Ottosson 2020)
M1 = [[0.4122214708, 0.5363325363, 0.0514459929],
      [0.2119034982, 0.6806995451, 0.1073969566],
      [0.0883024619, 0.2817188376, 0.6299787005]]
M2 = [[0.2104542553, 0.7936177850, -0.0040720468],
      [1.9779984951, -2.4285922050, 0.4505937099],
      [0.0259040371, 0.7827717662, -0.8086757660]]
M1i, M2i = inv3(M1), inv3(M2)

def lin_to_lab(c):
    return mat(M2, [cbrt(x) for x in mat(M1, c)])

def lab_to_lin(lab):
    return mat(M1i, [x ** 3 for x in mat(M2i, lab)])

def lch_to_lab(L, C, h):
    return [L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))]

def lch_to_lin(L, C, h):
    return lab_to_lin(lch_to_lab(L, C, h))

def lab_to_lch(lab):
    L, a, b = lab
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

def in_gamut(c, eps=1e-4):
    return all(-eps <= x <= 1 + eps for x in c)

def encode(x):
    x = min(max(x, 0.0), 1.0)
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055

def decode(x):
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4

def to_hex(c):
    return "#" + "".join(f"{int(round(encode(x) * 255)):02x}" for x in c)

def to_rgb(c):
    return [int(round(encode(x) * 255)) for x in c]

def hex_to_lin(h):
    return [decode(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5)]

def luminance(c):
    c = [min(max(x, 0), 1) for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contrast(a, b):
    ya, yb = luminance(a), luminance(b)
    return (max(ya, yb) + 0.05) / (min(ya, yb) + 0.05)

# CIE 1931 2-degree standard observer, official 1 nm table
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cie1931 import cmf  # noqa: E402

RGB2XYZ = [[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]
XYZ2RGB = inv3(RGB2XYZ)

def xy_of_lin(c):
    X = mat(RGB2XYZ, c); s = sum(X)
    return X[0] / s, X[1] / s

def spectral_xy(l):
    X = cmf(l); s = sum(X)
    return X[0] / s, X[1] / s

def spectral_hue(l):
    return lab_to_lch(lin_to_lab(mat(XYZ2RGB, cmf(l))))[2]

def ray_hue(L, C, anchor_xy, away=False):
    """OKLCH hue of the colour at (L, C) whose chromaticity lies on the ray from
    D65 toward anchor_xy (or directly away from it when away=True)."""
    dx, dy = anchor_xy[0] - D65[0], anchor_xy[1] - D65[1]
    if away:
        dx, dy = -dx, -dy
    n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
    best = None
    for i in range(7200):  # hue 0.00 to 359.95 in steps of 0.05
        h = (5 * i) / 100
        x, y = xy_of_lin(lch_to_lin(L, C, h))
        vx, vy = x - D65[0], y - D65[1]
        if dx * vx + dy * vy <= 0:
            continue
        cross = abs(dx * vy - dy * vx)
        if best is None or cross < best[0]:
            best = (cross, i)
    return ((5 * best[1] + 5) // 10) / 10 % 360  # round half up to 0.1, in integers

# Blackbody chromaticity from Planck's law; T=None is the lambda^-4 limit, also the shape of Rayleigh scattering
C2_PLANCK = 1.438776877e-2  # second radiation constant, m*K

def blackbody_xy(T):
    """CIE xy of a blackbody at T kelvin; T=None is the infinite-temperature limit."""
    from cie1931 import CMF_1931_2DEG, START_NM
    X = [0.0, 0.0, 0.0]
    for i, row in enumerate(CMF_1931_2DEG):
        lam = (START_NM + i) * 1e-9
        B = lam ** -4 if T is None else lam ** -5 / (math.exp(C2_PLANCK / (lam * T)) - 1)
        for k in range(3):
            X[k] += B * row[k]
    s = sum(X)
    return X[0] / s, X[1] / s


# Colour vision deficiency, Machado, Oliveira and Fernandes (2009), severity 1.0, linear RGB
CVD = {
    "protanopia": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritanopia": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}

def delta_e(a, b, m=None):
    if m:
        a = [min(max(x, 0), 1) for x in mat(m, [min(max(x, 0), 1) for x in a])]
        b = [min(max(x, 0), 1) for x in mat(m, [min(max(x, 0), 1) for x in b])]
    A, B = lin_to_lab(a), lin_to_lab(b)
    return math.dist(A, B)

# ---------------------------------------------------------------- design parameters
# ("n", L)            neutral, chroma 0
# ("g", L, C)         green: hue of GREEN_NM
# ("p", L, C)         purple: hue solved as the complement of GREEN_NM at this L and C
# ("h", L, C, hue)    convention colour at a fixed conventional hue

FLAVORS = {
    "kuromurasaki": {
        "name": "Kuromurasaki", "jp": "黒紫", "reading": "くろむらさき",
        "appearance": "dark", "ground": "black", "home": "purple", "seed_hue": "green",
        "tokens": {
            "mantle": ("n", 0.165), "base": ("n", 0.19), "surface": ("n", 0.225), "overlay": ("n", 0.27),
            "dim": ("n", 0.45), "muted": ("n", 0.63), "subtle": ("n", 0.76), "text": ("n", 0.92),
            "hl_low": ("n", 0.215), "hl_med": ("n", 0.255), "hl_high": ("n", 0.34),
            "keyword": ("p", 0.70, 0.16), "special": ("p", 0.86, 0.075),
            "function": ("g", 0.83, 0.13), "seed": ("g", 0.90, 0.20),
            "string": ("b", 0.79, 0.095), "blue": ("b", 0.72, 0.13),
            "yellow": ("y", 0.90, 0.15), "yellow_text": ("y", 0.90, 0.15),
            "type": ("q", 0.68, 0.10), "cyan": ("q", 0.84, 0.11),
            "red": ("r", 0.68, 0.17),
        },
    },
    "byakuroku": {
        "name": "Byakuroku", "jp": "白緑", "reading": "びゃくろく",
        "appearance": "light", "ground": "white", "home": "green", "seed_hue": "purple",
        "tokens": {
            "mantle": ("n", 0.945), "base": ("n", 0.975), "surface": ("n", 0.995), "overlay": ("n", 0.905),
            "dim": ("n", 0.72), "muted": ("n", 0.515), "subtle": ("n", 0.38), "text": ("n", 0.25),
            "hl_low": ("n", 0.955), "hl_med": ("n", 0.93), "hl_high": ("n", 0.86),
            "keyword": ("p", 0.42, 0.17), "special": ("p", 0.54, 0.10),
            "function": ("g", 0.40, 0.11), "seed": ("p", 0.47, 0.22),
            "string": ("b", 0.49, 0.14), "blue": ("b", 0.50, 0.16),
            "yellow": ("y", 0.645, 0.135), "yellow_text": ("y", 0.525, 0.12),
            "type": ("q", 0.45, 0.09), "cyan": ("q", 0.515, 0.09),
            "red": ("r", 0.455, 0.19),
        },
    },
}

GROUPS = {
    "ink": ["mantle", "base", "surface", "overlay", "dim", "muted", "subtle", "text", "hl_low", "hl_med", "hl_high"],
    "leaf": ["keyword", "special", "function", "seed"],
    "water": ["type", "cyan", "red"],
    "sky": ["string", "blue", "yellow", "yellow_text"],
}

ROLES = {
    "mantle": "Recessed frames: sidebar, title bar, tab strip, status bar",
    "base": "Editor and terminal background",
    "surface": "Raised elements: popups, hovers, suggestions, inputs",
    "overlay": "Borders, dividers, indent guides",
    "dim": "Disabled text, whitespace marks, scrollbar thumb",
    "muted": "Comments, line numbers, placeholders",
    "subtle": "Punctuation, operators, secondary text",
    "text": "Identifiers, body text",
    "hl_low": "Current line",
    "hl_med": "Other occurrences of the word or selection, inactive selection",
    "hl_high": "Selection",
    "keyword": "Keywords, storage, control flow, markup tags; home colour of the dark flavor",
    "special": "Numbers, constants, escapes, regex, decorators",
    "function": "Function and method names, added lines; home colour of the light flavor",
    "seed": "Cursor, current search match, focus ring",
    "type": "Types, classes, interfaces, enums",
    "cyan": "Hints, symlinks, ANSI cyan",
    "red": "Errors, deletions, breakpoints",
    "string": "Strings, inline code",
    "blue": "Links, information, modified lines, directories",
    "yellow": "Warnings as a signal; the search highlighter",
    "yellow_text": "Warnings as text; ANSI yellow",
}

DERIVED = {
    "search": ("yellow", 0.20), "search_current": ("yellow", 0.26),
    "diff_add": ("function", 0.15), "diff_add_strong": ("function", 0.28),
    "diff_delete": ("red", 0.15), "diff_delete_strong": ("red", 0.28),
    "diff_change": ("blue", 0.13), "diff_change_strong": ("blue", 0.26),
    "error_bg": ("red", 0.12), "warning_bg": ("yellow", 0.12), "info_bg": ("cyan", 0.12),
    "debug_line": ("yellow", 0.14),
}
DERIVED_ROLES = {
    "search": "Search matches, like a highlighter",
    "search_current": "Current search match, under a seed outline",
    "diff_add": "Added line background; merge conflict, current",
    "diff_add_strong": "Added characters inside a changed line",
    "diff_delete": "Deleted line background",
    "diff_delete_strong": "Deleted characters inside a changed line",
    "diff_change": "Changed line background; merge conflict, incoming",
    "diff_change_strong": "Changed characters",
    "error_bg": "Background behind inline error text",
    "warning_bg": "Background behind inline warning text",
    "info_bg": "Background behind inline information text",
    "debug_line": "Line where the debugger is paused",
}

TEXT_ROLES = ["muted", "subtle", "text", "keyword", "special", "function", "type", "string", "red", "yellow_text", "blue", "cyan"]
SYNTAX = ["keyword", "special", "function", "type", "string"]
ON_ACCENT = ["keyword", "function", "seed", "red", "yellow_text", "blue", "cyan"]

# ---------------------------------------------------------------- derivation

GREEN_HUE = round(spectral_hue(GREEN_NM), 1)   # hue of the pure spectral colour, for reference
RED_NM = 700.0
ANCHORS = {
    "g": (spectral_xy(GREEN_NM), False),    # leaf: green, dominant wavelength 555 nm
    "p": (spectral_xy(GREEN_NM), True),     # leaf: purple, complementary wavelength 555 nm
    "r": (spectral_xy(RED_NM), False),      # water: red, 700 nm
    "q": (spectral_xy(RED_NM), True),       # water: cyan, complementary wavelength 700 nm
    "b": (blackbody_xy(None), False),       # sky: blue, the lambda^-4 spectrum
    "y": (blackbody_xy(None), True),        # sky: yellow, its complement
}

def resolve(spec):
    kind = spec[0]
    if kind == "n":
        return spec[1], 0.0, 0.0
    if kind in ANCHORS:
        xy, away = ANCHORS[kind]
        return spec[1], spec[2], ray_hue(spec[1], spec[2], xy, away)
    return spec[1], spec[2], float(spec[3])

def fit(L, C, h):
    """Reduce chroma until in sRGB gamut. Returns (L, C, h, clamped?)."""
    clamped = False
    while C > 0 and not in_gamut(lch_to_lin(L, C, h)):
        C = round(C - 0.002, 3); clamped = True
    return L, C, h, clamped

def solve(spec):
    """Resolve a token to (L, C, h). Anchored accents re-solve their hue after every
    gamut step, so the stored lightness, chroma and hue always agree with the ray rule."""
    kind = spec[0]
    if kind in ANCHORS:
        L, C = spec[1], spec[2]
        xy, away = ANCHORS[kind]
        while True:
            h = ray_hue(L, C, xy, away)
            if C <= 0 or in_gamut(lch_to_lin(L, C, h)):
                return L, C, h
            C = round(C - 0.002, 3)
    return fit(*resolve(spec))[:3]

def entry(L, C, h, base_lin, role=None, group=None):
    lin = lch_to_lin(L, C, h)
    e = {"hex": to_hex(lin), "rgb": to_rgb(lin), "oklch": [round(L, 3), round(C, 3), round(h, 1)],
         "contrast": round(contrast(lin, base_lin), 2)}
    if group: e["group"] = group
    if role: e["role"] = role
    return e

def alpha_equivalent(target_hex, base_hex, min_alpha=0.15):
    """A translucent colour that composites over base (in encoded sRGB, as editors do)
    to the opaque target. Uses the smallest alpha at or above min_alpha whose source
    colour stays in gamut, so the layer is as light as possible while staying exact."""
    T = [int(target_hex[i:i + 2], 16) for i in (1, 3, 5)]
    B = [int(base_hex[i:i + 2], 16) for i in (1, 3, 5)]
    for step in range(int(min_alpha * 100), 101):
        a = step / 100
        S = [B[i] + (T[i] - B[i]) / a for i in range(3)]
        if all(-0.5 <= x <= 255.5 for x in S):
            S = [min(max(int(round(x)), 0), 255) for x in S]
            A = int(round(a * 255))
            comp = "#" + "".join(f"{int(round(A / 255 * S[i] + (1 - A / 255) * B[i])):02x}" for i in range(3))
            src = "#" + "".join(f"{x:02x}" for x in S)
            return {"hex8": src + f"{A:02x}", "over": "base", "composite": comp,
                    "error": round(delta_e(hex_to_lin(comp), hex_to_lin(target_hex)), 4)}
    return None

def bright(lch, step, C=None):
    L = min(max(lch[0] + step, 0.0), 0.97)
    return fit(round(L, 3), lch[1] if C is None else min(C, lch[1]), lch[2])[:3]

def build():
    out = {
        "name": "Ma no Iro", "short": "Ma", "slug": "ma-no-iro", "jp": "間の色", "version": VERSION,
        "description": "Eight colours in four complementary pairs, all crossing at one grey, and a guide to how colour works.",
        "derivation": {
            "white_point": "D65", "space": "OKLCH",
            "pairs": {
                "leaf": {"anchor": "green", "spectrum": "555 nm", "xy": [round(v, 4) for v in spectral_xy(GREEN_NM)], "complement": "purple"},
                "water": {"anchor": "red", "spectrum": "700 nm", "xy": [round(v, 4) for v in spectral_xy(RED_NM)], "complement": "cyan"},
                "sky": {"anchor": "blue", "spectrum": "lambda^-4", "xy": [round(v, 4) for v in blackbody_xy(None)], "complement": "yellow"},
                "ink": {"anchor": "black and white", "spectrum": "none and all"},
            },
            "method": "each accent lies on the ray from D65 toward its anchor chromaticity, solved at its lightness and chroma",
            "script": "tools/derive.py",
        },
        "flavors": {},
    }
    for fid, f in FLAVORS.items():
        lch = {k: solve(v) for k, v in f["tokens"].items()}
        base_lin = lch_to_lin(*lch["base"])
        group_of = {k: g for g, ks in GROUPS.items() for k in ks}
        colors = {k: entry(*lch[k], base_lin, ROLES[k], group_of[k]) for k in f["tokens"]}

        derived = {}
        base_lab = lch_to_lab(*lch["base"])
        for k, (src, t) in DERIVED.items():
            s = lch_to_lab(*lch[src])
            mix = [base_lab[i] + (s[i] - base_lab[i]) * t for i in range(3)]
            L, C, h = lab_to_lch(mix)
            derived[k] = entry(L, C, h, base_lin, DERIVED_ROLES[k])
            derived[k]["mix"] = {"from": "base", "to": src, "amount": t}

        for k in ["hl_low", "hl_med", "hl_high"]:
            colors[k]["alpha"] = alpha_equivalent(colors[k]["hex"], colors["base"]["hex"])
        for k, (src, t) in DERIVED.items():
            derived[k]["alpha"] = alpha_equivalent(derived[k]["hex"], colors["base"]["hex"])

        dark = f["appearance"] == "dark"
        step = BRIGHT_STEP if dark else -BRIGHT_STEP
        normal = {
            "black": "overlay" if dark else "text", "red": "red", "green": "function", "yellow": "yellow_text",
            "blue": "blue", "magenta": "keyword", "cyan": "cyan", "white": "subtle" if dark else "dim",
        }
        brights = {
            "black": ("token", "muted"), "red": ("step", "red"),
            "green": ("step", "function"),
            "yellow": ("step", "yellow_text") if dark else ("token", "yellow"),
            "blue": ("step", "blue"),
            "magenta": ("step", "keyword"),
            "cyan": ("step", "cyan"), "white": ("token", "text" if dark else "overlay"),
        }
        ansi = {"normal": {}, "bright": {}, "rule": "Bright colours step one rung toward the text colour: "
                f"lightness +{BRIGHT_STEP} on the dark flavor, -{BRIGHT_STEP} on the light, chroma reduced only if out of gamut. "
                "Bright green on the dark flavor is also capped at chroma 0.11 so it stays apart from the seed. "
                "The seed is never an ANSI colour. Exception: on the light flavor bright yellow is the gold signal."}
        for i, (name, tok) in enumerate(normal.items()):
            ansi["normal"][name] = {"index": i, "token": tok, "hex": colors[tok]["hex"]}
        for i, (name, (kind, tok)) in enumerate(brights.items()):
            if kind == "token":
                ansi["bright"][name] = {"index": i + 8, "token": tok, "hex": colors[tok]["hex"]}
            else:
                L, C, h = bright(lch[tok], step, BRIGHT_GREEN_C if dark and name == "green" else None)
                ansi["bright"][name] = {"index": i + 8, "from": tok, "hex": to_hex(lch_to_lin(L, C, h)),
                                        "oklch": [round(L, 3), round(C, 3), round(h, 1)]}

        out["flavors"][fid] = {
            "name": f["name"], "jp": f["jp"], "reading": f["reading"], "appearance": f["appearance"],
            "ground": f["ground"], "home": f["home"], "seed_hue": f["seed_hue"],
            "aliases": {"home": "keyword" if dark else "function", "on_accent": "base", "cursor_text": "base"},
            "colors": colors, "derived": derived, "ansi": ansi,
        }
    return out

# ---------------------------------------------------------------- policy

def report(pal, verbose=True):
    failures, notes = [], []
    for fid, f in pal["flavors"].items():
        c = f["colors"]
        lin = {k: hex_to_lin(v["hex"]) for k, v in c.items()}
        base = lin["base"]
        for k in TEXT_ROLES:
            if c[k]["contrast"] < 4.5:
                failures.append(f"{fid}: {k} is {c[k]['contrast']}:1 on base, text needs 4.5:1")
        if c["yellow"]["contrast"] < 3.0 - 1e-6:
            failures.append(f"{fid}: yellow signal is {c['yellow']['contrast']}:1, signals need 3:1")
        if c["seed"]["contrast"] < 3.0:
            failures.append(f"{fid}: seed is {c['seed']['contrast']}:1, the cursor needs 3:1")
        # the seed is the one point of attention: no ANSI colour may pass for it
        for r in ("normal", "bright"):
            for name, e in f["ansi"][r].items():
                d = delta_e(lin["seed"], hex_to_lin(e["hex"]))
                if d < 0.07:
                    failures.append(f"{fid}: ANSI {r} {name} is only {d:.3f} from the seed")
        # every bright must read as a step of its own from its normal
        for name, e in f["ansi"]["normal"].items():
            d = delta_e(hex_to_lin(e["hex"]), hex_to_lin(f["ansi"]["bright"][name]["hex"]))
            if d < 0.07:
                failures.append(f"{fid}: ANSI {name} and bright {name} are only {d:.3f} apart")
        # the dose (R7): only the seed is vivid
        for k, v in c.items():
            if k != "seed" and v["oklch"][1] >= c["seed"]["oklch"][1]:
                failures.append(f"{fid}: {k} has chroma {v['oklch'][1]}, as vivid as the seed")
        # selection must read as a step of its own, apart from borders and the word highlight
        for other in ["overlay", "hl_med"]:
            d = abs(c["hl_high"]["oklch"][0] - c[other]["oklch"][0])
            if d < 0.04 - 1e-9:
                failures.append(f"{fid}: hl_high is only {d:.3f} lightness from {other}, selection needs 0.04")
        for k in ON_ACCENT:
            r = contrast(base, lin[k])
            if r < 4.5:
                failures.append(f"{fid}: base text on {k} is {r:.2f}:1")
        syntax_fg = ["text"] + SYNTAX
        # resting grounds: every text role at 4.5:1
        for g in ["surface", "hl_low"]:
            bg = lin[g]
            for t in TEXT_ROLES:
                r = contrast(lin[t], bg)
                if r < 4.5:
                    failures.append(f"{fid}: {t} on {g} is {r:.2f}:1, resting text needs 4.5:1")
        for t in ["text", "subtle", "muted"]:
            r = contrast(lin[t], lin["mantle"])
            if r < 4.5:
                failures.append(f"{fid}: {t} on mantle is {r:.2f}:1")
        # overlays: selection, search, diff and diagnostic washes keep syntax at 3:1
        overlays = {"hl_med": lin["hl_med"], "hl_high": lin["hl_high"]}
        overlays.update({k: hex_to_lin(d["hex"]) for k, d in f["derived"].items()})
        for g, bg in overlays.items():
            worst = min((contrast(lin[t], bg), t) for t in syntax_fg)
            if worst[0] < 3.0:
                failures.append(f"{fid}: {worst[1]} on {g} is {worst[0]:.2f}:1, overlays need 3:1")
        for name, m in [("normal", None)] + list(CVD.items()):
            d = delta_e(lin["keyword"], lin["function"], m)
            if d < 0.10:
                failures.append(f"{fid}: purple and green are {d:.3f} apart under {name}")
        for a, b in combinations(SYNTAX + ["text", "muted"], 2):
            d = delta_e(lin[a], lin[b])
            if d < 0.07:
                failures.append(f"{fid}: {a} and {b} are only {d:.3f} apart in normal vision")
        syntax = SYNTAX + ["text", "subtle", "muted"]
        terminal = ["red", "yellow_text", "blue", "cyan", "function", "keyword"]
        for label, keys in [("syntax", syntax), ("terminal", terminal)]:
            for a, b in combinations(keys, 2):
                for name, m in CVD.items():
                    d = delta_e(lin[a], lin[b], m)
                    if d < 0.05:
                        notes.append(f"{fid} {label}: {a}/{b} under {name}, dE {d:.3f}")
    if verbose:
        print(f"Ma no Iro {pal['version']}  green {GREEN_NM:g} nm -> hue {GREEN_HUE}")
        for fid, f in pal["flavors"].items():
            print(f"\n{f['jp']} {f['name']}")
            for k, v in f["colors"].items():
                L, C, h = v["oklch"]
                print(f"  {k:12s} {v['hex']}  oklch({L:.3f} {C:.3f} {h:5.1f})  {v['contrast']:5.2f}:1")
            for k, v in f["derived"].items():
                print(f"  {k:18s} {v['hex']}")
        print("\nPolicy:", "pass" if not failures else "FAIL")
        for x in failures: print("  -", x)
        print("Known weak pairs (documented, not blocking):")
        for x in notes: print("  -", x)
    return failures

def spec_tables(pal):
    lines = []
    for fid, f in pal["flavors"].items():
        lines += [f"### {f['jp']} {f['name']}", "",
                  "| Layer | Token | Hex | OKLCH | vs base | Role |", "| --- | --- | --- | --- | --- | --- |"]
        layer = {"ink": "ink", "leaf": "leaf", "water": "water", "sky": "sky"}
        for k, v in f["colors"].items():
            L, C, h = v["oklch"]
            lines.append(f"| {layer[v['group']]} | `{k}` | `{v['hex']}` | {L:.3f} {C:.3f} {h:.1f} | "
                         f"{v['contrast']:.2f} | {v['role']} |")
        lines += ["", "| Derived | Hex | Alpha over base | Mix | Role |", "| --- | --- | --- | --- | --- |"]
        for k, v in f["derived"].items():
            m = v["mix"]
            lines.append(f"| `{k}` | `{v['hex']}` | `{v['alpha']['hex8']}` | {int(m['amount'] * 100)}% `{m['to']}` | {v['role']} |")
        lines += ["", "| ANSI | Normal | Bright |", "| --- | --- | --- |"]
        for name in f["ansi"]["normal"]:
            n, b = f["ansi"]["normal"][name], f["ansi"]["bright"][name]
            bsrc = b.get("token") or ("+1 rung " + b["from"])
            lines.append(f"| {n['index']} / {b['index']} {name} | `{n['hex']}` `{n['token']}` | `{b['hex']}` {bsrc} |")
        lines.append("")
    return "\n".join(lines)

def render_spec(pal):
    if not os.path.exists(SPEC):
        return None
    doc = open(SPEC, encoding="utf-8").read()
    a, b = "<!-- palette:start -->", "<!-- palette:end -->"
    i, j = doc.index(a) + len(a), doc.index(b)
    return doc[:i] + "\n" + spec_tables(pal) + doc[j:]

def replace_between(doc, a, b, body):
    i, j = doc.index(a) + len(a), doc.index(b)
    return doc[:i] + body + doc[j:]

def render_readme(pal):
    if not os.path.exists(README):
        return None
    k, b = pal["flavors"]["kuromurasaki"], pal["flavors"]["byakuroku"]
    c = lambda f, t: f"`{f['colors'][t]['hex']}`"
    table = ("\n| | 黒紫 Kuromurasaki | 白緑 Byakuroku |\n| --- | --- | --- |\n"
             f"| Ground | black {c(k, 'base')} | white {c(b, 'base')} |\n"
             f"| Home colour | purple {c(k, 'keyword')} | green {c(b, 'function')} |\n"
             f"| Seed (cursor, focus, current match) | green {c(k, 'seed')} | purple {c(b, 'seed')} |\n")
    doc = open(README, encoding="utf-8").read()
    return replace_between(doc, "<!-- flavors:start -->", "<!-- flavors:end -->", table)

def render_showcase(pal):
    if not os.path.exists(SHOWCASE):
        return None
    doc = open(SHOWCASE, encoding="utf-8").read()
    k, b = pal["flavors"]["kuromurasaki"], pal["flavors"]["byakuroku"]
    def block(f, prefix):
        v = {t: c["hex"] for t, c in f["colors"].items()}
        v["home"] = f["colors"][f["aliases"]["home"]]["hex"]
        return "".join(f"--{prefix}-{t}:{h};" for t, h in v.items())
    tokens = ("\n:root{" + block(k, "k") + block(b, "b") + block(b, "c") + "}\n"
              "@media (prefers-color-scheme: dark){:root:not([data-theme=\"light\"]){" + block(k, "c") + "}}\n"
              ":root[data-theme=\"dark\"]{" + block(k, "c") + "}\n")
    slim = {"version": pal["version"], "derivation": pal["derivation"], "flavors": {}}
    for fid, f in pal["flavors"].items():
        slim["flavors"][fid] = {
            "name": f["name"], "jp": f["jp"], "appearance": f["appearance"], "aliases": f["aliases"],
            "colors": {t: {x: c[x] for x in ("hex", "oklch", "contrast", "role", "group")} for t, c in f["colors"].items()},
            "derived": {t: {x: c[x] for x in ("hex", "oklch", "contrast", "role")} for t, c in f["derived"].items()},
            "ansi": {r: {n: {"hex": e["hex"], "index": e["index"]} for n, e in f["ansi"][r].items()} for r in ("normal", "bright")},
        }
    from cie1931 import CMF_1931_2DEG
    slim["cmf"] = [[float(f"{v:.6g}") for v in row] for row in CMF_1931_2DEG]
    data = json.dumps(slim, ensure_ascii=False, separators=(",", ":"))
    sample = json.dumps(open(SAMPLE, encoding="utf-8").read().rstrip("\n").split("\n"), ensure_ascii=False)
    doc = replace_between(doc, "/* tokens:start */", "/* tokens:end */", tokens)
    doc = replace_between(doc, "/* data:start */", "/* data:end */", data)
    doc = replace_between(doc, "/* sample:start */", "/* sample:end */", sample)
    return doc

def main():
    pal = build()
    text = json.dumps(pal, ensure_ascii=False, indent=2) + "\n"
    if "--write" in sys.argv:
        with open(OUT, "w", encoding="utf-8") as fh: fh.write(text)
        print(f"wrote {os.path.normpath(OUT)}")
        spec = render_spec(pal)
        if spec is not None:
            with open(SPEC, "w", encoding="utf-8") as fh: fh.write(spec)
            print(f"updated palette tables in {os.path.normpath(SPEC)}")
        for path, doc in ((SHOWCASE, render_showcase(pal)), (README, render_readme(pal))):
            if doc is not None:
                with open(path, "w", encoding="utf-8") as fh: fh.write(doc)
                print(f"updated generated regions in {os.path.normpath(path)}")
        sys.exit(1 if report(pal) else 0)
    if "--check" in sys.argv:
        ok = os.path.exists(OUT) and open(OUT, encoding="utf-8").read() == text
        spec = render_spec(pal)
        if spec is not None and open(SPEC, encoding="utf-8").read() != spec:
            ok = False; print("SPEC.md palette tables are out of date: run tools/derive.py --write")
        for path, doc in ((SHOWCASE, render_showcase(pal)), (README, render_readme(pal))):
            if doc is not None and open(path, encoding="utf-8").read() != doc:
                ok = False; print(f"{os.path.relpath(path, os.path.join(HERE, '..'))} is out of date: run tools/derive.py --write")
        failures = report(pal, verbose=False)
        if not ok: print("palette.json is out of date: run tools/derive.py --write")
        for x in failures: print("policy:", x)
        sys.exit(0 if ok and not failures else 1)
    report(pal)

if __name__ == "__main__":
    main()
