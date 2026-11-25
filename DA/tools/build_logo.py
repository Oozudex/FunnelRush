#!/usr/bin/env python3
"""Generate the "The Last Query" logo SVG variants.

Run:  python3 DA/tools/build_logo.py
Output: DA/logo/*.svg  (then DA/tools/render.sh for PNG exports)

Board-game look: every shape gets a solid 45° extrusion (like a die-cut
token), and a ribbon carries the tagline in a pixel "terminal" font.
All shapes are hand-placed; no fonts are used, nothing needs outlining.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "logo"

# Brand colours (sRGB). CMYK equivalents are documented in DA/README.md.
NOIR = "#0B0B0C"     # ink black / background
BONE = "#F4F0E6"     # warm paper white
RED = "#E31B3B"      # "last query" red
OXBLOOD = "#7E0C1F"  # deep red, extrusion of red shapes

VIEWBOX = (90, 50, 1150, 655)  # x, y, w, h  (includes the clear-space margin)
DX = 45        # detective offset to the right of the ";"
DEPTH = 10     # extrusion depth (units, 45° down-right)
TAGLINE = "A MURDER MYSTERY BOARD GAME"

VARIANTS = {
    # name: (background, ink, accent, ink_extrusion, accent_extrusion, ghost)
    "logo_dark":              (NOIR, BONE, RED, RED, OXBLOOD, True),
    "logo_dark_transparent":  (None, BONE, RED, RED, OXBLOOD, True),
    "logo_light":             (BONE, NOIR, RED, RED, OXBLOOD, True),
    "logo_light_transparent": (None, NOIR, RED, RED, OXBLOOD, True),
    "logo_mono_white":        (NOIR, BONE, BONE, None, None, False),
    "logo_mono_black":        (BONE, NOIR, NOIR, None, None, False),
}

# ---------- 5x7 pixel font for the tagline ----------
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    " ": ["....."] * 7,
}


def pixel_text(text, x0, y0, px):
    out, x = [], x0
    for ch in text:
        for row, line in enumerate(FONT[ch]):
            col = 0
            while col < 5:                      # merge runs into one rect
                if line[col] == "#":
                    start = col
                    while col < 5 and line[col] == "#":
                        col += 1
                    out.append(f'<rect x="{x + start * px:.1f}" y="{y0 + row * px:.1f}" '
                               f'width="{(col - start) * px:.1f}" height="{px:.1f}"/>')
                else:
                    col += 1
        x += 6 * px
    return "".join(out), x - px - x0          # markup, width


PX = 3.4
TAG, TAG_W = pixel_text(TAGLINE, 0, 0, PX)
RIB_X1, RIB_X2, RIB_Y1, RIB_Y2 = 380, 962, 600, 640


def cuts(colour):
    """Detective coat details, in the detective's local coordinates."""
    return (f'<g fill="none" stroke="{colour}" stroke-linejoin="miter">'
            '<path d="M984,392 H1134" stroke-width="7"/>'                 # belt
            '<path d="M1057,300 L1049,592" stroke-width="6"/>'            # coat split
            '<path d="M1122,296 L1096,352 L1064,348" stroke-width="7"/>'  # raised arm
            '</g>')


def artwork(ink, accent, banner_text, front, bg, ghost):
    """All logo shapes. front=False draws the flat silhouette for the extrusion."""
    s = []
    a = s.append
    # Row 1 : "> THE"
    a('<g fill="none" stroke-width="14" stroke-linejoin="miter" stroke-linecap="butt">')
    a(f'<path d="M150,113 L176,140 L150,167" stroke="{accent}"/>')
    a(f'<path d="M196,117 H246 M221,117 V170 M265,110 V170 M297,110 V170 M265,140 H297 '
      f'M358,117 H323 V163 H358 M323,140 H350" stroke="{ink}"/>')
    a('</g>')
    # Row 2 : "LAST"
    a(f'<g fill="none" stroke="{accent}" stroke-width="30" stroke-linejoin="miter" stroke-linecap="butt">'
      '<path d="M165,190 V325 H262 M297,340 V205 H377 V340 M297,272 H377 '
      'M524,205 H429 V265 H509 V325 H414 M546,205 H656 M601,205 V340"/></g>')
    # Row 3 : Q (magnifying glass) U E Y
    a(f'<g fill="none" stroke="{ink}" stroke-width="34" stroke-linejoin="miter" stroke-linecap="butt">'
      '<path d="M193,387 H267 L293,413 V487 L267,513 H193 L167,487 V413 Z"/>'
      '<path d="M282,492 L346,574 M361,370 V513 H457 V370 M618,387 H515 V513 H618 M515,450 H600 '
      'M813,370 V450 H909 V370 M861,450 V530"/></g>')
    # R = corrupted record
    r = ('<path d="M659,530 V387 H755 V450 H659" fill="none" stroke-width="34" '
         'stroke-linejoin="miter"/><polygon points="684,433 722,433 776,530 736,530"/>')
    def band(clip, dx, colour):
        return (f'<g clip-path="url(#{clip})" transform="translate({dx},0)" '
                f'fill="{colour}" stroke="{colour}">{r}</g>')
    if front and ghost:
        a(band("bandB", -8, accent))
    a(band("bandA", 0, ink))
    a(band("bandB", 16, ink))
    a(band("bandC", 0, ink))
    # ";"
    a(f'<g fill="{accent}"><rect x="950" y="414" width="34" height="34"/>'
      '<polygon points="950,488 984,488 984,530 964,566 940,566 950,530"/></g>')
    # ribbon with notched tails
    a(f'<polygon fill="{accent}" points="{RIB_X1 - 22},{RIB_Y1} {RIB_X2 + 22},{RIB_Y1} '
      f'{RIB_X2 + 8},{(RIB_Y1 + RIB_Y2) / 2} {RIB_X2 + 22},{RIB_Y2} {RIB_X1 - 22},{RIB_Y2} '
      f'{RIB_X1 - 8},{(RIB_Y1 + RIB_Y2) / 2}"/>')
    if front:
        tx = (RIB_X1 + RIB_X2 - TAG_W) / 2
        ty = (RIB_Y1 + RIB_Y2 - 7 * PX) / 2
        a(f'<g fill="{banner_text}" transform="translate({tx:.1f},{ty:.1f})">{TAG}</g>')
    # Detective
    a(f'<g transform="translate({DX},0)">')
    a(f'<g fill="{ink}">'
      '<polygon points="1028,150 1092,150 1100,198 1020,198"/>'
      '<polygon points="996,198 1124,198 1114,212 1006,212"/>'
      '<polygon points="1047,222 1080,222 1075,244 1055,249"/>'
      '<polygon points="1030,228 1056,300 1092,228 1120,262 1128,420 1138,590 978,590 988,420 998,262"/>'
      '<rect x="1005" y="588" width="30" height="46"/><rect x="1081" y="588" width="30" height="46"/>'
      '<polygon points="992,630 1040,630 1040,645 986,645"/>'
      '<polygon points="1076,630 1124,630 1132,645 1076,645"/></g>')
    if front:
        if bg:
            a(cuts(bg))
        a(f'<rect x="1021" y="185" width="78" height="10" fill="{accent}"/>'
          f'<polygon points="1034,318 1060,312 1068,352 1042,358" fill="{accent}"/>')
    a('</g>')
    return "".join(s)


def svg(name, bg, ink, accent, ink_ext, acc_ext, ghost):
    x, y, w, h = VIEWBOX
    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" '
      f'width="{w}" height="{h}">')
    a(f'<title>The Last Query - {name}</title>')
    a('<defs>')
    if not bg:
        a(f'<mask id="cuts" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">'
          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>'
          f'<g transform="translate({DX},0)">{cuts("#000")}</g></mask>')
    a('<clipPath id="bandA"><rect x="600" y="360" width="220" height="116"/></clipPath>'
      '<clipPath id="bandB"><rect x="600" y="476" width="220" height="22"/></clipPath>'
      '<clipPath id="bandC"><rect x="600" y="498" width="220" height="60"/></clipPath>')
    a('</defs>')
    if bg:
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>')
    a('<g mask="url(#cuts)">' if not bg else '<g>')

    # extrusion: the flat silhouette repeated 1..DEPTH units down-right
    if ink_ext:
        flat = artwork(ink_ext, acc_ext, None, False, bg, ghost)
        a('<g>' + "".join(f'<g transform="translate({k},{k})">{flat}</g>'
                          for k in range(DEPTH, 0, -1)) + '</g>')

    banner_text = BONE if bg != BONE and ink != NOIR else BONE
    if accent == ink:            # mono: punch the tagline out of the ribbon
        banner_text = bg or "#000"
    a(artwork(ink, accent, banner_text, True, bg, ghost))
    a('</g></svg>')
    return "\n".join(s)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, v in VARIANTS.items():
        (OUT / f"the-last-query_{name}.svg").write_text(svg(name, *v))
        print("wrote", name)
