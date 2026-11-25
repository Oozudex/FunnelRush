#!/usr/bin/env python3
"""Build the print HTML sources for The Last Query:
brand sheet (palette + typography), game board (A2) and cards (63 x 88 mm).

Run:  python3 DA/tools/build_print.py   then   zsh DA/tools/render_print.sh
All sizes are real millimetres. Bleed 3 mm, safe area 5 mm inside the trim,
crop marks drawn in a 10 mm slug outside the bleed.
"""
import html
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # DA/
SRC = Path(__file__).resolve().parent / "print_src"
LOGO = "../../logo/the-last-query_logo_dark_transparent.svg"   # relative to print_src/*

BLEED, SLUG = 3, 10

# ---------------------------------------------------------------- palette
PALETTE = [
    # name, hex, rgb, cmyk, role
    ("Noir", "#0B0B0C", "11 11 12", "C60 M40 Y40 K100", "Backgrounds, night"),
    ("Graphite", "#232327", "35 35 39", "C70 M60 Y55 K75", "Panels, room tiles"),
    ("Bone", "#F4F0E6", "244 240 230", "C3 M4 Y9 K0", "Text, lines, Table cards"),
    ("Ash", "#8C877D", "140 135 125", "C40 M35 Y45 K15", "Secondary text"),
    ("Query Red", "#E31B3B", "227 27 59", "C0 M95 Y75 K0", "Accent, Keyword cards"),
    ("Oxblood", "#7E0C1F", "126 12 31", "C20 M100 Y80 K45", "3D depth, Twist cards"),
    ("Lamp Amber", "#F2A93B", "242 169 59", "C0 M38 Y85 K0", "Coffee cards and tokens"),
    ("Storm Blue", "#5B7C99", "91 124 153", "C65 M35 Y20 K15", "Evidence cards, rain"),
    ("Brass", "#C9923A", "201 146 58", "C15 M45 Y85 K5", "Board details, medallions"),
    ("Case Paper", "#EFE8D8", "239 232 216", "C5 M7 Y15 K0", "Card faces"),
    ("Kraft", "#C9A46E", "201 164 110", "C20 M35 Y60 K5", "Card backs (folder)"),
]
C = {n.split()[-1].lower() if n != "Query Red" else "red": h for n, h, *_ in PALETTE}
# -> noir, graphite, bone, ash, red, oxblood, amber, blue

FONTS_LINK = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,800;1,400'
              '&family=Bungee&family=IBM+Plex+Mono:wght@400;700&family=Silkscreen&display=block" rel="stylesheet">')
QR_JS = '<script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js"></script>'
QR_RUN = """<script>
document.querySelectorAll('.qr').forEach(function(el){
  var q = qrcode(0, 'M'); q.addData('TLQ:' + el.dataset.code); q.make();
  var n = q.getModuleCount(), s = '';
  for (var r = 0; r < n; r++) for (var c = 0; c < n; c++)
    if (q.isDark(r, c)) s += 'M' + c + ',' + r + 'h1v1h-1z';
  el.innerHTML = '<svg viewBox="-2 -2 ' + (n + 4) + ' ' + (n + 4) + '" shape-rendering="crispEdges">'
    + '<rect x="-2" y="-2" width="' + (n + 4) + '" height="' + (n + 4) + '" fill="#F4F0E6"/>'
    + '<path d="' + s + '" fill="#0B0B0C"/></svg>';
});
</script>"""

BASE_CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Archivo', sans-serif; color: {C['bone']}; }}
.disp {{ font-family: 'Bungee', sans-serif; font-weight: 400; letter-spacing: .02em; }}
.mono {{ font-family: 'IBM Plex Mono', monospace; }}
.pix {{ font-family: 'Silkscreen', monospace; letter-spacing: .04em; }}
.mark {{ position: absolute; background: #000; }}
svg.i {{ display: inline-block; vertical-align: middle; fill: none; stroke: currentColor;
        stroke-width: 2; stroke-linecap: square; stroke-linejoin: miter; }}
"""

# ---------------------------------------------------------------- icons (24 x 24, stroke)
ICONS = {
    "book": "M3 5h7l2 2 2-2h7v14h-7l-2 2-2-2H3z M12 7v14",
    "cup": "M4 9h12v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z M16 11h2.5a2 2 0 0 1 0 4H16 M8 3v3 M12 3v3",
    "telescope": "M3 15l13-7 2.5 4.5-13 7z M10 16.5L7 22 M12 15.5l3.5 6.5 M17 5l2 4",
    "note": "M9 18V5l11-2v13 M9 8l11-2 M4 15h5v5H4z M15 13h5v5h-5z",
    "candle": "M9 11h6v10H9z M12 3c2.2 2 2.2 4.5 0 6-2.2-1.5-2.2-4 0-6z M5 21h14",
    "leaf": "M5 19C5 9 11 4 20 4c0 9-5 15-15 15z M5 19l9-9",
    "bottle": "M10 2h4v5l2 3v12H8V10l2-3z M8 14h8",
    "server": "M4 3h16v7H4z M4 14h16v7H4z M7 6.5h3 M7 17.5h3 M16 6.5h1 M16 17.5h1",
    "door": "M6 21V3h12v18 M3 21h18 M14 12h1",
    "key": "M3 12a4 4 0 1 0 8 0a4 4 0 1 0-8 0 M11 12h10 M17 12v4 M20 12v3",
    "table": "M3 5h18v14H3z M3 10h18 M3 15h18 M9 5v14",
    "magnifier": "M3 10a7 7 0 1 0 14 0a7 7 0 1 0-14 0 M15 15l6 6",
    "bolt": "M13 2L5 14h6l-1 8 8-12h-6z",
    "pawn": "M9 6a3 3 0 1 0 6 0a3 3 0 1 0-6 0 M8 21l2-11h4l2 11z M6 21h12",
    "clock": "M3 12a9 9 0 1 0 18 0a9 9 0 1 0-18 0 M12 7v5l3 2",
    "passage": "M4 21V9l8-5 8 5v12 M9 21v-6h6v6",
    "sun": "M8 15a4 4 0 0 1 8 0 M3 15h18 M12 5v3 M5 8l2 2 M19 8l-2 2 M6 19h12",
    "badge": "M4 4h16v16H4z M8 9h8 M8 13h8 M8 17h4",
}


def icon(name, size="1em", sw=2, extra=""):
    return (f'<svg class="i" viewBox="0 0 24 24" style="width:{size};height:{size};stroke-width:{sw};{extra}">'
            f'<path d="{ICONS[name]}"/></svg>')


def cup(size=".95em"):
    return icon("cup", size, 2.4, "margin-top:-.15em")


def esc(t):
    return html.escape(t)


def cropmarks(x, y, w, h, bleed=BLEED, length=6, gap=1.5):
    """Crop marks for a trim box at (x, y, w, h) in mm, drawn outside the bleed."""
    o = bleed + gap
    out = []
    for cx in (x, x + w):
        out.append(f'<div class="mark" style="left:{cx - .125}mm;top:{y - o - length}mm;width:.25mm;height:{length}mm"></div>')
        out.append(f'<div class="mark" style="left:{cx - .125}mm;top:{y + h + o}mm;width:.25mm;height:{length}mm"></div>')
    for cy in (y, y + h):
        out.append(f'<div class="mark" style="top:{cy - .125}mm;left:{x - o - length}mm;height:.25mm;width:{length}mm"></div>')
        out.append(f'<div class="mark" style="top:{cy - .125}mm;left:{x + w + o}mm;height:.25mm;width:{length}mm"></div>')
    return "".join(out)


def page(title, w, h, body, extra_css="", qr=False):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(title)}</title>
{FONTS_LINK}{QR_JS if qr else ''}
<style>@page {{ size: {w}mm {h}mm; margin: 0; }}
html, body {{ width: {w}mm; }}
.sheet {{ position: relative; width: {w}mm; height: {h}mm; overflow: hidden; page-break-after: always; }}
{BASE_CSS}{extra_css}</style></head><body>{body}{QR_RUN if qr else ''}</body></html>"""


RAIN = f"""<svg width="100%" height="100%" style="position:absolute;inset:0">
<defs><pattern id="rain" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(18)">
<line x1="0" y1="0" x2="0" y2="4" stroke="{C['graphite']}" stroke-width="1"/></pattern></defs>
<rect width="100%" height="100%" fill="url(#rain)"/></svg>"""


# ================================================================= BRAND SHEET
def brand_sheet():
    W, H = 297, 210
    pw, ph = W + 2 * (BLEED + SLUG), H + 2 * (BLEED + SLUG)
    tx = ty = BLEED + SLUG
    sw = "".join(f"""
      <div class="sw"><div class="chip" style="background:{hx};{'border:.3mm solid #F4F0E6;' if hx in ('#0B0B0C','#232327') else ''}"></div>
      <div class="disp nm">{esc(n)}</div><div class="mono val">{hx}<br>RGB {rgb}<br>{cmyk}</div>
      <div class="role">{esc(role)}</div></div>""" for n, hx, rgb, cmyk, role in PALETTE)
    icons = "".join(f'<div class="ic">{icon(k, "9mm", 1.8)}<span class="pix">{k}</span></div>'
                    for k in ["book", "cup", "telescope", "note", "candle", "leaf", "bottle", "server",
                              "door", "key", "table", "magnifier", "bolt", "pawn", "clock", "passage"])
    types = "".join(f'<div class="ty" style="--c:{c}"><span class="pix">{icon(i, "4.5mm")} {t}</span></div>'
                    for t, c, i in [("KEYWORD", C['red'], "key"), ("TABLE", C['bone'], "table"),
                                    ("EVIDENCE", C['blue'], "magnifier"), ("COFFEE", C['amber'], "cup"),
                                    ("TWIST", C['oxblood'], "bolt"), ("DETECTIVE", C['red'], "pawn")])
    css = f"""
    .bleed {{ position:absolute; left:{SLUG}mm; top:{SLUG}mm; width:{W + 2 * BLEED}mm; height:{H + 2 * BLEED}mm; background:{C['noir']}; }}
    .trim {{ position:absolute; left:{tx}mm; top:{ty}mm; width:{W}mm; height:{H}mm; padding:9mm 10mm; }}
    h1 {{ font-family:'Bungee'; font-weight:400; font-size:20pt; color:{C['bone']}; }}
    h2 {{ font-family:'Silkscreen'; font-weight:400; font-size:8pt; color:{C['red']}; margin:0 0 2.5mm; letter-spacing:.08em; }}
    .top {{ display:flex; justify-content:space-between; align-items:flex-start; }}
    .top img {{ width:62mm; }}
    .sub {{ font-size:8.5pt; color:{C['ash']}; margin-top:1mm; }}
    .grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:6mm; margin-top:4mm; }}
    .sws {{ display:grid; grid-template-columns: repeat(4, 1fr); gap:2.2mm 3mm; }}
    .chip {{ height:9mm; }}
    .nm {{ font-size:8pt; margin-top:1.2mm; }}
    .val {{ font-size:6.2pt; color:{C['ash']}; line-height:1.35; margin-top:.6mm; }}
    .role {{ font-size:6.5pt; margin-top:.6mm; }}
    .spec {{ border-top:.3mm solid {C['graphite']}; padding:2.2mm 0; display:grid; grid-template-columns: 30mm 1fr; gap:3mm; align-items:baseline; }}
    .spec .lbl {{ font-family:'Silkscreen'; font-size:6.5pt; color:{C['ash']}; }}
    .spec .use {{ font-size:6.5pt; color:{C['ash']}; margin-top:.8mm; }}
    .ics {{ display:grid; grid-template-columns: repeat(8, 1fr); gap:2.5mm; color:{C['bone']}; }}
    .ic {{ display:flex; flex-direction:column; align-items:center; gap:1mm; font-size:5pt; color:{C['ash']}; }}
    .tys {{ display:flex; gap:2mm; flex-wrap:wrap; }}
    .ty span {{ display:inline-block; font-size:6.5pt; padding:1.2mm 2mm; background:var(--c);
               color:{C['noir']}; }}
    .ty:nth-child(5) span, .ty:nth-child(6) span {{ color:{C['bone']}; }}
    .rules {{ font-size:6.8pt; line-height:1.45; color:{C['bone']}; }}
    .rules b {{ color:{C['red']}; font-weight:600; }}
    """
    body = f"""<div class="sheet" style="width:{pw}mm;height:{ph}mm">
    <div class="bleed"></div>
    <div class="trim">
      <div class="top"><div><h1>Brand sheet</h1>
        <div class="sub">Graphic film noir &times; terminal. Flat colours, block shapes, one blood red. Print: CMYK FOGRA39, 300 DPI, 3 mm bleed.</div></div>
        <img src="{LOGO}"></div>
      <div class="grid">
        <div><h2>&gt; PALETTE</h2><div class="sws">{sw}</div>
          <h2 style="margin-top:5mm">&gt; CARD TYPE CODES</h2><div class="tys">{types}</div>
          <h2 style="margin-top:5mm">&gt; ICONS &middot; 24 px grid, 2 px stroke, square ends</h2><div class="ics">{icons}</div>
        </div>
        <div><h2>&gt; TYPOGRAPHY</h2>
          <div class="spec"><div><div class="lbl">TITLES</div><div class="use">Bungee &middot; 14-40 pt</div></div>
            <div class="disp" style="font-size:20pt;line-height:1">The Library</div></div>
          <div class="spec"><div><div class="lbl">BODY / RULES</div><div class="use">Archivo &middot; 7.5-10 pt<br>min. 7 pt on cards</div></div>
            <div style="font-size:9pt;line-height:1.35">Victor is found dead at 11:45 PM. <b style="font-weight:800">Search</b> the rooms, <i>question</i> the guests and query the data before dawn.</div></div>
          <div class="spec"><div><div class="lbl">DATA / SQL</div><div class="use">IBM Plex Mono &middot; 7-24 pt</div></div>
            <div class="mono" style="font-size:9pt;line-height:1.4"><span style="color:{C['red']}">SELECT</span> name <span style="color:{C['red']}">FROM</span> timeline<br><span style="color:{C['red']}">WHERE</span> room = 'Library' <span style="color:{C['red']}">AND</span> hour = '11 PM';</div></div>
          <div class="spec"><div><div class="lbl">LABELS</div><div class="use">Silkscreen &middot; 6-12 pt<br>caps only</div></div>
            <div class="pix" style="font-size:10pt">A MURDER MYSTERY BOARD GAME</div></div>
          <h2 style="margin-top:4mm">&gt; PRINT RULES</h2>
          <div class="rules"><b>Bleed</b> 3 mm &middot; <b>Safe area</b> 5 mm inside the trim &middot; <b>Crop marks</b> outside the bleed.<br>
          <b>Cards</b> 63 &times; 88 mm &middot; <b>Board</b> A2 594 &times; 420 mm &middot; <b>Rules</b> A5.<br>
          <b>Black</b>: rich black C60 M40 Y40 K100 for big areas, K100 for small text.<br>
          <b>Fonts</b>: Google Fonts, SIL Open Font License (free for print). Embedded in every PDF.</div>
        </div>
      </div>
    </div>
    {cropmarks(tx, ty, W, H)}
    </div>"""
    return page("The Last Query - brand sheet", pw, ph, body, css)


# ================================================================= BOARD
ROOMS = [
    # V2 (2026-11-25): name, icon, has a deck, action, text, secret passage (none in V2)
    ("OBSERVATORY", "telescope", True, "Search", "Draw the top card of the deck.", None),
    ("LIBRARY", "book", True, "Accuse here", "Crime scene. The only room where you can accuse.", None),
    ("CHAPEL", "candle", True, "Search", "Draw the top card of the deck.", None),
    ("MUSIC ROOM", "note", True, "Search", "Draw the top card of the deck.", None),
    ("GRAND HALL", "door", False, "Start", "Everyone starts here. No deck.", None),
    ("KITCHEN", "cup", True, "Search", "Draw the top card of the deck.", None),
    ("GREENHOUSE", "leaf", True, "Search", "Draw the top card of the deck.", None),
    ("WINE CELLAR", "bottle", True, "Search", "Draw the top card of the deck.", None),
    ("SERVER ROOM", "server", False, "Recharge", "Refill up to 3 Query Tokens. No deck here.", None),
]


def board():
    W, H = 594, 420
    pw, ph = W + 2 * (BLEED + SLUG), H + 2 * (BLEED + SLUG)
    tx = ty = BLEED + SLUG
    RW, RH, G = 124, 112, 26           # room size, corridor gap
    MX, MY = 14, 16                    # map origin inside trim
    tiles, corridors = [], []
    for i, (name, ic, search, ptitle, ptext, passage) in enumerate(ROOMS):
        r, c = divmod(i, 3)
        x, y = MX + c * (RW + G), MY + r * (RH + G)
        extra = ""
        if name == "LIBRARY":
            extra = (f'<div class="tape pix">CRIME SCENE &middot; DO NOT CROSS &middot; CRIME SCENE &middot; DO NOT CROSS</div>')
        if name == "GRAND HALL":
            extra = ('<div class="starts">' + "".join(f'<div class="start pix">{icon("pawn", "9mm", 1.6)}<span>P{k}</span></div>'
                                                      for k in range(1, 5)) + '</div><div class="pix starthere">&gt; START HERE</div>')
        if name == "SERVER ROOM":
            leds = "".join('<i style="opacity:%s"></i>' % o for o in (1, .5, 1, .3, 1, .7))
            extra = ('<div class="racks">' + ('<div class="rack">' + leds + '</div>') * 3
                     + '</div><div class="corrupt mono">&#9608;&#9608;&#9608;&#9608; CORRUPTED</div>')
        slot = ('<div class="slot"><div class="pix">ROOM DECK</div><div class="mono" style="font-size:7pt;opacity:.7">63 &times; 88</div></div>'
                if search else "")
        pas = (f'<div class="passage pix">{icon("passage", "4.6mm")} SECRET PASSAGE &#8644; {passage}</div>' if passage else "")
        action = "SEARCH or POWER" if search else "POWER"
        tiles.append(f"""<div class="room{' lib' if name == 'LIBRARY' else ''}" style="left:{x}mm;top:{y}mm;width:{RW}mm;height:{RH}mm">
          {extra}
          <div class="rh">{icon(ic, "9mm", 2)}<div class="disp rn">{name}</div></div>
          <div class="pw"><span class="pix act">{action}</span><b>{esc(ptitle)}:</b> {esc(ptext).replace('coffee', 'coffee ' + cup())}</div>
          {slot}{pas}</div>""")
        if c < 2:
            corridors.append(f'<div class="cor h" style="left:{x + RW}mm;top:{y + RH / 2 - 5}mm;width:{G}mm"></div>')
        if r < 2:
            corridors.append(f'<div class="cor v" style="left:{x + RW / 2 - 5}mm;top:{y + RH}mm;height:{G}mm"></div>')

    SX = MX + 3 * RW + 2 * G + 14      # sidebar x
    SW = W - SX - 12
    times = ["12:00", "12:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30"]
    clock = "".join(f'<div class="t{" st" if k == 0 else ""}"><span class="pix">ROUND {k + 1}</span><b class="mono">{t}<small> AM</small></b></div>'
                    for k, t in enumerate(times))
    clock += f'<div class="t dawn"><span class="pix">{icon("sun", "4mm")} DAWN</span><b class="mono">4:00<small> AM</small></b></div>'
    css = f"""
    .bleed {{ position:absolute; left:{SLUG}mm; top:{SLUG}mm; width:{W + 2 * BLEED}mm; height:{H + 2 * BLEED}mm; background:{C['noir']}; }}
    .trim {{ position:absolute; left:{tx}mm; top:{ty}mm; width:{W}mm; height:{H}mm; }}
    .room {{ position:absolute; background:{C['graphite']}; border:1.2mm solid {C['bone']}; padding:5mm 6mm; overflow:hidden;
             clip-path: polygon(6mm 0, calc(100% - 6mm) 0, 100% 6mm, 100% calc(100% - 6mm), calc(100% - 6mm) 100%, 6mm 100%, 0 calc(100% - 6mm), 0 6mm); }}
    .room.lib {{ border-color:{C['red']}; }}
    .rh {{ display:flex; align-items:center; gap:3mm; color:{C['bone']}; position:relative; }}
    .lib .rh {{ color:{C['red']}; }}
    .rn {{ font-size:19pt; line-height:1; }}
    .pw {{ font-size:10.5pt; line-height:1.3; margin-top:2.5mm; position:relative; }}
    .pw b {{ font-weight:800; }}
    .act {{ display:inline-block; font-size:6.5pt; background:{C['bone']}; color:{C['noir']}; padding:.6mm 1.5mm; margin-right:2mm; vertical-align:2px; }}
    .lib .act {{ background:{C['red']}; color:{C['bone']}; }}
    .slot {{ position:absolute; left:50%; bottom:5mm; transform:translateX(-50%); width:88mm; height:63mm;
             border:.6mm dashed {C['ash']}; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1mm;
             color:{C['ash']}; font-size:9pt; }}
    .passage {{ position:absolute; right:9mm; top:1mm; font-size:6.5pt; color:{C['red']}; display:flex; align-items:center; gap:1mm; }}
    .tape {{ position:absolute; right:-34mm; top:13mm; transform:rotate(38deg); background:{C['red']}; color:{C['noir']};
             font-size:8pt; padding:1.2mm 0; width:120mm; text-align:center; white-space:nowrap; z-index:0; opacity:.95; }}
    .lib .slot {{ background:{C['graphite']}; z-index:1; }}
    .lib .pw {{ padding-right:24mm; }}
    .starts {{ position:absolute; left:6mm; right:6mm; bottom:14mm; display:grid; grid-template-columns:repeat(4,1fr); gap:3mm; }}
    .start {{ height:30mm; border:.6mm dashed {C['ash']}; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1.5mm; color:{C['ash']}; font-size:7pt; }}
    .starthere {{ position:absolute; left:6mm; bottom:6mm; font-size:9pt; color:{C['red']}; }}
    .racks {{ position:absolute; left:6mm; right:6mm; bottom:16mm; display:grid; grid-template-columns:repeat(3,1fr); gap:4mm; }}
    .rack {{ height:52mm; border:.8mm solid {C['bone']}; padding:2mm; display:flex; flex-direction:column; gap:2.2mm; }}
    .rack i {{ display:block; height:4.5mm; background:{C['bone']}; }}
    .rack i:nth-child(4) {{ background:{C['red']}; opacity:1 !important; }}
    .corrupt {{ position:absolute; left:6mm; bottom:6mm; font-size:9pt; color:{C['red']}; }}
    .cor {{ position:absolute; background:{C['bone']}; }}
    .cor.h {{ height:10mm; }} .cor.v {{ width:10mm; }}
    .cor::after {{ content:''; position:absolute; inset:0; margin:auto; background:repeating-linear-gradient(90deg, {C['noir']} 0 2mm, transparent 2mm 5mm); }}
    .cor.h::after {{ height:1mm; }} .cor.v::after {{ width:1mm; background:repeating-linear-gradient(0deg, {C['noir']} 0 2mm, transparent 2mm 5mm); }}
    .side {{ position:absolute; left:{SX}mm; top:{MY}mm; width:{SW}mm; height:{H - MY - 12}mm; display:flex; flex-direction:column; gap:7mm; }}
    .side img {{ width:100%; }}
    .box {{ border:1mm solid {C['bone']}; padding:4mm 5mm; }}
    .box h3 {{ font-family:'Silkscreen'; font-weight:400; font-size:10pt; color:{C['red']}; margin-bottom:3mm; letter-spacing:.06em; }}
    .clock {{ display:grid; grid-template-columns:repeat(3,1fr); gap:2.5mm; }}
    .t {{ border:.6mm solid {C['bone']}; height:17mm; padding:1.6mm 2mm; display:flex; flex-direction:column; justify-content:space-between; }}
    .t span {{ font-size:6pt; color:{C['ash']}; }}
    .t b {{ font-size:15pt; font-weight:700; }} .t small {{ font-size:7pt; }}
    .t.st {{ background:{C['bone']}; color:{C['noir']}; }} .t.st span {{ color:{C['noir']}; }}
    .t.dawn {{ background:{C['red']}; border-color:{C['red']}; }} .t.dawn span {{ color:{C['bone']}; }}
    .steps {{ font-size:10pt; line-height:1.35; display:flex; flex-direction:column; gap:2.5mm; }}
    .steps .n {{ font-family:'Bungee'; color:{C['red']}; margin-right:1.5mm; }}
    .steps small {{ display:block; color:{C['ash']}; font-size:8.5pt; margin-left:7mm; }}
    .bank {{ display:flex; gap:5mm; align-items:center; }}
    .bank .spot {{ width:42mm; height:42mm; border-radius:50%; border:.8mm dashed {C['amber']}; color:{C['amber']};
                  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1mm; flex:none; }}
    .bank p {{ font-size:9pt; line-height:1.35; }}
    .bank b {{ color:{C['red']}; }}
    """
    body = f"""<div class="sheet" style="width:{pw}mm;height:{ph}mm">
    <div class="bleed">{RAIN}</div>
    <div class="trim">{''.join(corridors)}{''.join(tiles)}
      <div class="side">
        <img src="{LOGO}">
        <div class="box"><h3>&gt; THE CLOCK</h3><div class="clock">{clock}</div>
          <div style="font-size:8.5pt;color:{C['ash']};margin-top:2.5mm">Move the clock token 1 space at the end of each round. At dawn the police arrive: if nobody solved the case, the killer escapes.</div></div>
        <div class="box"><h3>&gt; YOUR TURN</h3><div class="steps">
          <div><span class="n">1</span><b>MOVE</b> up to 2 rooms.<small>A secret passage counts as 1 move.</small></div>
          <div><span class="n">2</span><b>ACT</b>: choose one.<small>Search &middot; Room power &middot; Interrogate (1 {cup()}) &middot; Trade</small></div>
          <div><span class="n">3</span><b>QUERY</b> on your phone.<small>1 {cup()} per query. Results stay private.</small></div></div></div>
        <div class="box bank"><div class="spot">{icon("cup", "13mm", 1.6)}<span class="pix" style="font-size:7pt">COFFEE BANK</span></div>
          <p>The killer is the only guest with all three:<br><b>OPPORTUNITY</b> + <b>MEANS</b> + <b>MOTIVE</b>.<br><br>Accuse in the Library, out loud, in English.</p></div>
      </div>
    </div>
    {cropmarks(tx, ty, W, H)}
    </div>"""
    return page("The Last Query - board A2", pw, ph, body, css)


# ================================================================= CARDS
CW, CH = 63, 88
TYPES = {
    "KEYWORD": (C['red'], C['bone'], "key"),
    "TABLE": (C['bone'], C['noir'], "table"),
    "EVIDENCE": (C['blue'], C['bone'], "magnifier"),
    "COFFEE": (C['amber'], C['noir'], "cup"),
    "TWIST": (C['oxblood'], C['bone'], "bolt"),
    "DETECTIVE": (C['red'], C['bone'], "pawn"),
}

KEYWORDS = [  # word, copies, code, text, example
    ("WHERE", 4, "WHR", "Keep only the rows that match a condition.", "WHERE room = 'Library'"),
    ("AND", 3, "AND", "Both conditions must be true.", "hour = '11 PM' AND room = 'Kitchen'"),
    ("OR", 2, "OR", "At least one condition must be true.", "room = 'Chapel' OR room = 'Kitchen'"),
    ("NOT", 2, "NOT", "Keep the rows that do NOT match.", "NOT room = 'Library'"),
    ("JOIN", 3, "JON", "Combine two tables in one query. Saves coffee!", "guests JOIN secrets ON name"),
    ("= / ≠", 2, "EQ", "Compare a column with a value.", "hand ≠ 'left'"),
]
TABLES = [
    ("TIMELINE", "TL", ["name", "hour", "room"], "Badge logs: who was where, and when."),
    ("ITEMS", "IT", ["item", "found_in", "owner"], "Every object found in the manor."),
    ("SECRETS", "SC", ["name", "motive", "secret"], "What each guest is hiding."),
    ("CALLS", "CL", ["from", "to", "time"], "Every phone call made tonight."),
]
EVIDENCE = ["AUTOPSY REPORT", "FOOTPRINT", "TORN GLOVE", "TEACUP", "BADGE READER", "LETTER",
            "PAPER NOTE", "PHONE", "FINGERPRINT", "PHOTOGRAPH", "RECEIPT", "VOICEMAIL"]
TWISTS = [
    ("SECRET DOOR", "Move to any room right now."),
    ("SPILLED COFFEE", "Oops! Lose 1 coffee."),
    ("WITNESS", "A guest wants to talk: interrogate a suspect for free."),
    ("BLACK CAT", "Swap places with another detective of your choice."),
    ("COLD DRAFT", "A window slams. Move 1 room."),
    ("SECOND WIND", "Take one more action this turn."),
]
DETECTIVES = [
    ("RUSTY HOLLOWAY", "RH", "Inspector", "Grumpy veteran. 30 years on the job. Hates computers.",
     "Old school", "Once per round, interrogate a suspect without paying coffee."),
    ("ADA \"NULL\" BYTE", "AB", "Hacker", "Teenage hacker. Talks in code.",
     "Overclock", "Your first query each round costs 0 coffee."),
    ("IRIS LUMEN", "IL", "Professor", "Forensic scientist. Always calm.",
     "Magnifier", "When you search, draw 2 cards and keep 1, in any room."),
    ("KIT MARLOWE", "KM", "Agent", "Ex-sprinter. Far too much energy.",
     "Sprint", "Move up to 3 rooms instead of 2."),
]
DECK_ROOMS = [r[0] for r in ROOMS if r[2]]


def clue_cards():
    cards = []
    for word, n, code, text, ex in KEYWORDS:
        for k in range(1, n + 1):
            cards.append(dict(type="KEYWORD", title=word, code=f"KW-{code}{k}", text=text, ex=ex))
    for name, code, cols, text in TABLES:
        for k in (1, 2):
            cards.append(dict(type="TABLE", title=name, code=f"TB-{code}{k}", text=text, cols=cols))
    for k, name in enumerate(EVIDENCE, 1):
        cards.append(dict(type="EVIDENCE", title=name, code=f"EV-{k:02d}",
                          text="Scan this card in the Police Console to analyze it. What it reveals depends on the case."))
    for k in range(12):
        two = k >= 8
        cards.append(dict(type="COFFEE", title="DOUBLE SHOT" if two else "ESPRESSO", amount=2 if two else 1, code=None,
                          text=f"Take {2 if two else 1} coffee from the bank, then discard this card."))
    for name, text in TWISTS:
        for _ in (1, 2):
            cards.append(dict(type="TWIST", title=name, code=None, text=text + " Resolve it now, then discard."))
    # deal into the 7 room decks (fixed seed: the same split every time)
    order = list(range(len(cards)))
    random.Random(7).shuffle(order)
    for pos, idx in enumerate(order):
        cards[idx]["room"] = DECK_ROOMS[pos % len(DECK_ROOMS)]
    return cards


CARD_CSS = f"""
.card {{ position:relative; width:{CW + 2 * BLEED}mm; height:{CH + 2 * BLEED}mm; background:{C['noir']}; overflow:hidden; color:{C['bone']}; }}
.card .fr {{ position:absolute; inset:0; }}
.card .in {{ position:absolute; left:{BLEED + 5}mm; top:{BLEED + 5}mm; width:{CW - 10}mm; height:{CH - 10}mm; display:flex; flex-direction:column; }}
.hd {{ display:flex; justify-content:space-between; align-items:center; height:6mm; padding:0 1.6mm; background:var(--c); color:var(--t); }}
.hd .pix {{ font-size:6pt; display:flex; align-items:center; gap:1mm; }}
.hd .mono {{ font-size:6pt; font-weight:700; }}
.mn {{ flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; gap:1.5mm; }}
.ttl {{ font-family:'Bungee'; font-size:12pt; line-height:1.05; }}
.term {{ width:100%; border:.4mm solid {C['bone']}; background:{C['graphite']}; padding:2.5mm 2mm; text-align:left; }}
.term .bar {{ font-family:'Silkscreen'; font-size:4.6pt; color:{C['ash']}; margin-bottom:1.5mm; }}
.term .kw {{ font-family:'IBM Plex Mono'; font-weight:700; font-size:20pt; line-height:1; white-space:nowrap; }}
.term .kw .p {{ color:{C['red']}; }}
.term .kw .cur {{ display:inline-block; width:3.2mm; height:5.5mm; background:{C['red']}; vertical-align:-.3mm; margin-left:1mm; }}
.lbl {{ font-family:'Silkscreen'; font-size:5.5pt; color:{C['ash']}; }}
.bd {{ font-size:7.5pt; line-height:1.3; text-align:center; padding:0 .5mm; }}
.ex {{ font-family:'IBM Plex Mono'; font-size:6.4pt; background:{C['graphite']}; padding:1.2mm 1.5mm; margin-top:1.5mm; text-align:center; }}
.cols {{ display:flex; width:100%; border:.4mm solid {C['bone']}; }}
.cols span {{ flex:1; font-family:'IBM Plex Mono'; font-size:6pt; font-weight:700; padding:1.2mm .5mm; text-align:center; }}
.cols span + span {{ border-left:.4mm solid {C['bone']}; }}
.rows {{ width:100%; }}
.rows i {{ display:block; height:2.2mm; margin-top:1mm; background:{C['graphite']}; }}
.rows i.hit {{ background:{C['red']}; }}
.big {{ font-family:'Bungee'; font-size:40pt; line-height:.9; }}
.ft {{ display:flex; align-items:flex-end; gap:2.5mm; margin-top:2mm; min-height:15mm; }}
.qr {{ width:15mm; height:15mm; flex:none; }}
.qr svg {{ width:100%; height:100%; display:block; }}
.ft .meta {{ display:flex; flex-direction:column; gap:.8mm; flex:1; }}
.ft .code {{ font-family:'IBM Plex Mono'; font-weight:700; font-size:9pt; }}
.ft .deck {{ font-family:'Silkscreen'; font-size:5pt; color:{C['ash']}; display:flex; gap:1mm; align-items:center; }}
.ft.noqr {{ min-height:9mm; justify-content:space-between; align-items:center; border-top:.3mm solid {C['graphite']}; padding-top:1.5mm; }}
/* backs */
.back .in {{ align-items:center; justify-content:center; gap:4mm; }}
.back img {{ width:47mm; }}
.back .rib {{ background:{C['red']}; color:{C['bone']}; font-family:'Bungee'; font-size:9pt; padding:1.4mm 4mm; display:flex; gap:1.5mm; align-items:center; }}
.back .hint {{ font-family:'Silkscreen'; font-size:5pt; color:{C['ash']}; }}
/* detective */
.mono-badge {{ width:24mm; height:24mm; display:flex; align-items:center; justify-content:center; font-family:'Bungee'; font-size:20pt;
  background:{C['bone']}; color:{C['noir']}; clip-path:polygon(30% 0,70% 0,100% 30%,100% 70%,70% 100%,30% 100%,0 70%,0 30%); }}
.role {{ font-family:'Silkscreen'; font-size:6pt; color:{C['red']}; }}
.quote {{ font-size:7pt; font-style:italic; color:{C['ash']}; }}
.power {{ border:.4mm solid {C['red']}; padding:2mm; font-size:7.5pt; line-height:1.3; text-align:left; width:100%; }}
.power b {{ font-family:'Bungee'; font-weight:400; color:{C['red']}; font-size:8pt; display:block; margin-bottom:.8mm; }}
"""


THEME = "dossier"       # card design (validated: Case File): "noir", "dossier" or "deco"
BRASS = "#C9923A"
STAMP = {"KEYWORD": "ACCESS GRANTED", "TABLE": "RECORDS", "EVIDENCE": "EVIDENCE",
         "COFFEE": "BREAK TIME", "TWIST": "URGENT", "DETECTIVE": "CLASSIFIED"}

THEME_CSS = f"""
/* ---------- square corners everywhere */
.card .fr {{ position:absolute; inset:0; }}
.ic-blue {{ color:{C['blue']}; }} .ic-amber {{ color:{C['amber']}; }} .ic-red {{ color:{C['red']}; }}
.medal {{ display:flex; align-items:center; justify-content:center; }}
/* ---------- CASE FILE (paper dossier) */
.t-dossier {{ background:#EFE8D8; color:{C['noir']}; }}
.t-dossier .margin {{ position:absolute; left:{BLEED + 3.4}mm; top:0; bottom:0; width:.3mm; background:{C['red']}; opacity:.55; }}
.t-dossier .hd {{ background:{C['noir']}; color:{C['bone']}; border-left:3.2mm solid var(--c); }}
.t-dossier .lbl, .t-dossier .ft .deck, .t-dossier .quote {{ color:#6B665C; }}
.t-dossier .ttl {{ color:{C['noir']}; }}
.t-dossier .term {{ background:#F8F4EA; border:.4mm dashed {C['noir']}; }}
.t-dossier .term .bar {{ color:#6B665C; }}
.t-dossier .ex {{ background:#E2D9C5; }}
.t-dossier .cols {{ border-color:{C['noir']}; }} .t-dossier .cols span + span {{ border-color:{C['noir']}; }}
.t-dossier .rows i {{ background:#D9CFBA; }} .t-dossier .rows i.hit {{ background:{C['red']}; }}
.t-dossier .ic-amber {{ color:#B8741A; }} .t-dossier .ic-blue {{ color:#3E5F7D; }}
.t-dossier .ft.noqr {{ border-top:.3mm dashed {C['noir']}; }}
.t-dossier .power {{ background:#F8F4EA; }}
.t-dossier .mono-badge {{ background:{C['noir']}; color:{C['bone']}; }}
.t-dossier .qr svg rect {{ fill:#fff; }}
.stamp {{ position:absolute; right:{BLEED + 4}mm; top:{BLEED + 15}mm; transform:rotate(-11deg); border:.6mm solid {C['red']};
  color:{C['red']}; font-family:'Bungee'; font-size:6.5pt; padding:.5mm 1.5mm; letter-spacing:.08em; opacity:.8; z-index:2; }}
.clip {{ position:absolute; left:{BLEED + 8}mm; top:{BLEED + 1}mm; width:5mm; height:13mm; }}
.t-dossier.back {{ background:#C9A46E; }}
.t-dossier.back .tab {{ position:absolute; left:{BLEED + 6}mm; top:{BLEED + 3}mm; width:26mm; height:6mm; background:#D8B77F;
  font-family:'Silkscreen'; font-size:5.5pt; color:#5A4325; display:flex; align-items:center; justify-content:center; }}
.t-dossier.back .label {{ background:#F8F4EA; border:.3mm solid #5A4325; padding:1.6mm 3mm; font-family:'IBM Plex Mono'; font-weight:700;
  font-size:8.5pt; color:{C['noir']}; display:flex; gap:1.5mm; align-items:center; }}
.t-dossier.back .bigstamp {{ border:.8mm solid {C['red']}; color:{C['red']}; font-family:'Bungee'; font-size:11pt; padding:1mm 3mm;
  transform:rotate(-8deg); opacity:.85; letter-spacing:.06em; }}
.t-dossier.back .hint {{ color:#5A4325; }}
/* ---------- ART DECO (noir + brass) */
.t-deco .hd {{ background:none; color:{BRASS}; border-top:.35mm solid {BRASS}; border-bottom:.35mm solid {BRASS}; }}
.t-deco .hd .pix svg {{ color:var(--c); }}
.t-deco .ttl {{ letter-spacing:.06em; }}
.t-deco .lbl {{ color:{BRASS}; }}
.t-deco .medal {{ width:23mm; height:23mm; border-radius:50%; border:.45mm solid {BRASS}; box-shadow:0 0 0 1mm {C['noir']}, 0 0 0 1.25mm {BRASS}; }}
.t-deco .term {{ border-color:{BRASS}; background:#141416; }}
.t-deco .term .kw .p {{ color:{BRASS}; }}
.t-deco .ex {{ background:#161618; border-top:.3mm solid {BRASS}; }}
.t-deco .cols, .t-deco .cols span + span {{ border-color:{BRASS}; }}
.t-deco .rows i {{ background:#1C1C1F; }}
.t-deco .power {{ border-color:{BRASS}; }} .t-deco .power b {{ color:{BRASS}; }}
.t-deco .mono-badge {{ background:{BRASS}; }}
.t-deco .role {{ color:{BRASS}; }}
.t-deco .ft.noqr {{ border-top:.3mm solid {BRASS}; }}
.t-deco .ft .code {{ color:{BRASS}; }}
.t-deco.back .cart {{ border:.4mm solid {BRASS}; outline:.25mm solid {BRASS}; outline-offset:.8mm; padding:1.4mm 4mm; color:{C['bone']};
  font-family:'Bungee'; font-size:9pt; display:flex; gap:1.5mm; align-items:center; background:{C['noir']}; }}
.t-deco.back .hint {{ color:{BRASS}; }}
"""


def frame_svg(colour, kind="face"):
    """Square-cornered frame, 2.2 mm inside the trim, in the current THEME."""
    w, h = CW + 2 * BLEED, CH + 2 * BLEED
    i = BLEED + 2.2
    o = [f'<svg class="fr" viewBox="0 0 {w} {h}">']
    if THEME == "dossier":
        o.append(f'<rect x="{i}" y="{i}" width="{w - 2 * i}" height="{h - 2 * i}" fill="none" stroke="#1B1B1D" stroke-width=".3"/>'
                 f'<rect x="{i + .8}" y="{i + .8}" width="{w - 2 * i - 1.6}" height="{h - 2 * i - 1.6}" fill="none" stroke="#1B1B1D" stroke-width=".15"/>')
    elif THEME == "deco":
        b = BRASS
        o.append(f'<rect x="{i}" y="{i}" width="{w - 2 * i}" height="{h - 2 * i}" fill="none" stroke="{b}" stroke-width=".35"/>'
                 f'<rect x="{i + 1}" y="{i + 1}" width="{w - 2 * i - 2}" height="{h - 2 * i - 2}" fill="none" stroke="{b}" stroke-width=".15"/>')
        for cx, cy, sx, sy in [(i + 1, i + 1, 1, 1), (w - i - 1, i + 1, -1, 1), (i + 1, h - i - 1, 1, -1), (w - i - 1, h - i - 1, -1, -1)]:
            rays = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + sx * 3.6 * __import__("math").cos(a)}" y2="{cy + sy * 3.6 * __import__("math").sin(a)}" stroke="{b}" stroke-width=".18"/>'
                           for a in [k * 3.14159 / 10 for k in range(1, 5)])
            o.append(rays + f'<path d="M{cx + sx * 3.6} {cy} A3.6 3.6 0 0 {1 if sx * sy > 0 else 0} {cx} {cy + sy * 3.6}" fill="none" stroke="{b}" stroke-width=".25"/>'
                     f'<rect x="{cx - .8 if sx > 0 else cx - .8}" y="{cy - .8}" width="1.6" height="1.6" fill="{b}" transform="rotate(45 {cx} {cy})"/>')
    else:  # noir
        o.append(f'<rect x="{i}" y="{i}" width="{w - 2 * i}" height="{h - 2 * i}" fill="none" stroke="{colour}" stroke-width=".35"/>')
        for cx, cy in [(i, i), (w - i, i), (i, h - i), (w - i, h - i)]:
            o.append(f'<rect x="{cx - .9}" y="{cy - .9}" width="1.8" height="1.8" fill="{colour}"/>')
    o.append("</svg>")
    return "".join(o)


PAPERCLIP = ('<svg class="clip" viewBox="0 0 10 26"><path d="M3 6V20a3 3 0 0 0 6 0V4a4 4 0 0 0-8 0v15" fill="none" '
             'stroke="#8C877D" stroke-width="1.1" stroke-linecap="round"/></svg>')


def theme_decor(kind):
    if THEME == "dossier":
        return '<div class="margin"></div>' + PAPERCLIP + f'<div class="stamp">{STAMP[kind]}</div>'
    return ""


def card_face(cd):
    col, txt, ic = TYPES[cd["type"]]
    t = cd["type"]
    head = (f'<div class="hd" style="--c:{col};--t:{txt}"><span class="pix">{icon(ic, "3.6mm", 2.4)} {t}</span>'
            f'<span class="mono">{cd["code"] or ""}</span></div>')
    if t == "KEYWORD":
        main = (f'<div class="lbl">UNLOCKS A KEYWORD</div><div class="term"><div class="bar">POLICE CONSOLE v1.0</div>'
                f'<div class="kw"><span class="p">&gt;</span> {esc(cd["title"])}<span class="cur"></span></div></div>'
                f'<div class="bd">{esc(cd["text"])}<div class="ex">{esc(cd["ex"])}</div></div>')
    elif t == "TABLE":
        cols = "".join(f"<span>{c_}</span>" for c_ in cd["cols"])
        main = (f'<div class="lbl">UNLOCKS A TABLE</div><div class="ttl">{esc(cd["title"])}</div>'
                f'<div class="cols">{cols}</div><div class="rows"><i></i><i></i><i class="hit"></i><i></i></div>'
                f'<div class="bd">{esc(cd["text"])}</div>')
    elif t == "EVIDENCE":
        main = (f'<div class="medal ic-blue">{icon("magnifier", "15mm", 1.6)}</div>'
                f'<div class="ttl">{esc(cd["title"])}</div><div class="bd">{esc(cd["text"])}</div>')
    elif t == "COFFEE":
        main = (f'<div class="medal ic-amber">{icon("cup", "14mm", 1.6)}</div>'
                f'<div class="big ic-amber">+{cd["amount"]}</div>'
                f'<div class="ttl" style="font-size:10pt">{esc(cd["title"])}</div><div class="bd">{esc(cd["text"])}</div>')
    else:  # TWIST
        main = (f'<div class="medal ic-red">{icon("bolt", "14mm", 1.6)}</div>'
                f'<div class="ttl">{esc(cd["title"])}</div><div class="bd">{esc(cd["text"]).replace("coffee", "coffee " + cup())}</div>')
    main = main.replace(" coffee from", f" coffee {cup()} from") if t == "COFFEE" else main
    room_ic = next(r[1] for r in ROOMS if r[0] == cd["room"])
    deck = f'<span class="deck">{icon(room_ic, "2.6mm", 2.6)} DECK: {cd["room"]}</span>'
    if cd["code"]:
        foot = (f'<div class="ft"><div class="qr" data-code="{cd["code"]}"></div><div class="meta">'
                f'<span class="lbl">SCAN IN THE POLICE CONSOLE</span><span class="code">{cd["code"]}</span>{deck}</div></div>')
    else:
        foot = f'<div class="ft noqr"><span class="lbl">RESOLVE NOW</span>{deck}</div>'
    return (f'<div class="card t-{THEME}">{frame_svg(C["red"] if t in ("TWIST", "TABLE") else col)}{theme_decor(t)}'
            f'<div class="in">{head}<div class="mn">{main}</div>{foot}</div></div>')


def card_back(room):
    ic = next(r[1] for r in ROOMS if r[0] == room) if room != "DETECTIVE" else "pawn"
    hint = "ROOM DECK" if room != "DETECTIVE" else "DETECTIVE CARD"
    if THEME == "dossier":
        light = LOGO.replace("dark_transparent", "light_transparent")
        return (f'<div class="card t-dossier back">{frame_svg(C["noir"])}<div class="tab">CASE FILE N&#176; 1123</div>'
                f'<div class="in"><img src="{light}"><div class="label">{icon(ic, "4mm", 2.4)} {room}</div>'
                f'<div class="bigstamp">CONFIDENTIAL</div><div class="hint pix">{hint}</div></div></div>')
    if THEME == "deco":
        rays = "".join(f'<line x1="34.5" y1="47" x2="{34.5 + 80 * __import__("math").cos(k * 3.14159 / 18)}" y2="{47 + 80 * __import__("math").sin(k * 3.14159 / 18)}" '
                       f'stroke="{BRASS}" stroke-width=".25" opacity=".35"/>' for k in range(36))
        sun = f'<svg class="fr" viewBox="0 0 {CW + 2 * BLEED} {CH + 2 * BLEED}">{rays}<circle cx="34.5" cy="47" r="26" fill="{C["noir"]}"/>' \
              f'<circle cx="34.5" cy="47" r="26" fill="none" stroke="{BRASS}" stroke-width=".35"/></svg>'
        return (f'<div class="card t-deco back">{sun}{frame_svg(BRASS)}<div class="in"><img src="{LOGO}">'
                f'<div class="cart">{icon(ic, "4mm", 2.4)} {room}</div><div class="hint pix">{hint}</div></div></div>')
    return (f'<div class="card t-noir back">{RAIN}{frame_svg(C["red"])}<div class="in"><img src="{LOGO}">'
            f'<div class="rib">{icon(ic, "4mm", 2.4)} {room}</div>'
            f'<div class="hint">{hint}</div></div></div>')


def detective_face(d):
    name, ini, role, quote, ptitle, ptext = d
    col, txt, ic = TYPES["DETECTIVE"]
    return (f'<div class="card t-{THEME}">{frame_svg(col)}{theme_decor("DETECTIVE")}<div class="in">'
            f'<div class="hd" style="--c:{col};--t:{txt}"><span class="pix">{icon(ic, "3.6mm", 2.4)} DETECTIVE</span><span class="mono">QUERY DIVISION</span></div>'
            f'<div class="mn"><div class="mono-badge">{ini}</div><div class="role">{role.upper()}</div>'
            f'<div class="ttl" style="font-size:11pt">{esc(name)}</div><div class="quote">{esc(quote)}</div>'
            f'<div class="power"><b>{esc(ptitle)}</b>{esc(ptext).replace("coffee", "coffee " + cup())}</div></div>'
            f'<div class="ft noqr"><span class="lbl">ONE POWER, ALL GAME</span><span class="lbl">2-4 PLAYERS</span></div></div></div>')


def all_cards():
    """(face_html, back_html, file_stem) for every printed card, in deck order."""
    out = []
    for cd in clue_cards():
        stem = (cd["code"] or f'{cd["type"][:2]}-{cd["title"].replace(" ", "-")}').lower()
        out.append((card_face(cd), card_back(cd["room"]), stem))
    for d in DETECTIVES:
        out.append((detective_face(d), card_back("DETECTIVE"), "det-" + d[1].lower()))
    # make file names unique (coffee / twist cards repeat)
    seen, res = {}, []
    for f, b, s in out:
        seen[s] = seen.get(s, 0) + 1
        res.append((f, b, s if seen[s] == 1 else f"{s}-{seen[s]}"))
    return res


def cards_bleed_pdf(which):
    """One card per page: 69 x 94 mm (bleed) + 10 mm slug with crop marks."""
    pw, ph = CW + 2 * (BLEED + SLUG), CH + 2 * (BLEED + SLUG)
    pages = []
    for f, b, _ in all_cards():
        html_ = f if which == "faces" else b
        pages.append(f'<div class="sheet" style="width:{pw}mm;height:{ph}mm"><div style="position:absolute;left:{SLUG}mm;top:{SLUG}mm">{html_}</div>'
                     f'{cropmarks(SLUG + BLEED, SLUG + BLEED, CW, CH)}</div>')
    return page(f"The Last Query - cards {which} (bleed)", pw, ph, "".join(pages), CARD_CSS + THEME_CSS, qr=(which == "faces"))


def cards_a4(which):
    """Home printing: 3 x 3 trimmed cards per A4 page, crop marks on the grid. Backs mirrored for duplex."""
    W, H = 210, 297
    gx, gy = (W - 3 * CW) / 2, (H - 3 * CH) / 2
    cards = all_cards()
    pages = []
    for p in range(0, len(cards), 9):
        cells = []
        for k, (f, b, _) in enumerate(cards[p:p + 9]):
            r, c = divmod(k, 3)
            if which == "backs":
                c = 2 - c
            content = f if which == "faces" else b
            cells.append(f'<div style="position:absolute;left:{gx + c * CW}mm;top:{gy + r * CH}mm;width:{CW}mm;height:{CH}mm;overflow:hidden">'
                         f'<div style="margin:-{BLEED}mm 0 0 -{BLEED}mm">{content}</div></div>')
        marks = []
        for c in range(4):
            x = gx + c * CW
            marks.append(f'<div class="mark" style="left:{x - .125}mm;top:{gy - 8}mm;width:.25mm;height:6mm"></div>')
            marks.append(f'<div class="mark" style="left:{x - .125}mm;top:{gy + 3 * CH + 2}mm;width:.25mm;height:6mm"></div>')
        for r in range(4):
            y = gy + r * CH
            marks.append(f'<div class="mark" style="top:{y - .125}mm;left:{gx - 8}mm;height:.25mm;width:6mm"></div>')
            marks.append(f'<div class="mark" style="top:{y - .125}mm;left:{gx + 3 * CW + 2}mm;height:.25mm;width:6mm"></div>')
        pages.append(f'<div class="sheet" style="width:{W}mm;height:{H}mm">{"".join(cells)}{"".join(marks)}</div>')
    return page(f"The Last Query - cards {which} A4", W, H, "".join(pages), CARD_CSS + THEME_CSS, qr=(which == "faces"))


def card_single(content):
    w, h = CW + 2 * BLEED, CH + 2 * BLEED
    return page("card", w, h, f'<div class="sheet" style="width:{w}mm;height:{h}mm">{content}</div>', CARD_CSS + THEME_CSS, qr=True)


def cards_overview(sample, title=""):
    """8 trimmed cards (4 x 2) on a 300 x 210 sheet, for proposals and previews."""
    head = (f'<div style="font-family:Bungee;font-size:14pt;color:#F4F0E6;margin-bottom:5mm">{title}</div>' if title else "")
    cells = "".join(f'<div style="width:{CW}mm;height:{CH}mm;overflow:hidden;box-shadow:0 1mm 3mm #000"><div style="margin:-{BLEED}mm 0 0 -{BLEED}mm">{s}</div></div>'
                    for s in sample)
    body = (f'<div style="background:#1A1A1D;padding:8mm 10mm;width:300mm;height:{232 if title else 210}mm">{head}'
            f'<div style="display:grid;grid-template-columns:repeat(4,{CW}mm);gap:7mm 8mm;justify-content:center">{cells}</div></div>')
    return page("cards overview", 300, 232 if title else 210, body, CARD_CSS + THEME_CSS, qr=True)


def proposal_sample():
    cards = clue_cards()
    pick = [next(c for c in cards if c["type"] == t) for t in ("KEYWORD", "TABLE", "EVIDENCE", "COFFEE", "TWIST")]
    return ([card_face(c) for c in pick] + [detective_face(DETECTIVES[1]), card_back(pick[0]["room"]), card_back("DETECTIVE")])


if __name__ == "__main__":
    SRC.mkdir(parents=True, exist_ok=True)
    (SRC / "cards").mkdir(exist_ok=True)
    (SRC / "brand_sheet.html").write_text(brand_sheet())
    import build_board  # v2 board: manor floor plan (the old board() above is kept for reference)
    (SRC / "board_A2.html").write_text(build_board.board_html())
    # cards V2 (40 cards): see build_cards.py
    import build_cards
    build_cards.main()

