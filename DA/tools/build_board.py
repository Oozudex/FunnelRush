#!/usr/bin/env python3
"""Game board v3: top-down floor plan of Ravenscroft Manor, flat noir style
with depth (cast shadows, moonlight through the windows, lamp light).
A2 landscape 594 x 420 mm, 3 mm bleed, crop marks. Pure SVG in millimetres.

Run:  python3 DA/tools/build_board.py   (also called by build_print.py)
"""
import math

import build_print as bp

C = bp.C
W, H, BLEED, SLUG = 594, 420, bp.BLEED, bp.SLUG
NOIR, BONE, RED, OX, AMBER, BLUE, ASH, GRAPH = (C[k] for k in ("noir", "bone", "red", "oxblood", "amber", "blue", "ash", "graphite"))

# material tones (muted, derived from the palette)
WOOD, WOOD2, WOODL, WOODH = "#3A2621", "#2A1A16", "#56382D", "#6B4636"
LEAF, LEAF2, LEAF3 = "#1F3528", "#2F4F3B", "#4A7556"
KT1, KT2 = "#1B2731", "#22313C"
STONE, STONEL = "#29292D", "#19191C"
HC1, HC2 = "#141417", "#212125"
M1, M2 = "#3C3C43", "#28282D"
NIGHT = "#10141C"
BRASS = "#C9923A"
MUD = "#5B4333"
GLASS = "#2B3B48"

# geometry (mm, trim coordinates)
MX, MY, MW, MH = 22, 20, 426, 380
WALL = 5
IX, IY = MX + WALL, MY + WALL
HALL = 24
RW = (MW - 2 * WALL - 2 * HALL) / 3
RH = (MH - 2 * WALL - 2 * HALL) / 3
DOOR = 15
DOOR_FRAC = .62          # top/bottom doors sit at 62 % of the wall (clear of the name plates)
SX, SW = 463, 119          # sidebar


def room_xy(r, c):
    return IX + c * (RW + HALL), IY + r * (RH + HALL)


# ------------------------------------------------------------------ svg helpers
def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def rect(x, y, w, h, fill="none", stroke="none", sw=0, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def circ(cx, cy, r, fill="none", stroke="none", sw=0, extra=""):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def ell(cx, cy, rx, ry, fill, extra=""):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" {extra}/>'


def line(x1, y1, x2, y2, stroke, sw, extra=""):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def path(d, fill="none", stroke="none", sw=0, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw)}" {extra}/>'


def poly(pts, fill, extra=""):
    return f'<polygon points="{" ".join(f"{f(x)},{f(y)}" for x, y in pts)}" fill="{fill}" {extra}/>'


def g(content, x=0, y=0, rot=0, scale=1, extra=""):
    t = f"translate({f(x)},{f(y)})" + (f" rotate({f(rot)})" if rot else "") + (f" scale({scale})" if scale != 1 else "")
    return f'<g transform="{t}" {extra}>{content}</g>'


def text(x, y, s, size, fill, family="Bungee", anchor="start", extra=""):
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{f(size)}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def html_box(x, y, w, h, inner, style=""):
    return (f'<foreignObject x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="{style}">{inner}</div></foreignObject>')


def shadow(content, dx=1.3, dy=1.6, op=.5):
    """Flat cast shadow (light from the top-left) + the object itself."""
    return f'<g class="sh" transform="translate({dx},{dy})" opacity="{op}">{content}</g>{content}'


def icon(name, x, y, size, colour, sw=2):
    s = size / 24
    return (f'<g transform="translate({f(x)},{f(y)}) scale({f(s)})"><path d="{bp.ICONS[name]}" fill="none" stroke="{colour}" '
            f'stroke-width="{sw}" stroke-linecap="square" stroke-linejoin="miter"/></g>')


bp.ICONS.update({
    "terminal": "M3 4h18v16H3z M6 9l3 3-3 3 M11 15h6",
    "heart": "M12 20l-8-8a4.6 4.6 0 0 1 8-5.5 4.6 4.6 0 0 1 8 5.5z M12 6.5l-2 4.5 3 2-1.5 4",
    "poison": "M9 2h6v4l3 4v12H6V10l3-4z M6 13h12 M10 16l4 3 M14 16l-4 3",
    "steps": "M6 3h4v7H6z M6 12h4v2H6z M14 9h4v7h-4z M14 18h4v2h-4z",
})


SEMI = "M10 4h4v4h-4z M10 12h4v4l-2 4h-2.6l1.6-4h-1z"   # block semicolon, like the logo (24 x 24)


def tok(size=3.6):
    """Inline Query Token (black disc, red ';') for HTML text; 1 css px = 1 mm on the board."""
    return (f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;vertical-align:-.2em;display:inline-block">'
            f'<circle cx="12" cy="12" r="11.2" fill="{NOIR}" stroke="{RED}" stroke-width="1.2"/><path d="{SEMI}" fill="{RED}"/></svg>')


def tok_svg(cx, cy, r, ring=BONE):
    s_ = r / 12
    return (circ(cx, cy, r, NOIR, ring, .45)
            + f'<path d="{SEMI}" fill="{RED}" transform="translate({f(cx - 12 * s_)},{f(cy - 12 * s_)}) scale({f(s_)})"/>')


PROFILE_CHIPS = "".join(
    f"<span style='display:inline-block;border:.3px solid {BONE};padding:.6px 1.4px;margin:0 1px 1.2px 0;"
    f"font-family:Silkscreen;font-size:2.4px'>{t}</span>" for t in ["AGE", "HEIGHT", "SHOE", "HAND", "HAIR", "GLASSES", "SMELL"])


def lamp(cx, cy, r=24, op=1):
    return circ(cx, cy, r, "url(#gLamp)", extra=f'opacity="{op}"')


# ------------------------------------------------------------------ defs
DEFS = f"""
<radialGradient id="gLamp"><stop offset="0" stop-color="{AMBER}" stop-opacity=".42"/>
  <stop offset=".35" stop-color="{AMBER}" stop-opacity=".16"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
<radialGradient id="gVig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<radialGradient id="gScreen"><stop offset="0" stop-color="{BLUE}" stop-opacity=".45"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="gRed"><stop offset="0" stop-color="{RED}" stop-opacity=".5"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<linearGradient id="gMoonD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FB6CC" stop-opacity=".26"/><stop offset="1" stop-color="#9FB6CC" stop-opacity="0"/></linearGradient>
<linearGradient id="gMoonU" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#9FB6CC" stop-opacity=".26"/><stop offset="1" stop-color="#9FB6CC" stop-opacity="0"/></linearGradient>
<linearGradient id="gMoonR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9FB6CC" stop-opacity=".26"/><stop offset="1" stop-color="#9FB6CC" stop-opacity="0"/></linearGradient>
<linearGradient id="gMoonL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#9FB6CC" stop-opacity=".26"/><stop offset="1" stop-color="#9FB6CC" stop-opacity="0"/></linearGradient>
<linearGradient id="gKeys" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BONE}"/><stop offset="1" stop-color="#D9D3C4"/></linearGradient>
<pattern id="pHall" width="12" height="12" patternUnits="userSpaceOnUse">
  {rect(0, 0, 12, 12, HC1)}{rect(0, 0, 6, 6, HC2)}{rect(6, 6, 6, 6, HC2)}</pattern>
<pattern id="pMarble" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  {rect(0, 0, 14, 14, M2)}{rect(0, 0, 7, 7, M1)}{rect(7, 7, 7, 7, M1)}
  {line(1, 3, 6, 5, "#4A4A52", .2)}{line(8, 10, 13, 9, "#33333A", .2)}</pattern>
<pattern id="pParquet" width="32" height="6" patternUnits="userSpaceOnUse">
  {rect(0, 0, 32, 6, WOOD)}{rect(0, 3, 32, 3, "#352219")}{line(0, 0, 32, 0, WOOD2, .3)}{line(0, 3, 32, 3, WOOD2, .3)}
  {line(0, 0, 0, 3, WOOD2, .3)}{line(19, 3, 19, 6, WOOD2, .3)}{line(9, 1.4, 14, 1.4, WOODL, .15)}</pattern>
<pattern id="pHerring" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  {rect(0, 0, 10, 10, WOOD)}{rect(0, 0, 10, 5, "#332019")}{line(0, 0, 10, 0, WOOD2, .3)}{line(0, 5, 10, 5, WOOD2, .3)}
  {line(5, 0, 5, 5, WOOD2, .3)}{line(0, 5, 0, 10, WOOD2, .3)}</pattern>
<pattern id="pTiles" width="10" height="10" patternUnits="userSpaceOnUse">
  {rect(0, 0, 10, 10, KT1)}{rect(0, 0, 5, 5, KT2)}{rect(5, 5, 5, 5, KT2)}
  <path d="M0 0H10M0 5H10M0 0V10M5 0V10" stroke="#0E1317" stroke-width=".25"/></pattern>
<pattern id="pStone" width="18" height="10" patternUnits="userSpaceOnUse">
  {rect(0, 0, 18, 10, STONE)}{rect(9, 5, 9, 5, "#2E2E33")}<path d="M0 0H18M0 5H18M0 0V5M9 5V10" stroke="{STONEL}" stroke-width=".45"/></pattern>
<pattern id="pCellar" width="14" height="8" patternUnits="userSpaceOnUse">
  {rect(0, 0, 14, 8, "#262224")}{rect(0, 4, 7, 4, "#2C2729")}<path d="M0 0H14M0 4H14M0 0V4M7 4V8" stroke="#141213" stroke-width=".45"/></pattern>
<pattern id="pGlass" width="12" height="12" patternUnits="userSpaceOnUse">
  {rect(0, 0, 12, 12, "#141E25")}<path d="M0 0H12M0 0V12" stroke="{BLUE}" stroke-width=".3" opacity=".5"/>
  {line(1, 11, 11, 1, "#9FB6CC", .12, 'opacity=".4"')}</pattern>
<pattern id="pRaised" width="10" height="10" patternUnits="userSpaceOnUse">
  {rect(0, 0, 10, 10, "#1C1C20")}<path d="M0 0H10M0 0V10" stroke="{ASH}" stroke-width=".18" opacity=".55"/>
  {circ(1, 1, .3, ASH)}</pattern>
<pattern id="pStars" width="24" height="24" patternUnits="userSpaceOnUse">
  {rect(0, 0, 24, 24, NIGHT)}{circ(3, 4, .35, BONE, extra='opacity=".7"')}{circ(15, 9, .25, BONE, extra='opacity=".5"')}
  {circ(8, 18, .3, BONE, extra='opacity=".6"')}{circ(20, 20, .2, BONE, extra='opacity=".4"')}{circ(21, 3, .2, AMBER, extra='opacity=".6"')}</pattern>
<pattern id="pRain" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(18)">
  {line(0, 0, 0, 2.6, "#26262B", .4)}</pattern>
<pattern id="pPersian" width="9" height="9" patternUnits="userSpaceOnUse">
  {rect(0, 0, 9, 9, "#6E0B1C")}<path d="M4.5 .8L8.2 4.5 4.5 8.2 .8 4.5Z" fill="none" stroke="{RED}" stroke-width=".35"/>
  {circ(4.5, 4.5, .7, BRASS)}{circ(0, 0, .5, BRASS)}{circ(9, 9, .5, BRASS)}</pattern>
<pattern id="pOriental" width="8" height="8" patternUnits="userSpaceOnUse">
  {rect(0, 0, 8, 8, "#2A2030")}<path d="M0 4H8M4 0V8" stroke="#3A2C40" stroke-width="1.2"/>{circ(4, 4, 1, BRASS, extra='opacity=".7"')}</pattern>
<pattern id="pPlanks" width="88" height="7" patternUnits="userSpaceOnUse">
  {rect(0, 0, 88, 7, WOODL)}{line(0, 0, 88, 0, WOOD2, .35)}{line(30, 0, 30, 7, WOOD2, .25)}{line(64, 0, 64, 7, WOOD2, .25)}
  {line(5, 3.5, 22, 3.6, WOODH, .15)}{line(40, 2.5, 58, 2.6, WOODH, .15)}</pattern>
<pattern id="pGravel" width="5" height="5" patternUnits="userSpaceOnUse">
  {rect(0, 0, 5, 5, "#2A2A2C")}{circ(1, 1, .35, "#3A3A3E")}{circ(3.5, 2.5, .3, "#34343A")}{circ(2, 4.2, .25, "#3F3F44")}</pattern>
"""


# ------------------------------------------------------------------ furniture library
def bookshelf(x, y, w, h, vertical=True):
    out = [rect(x, y, w, h, WOOD2, WOODL, .4)]
    cols = [RED, AMBER, BLUE, ASH, BONE, OX, "#4A6B55", BRASS]
    n = int((h if vertical else w) / 1.5)
    for k in range(n):
        col = cols[(k * 5 + k // 3) % len(cols)]
        depth = .7 + ((k * 37) % 5) * .07
        if vertical:
            out.append(rect(x + .7, y + .7 + k * 1.5, (w - 1.4) * depth, 1.15, col))
        else:
            out.append(rect(x + .7 + k * 1.5, y + .7, 1.15, (h - 1.4) * depth, col))
    return shadow("".join(out), .9, 1.1)


def armchair(x, y, rot=0, fill=OX):
    body = (rect(-7, -6, 14, 13, fill, NOIR, .3, 'rx="2.2"') + rect(-7, -7.5, 14, 4.5, fill, NOIR, .3, 'rx="1.8"')
            + rect(-8, -6, 3.2, 13, fill, NOIR, .3, 'rx="1.4"') + rect(4.8, -6, 3.2, 13, fill, NOIR, .3, 'rx="1.4"')
            + rect(-4.6, -2.5, 9.2, 8.5, "#8E1428", extra='rx="1.4"'))
    return g(shadow(body), x, y, rot)


def chair(x, y, rot=0, fill=WOOD2):
    return g(shadow(rect(-2.8, -2.6, 5.6, 5.6, fill, WOODL, .3, 'rx=".8"') + rect(-2.8, -3.4, 5.6, 1.6, WOODL, extra='rx=".5"'), .7, .8), x, y, rot)


def plant(x, y, r=5, flowers=False, pot=True):
    out = []
    if pot:
        out.append(circ(x, y, r * .62, "#4A2E25", NOIR, .25))
    for k in range(8):
        a = k * 2 * math.pi / 8 + .3
        px, py = x + math.cos(a) * r * .55, y + math.sin(a) * r * .55
        out.append(ell(px, py, r * .48, r * .28, LEAF2, f'transform="rotate({f(math.degrees(a))} {f(px)} {f(py)})"'))
    out.append(circ(x, y, r * .38, LEAF3))
    if flowers:
        for k in range(6):
            a = k * 2 * math.pi / 6 + .5
            px, py = x + math.cos(a) * r * .72, y + math.sin(a) * r * .72
            out.append(circ(px, py, r * .17, RED) + circ(px, py, r * .07, BONE))
    return shadow("".join(out), 1, 1.2, .55)


def barrel(x, y, r=5.8):
    return shadow(circ(x, y, r, WOOD, NOIR, .3) + circ(x, y, r * .86, "none", "#2A2A2E", .55) + circ(x, y, r * .6, "none", WOOD2, .35)
                  + circ(x, y, r * .34, "none", WOOD2, .35) + circ(x - r * .25, y - r * .25, r * .14, WOODH))


def candle(x, y):
    return circ(x, y, .9, BONE) + circ(x, y, .45, AMBER) + lamp(x, y, 6)


def trapdoor(x, y, dest):
    body = (rect(x, y, 14, 14, WOOD2, RED, .55) + "".join(line(x, y + k * 3.5, x + 14, y + k * 3.5, WOOD, .3) for k in range(1, 4))
            + circ(x + 10.5, y + 7, 1.2, "none", BRASS, .45) + rect(x + 1.5, y + 1.5, 11, 11, "none", RED, .25, 'stroke-dasharray=".8 .6"'))
    lab = (rect(x - 7, y + 15, 28, 8.4, NOIR, RED, .3) + text(x + 7, y + 18.4, "SECRET PASSAGE", 2.3, RED, "Silkscreen", "middle")
           + text(x + 7, y + 21.9, "&#8594; " + dest, 2.3, BONE, "Silkscreen", "middle"))
    return shadow(body) + lab


def deck_zone(x, y, w=88, h=63, colour=BONE, label="ROOM DECK"):
    """Card-size zone: corner brackets + label tab. The 63 x 88 card fits inside."""
    L = 6
    c = []
    for cx, cy, sx, sy in [(x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)]:
        c.append(path(f"M{f(cx)} {f(cy + sy * L)}V{f(cy)}H{f(cx + sx * L)}", "none", colour, .7))
    tab = rect(x + w / 2 - 19, y + h - 3.8, 38, 7.6, NOIR, colour, .4) + text(x + w / 2, y + h + 1.2, label, 2.9, colour, "Silkscreen", "middle")
    return "".join(c) + tab


def rug(x, y, w, h, fill, border, inner=None):
    out = rect(x, y, w, h, fill, border, .8) + rect(x + 2.2, y + 2.2, w - 4.4, h - 4.4, "none", inner or border, .3)
    fringe = "".join(line(x + 2 + k * 2, y - 1.4, x + 2 + k * 2, y, BONE, .25, 'opacity=".6"') + line(x + 2 + k * 2, y + h, x + 2 + k * 2, y + h + 1.4, BONE, .25, 'opacity=".6"')
                     for k in range(int((w - 3) / 2)))
    return shadow(out, .8, 1, .45) + fringe


def table_top(x, y):
    return shadow(rect(x, y, 88, 63, "url(#pPlanks)", WOOD2, .6), 1.4, 1.8, .55)


# ------------------------------------------------------------------ rooms
RX, RY = (RW - 88) / 2, RH - 63 - 7          # default deck zone
DECK_SHIFT = {"KITCHEN": -5, "MUSIC ROOM": 5, "WINE CELLAR": 3}


def room_contents(name):
    o = []
    rx, ry = RX, RY
    if name == "OBSERVATORY":
        o.append(circ(RW / 2, RH / 2 + 4, 50, "none", "#2B3442", 1.2) + circ(RW / 2, RH / 2 + 4, 47.5, "none", "#2B3442", .3, 'stroke-dasharray="1 2"'))
        o.append(rug(rx, ry, 88, 63, "#0C1018", BLUE, "#33475B"))
        cx, cy = rx + 44, ry + 31.5
        o.append(circ(cx, cy, 26, "none", BLUE, .35) + circ(cx, cy, 22, "none", BLUE, .2)
                 + "".join(line(cx + 22 * math.cos(a), cy + 22 * math.sin(a), cx + 26 * math.cos(a), cy + 26 * math.sin(a), BLUE, .3)
                           for a in [k * math.pi / 6 for k in range(12)]))
        cons = [(-30, -18), (-20, -24), (-12, -14), (-2, -20), (18, 10), (26, 2), (34, 14), (8, 20)]
        o.append(path(f"M{cx-30} {cy-18}L{cx-20} {cy-24}L{cx-12} {cy-14}L{cx-2} {cy-20} M{cx+18} {cy+10}L{cx+26} {cy+2}L{cx+34} {cy+14} M{cx+18} {cy+10}L{cx+8} {cy+20}", "none", "#7F9CB8", .3))
        o += [circ(cx + a, cy + b, .7, BONE) for a, b in cons]
        o.append(circ(cx, cy, 3, "none", AMBER, .35) + circ(cx, cy, .9, AMBER))
        o.append(shadow(circ(RW - 22, 24, 13, "#1E2530", "#3C4A5C", .5)))
        tel = (rect(-17, -2.7, 32, 5.4, BONE, NOIR, .3, 'rx="1.2"') + rect(12, -3.6, 5, 7.2, BRASS, NOIR, .25) + rect(-19, -1.9, 3, 3.8, ASH)
               + rect(-4, -3.3, 3, 6.6, BRASS) + line(0, 0, -7, 10, ASH, .9) + line(0, 0, 7, 10, ASH, .9) + line(0, 0, 0, -11, ASH, .9))
        o.append(g(shadow(tel, 1.4, 1.8), RW - 22, 24, -34))
        o.append(bookshelf(2.5, 44, 6.5, 52))
        o.append(lamp(RW - 22, 24, 22, .8))
    elif name == "LIBRARY":
        o.append(bookshelf(2.5, 26, 7, 19) + bookshelf(2.5, 67, 7, 38) + bookshelf(RW - 9.5, 26, 7, 19) + bookshelf(RW - 9.5, 67, 7, 38) + bookshelf(RW - 46, 2.5, 43, 6.5, False))
        o.append(rug(rx, ry, 88, 63, "url(#pPersian)", BRASS, RED))
        cx, cy = rx + 44, ry + 31.5
        o.append(path(f"M{cx} {cy-15}L{cx+22} {cy}L{cx} {cy+15}L{cx-22} {cy}Z", "#5A0916", BRASS, .4) + circ(cx, cy, 5, "#8E1428", BRASS, .35))
        o.append(armchair(RW - 22, 22, 205))
        o.append(shadow(circ(RW - 10, 15, 3.6, WOOD, WOODL, .3)) + circ(RW - 10, 15, 1.5, BONE) + circ(RW - 10, 15, .8, "#7A5A3A"))
        o.append(g(rect(-1.6, -2.8, 3.2, 5.6, NOIR, RED, .3, 'rx=".5"') + rect(-1.1, -2.2, 2.2, 4, "#3A0A14"), RW - 36, 32, 30))
        body = ('<path d="M0 0 l4 -2.5 l3 1 l1 4.5 l7.5 -1.2 l2 3.2 l-6.5 2 l-1 6.5 l3.2 6.2 l-2.2 1.2 l-4.2 -5.2 l-3.2 5.2 l-2.2 -1.2 '
                f'l2.2 -6.4 l-3.2 -6 l-5.5 3 l-1 -2.1 l5.2 -4.4 z" fill="none" stroke="{BONE}" stroke-width=".55" stroke-dasharray="1.3 .7"/>')
        o.append(g(body, RW - 47, 26, 22))
        o.append(rect(RW - 32, 6, 5, 5, NOIR, BONE, .25) + text(RW - 29.5, 9.9, "1", 2.8, BONE, "Bungee", "middle"))
        o.append(lamp(RW - 22, 22, 26, .9))
    elif name == "CHAPEL":
        for k, col in enumerate([RED, BLUE, AMBER, RED]):
            x0 = 14 + k * 26
            o.append(poly([(x0, 0), (x0 + 12, 0), (x0 + 26, 40), (x0 + 12, 40)], col, 'opacity=".13"'))
        o.append(rug(rx, ry, 88, 63, OX, BRASS, RED))
        o.append(path(f"M{rx+44} {ry+8}V{ry+52} M{rx+31} {ry+21}H{rx+57}", "none", BRASS, .6, 'opacity=".55"'))
        pews = [(RW - 16.5, 42 + k * 14) for k in range(4)] + [(2.5, 62.5), (2.5, 71.5)]
        for xk, yk in pews:
            o.append(shadow(rect(xk, yk, 14, 7, WOOD, WOODL, .3, 'rx=".6"') + rect(xk, yk, 14, 2, WOOD2)))
        alt = rect(RW - 44, 26, 38, 8, BONE, NOIR, .3) + rect(RW - 44, 26, 38, 2.4, RED) + rect(RW - 28, 28.8, 6, 4, BRASS)
        o.append(shadow(alt))
        o.append(shadow("".join(rect(RW - 40 + k * 3.4, 3, 2.4, 12 + (k % 3) * 3, ASH, NOIR, .2) for k in range(10))))
        o.append(candle(RW - 41, 30) + candle(RW - 9, 30))
    elif name == "MUSIC ROOM":
        o.append(rug(rx + 5, ry, 88, 63, "url(#pOriental)", BRASS, AMBER))
        piano = (path("M0 0H30V13C30 27 23 34 14 38C7 40 0 36 0 29Z", NOIR, BONE, .45)
                 + path("M2 4H28V13C28 25 22 31 14 34.5C8 36.5 2 33 2 28Z", "#16161A", ASH, .2)
                 + line(2, 4, 26, 30, ASH, .3) + rect(0, 0, 30, 4, "url(#gKeys)", NOIR, .2)
                 + "".join(rect(1.3 + k * 1.85, 0, .9, 2.4, NOIR) for k in range(15) if k % 7 not in (2, 6))
                 + rect(8, -6.5, 14, 4.2, WOOD, WOODL, .3, 'rx=".6"'))
        o.append(g(shadow(piano, 1.6, 2), RW - 38, 10))
        cello = (path("M0 -10C4.6 -10 5.6 -5 3.4 -1C5.6 3 4.6 10 0 10C-4.6 10 -5.6 3 -3.4 -1C-5.6 -5 -4.6 -10 0 -10Z", WOODH, WOOD2, .35)
                 + path("M-1.4 -3Q0 -4 1.4 -3M-1.4 3Q0 4 1.4 3", "none", NOIR, .3) + line(0, -16, 0, 10, BONE, .45) + rect(-.8, -17.5, 1.6, 2, NOIR))
        o.append(g(shadow(cello), 9, 66, 14))
        gram = (circ(0, 0, 4.4, WOOD, WOODL, .3) + circ(0, 0, 3.4, NOIR) + circ(0, 0, .7, RED) + path("M2 -2L8 -9", "none", BRASS, .6)
                + circ(9, -10, 3.4, BRASS, NOIR, .25) + circ(9, -10, 1.6, NOIR))
        o.append(g(shadow(gram), 9, 98))
        o.append(shadow(line(RW - 9, 72, RW - 9, 82, ASH, .5) + rect(RW - 14, 69, 10, 3.2, NOIR, ASH, .3)))
        o.append(chair(RW - 9, 90, 180))
        o.append(lamp(RW - 24, 28, 24, .7))
    elif name == "GRAND HALL":
        sx, sy, sw_, sh_ = RW - 36, 2.5, 33, 30
        o.append(shadow(rect(sx, sy, sw_, sh_, M1, NOIR, .3)))
        o.append("".join(line(sx, sy + 2 + k * 3, sx + sw_, sy + 2 + k * 3, "#55555E", .35) for k in range(10)))
        o.append(rect(sx + 9, sy, 15, sh_, RED) + rect(sx + 9, sy, 15, sh_, "none", BRASS, .3)
                 + "".join(line(sx + 9, sy + 2 + k * 3, sx + 24, sy + 2 + k * 3, BRASS, .25) for k in range(10)))
        o.append(rect(sx - 1.5, sy, 2.4, sh_ + 2, WOODH) + rect(sx + sw_ - .9, sy, 2.4, sh_ + 2, WOODH)
                 + circ(sx - .3, sy + sh_ + 2, 1.8, BRASS) + circ(sx + sw_ + .3, sy + sh_ + 2, 1.8, BRASS))
        cx, cy = RW / 2, RH / 2 + 12
        o.append(lamp(cx, cy, 38, 1))
        o.append(circ(cx, cy, 11, "none", BRASS, .5) + circ(cx, cy, 6.5, "none", BRASS, .35)
                 + "".join(line(cx, cy, cx + 11 * math.cos(a), cy + 11 * math.sin(a), BRASS, .3) + circ(cx + 11 * math.cos(a), cy + 11 * math.sin(a), 1, AMBER)
                           + circ(cx + 6.5 * math.cos(a + .39), cy + 6.5 * math.sin(a + .39), .55, BONE)
                           for a in [k * math.pi / 4 for k in range(8)]) + circ(cx, cy, 2.4, AMBER))
        for k, (px, py) in enumerate([(22, 60), (RW - 22, 60), (22, 94), (RW - 22, 94)]):
            o.append(shadow(circ(px, py, 9, NOIR, BRASS, .7)) + circ(px, py, 7.4, "none", BRASS, .25, 'stroke-dasharray="1 .8"')
                     + text(px, py + 1.5, f"P{k + 1}", 4.2, BONE, "Bungee", "middle"))
        o.append(text(cx, RH - 4, "&gt; START HERE &lt;", 3.4, RED, "Silkscreen", "middle"))
    elif name == "KITCHEN":
        o.append(shadow(rect(RW - 13, 2.5, 10.5, RH - 5, "#2C2C31", BONE, .3) + rect(RW - 48, 2.5, 36, 10.5, "#2C2C31", BONE, .3)))
        o.append(rect(RW - 46, 3.5, 22, 8.5, NOIR, ASH, .25) + "".join(circ(RW - 42 + j * 5, 6, 1.7, "none", ASH, .4) + circ(RW - 42 + j * 5, 10, 1.7, "none", ASH, .4) for j in range(4)))
        o.append(shadow(circ(RW - 37, 6, 2.6, "#5A5A62", NOIR, .25) + line(RW - 37, 6, RW - 31, 3, "#5A5A62", .6), .5, .6))
        o.append(rect(RW - 12, 30, 8.5, 12, GLASS, BONE, .3) + circ(RW - 7.8, 36, 1.1, BONE) + line(RW - 7.8, 36, RW - 7.8, 31.5, ASH, .4))
        o.append(rect(RW - 12, RH - 30, 8.5, 9, NOIR, AMBER, .5) + circ(RW - 7.8, RH - 25.5, 2.2, AMBER) + lamp(RW - 7.8, RH - 25.5, 14, .9))
        o.append(rect(RW - 12, 56, 8.5, 12, WOOD, WOODL, .3) + "".join(line(RW - 12, 58 + k * 2.5, RW - 3.5, 58 + k * 2.5, WOOD2, .3) for k in range(4)))
        o.append(shadow(rect(2.5, 68, 11, 17, "#4A4A52", BONE, .35) + line(4.5, 74, 11.5, 74, NOIR, .3) + rect(10.5, 70, .8, 3, BONE)))
        tx, ty = rx - 5, ry
        o.append(table_top(tx, ty))
        for k in range(4):
            o.append(chair(tx + 14 + k * 20, ty - 4, 0) + chair(tx + 14 + k * 20, ty + 67, 180))
        o.append(lamp(tx + 44, ty + 31, 40, .9))
    elif name == "GREENHOUSE":
        o.append(path(f"M0 {RH/3}H{RW} M0 {2*RH/3}H{RW} M{RW/3} 0V{RH} M{2*RW/3} 0V{RH}", "none", "#0A0F13", 1.2, 'opacity=".6"'))
        o.append(shadow(rect(RW - 52, 2.5, 49.5, 12, "#3A2A22", WOODL, .35)))
        for k in range(4):
            o.append(plant(RW - 46 + k * 12.5, 8.5, 5.2, flowers=True, pot=False))
        o.append(text(RW - 27.5, 19, "DIGITALIS PURPUREA", 2.2, RED, "Silkscreen", "middle"))
        o.append(table_top(rx, ry))
        o.append(circ(rx + 8, ry + 8, 2.6, MUD) + circ(rx + 80, ry + 55, 3, MUD, extra='opacity=".7"') + circ(rx + 84, ry + 8, 1.6, MUD))
        for py in (46, 72):
            o.append(plant(9.5, py, 5.6) + (plant(RW - 9.5, py, 5.6, flowers=True) if py == 72 else ""))
        o.append(plant(9.5, 97, 5.6))
        can = rect(-3, -2.2, 6, 4.4, "#6E7E86", NOIR, .25, 'rx=".8"') + line(3, -1, 6.5, -3, "#6E7E86", .8)
        o.append(g(shadow(can, .6, .7), 82, 30, -20))
        o.append(lamp(RW / 2, RH / 2, 40, .35))
    elif name == "SERVER ROOM":
        o.append(circ(RW - 30, 72, 40, "url(#gScreen)"))
        o.append(shadow(rect(10, 30, RW - 20, 3.6, "#2C2C31", ASH, .3)))
        for k, col in enumerate([RED, BLUE, AMBER, BONE]):
            o.append(path(f"M{RW-60+k*2.5} 33 V40 Q{RW-60+k*2.5} 42 {RW-58+k*2.5} 42", "none", col, .45, 'opacity=".8"'))
        for k in range(2):
            x0 = RW - 62 + k * 30
            rack = [rect(x0, 42, 26, RH - 50, NOIR, BONE, .45)]
            for j in range(9):
                yj = 45 + j * 6.4
                rack.append(rect(x0 + 2, yj, 22, 4.6, "#232328") + rect(x0 + 8, yj + 1.7, 12, 1.2, ASH, extra='opacity=".55"'))
                rack.append(circ(x0 + 4.3, yj + 2.3, .75, RED if (j * 3 + k) % 5 == 1 else (AMBER if (j + k) % 4 == 0 else BONE)))
            o.append(shadow("".join(rack), 1.5, 1.8))
        o.append(circ(RW - 49, 42 + 3 * 6.4 + 2.3, 6, "url(#gRed)"))
        # recharge station
        sx, sy, sw, sh = 7, 44, 44, 52
        o.append(circ(sx + sw / 2, sy + sh / 2, 34, "url(#gRed)", extra='opacity=".7"'))
        o.append(shadow(rect(sx, sy, sw, sh, NOIR, RED, .8), 1.4, 1.8))
        o.append(rect(sx + 1.6, sy + 1.6, sw - 3.2, sh - 3.2, "none", RED, .25, 'stroke-dasharray="1 .7"'))
        o.append(text(sx + sw / 2, sy + 8, "RECHARGE", 4.6, RED, "Bungee", "middle"))
        o.append(text(sx + sw / 2, sy + 12.5, "STATION", 2.6, BONE, "Silkscreen", "middle"))
        for k in range(3):
            o.append(tok_svg(sx + 9 + k * 13, sy + 25, 5))
        o.append(text(sx + sw / 2, sy + 40, "REFILL TO 3", 3.4, BONE, "Bungee", "middle"))
        o.append(text(sx + sw / 2, sy + 45.5, "NO DECK HERE", 2.2, ASH, "Silkscreen", "middle"))
        desk = rect(0, 0, 30, 11, WOOD, WOODL, .3) + rect(9, 1, 13, 7.5, NOIR, BONE, .3) + rect(10, 2, 11, 5.5, "#0E1A24")
        o.append(g(shadow(desk), RW - 36, 15))
        o.append(text(RW - 25.5, 18.6, "&gt; SELECT *", 1.3, "#9FB6CC", "IBM Plex Mono"))
        o.append(text(RW - 25.5, 20.4, "&#9608;&#9608;&#9608; ERR", 1.3, RED, "IBM Plex Mono"))
        o.append(chair(RW - 21, 30, 180, "#2C2C31"))
    elif name == "WINE CELLAR":
        o.append(path(f"M0 38Q{RW/2} 30 {RW} 38 M0 76Q{RW/2} 68 {RW} 76", "none", "#141213", 1.4, 'opacity=".7"'))
        o.append(barrel(10, 72))
        for k in range(3):
            o.append(barrel(RW - 30.5 + k * 12, 9))
        rack = [rect(RW - 12, 64, 9.5, RH - 68, WOOD2, WOODL, .35)]
        for j in range(7):
            for i in range(2):
                rack.append(circ(RW - 9.6 + i * 4.6, 67.5 + j * 5.4, 1.5, "#3C0A14", NOIR, .2) + circ(RW - 9.6 + i * 4.6, 67.5 + j * 5.4, .55, "#1E3A2A"))
        o.append(shadow("".join(rack)))
        o.append(table_top(rx + 3, ry))
        o.append(candle(rx + 9, ry + 6) + circ(rx + 83, ry + 57, 1.6, "none", BONE, .3) + circ(rx + 79, ry + 58, 1.6, "none", BONE, .3))
        for cx_, sx_ in [(0, 1), (RW, -1)]:
            o.append(path(f"M{cx_} 10Q{cx_+sx_*4} 4 {cx_+sx_*10} 0 M{cx_} 6Q{cx_+sx_*2.5} 2.5 {cx_+sx_*6} 0 M{cx_} 0L{cx_+sx_*8} 8",
                          "none", BONE, .18, 'opacity=".55"'))
        o.append(lamp(rx + 9, ry + 6, 30, .9))
    return "".join(o)


ROOM_FLOOR = {
    "OBSERVATORY": "url(#pStars)", "LIBRARY": "url(#pParquet)", "CHAPEL": "url(#pStone)",
    "MUSIC ROOM": "url(#pHerring)", "GRAND HALL": "url(#pMarble)", "KITCHEN": "url(#pTiles)",
    "GREENHOUSE": "url(#pGlass)", "SERVER ROOM": "url(#pRaised)", "WINE CELLAR": "url(#pCellar)",
}


def moonlight(r, c):
    o = []
    if r == 0:
        for k in (.3, .7):
            wx = RW * k
            o.append(poly([(wx - 9, 0), (wx + 9, 0), (wx + 21, 44), (wx + 3, 44)], "url(#gMoonD)"))
            o.append(line(wx + .3, 0, wx + 12, 44, NOIR, .6, 'opacity=".25"'))
    if r == 2:
        for k in (.3, .7):
            wx = RW * k
            o.append(poly([(wx - 9, RH), (wx + 9, RH), (wx + 21, RH - 34), (wx + 3, RH - 34)], "url(#gMoonU)"))
    if c == 0:
        for k in (.35, .75):
            wy = RH * k
            o.append(poly([(0, wy - 9), (0, wy + 9), (40, wy + 21), (40, wy + 3)], "url(#gMoonR)"))
    if c == 2:
        for k in (.35, .75):
            wy = RH * k
            o.append(poly([(RW, wy - 9), (RW, wy + 9), (RW - 40, wy + 21), (RW - 40, wy + 3)], "url(#gMoonL)"))
    return "".join(o)


def walls(x, y, r, c):
    wall, ws = BONE, 2.6
    sides = {"top": r > 0, "bottom": r < 2, "left": c > 0, "right": c < 2}
    o = []

    def seg(x1, y1, x2, y2):
        return line(x1, y1, x2, y2, wall, ws, 'stroke-linecap="square"')
    for side, door in sides.items():
        if side in ("top", "bottom"):
            yy = y if side == "top" else y + RH
            if door:
                mid = x + RW * DOOR_FRAC
                d = -1 if side == "top" else 1
                o.append(seg(x, yy, mid - DOOR / 2, yy) + seg(mid + DOOR / 2, yy, x + RW, yy))
                o.append(rect(mid - DOOR / 2, yy - .8, DOOR, 1.6, WOODH))
                o.append(path(f"M{f(mid - DOOR / 2)} {f(yy + d * DOOR)} A{DOOR} {DOOR} 0 0 {0 if d > 0 else 1} {f(mid + DOOR / 2)} {f(yy)}", "none", wall, .25, 'stroke-dasharray=".8 .6"'))
                o.append(line(mid - DOOR / 2, yy, mid - DOOR / 2, yy + d * DOOR, wall, .9))
            else:
                o.append(seg(x, yy, x + RW, yy))
        else:
            xx = x if side == "left" else x + RW
            if door:
                mid = y + RH / 2
                d = -1 if side == "left" else 1
                o.append(seg(xx, y, xx, mid - DOOR / 2) + seg(xx, mid + DOOR / 2, xx, y + RH))
                o.append(rect(xx - .8, mid - DOOR / 2, 1.6, DOOR, WOODH))
                o.append(path(f"M{f(xx + d * DOOR)} {f(mid - DOOR / 2)} A{DOOR} {DOOR} 0 0 {1 if d > 0 else 0} {f(xx)} {f(mid + DOOR / 2)}", "none", wall, .25, 'stroke-dasharray=".8 .6"'))
                o.append(line(xx, mid - DOOR / 2, xx + d * DOOR, mid - DOOR / 2, wall, .9))
            else:
                o.append(seg(xx, y, xx, y + RH))
    return "".join(o)


def plaque(i, x, y):
    name, ic, search, ptitle, ptext, passage = bp.ROOMS[i]
    lib = name == "LIBRARY"
    acc = RED if lib else BONE
    w = 18 + len(name) * 4.15
    o = [shadow(rect(x + 4, y + 4, w, 10.5, acc, NOIR, .35), 1, 1.2, .6)]
    o.append(rect(x + 4, y + 4, 10.5, 10.5, NOIR) + icon(ic, x + 5.6, y + 5.6, 7.3, acc, 2.2))
    o.append(rect(x + 15.2, y + 5, w - 12, 8.5, "none", NOIR, .25))
    o.append(text(x + 17.2, y + 12, name, 5.4, NOIR if not lib else BONE))
    o.append(text(x + 4 + w - 1.6, y + 3.1, f"N&#176;{i + 1:02d}", 2.4, ASH, "IBM Plex Mono", "end"))
    if search and not lib:
        o.append(rect(x + 4, y + 16, 15, 4.2, NOIR) + text(x + 11.5, y + 19.1, "SEARCH", 2.4, BONE, "Silkscreen", "middle"))
        return "".join(o)
    tagtxt = {"LIBRARY": "SEARCH OR ACCUSE", "GRAND HALL": "START", "SERVER ROOM": "RECHARGE"}[name]
    srv = name == "SERVER ROOM"
    tc = RED if (lib or srv) else BONE
    tag = (f'<span style="font-family:Silkscreen;font-size:2.4px;background:{tc};color:{NOIR if tc == BONE else BONE};'
           f'padding:.25px 1px;margin-right:1.2px;vertical-align:.3px">{tagtxt}</span>')
    txt = bp.esc(ptext).replace("3 Query Tokens", "3 " + tok())
    body = f'{tag}{txt}'
    o.append(html_box(x + 4, y + 16, 80, 22, body,
                      f"font:400 3.6px Archivo;color:{BONE};line-height:1.32;background:{NOIR}eb;padding:1.1px 1.6px;"
                      f"border-left:.7px solid {tc};display:inline-block"))
    return "".join(o)


def room(i):
    name, ic, search, ptitle, ptext, passage = bp.ROOMS[i]
    r, c = divmod(i, 3)
    x, y = room_xy(r, c)
    o = [f'<clipPath id="cr{i}"><rect x="{f(x)}" y="{f(y)}" width="{f(RW)}" height="{f(RH)}"/></clipPath>']
    o.append(rect(x, y, RW, RH, ROOM_FLOOR[name]))
    inner = [moonlight(r, c), rect(0, 0, RW, RH, "url(#gVig)")]
    inner.append(rect(0, 0, RW, 2.6, "#000", extra='opacity=".35"') + rect(0, 0, 2.6, RH, "#000", extra='opacity=".35"'))
    inner.append(room_contents(name))
    if search:
        dx = DECK_SHIFT.get(name, 0)
        col = {"OBSERVATORY": "#7F9CB8", "LIBRARY": BRASS, "CHAPEL": BRASS, "MUSIC ROOM": AMBER}.get(name, BONE)
        inner.append(deck_zone(RX + dx, RY, colour=col))
    o.append(f'<g clip-path="url(#cr{i})">' + g("".join(inner), x, y) + "</g>")
    o.append(walls(x, y, r, c))
    o.append(plaque(i, x, y))
    return "".join(o)


def passages():
    spots = {"OBSERVATORY": ("WINE CELLAR", "br"), "CHAPEL": ("GREENHOUSE", "bl"),
             "GREENHOUSE": ("CHAPEL", "br"), "WINE CELLAR": ("OBSERVATORY", "bl")}
    out = []
    for i, rm in enumerate(bp.ROOMS):
        if rm[0] in spots:
            r, c = divmod(i, 3)
            x, y = room_xy(r, c)
            dest, corner = spots[rm[0]]
            tx = x + RW - 21.5 if corner == "br" else x + 7.5
            out.append(trapdoor(tx, y + RH - 29, dest))
    return "".join(out)


# ------------------------------------------------------------------ hallways & outside
def hallways():
    iw, ih = MW - 2 * WALL, MH - 2 * WALL
    o = [rect(IX, IY, iw, ih, "url(#pHall)"), rect(IX, IY, iw, ih, "url(#gVig)", extra='opacity=".6"')]
    runs = []
    for k in range(2):
        cy = IY + (k + 1) * RH + k * HALL + HALL / 2
        runs.append((IX + 4, cy - 4.5, iw - 8, 9))
        cx = IX + (k + 1) * RW + k * HALL + HALL / 2
        runs.append((cx - 4.5, IY + 4, 9, ih - 8))
    for x, y, w, h in runs:
        o.append(shadow(rect(x, y, w, h, OX), .8, 1, .5))
    for x, y, w, h in runs:
        o.append(rect(x + 1, y + 1, w - 2, h - 2, "none", BRASS, .3) + rect(x + 2, y + 2, w - 4, h - 4, "none", RED, .25, 'stroke-dasharray="2 1.2"'))
    for i in range(2):
        for j in range(2):
            cx = IX + (j + 1) * RW + j * HALL + HALL / 2
            cy = IY + (i + 1) * RH + i * HALL + HALL / 2
            o.append(shadow(circ(cx, cy, 8, OX, BRASS, .5)) + circ(cx, cy, 5.5, "none", BRASS, .3)
                     + path(f"M{f(cx)} {f(cy-5)}L{f(cx+1.2)} {f(cy)}L{f(cx)} {f(cy+5)}L{f(cx-1.2)} {f(cy)}Z", BRASS)
                     + path(f"M{f(cx-5)} {f(cy)}L{f(cx)} {f(cy+1.2)}L{f(cx+5)} {f(cy)}L{f(cx)} {f(cy-1.2)}Z", RED))
    for k in range(3):
        for j in range(2):
            cy = IY + (j + 1) * RH + j * HALL
            cx = IX + k * (RW + HALL) + RW / 2 + (28 if k != 1 else -30)
            o.append(lamp(cx, cy + HALL / 2, 16, .55))
    clock = (rect(-4.5, -3, 9, 7, WOOD, WOODL, .35) + circ(0, .4, 2.6, BONE, NOIR, .25)
             + line(0, .4, 0, -1.6, NOIR, .35) + line(0, .4, -1.7, .4, RED, .35))
    o.append(g(shadow(clock), IX + RW + HALL / 2, IY + 8))
    o.append(g(shadow(clock), IX + 2 * RW + HALL * 1.5, IY + ih - 8, 180))
    # muddy footprints: Greenhouse -> Library (size 44...)
    x0 = IX + RW + 3.8
    y_start = IY + 2 * (RH + HALL) + RH / 2 - 10
    y_end = IY + RH / 2 + 12
    n = int((y_start - y_end) / 7)
    for k in range(n):
        yy = y_start - k * 7
        xx = x0 + (2.4 if k % 2 else 0)
        op = f'opacity="{.85 - k * .016:.2f}"'
        o.append(ell(xx, yy, 1.1, 1.9, MUD, op) + ell(xx, yy + 2.6, .9, .8, MUD, op))
    o.append(rect(x0 - 2, y_start + 4.6, 15.5, 4.6, NOIR, AMBER, .25) + text(x0 - .8, y_start + 8, "SIZE 44?", 2.6, AMBER, "Silkscreen"))
    o.append(plant(IX + 6.5, IY + RH + HALL / 2, 4) + plant(IX + iw - 6.5, IY + 2 * RH + HALL * 1.5, 4))
    return "".join(o)


def grounds():
    o = []
    fx = IX + RW + HALL / 2
    o.append(rect(fx - 12, MY + MH, 24, H - (MY + MH) + BLEED, "url(#pGravel)"))
    for k in range(int(MW / 9) + 2):
        hx = MX - 4 + k * 9
        if abs(hx - fx) > 16:
            o.append(plant(hx, MY + MH + 6.5, 3.4, pot=False))
        o.append(plant(hx, MY - 6.2, 3.2, pot=False))
    for k in range(int(MH / 9) + 1):
        hy = MY + 2 + k * 9
        o.append(plant(MX - 6.2, hy, 3.2, pot=False) + plant(MX + MW + 6.2, hy, 3.2, pot=False))
    return "".join(o)


def outer_walls():
    box_ = f"M{MX + WALL / 2} {MY + WALL / 2}h{MW - WALL}v{MH - WALL}h{-(MW - WALL)}z"
    o = [path(box_, "none", "#000", WALL, 'transform="translate(1.4,1.8)" opacity=".5"'), path(box_, "none", BONE, WALL),
         path(f"M{MX + WALL - .6} {MY + WALL - .6}h{MW - 2 * WALL + 1.2}v{MH - 2 * WALL + 1.2}h{-(MW - 2 * WALL + 1.2)}z", "none", "#CFC8B8", .5)]
    for i in range(9):
        r, c = divmod(i, 3)
        x, y = room_xy(r, c)
        wins = []
        if r == 0:
            wins += [("h", x + RW * .3, MY), ("h", x + RW * .7, MY)]
        if r == 2:
            wins += [("h", x + RW * .3, MY + MH - WALL), ("h", x + RW * .7, MY + MH - WALL)]
        if c == 0:
            wins += [("v", MX, y + RH * .35), ("v", MX, y + RH * .75)]
        if c == 2:
            wins += [("v", MX + MW - WALL, y + RH * .35), ("v", MX + MW - WALL, y + RH * .75)]
        for kind, a, b in wins:
            if kind == "h":
                o.append(rect(a - 9, b + .7, 18, WALL - 1.4, GLASS) + line(a - 9, b + WALL / 2, a + 9, b + WALL / 2, BONE, .3)
                         + line(a, b + .7, a, b + WALL - .7, BONE, .3))
            else:
                o.append(rect(a + .7, b - 9, WALL - 1.4, 18, GLASS) + line(a + WALL / 2, b - 9, a + WALL / 2, b + 9, BONE, .3)
                         + line(a + .7, b, a + WALL - .7, b, BONE, .3))
    fx = IX + RW + HALL / 2
    o.append(rect(fx - 10, MY + MH - WALL - .4, 20, WALL + .8, OX) + rect(fx - .3, MY + MH - WALL, .6, WALL, BRASS)
             + circ(fx - 2, MY + MH - WALL / 2, .5, BRASS) + circ(fx + 2, MY + MH - WALL / 2, .5, BRASS))
    for k in range(3):
        o.append(rect(fx - 13, MY + MH + .5 + k * 2.2, 26, 2.2, "#3A3A40" if k % 2 else "#45454C"))
    o.append(text(fx, MY + MH + 11.6, "FRONT DOOR", 2.6, BONE, "Silkscreen", "middle"))
    for tx, ty in [(MX, MY), (MX + MW, MY), (MX, MY + MH), (MX + MW, MY + MH)]:
        tower = circ(tx, ty, 7, "#2E2E34", BONE, 1.1) + "".join(line(tx, ty, tx + 7 * math.cos(a), ty + 7 * math.sin(a), "#45454C", .4)
                                                               for a in [k * math.pi / 6 for k in range(12)]) + circ(tx, ty, 1.6, BRASS)
        o.append(shadow(tower, 1.6, 2))
    return "".join(o)


def frame():
    o = [rect(6, 6, W - 12, H - 12, "none", BONE, .7), rect(8, 8, W - 16, H - 16, "none", RED, .3)]
    for cx, cy, sx, sy in [(6, 6, 1, 1), (W - 6, 6, -1, 1), (6, H - 6, 1, -1), (W - 6, H - 6, -1, -1)]:
        o.append(path(f"M{cx} {cy + sy * 14}V{cy}H{cx + sx * 14} M{cx + sx * 3} {cy + sy * 10}V{cy + sy * 3}H{cx + sx * 10}", "none", RED, .8)
                 + rect(cx + (0 if sx > 0 else -3), cy + (0 if sy > 0 else -3), 3, 3, RED))
    return "".join(o)


# ------------------------------------------------------------------ sidebar
def box(x, y, w, h, title):
    return (rect(x, y, w, h, "#0E0E10", BONE, .8) + rect(x + 1.6, y + 1.6, w - 3.2, h - 3.2, "none", GRAPH, .3)
            + rect(x + 4, y - 3, len(title) * 3.4 + 7, 6, NOIR) + text(x + 7, y + 1.5, title, 4, RED, "Silkscreen"))


def sidebar():
    o = [f'<image href="{bp.LOGO}" x="{SX}" y="12" width="{SW}" height="{f(SW * 655 / 1150)}"/>']
    o.append(text(SX + 2, 89, "RAVENSCROFT MANOR", 5.6, BONE))
    o.append(html_box(SX + 2, 92, SW - 4, 14,
                      f"11:45 PM. Sir Victor is found dead in his Library. <b style='color:{RED}'>Be the first to name the killer.</b>",
                      f"font:400 3.6px Archivo;color:{ASH};line-height:1.35"))
    # ---- your turn
    ty = 114
    o.append(box(SX, ty, SW, 82, "YOUR TURN"))
    steps = [("steps", "1. MOVE", "Up to 2 rooms. You may also stay."),
             ("magnifier", "2. ACT", f"<b>Search</b> (rooms with a deck), <b>Recharge</b> (Server Room) or <b>Accuse</b> (Library)."),
             ("terminal", "ANYTIME: QUERY", f"On your phone: 1 {tok()} = 1 search, max 2 conditions.")]
    for k, (ic, t, d) in enumerate(steps):
        yy = ty + 7 + k * 24.5
        hl = k == 2
        o.append(rect(SX + 5, yy, 16, 16, RED if hl else NOIR, RED, .6) + icon(ic, SX + 7, yy + 2, 12, BONE, 2))
        o.append(text(SX + 24.5, yy + 5.2, t, 4.4, RED))
        o.append(html_box(SX + 24.5, yy + 6.8, SW - 29, 15, d, f"font:400 3.4px Archivo;color:{BONE};line-height:1.3"))
    # ---- golden rules
    gy = ty + 90
    o.append(box(SX, gy, SW, 40, "GOLDEN RULES"))
    o.append(html_box(SX + 5, gy + 7, SW - 10, 32,
                      f"<div style='border-left:1px solid {RED};padding-left:2px;margin-bottom:2.5px'>&#8220;Find the same clue <b>twice</b>, and it&#8217;s probably true.&#8221;</div>"
                      f"<div style='border-left:1px solid {RED};padding-left:2px'>&#8220;<b style='color:{RED}'>0 suspects found?</b> One of your clues is fake!&#8221;</div>",
                      f"font:italic 400 4.3px Archivo;color:{BONE};line-height:1.35"))
    # ---- W.A.T.S.O.N. updates
    wy = gy + 48
    o.append(box(SX, wy, SW, 58, "W.A.T.S.O.N. UPDATES"))
    for k in range(12):
        xx = SX + 5.5 + k * 9.1
        up = (k + 1) % 4 == 0
        o.append(rect(xx, wy + 8, 8, 10, RED if up else NOIR, RED if up else BONE, .4)
                 + text(xx + 4, wy + 15.2, str(k + 1), 4, BONE if up else ASH, "Bungee", "middle"))
        if up:
            o.append(path(f"M{f(xx + 4)} {f(wy + 18.6)}V{f(wy + 21.5)}", "none", RED, .5) + tok_svg(xx + 4, wy + 25.2, 3.4, RED))
            o.append(text(xx + 4, wy + 32, "+1", 2.6, RED, "Bungee", "middle"))
    o.append(text(SX + 5.5, wy + 6, "ROUND", 2.2, ASH, "Silkscreen", "start"))
    o.append(html_box(SX + 5, wy + 35, SW - 10, 22,
                      f"Every 4 rounds the host taps <b>End round</b>: everyone gets <b style='color:{RED}'>+1 {tok()}</b> (max 3) and the app reveals <b>1 true trait</b> of the killer.",
                      f"font:400 3.3px Archivo;color:{BONE};line-height:1.3"))
    # ---- accuse
    ay = wy + 66
    o.append(box(SX, ay, SW, H - 14 - ay, "ACCUSE"))
    o.append(html_box(SX + 5, ay + 6, SW - 10, H - 22 - ay,
                      f"In the <b style='color:{RED}'>Library</b>, say the killer&#8217;s full profile out loud:"
                      f"<div style='font-style:italic;border-left:1px solid {RED};padding-left:2px;margin:2px 0'>&#8220;The killer is ___: 47 years old, 1.86 m tall, size 44 shoes, left-handed!&#8221;</div>"
                      f"<span style='color:{ASH}'>Wrong? Back to the Grand Hall and lose all your {tok()}.</span>"
                      f"<div style='margin-top:3px;font-size:3.1px;color:{ASH}'>The profile, trait by trait (check your notebook):</div><div style='margin-top:1.2px'>{PROFILE_CHIPS}</div>",
                      f"font:400 4px Archivo;color:{BONE};line-height:1.38"))
    return "".join(o)


def board_svg():
    vb = f"{-(BLEED + SLUG)} {-(BLEED + SLUG)} {W + 2 * (BLEED + SLUG)} {H + 2 * (BLEED + SLUG)}"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{W + 2 * (BLEED + SLUG)}mm" height="{H + 2 * (BLEED + SLUG)}mm">',
         f"<defs>{DEFS}</defs>",
         rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, NOIR),
         rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, "url(#pRain)"),
         grounds(), hallways()]
    o += [room(i) for i in range(9)]
    o += [outer_walls(), frame(), sidebar(), "</svg>"]
    return "".join(o)


def board_html():
    pw, ph = W + 2 * (BLEED + SLUG), H + 2 * (BLEED + SLUG)
    tx = ty = BLEED + SLUG
    body = f'<div class="sheet" style="width:{pw}mm;height:{ph}mm">{board_svg()}{bp.cropmarks(tx, ty, W, H)}</div>'
    css = (".sheet > svg{position:absolute;left:0;top:0} svg text{letter-spacing:.02em}"
           " .sh *{fill:#000 !important;stroke:#000 !important} .sh text, .sh foreignObject{display:none}")
    return bp.page("The Last Query - board A2", pw, ph, body, css)


if __name__ == "__main__":
    (bp.SRC / "board_A2.html").write_text(board_html())
    print("board written")
