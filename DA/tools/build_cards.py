#!/usr/bin/env python3
"""Clue cards V2 (2026-11-25): 34 evidence cards to scan + 6 bonus cards (effect printed, QR to keep them in the app),
"Case File" style, 63 x 88 mm. Data: game design section 8 (Case 1).

The scannable cards never print the clue: only the object, its room and a QR code.
Run through build_print.py (it calls main()).
"""
import build_print as bp
import card_art

C = bp.C
NOIR, BONE, RED, OX, AMBER, BLUE, ASH, GRAPH = (C[k] for k in ("noir", "bone", "red", "oxblood", "amber", "blue", "ash", "graphite"))
BRASS = "#C9923A"
WOOD, WOOD2, WOODL = "#5A3A2C", "#3A2621", "#7A5240"
LEAF, LEAF2 = "#2F4F3B", "#4A7556"
MUD, PAPER, DUST = "#6B4A32", "#E9E1CC", "#8A857A"
PH = "#17171A"                                     # photo background

ROOM_CODE = {"LIBRARY": "LIB", "GREENHOUSE": "GRE", "OBSERVATORY": "OBS", "CHAPEL": "CHA",
             "MUSIC ROOM": "MUS", "KITCHEN": "KIT", "WINE CELLAR": "CEL"}

# (room, object, illustration key) - order = game design section 8
OBJECTS = [
    ("LIBRARY", "Wet sock on the rug", "sock"), ("LIBRARY", "Teacup handle", "teacup"), ("LIBRARY", "Ashtray", "ashtray"),
    ("LIBRARY", "Victor's diary", "diary"), ("LIBRARY", "Hair on Victor's jacket", "jacket"),
    ("GREENHOUSE", "Muddy footprint", "footprint"), ("GREENHOUSE", "Broken branch", "branch"),
    ("GREENHOUSE", "Watering schedule", "clipboard"), ("GREENHOUSE", "Plant label", "label"), ("GREENHOUSE", "Petals on the floor", "petals"),
    ("OBSERVATORY", "Telescope eyepiece", "eyepiece"), ("OBSERVATORY", "Hair on the telescope", "telescope"),
    ("OBSERVATORY", "Star chart", "starchart"), ("OBSERVATORY", "Security camera", "camera"), ("OBSERVATORY", "Reading glasses", "glasses"),
    ("CHAPEL", "Glove on a pew", "glove"), ("CHAPEL", "Confessional", "confessional"), ("CHAPEL", "Hymn book", "hymn"),
    ("CHAPEL", "Wedding photo", "photo"),
    ("MUSIC ROOM", "Piano bench", "bench"), ("MUSIC ROOM", "Sheet music", "sheet"), ("MUSIC ROOM", "Opera programme", "programme"),
    ("MUSIC ROOM", "Broken metronome", "metronome"), ("MUSIC ROOM", "Curtains", "curtains"),
    ("KITCHEN", "Spilled flour", "flour"), ("KITCHEN", "Top cupboard", "cupboard"), ("KITCHEN", "Dinner menu", "menu"),
    ("KITCHEN", "Grocery list", "grocery"), ("KITCHEN", "Sugar bowl", "sugar"),
    ("WINE CELLAR", "Behind the barrels", "barrels"), ("WINE CELLAR", "Dusty barrel", "barrel"), ("WINE CELLAR", "Poker IOU", "iou"),
    ("WINE CELLAR", "Dusty bottle", "bottle"), ("WINE CELLAR", "Footprint in the dust", "dustprint"),
]
BONUS = [
    ("OBSERVATORY", "Spare Battery", "battery", "+1 QUERY TOKEN", "Take 1 Query Token (max 3)."),
    ("MUSIC ROOM", "Spare Battery", "battery", "+1 QUERY TOKEN", "Take 1 Query Token (max 3)."),
    ("KITCHEN", "Spare Battery", "battery", "+1 QUERY TOKEN", "Take 1 Query Token (max 3)."),
    ("GREENHOUSE", "Running Shoes", "shoes", "MOVE AGAIN", "Move up to 2 more rooms this turn."),
    ("CHAPEL", "Running Shoes", "shoes", "MOVE AGAIN", "Move up to 2 more rooms this turn."),
    ("WINE CELLAR", "Master Key", "key", "PEEK", "Look at the top card of any room deck, then put it back."),
]


# ------------------------------------------------------------------ illustrations (48 x 48)
def L(x1, y1, x2, y2, c=BONE, w=1.2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'


def R(x, y, w, h, f, s="none", sw=0, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="{sw}" {extra}/>'


def O(cx, cy, r, f, s="none", sw=0, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" stroke="{s}" stroke-width="{sw}" {extra}/>'


def P(d, f="none", s="none", sw=0, extra=""):
    return f'<path d="{d}" fill="{f}" stroke="{s}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def lines(x, y, w, n, gap=3.2, c=GRAPH, sw=.9):
    return "".join(L(x, y + k * gap, x + w * (.65 if k == n - 1 else 1), y + k * gap, c, sw) for k in range(n))


def hair(d):
    return P(d, "none", BONE, .7)


ART = {
    "sock": R(6, 30, 36, 10, OX, rx=2) + P("M19 8h11v19l7 7a5 5 0 0 1-7 7L19 31z", BONE) + R(19, 8, 11, 4, RED)
            + O(14, 24, 1.3, BLUE) + O(11, 29, 1, BLUE) + O(36, 22, 1.1, BLUE),
    "teacup": O(24, 26, 15, ASH) + O(24, 26, 10.5, BONE) + O(24, 26, 8, "#7A4E2E") + P("M13.5 26a5 5 0 0 1-6 0", "none", BONE, 2.6)
              + O(30, 20, 1.2, BONE, extra='opacity=".5"'),
    "ashtray": O(24, 26, 15, "#3A3A40", BONE, .8) + O(24, 26, 10, "#2A2A2E") + R(14, 23, 16, 5, "#7A4E2E", rx=1.5)
               + R(28, 23, 4, 5, "#8C877D", rx=1) + P("M33 21c3-3 0-6 3-9c2-2 0-5 2-7", "none", ASH, .9),
    "diary": R(10, 8, 28, 34, OX, rx=1.5) + R(10, 8, 4, 34, "#5A0916") + R(30, 8, 3, 38, RED)
             + R(17, 15, 17, 7, "none", BRASS, .6) + f'<text x="25.5" y="20.6" font-family="Bungee" font-size="4.5" fill="{BRASS}" text-anchor="middle">V.R.</text>',
    "jacket": P("M8 44L14 10L24 18L34 10L40 44Z", "#3A3A40") + P("M14 10L24 30L34 10", "none", "#1E1E22", 1.4)
              + O(24, 33, 1, BRASS) + O(24, 38, 1, BRASS) + hair("M28 20c3 4 5 2 7 6"),
    "footprint": P("M18 10c6-4 13 0 12 9c-1 6-3 9-3 14c0 3-2 6-6 6c-4 0-6-3-5-7c1-5-2-9-2-14c0-4 1-6 4-8z", MUD)
                 + R(17, 34, 12, 2, "#4A3220", extra='opacity=".6"') + O(36, 40, 2, MUD, extra='opacity=".6"') + O(10, 14, 1.4, MUD, extra='opacity=".6"'),
    "branch": P("M6 38L22 24L26 26", "none", WOODL, 3) + P("M26 26L30 20", "none", WOODL, 3) + P("M30 20l6-2l-4 4l5 1l-6 1z", BONE)
              + "".join(P(f"M{x} {y}c3-3 7-2 7 2c-3 3-7 2-7-2z", LEAF2) for x, y in [(12, 28), (18, 22), (24, 30), (8, 34)]),
    "clipboard": R(11, 8, 26, 34, WOOD, rx=1.5) + R(14, 13, 20, 26, PAPER) + R(19, 6, 10, 5, ASH, rx=1) + lines(17, 19, 14, 5)
                 + P("M33 34c0-2 2-4 2-4s2 2 2 4a2 2 0 0 1-4 0z", BLUE),
    "label": P("M24 44V24", "none", WOODL, 2) + R(13, 9, 22, 15, PAPER, rx=1.5) + O(16.5, 12.5, 1, GRAPH) + lines(18, 15.5, 13, 3, 3)
             + P("M24 32c-6-1-9-5-8-9c4 0 8 3 8 9zM24 34c5-1 8-4 7-8c-4 0-7 3-7 8z", LEAF2),
    "petals": "".join(P(f"M{x} {y}c3-4 8-3 8 1c-3 3-7 3-8-1z", c, extra=f'transform="rotate({a} {x} {y})"')
                      for x, y, a, c in [(12, 14, 20, "#B58AA8"), (26, 10, -30, "#9D6F93"), (30, 26, 50, "#B58AA8"), (14, 30, -10, "#9D6F93"),
                                         (22, 36, 80, "#B58AA8"), (34, 38, 10, "#9D6F93")]),
    "eyepiece": O(24, 24, 16, BRASS) + O(24, 24, 12.5, "#7A5A24") + O(24, 24, 9, "#2A2A30", BONE, .6) + O(24, 24, 5.5, "#0E1A24")
                + O(21.5, 21.5, 1.6, BONE, extra='opacity=".6"'),
    "telescope": P("M6 36L38 14L42 20L10 42Z", BONE) + R(34, 10, 6, 10, BRASS, extra='transform="rotate(-34 37 15)"') + L(20, 36, 16, 46, ASH, 1.5)
                 + L(20, 36, 26, 46, ASH, 1.5) + hair("M16 31c4-2 6 1 10-1c3-1 4 1 6 0"),
    "starchart": R(7, 9, 34, 30, "#162236", BLUE, .6) + O(24, 24, 11, "none", BLUE, .5)
                 + P("M13 16L19 13L23 18L30 14M27 30L33 27L36 33", "none", "#9FB6CC", .5)
                 + "".join(O(x, y, .9, BONE) for x, y in [(13, 16), (19, 13), (23, 18), (30, 14), (27, 30), (33, 27), (36, 33), (15, 32)]),
    "camera": R(8, 16, 24, 14, "#3A3A40", BONE, .6, 2) + O(32, 23, 6, "#2A2A30", BONE, .6) + O(32, 23, 3.4, "#0E1A24") + R(16, 30, 4, 10, ASH)
              + O(14, 21, 1.2, RED) + "".join(L(x, y, x - 2, y + 5, BLUE, .7) for x, y in [(36, 8), (42, 12), (28, 6), (40, 32)]),
    "glasses": O(15, 26, 8, "#2A3A48", BONE, 1.4) + O(33, 26, 8, "#2A3A48", BONE, 1.4) + P("M23 25c1-2 1-2 2 0", "none", BONE, 1.4)
               + L(7, 24, 3, 18, BONE, 1.2) + L(41, 24, 45, 18, BONE, 1.2) + L(12, 23, 15, 21, BONE, .5),
    "glove": R(4, 30, 40, 10, WOOD, WOODL, .6) + P("M15 30V16c0-2 3-2 3 0v-4c0-2 3-2 3 0v-1c0-2 3-2 3 0v2c0-2 3-2 3 0v13l3-4c1-2 4 0 3 2l-5 9H15z", "#8C6A4E"),
    "confessional": R(9, 6, 30, 38, WOOD, WOODL, .7) + R(13, 11, 22, 18, "#1E1410") + "".join(L(13 + k * 4.4, 11, 13 + k * 4.4, 29, WOODL, .5) for k in range(6))
                    + "".join(L(13, 11 + k * 4.5, 35, 11 + k * 4.5, WOODL, .5) for k in range(5)) + R(9, 33, 30, 3, OX) + O(34, 39, .9, BRASS),
    "hymn": R(8, 10, 32, 28, OX, rx=1.5) + R(10, 12, 13, 24, PAPER) + P("M25 12h13v24h-6l-2-3-2 3-1-2-2 2z", PAPER)
            + lines(12, 16, 9, 5, 3.4) + lines(27, 16, 9, 3, 3.4),
    "photo": R(9, 7, 30, 34, BRASS, rx=1) + R(12, 10, 24, 28, "#5A5A62") + O(20, 20, 3, BONE) + P("M15 36c0-7 2-10 5-10s5 3 5 10z", NOIR)
             + O(29, 20, 3, BONE) + P("M23 36c1-7 3-10 6-10s5 3 6 10z", BONE) + O(24, 13, 1.2, BONE),
    "bench": R(7, 18, 34, 14, NOIR, BONE, .6, 1.5) + R(9, 20, 30, 10, OX, rx=1) + R(9, 32, 3, 10, WOOD) + R(36, 32, 3, 10, WOOD)
             + hair("M18 24c4-2 6 2 10 0c2-1 4 1 5 0"),
    "sheet": R(10, 7, 28, 36, PAPER) + "".join(lines(13, y, 22, 5, 1.4, GRAPH, .4) for y in (12, 24))
             + "".join(O(x, y, 1.1, NOIR) for x, y in [(16, 15), (21, 13.6), (26, 16.4), (17, 27), (24, 25.6)])
             + P("M26 31c4-1 8 1 9 5c-3 2-8 1-9-5z", "#3A3A40", extra='opacity=".65"'),
    "programme": R(10, 6, 28, 36, OX) + R(13, 9, 22, 30, "none", BRASS, .5) + P("M18 18c2-3 10-3 12 0c-1 5-11 5-12 0z", BONE)
                 + O(21.5, 18.5, 1, NOIR) + O(26.5, 18.5, 1, NOIR) + lines(16, 29, 16, 3, 2.8, BRASS, .7),
    "metronome": P("M16 42L21 8H27L32 42Z", WOOD, WOODL, .7) + R(19, 30, 10, 8, WOOD2) + L(24, 34, 34, 12, BONE, 1.1)
                 + R(29, 18, 4, 3, BRASS, extra='transform="rotate(-25 31 19)"') + P("M33 10l3-3m-1 5l4-2", "none", RED, .8),
    "curtains": R(4, 6, 40, 3, BRASS) + P("M6 9h14c-2 10 2 18-2 33H6z", OX) + P("M42 9H28c2 10-2 18 2 33h12z", OX)
                + P("M10 9v30M14 9v31M34 9v30M38 9v31", "none", "#5A0916", .8) + R(15, 26, 6, 2, BRASS) + R(27, 26, 6, 2, BRASS),
    "flour": P("M10 30c2-6 10-8 16-6c6-4 14 0 13 6c4 4-2 10-8 8c-5 4-14 3-17-1c-6-1-7-6-4-7z", PAPER)
             + P("M24 26c3-2 6 0 6 3c0 3-1 4-1 7c0 2-1 3-3 3s-3-2-2-4c0-3-2-5-1-7z", "#BDB49F")
             + R(30, 8, 12, 14, "#C9B98F", rx=1) + f'<text x="36" y="17" font-family="Bungee" font-size="3.4" fill="{WOOD2}" text-anchor="middle">FLOUR</text>',
    "cupboard": R(8, 6, 32, 20, WOOD, WOODL, .7) + R(10, 8, 13, 16, "#2A1A16") + P("M24 8l10 3v12l-10 1z", WOODL)
                + O(31, 17, .8, BRASS) + R(12, 14, 4, 8, BONE) + R(17, 16, 4, 6, AMBER) + L(24, 34, 24, 44, ASH, .8) + P("M20 38l4-4 4 4", "none", ASH, .8),
    "menu": R(11, 6, 26, 36, PAPER, BRASS, .6) + f'<text x="24" y="15" font-family="Bungee" font-size="5" fill="{OX}" text-anchor="middle">MENU</text>'
            + lines(15, 21, 18, 5, 3.6, GRAPH, .7) + O(24, 38, 1, BRASS),
    "grocery": R(12, 6, 24, 36, PAPER) + "".join(R(15, 12 + k * 6, 3, 3, "none", GRAPH, .5) + L(20, 13.5 + k * 6, 32, 13.5 + k * 6, GRAPH, .7) for k in range(4))
               + P("M15.5 13.5l1 1 2-2.5", "none", RED, .7) + P("M30 40l8-10", "none", AMBER, 1.6),
    "sugar": O(24, 28, 13, BONE) + O(24, 28, 10, "#F8F4EA", ASH, .4) + "".join(R(x, y, 3, 3, "#FFFFFF", ASH, .3) for x, y in [(19, 24), (24, 27), (21, 30), (27, 23)])
             + P("M31 16l9-9", "none", ASH, 1.6) + O(30, 18, 2.5, ASH),
    "barrels": O(15, 28, 11, WOOD, NOIR, .6) + O(15, 28, 7, "none", "#2A2A2E", .8) + O(34, 30, 10, WOOD, NOIR, .6) + O(34, 30, 6.5, "none", "#2A2A2E", .8)
               + P("M22 40h7", "none", "#7A4E2E", 2.4) + R(28, 39, 3, 2.4, ASH),
    "barrel": O(24, 26, 16, WOOD, NOIR, .6) + O(24, 26, 13, "none", "#2A2A2E", 1) + O(24, 26, 7, "none", WOOD2, .6)
              + P("M8 12c6 2 10 0 14-6M8 12c4 5 4 10 2 14M8 12L18 20", "none", BONE, .35, 'opacity=".7"') + O(24, 26, 2, WOODL),
    "iou": R(6, 10, 22, 30, BONE, RED, .6, 1.5, 'transform="rotate(-10 17 25)"') + f'<text x="15" y="24" font-family="Bungee" font-size="6" fill="{RED}" transform="rotate(-10 17 25)">A</text>'
           + R(18, 12, 24, 26, PAPER) + f'<text x="30" y="21" font-family="Bungee" font-size="5" fill="{NOIR}" text-anchor="middle">IOU</text>'
           + f'<text x="30" y="29" font-family="IBM Plex Mono" font-size="4" fill="{OX}" text-anchor="middle" font-weight="700">&#163;&#8212;</text>' + L(22, 33, 38, 33, GRAPH, .5),
    "bottle": P("M21 6h6v9c4 2 6 5 6 9v18H15V24c0-4 2-7 6-9z", "#1E3A2A") + R(15, 26, 18, 10, PAPER) + R(20, 4, 8, 4, OX)
              + f'<text x="24" y="32.6" font-family="Bungee" font-size="3" fill="{OX}" text-anchor="middle">1956</text>'
              + "".join(O(x, y, .7, DUST) for x, y in [(19, 19), (27, 21), (22, 40), (30, 39), (17, 38)]),
    "dustprint": R(4, 4, 40, 40, "#3A3633", rx=2) + "".join(O(x, y, .5, DUST) for x, y in [(8, 9), (38, 11), (12, 40), (36, 36), (30, 7), (6, 26)])
                 + P("M19 12c4-3 9 0 8 6c-1 4-2 6-2 10c0 2-1 4-4 4c-3 0-4-2-3-5c1-3-1-6-1-9c0-3 0-5 2-6z", "none", DUST, 1.1, 'stroke-dasharray="1.4 1"'),
    # bonus
    "battery": R(12, 12, 24, 30, NOIR, BONE, 1.2, 2.5) + R(19, 8, 10, 4, BONE, rx=1) + R(15, 28, 18, 11, RED, rx=1)
               + P("M26 15l-6 9h5l-3 7 7-10h-5z", AMBER),
    "shoes": P("M6 30c6 0 10-6 14-10l6 2c2 4 8 6 14 6c3 0 4 3 4 6v3H6z", BONE) + P("M6 37h38v3H6z", RED) + L(22, 24, 26, 25, NOIR, .8)
             + L(21, 27, 25, 28, NOIR, .8) + L(2, 22, 10, 22, ASH, 1) + L(4, 27, 9, 27, ASH, 1) + L(1, 32, 5, 32, ASH, 1),
    "key": O(14, 24, 8, "none", BRASS, 3) + O(14, 24, 3, "none", BRASS, 1) + R(21, 22.5, 22, 3, BRASS) + R(35, 25, 3, 7, BRASS) + R(40, 25, 3, 5, BRASS),
}


def art(key, size="30mm"):
    return (f'<svg viewBox="0 0 48 48" style="width:{size};height:{size};display:block">{ART[key]}</svg>')


CSS = f"""
.photo {{ background:#FFFDF6; padding:1.8mm 1.8mm 5.5mm; box-shadow:.3mm .6mm 0 rgba(0,0,0,.25); transform:rotate(-2.2deg); position:relative; }}
.photo .ph {{ background:{PH}; width:33mm; height:27mm; display:flex; align-items:center; justify-content:center; overflow:hidden; }}
.photo .cap {{ position:absolute; left:0; right:0; bottom:1.2mm; text-align:center; font-family:'IBM Plex Mono'; font-size:5pt; color:#6B665C; }}
.photo .tape {{ position:absolute; top:-2mm; left:50%; width:12mm; height:4mm; margin-left:-6mm; background:#E8DDBF; opacity:.85; transform:rotate(3deg); }}
.found {{ font-family:Silkscreen; font-size:5.8pt; color:#6B665C; display:flex; align-items:center; gap:1mm; justify-content:center; }}
.obj {{ font-family:Bungee; font-size:11pt; line-height:1.05; text-align:center; color:{NOIR}; }}
.hint2 {{ font-size:7.5pt; line-height:1.3; text-align:center; color:{NOIR}; }}
.effect {{ font-family:Bungee; font-size:12pt; color:{RED}; text-align:center; line-height:1; }}
"""


def evidence_face(room, name, key, code):
    col, txt, ic = bp.TYPES["EVIDENCE"]
    room_ic = next(r[1] for r in bp.ROOMS if r[0] == room)
    head = (f'<div class="hd" style="--c:{col};--t:{txt}"><span class="pix">{bp.icon("magnifier", "3.6mm", 2.4)} EVIDENCE</span>'
            f'<span class="mono">{code}</span></div>')
    main = (f'<div class="photo"><div class="tape"></div><div class="ph">{card_art.art(key, room)}</div><div class="cap">EXHIBIT {code}</div></div>'
            f'<div class="obj">{bp.esc(name)}</div>'
            f'<div class="found">{bp.icon(room_ic, "2.8mm", 2.6)} FOUND IN THE {room}</div>'
            f'<div class="hint2">Scan it to see what it reveals.<br>Keep it face down.</div>')
    foot = (f'<div class="ft"><div class="qr" data-code="{code}"></div><div class="meta">'
            f'<span class="lbl">SCAN IN THE POLICE CONSOLE</span><span class="code">{code}</span>'
            f'<span class="deck">{bp.icon(room_ic, "2.6mm", 2.6)} DECK: {room}</span></div></div>')
    return (f'<div class="card t-{bp.THEME}">{bp.frame_svg(col)}{bp.theme_decor("EVIDENCE")}'
            f'<div class="in">{head}<div class="mn" style="gap:1.8mm">{main}</div>{foot}</div></div>')


def bonus_face(room, name, key, effect, text_, code):
    room_ic = next(r[1] for r in bp.ROOMS if r[0] == room)
    head = (f'<div class="hd" style="--c:{AMBER};--t:{NOIR}"><span class="pix">{bp.icon("bolt", "3.6mm", 2.4)} BONUS</span>'
            f'<span class="mono">{code}</span></div>')
    main = (f'<div class="photo"><div class="tape"></div><div class="ph">{card_art.art(key, room)}</div><div class="cap">BONUS</div></div>'
            f'<div class="obj">{bp.esc(name)}</div><div class="effect">{effect}</div>'
            f'<div class="hint2">{bp.esc(text_)}</div>')
    # playtest 1: bonus cards are kept and played later in the app, so they get a QR too
    foot = (f'<div class="ft"><div class="qr" data-code="{code}"></div><div class="meta">'
            f'<span class="lbl">KEEP IT FACE UP &#183; PLAY IT ON YOUR TURN</span><span class="code">{code}</span>'
            f'<span class="deck">{bp.icon(room_ic, "2.6mm", 2.6)} DECK: {room}</span></div></div>')
    stamp = '<div class="margin"></div>' + bp.PAPERCLIP + '<div class="stamp">BONUS</div>'
    return (f'<div class="card t-{bp.THEME}">{bp.frame_svg(AMBER)}{stamp}'
            f'<div class="in">{head}<div class="mn" style="gap:1.6mm">{main}</div>{foot}</div></div>')


def all_cards_v2():
    """(face, back, file stem) for the 40 cards, in deck order (room by room)."""
    out, count = [], {}
    rooms = ["LIBRARY", "GREENHOUSE", "OBSERVATORY", "CHAPEL", "MUSIC ROOM", "KITCHEN", "WINE CELLAR"]
    for room in rooms:
        for r_, name, key in [o for o in OBJECTS if o[0] == room]:
            count[room] = count.get(room, 0) + 1
            code = f"{ROOM_CODE[room]}-{count[room]:02d}"
            out.append((evidence_face(room, name, key, code), bp.card_back(room), code.lower()))
        for r_, name, key, eff, txt in [b for b in BONUS if b[0] == room]:
            count[room] = count.get(room, 0) + 1
            code = f"{ROOM_CODE[room]}-{count[room]:02d}"
            out.append((bonus_face(room, name, key, eff, txt, code), bp.card_back(room), f"{code.lower()}-bonus"))
    return out


def main():
    bp.THEME = "dossier"
    bp.THEME_CSS += CSS
    bp.all_cards = all_cards_v2
    src = bp.SRC
    (src / "cards").mkdir(parents=True, exist_ok=True)
    for old in (src / "cards").glob("*.html"):
        old.unlink()
    (src / "cards_faces_bleed.html").write_text(bp.cards_bleed_pdf("faces"))
    (src / "cards_backs_bleed.html").write_text(bp.cards_bleed_pdf("backs"))
    (src / "cards_faces_A4.html").write_text(bp.cards_a4("faces"))
    (src / "cards_backs_A4.html").write_text(bp.cards_a4("backs"))
    cards = all_cards_v2()
    for f, b, stem in cards:
        (src / "cards" / f"{stem}.html").write_text(bp.card_single(f).replace("../../logo", "../../../logo"))
    backs = list(dict.fromkeys(b for _, b, _ in cards))
    for b in backs:
        label = [r for r in bp.DECK_ROOMS if f"</svg> {r}</div>" in b][0]
        (src / "cards" / f"back-{label.lower().replace(' ', '-')}.html").write_text(bp.card_single(b).replace("../../logo", "../../../logo"))
    pick = [cards[0][0], cards[5][0], cards[11][0], cards[16][0], cards[30][0], cards[10][0], cards[39][0], cards[0][1]]
    (src / "cards_overview.html").write_text(bp.cards_overview(pick))
    print(f"{len(cards)} cards ({len(OBJECTS)} evidence + {len(BONUS)} bonus), {len(backs)} backs")


if __name__ == "__main__":
    main()
