#!/usr/bin/env python3
"""Tokens (coffee, clock, suspended), detective standees and the Detective
Notebook sheet for The Last Query. Pure SVG in millimetres.

Run:  python3 DA/tools/build_tokens.py   (writes DA/tools/print_src/tokens_A4.html and notebook_A5.html)
"""
import build_print as bp

C = bp.C
NOIR, BONE, RED, OX, AMBER, BLUE, ASH, GRAPH = (C[k] for k in ("noir", "bone", "red", "oxblood", "amber", "blue", "ash", "graphite"))
BRASS, PAPER = "#C9923A", "#EFE8D8"
TB = 1.5                                 # token bleed (mm)
CUT = "#8C877D"                          # cut-line colour

# detective colours: background, ink
DET_COL = {"RH": (AMBER, NOIR), "AB": (RED, BONE), "IL": (BLUE, BONE), "KM": (BONE, NOIR),
           "P1": (AMBER, NOIR), "P2": (RED, BONE), "P3": (BLUE, BONE), "P4": (BONE, NOIR)}
PAWNS = [("PLAYER 1", "P1", "Detective"), ("PLAYER 2", "P2", "Detective"), ("PLAYER 3", "P3", "Detective"), ("PLAYER 4", "P4", "Detective")]
SEMI = "M10 4h4v4h-4z M10 12h4v4l-2 4h-2.6l1.6-4h-1z"
SUSPECTS = ["Lady Margaret Ravenscroft", "Dr. Felix Moreau", "Ivy Ravenscroft", "Colonel Bram Hartley", "Sofia Delacroix", "Gideon Pike",
            "Oscar Lindqvist", "Nora Quill", "Hugo Ravenscroft", "Clara Finch", "Father Thomas Reilly", "Dante Russo"]


def icon(name, cx, cy, size, colour, sw=2):
    s = size / 24
    return (f'<g transform="translate({cx - size / 2:.2f},{cy - size / 2:.2f}) scale({s:.4f})"><path d="{bp.ICONS[name]}" '
            f'fill="none" stroke="{colour}" stroke-width="{sw}" stroke-linecap="square" stroke-linejoin="miter"/></g>')


def text(x, y, s, size, fill, family="Bungee", anchor="middle", extra=""):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'


def cut_circle(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CUT}" stroke-width=".15" stroke-dasharray="1 .6"/>'


# ------------------------------------------------------------------ token art (centred on cx, cy, radius r = trim)
def coffee_token(cx, cy, r=10, cut=True):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r + TB}" fill="{AMBER}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r - 1.3}" fill="none" stroke="{NOIR}" stroke-width=".45"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r - 2.1}" fill="none" stroke="{NOIR}" stroke-width=".2" stroke-dasharray=".7 .5"/>',
         icon("cup", cx, cy - 1, r * 1.05, NOIR, 2.3),
         text(cx, cy + r * .62, "COFFEE", r * .2, NOIR, "Silkscreen")]
    if cut:
        o.append(cut_circle(cx, cy, r))
    return "".join(o)


def clock_token(cx, cy, r=4.4, cut=True):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r + TB}" fill="{RED}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r - .6}" fill="none" stroke="{BONE}" stroke-width=".3"/>',
         f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r * .62}" stroke="{BONE}" stroke-width=".55"/>',
         f'<line x1="{cx}" y1="{cy}" x2="{cx + r * .45}" y2="{cy + r * .2}" stroke="{BONE}" stroke-width=".55"/>',
         f'<circle cx="{cx}" cy="{cy}" r=".55" fill="{BONE}"/>']
    if cut:
        o.append(cut_circle(cx, cy, r))
    return "".join(o)


def suspended_token(cx, cy, r=11, cut=True):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r + TB}" fill="{NOIR}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r - 1.2}" fill="none" stroke="{RED}" stroke-width=".7"/>',
         f'<g transform="rotate(-14 {cx} {cy})"><rect x="{cx - r * .82}" y="{cy - 3.4}" width="{r * 1.64}" height="6.8" fill="{RED}"/>',
         text(cx, cy + 1.4, "SUSPENDED", 3.1, BONE), "</g>",
         text(cx, cy - r * .48, "OFF THE CASE", 1.7, BONE, "Silkscreen"),
         text(cx, cy + r * .55, "SKIP 2 TURNS", 1.7, RED, "Silkscreen")]
    if cut:
        o.append(cut_circle(cx, cy, r))
    return "".join(o)


def detective_figure(x, y, h, fill, accent):
    """Logo detective silhouette, scaled to height h with its top-left at (x, y)."""
    s = h / 495
    pts = ["1028,150 1092,150 1100,198 1020,198", "996,198 1124,198 1114,212 1006,212",
           "1047,222 1080,222 1075,244 1055,249",
           "1030,228 1056,300 1092,228 1120,262 1128,420 1138,590 978,590 988,420 998,262",
           "992,630 1040,630 1040,645 986,645", "1076,630 1124,630 1132,645 1076,645"]
    body = "".join(f'<polygon points="{p}" fill="{fill}"/>' for p in pts)
    body += f'<rect x="1005" y="588" width="30" height="46" fill="{fill}"/><rect x="1081" y="588" width="30" height="46" fill="{fill}"/>'
    body += f'<rect x="1021" y="185" width="78" height="10" fill="{accent}"/>'
    body += f'<polygon points="1034,318 1060,312 1068,352 1042,358" fill="{accent}"/>'
    body += f'<path d="M984 392H1134 M1057 300L1049 592" stroke="{accent if fill == BONE else NOIR}" stroke-width="6" opacity=".55"/>'
    return f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f}) translate(-978,-150)">{body}</g>'


def standee(x, y, d, w=26, panel=38, tab=10):
    """Fold-up A-frame standee. Strip: tab | back (upside down) | fold | front | tab. Cut = solid, fold = dashed."""
    name, ini, role, *_ = d
    bg, ink = DET_COL[ini]
    total = 2 * tab + 2 * panel
    o = [f'<rect x="{x - TB}" y="{y - TB}" width="{w + 2 * TB}" height="{total + 2 * TB}" fill="{GRAPH}"/>']

    def face(py, flip):
        g = [f'<rect x="{x}" y="{py}" width="{w}" height="{panel}" fill="{bg}"/>',
             f'<rect x="{x + 1}" y="{py + 1}" width="{w - 2}" height="{panel - 2}" fill="none" stroke="{ink}" stroke-width=".25"/>',
             detective_figure(x + w / 2 - 4.4, py + 3.2, 24, ink, RED if bg != RED else NOIR),
             f'<rect x="{x + 1.6}" y="{py + panel - 9.6}" width="{w - 3.2}" height="7.6" fill="{NOIR}"/>',
             text(x + w / 2, py + panel - 5.1, ini, 3.6, BONE),
             text(x + w / 2, py + panel - 2.7, role.upper(), 1.6, ASH, "Silkscreen")]
        inner = "".join(g)
        if flip:
            inner = f'<g transform="rotate(180 {x + w / 2} {py + panel / 2})">{inner}</g>'
        return inner
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{tab}" fill="{NOIR}"/>' + text(x + w / 2, y + tab / 2 + .8, "GLUE", 2, ASH, "Silkscreen"))
    o.append(face(y + tab, True))
    o.append(face(y + tab + panel, False))
    o.append(f'<rect x="{x}" y="{y + tab + 2 * panel}" width="{w}" height="{tab}" fill="{NOIR}"/>'
             + text(x + w / 2, y + tab + 2 * panel + tab / 2 + .8, "GLUE", 2, ASH, "Silkscreen"))
    # cut + folds
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{total}" fill="none" stroke="{CUT}" stroke-width=".2"/>')
    for fy in (y + tab, y + tab + panel, y + tab + 2 * panel):
        o.append(f'<line x1="{x - 3}" y1="{fy}" x2="{x + w + 3}" y2="{fy}" stroke="{RED}" stroke-width=".25" stroke-dasharray="1.2 .8"/>')
    return "".join(o)


# ------------------------------------------------------------------ A4 sheets
def query_token(cx, cy, r=10, cut=True):
    """V2 Query Token: black disc, red block semicolon (the logo's ';')."""
    k = r * .78 / 12
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r + TB}" fill="{NOIR}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r - 1.1}" fill="none" stroke="{RED}" stroke-width=".6"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r - 2}" fill="none" stroke="{RED}" stroke-width=".2" stroke-dasharray=".8 .6"/>',
         f'<g transform="translate({cx - 12 * k},{cy - 12 * k - 1.3}) scale({k})"><path d="{SEMI}" fill="#7E0C1F" transform="translate(.9,.9)"/><path d="{SEMI}" fill="{RED}"/></g>',
         text(cx, cy + r * .66, "QUERY", r * .16, BONE, "Silkscreen")]
    if cut:
        o.append(cut_circle(cx, cy, r))
    return "".join(o)


QB = 3.0                                 # Query Token bleed (mm): print norm of the project
TOKEN_CODES = [f"Q-{k:02d}" for k in range(1, 21)]   # QR on the back: TLQ:Q-01 ... TLQ:Q-20 (same codes in the app)
GRID = [(30 + c_ * 37.5, 47 + r_ * 26) for r_ in range(4) for c_ in range(5)]


def query_token_front(cx, cy, r=10):
    """Front: the V2 token art, with a 3 mm bleed."""
    return query_token(cx, cy, r, True).replace(f'r="{r + TB}" fill="{NOIR}"', f'r="{r + QB}" fill="{NOIR}"', 1)


def query_token_back(cx, cy, code, r=10):
    """Back (playtest 1, T1): bone disc, QR 'TLQ:<code>' in the safe area, backup code under it."""
    q = 11.0                                                    # QR side incl. quiet zone (mm)
    return "".join([
        f'<circle cx="{cx}" cy="{cy}" r="{r + QB}" fill="{BONE}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - .7}" fill="none" stroke="{RED}" stroke-width=".45"/>',
        f'<g class="qrg" data-code="{code}" data-x="{cx - q / 2:.2f}" data-y="{cy - 1.0 - q / 2:.2f}" data-s="{q}"></g>',
        text(cx, cy + 7.35, code, 2.3, NOIR, "IBM Plex Mono", extra='font-weight="700" letter-spacing=".12"'),
        cut_circle(cx, cy, r)])


QR_SVG_RUN = """<script>
document.querySelectorAll('g.qrg').forEach(function(g){
  var q = qrcode(0, 'M'); q.addData('TLQ:' + g.dataset.code); q.make();
  var n = q.getModuleCount(), m = n + 2, s = '';
  for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) if (q.isDark(r, c)) s += 'M' + (c + 1) + ',' + (r + 1) + 'h1v1h-1z';
  var k = g.dataset.s / m;
  g.setAttribute('transform', 'translate(' + g.dataset.x + ',' + g.dataset.y + ') scale(' + k + ')');
  g.innerHTML = '<rect width="' + m + '" height="' + m + '" fill="#FFFFFF"/><path d="' + s + '" fill="#0B0B0C" shape-rendering="crispEdges"/>';
});
</script>"""


def _sheet(o, W=210, H=297):
    return (f'<div class="sheet" style="width:{W}mm;height:{H}mm;background:#fff"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}mm" height="{H}mm">{"".join(o)}</svg></div>')


def _page(title, sheets):
    html = bp.page(title, 210, 297, "".join(sheets), ".sheet svg{display:block}", qr=True)
    return html.replace("</body>", QR_SVG_RUN + "</body>")


def tokens_sheet():
    """Duplex A4 (playtest 1): page 1 = 20 token fronts + 4 pawns, page 2 = token backs (QR), mirrored for a long-edge flip."""
    W = 210
    o = [text(12, 16, "THE LAST QUERY &#183; QUERY TOKENS &amp; PAWNS &#183; SIDE 1 / 2", 5, NOIR, "Bungee", "start"),
         text(12, 21, "Print BOTH pages double-sided (flip on long edge), 100 %, on 250-350 g/m&#178; card. Cut along the dotted circles. Bleed 3 mm. No duplex? Use the GLUE version.", 2.6, "#555", "Archivo", "start"),
         text(12, 30, "QUERY TOKENS &#215; 20 (Q-01 &#8230; Q-20) &#183; &#216; 20 MM &#183; QR ON THE BACK", 2.8, RED, "Silkscreen", "start")]
    for cx, cy in GRID:
        o.append(query_token_front(cx, cy))
    y0 = 47 + 4 * 26 + 4
    o.append(text(12, y0, "DETECTIVE PAWNS &#215; 4 &#183; FOLD INTO A TENT", 2.8, RED, "Silkscreen", "start"))
    for k, d in enumerate(PAWNS):
        o.append(standee(22 + k * 46, y0 + 6, d))
    o.append(text(12, y0 + 116, "Cut along the grey line, fold on the red dashed lines into a triangle, glue the two GLUE tabs together.", 2.6, "#333", "Archivo", "start"))
    b = [text(W - 12, 16, "SIDE 2 / 2 &#183; BACKS OF THE QUERY TOKENS", 5, NOIR, "Bungee", "end"),
         text(W - 12, 21, "Mirrored on purpose: each back lands behind its front when you flip on the long edge.", 2.6, "#555", "Archivo", "end")]
    for (cx, cy), code in zip(GRID, TOKEN_CODES):
        b.append(query_token_back(W - cx, cy, code))
    return _page("The Last Query - query tokens A4 duplex", [_sheet(o), _sheet(b)])


def tokens_glue_sheet():
    """One-sided A4 (playtest 1): fronts on top, backs below, same order. Glue a front and its back on each side of the card."""
    o = [text(12, 16, "THE LAST QUERY &#183; QUERY TOKENS &#183; GLUE VERSION", 5, NOIR, "Bungee", "start"),
         text(12, 21, "One-sided, 100 %. Glue the FRONTS on one side of a 1.5 mm card and the BACKS on the other side, then cut. Bleed 3 mm.", 2.6, "#555", "Archivo", "start"),
         text(12, 30, "FRONTS &#215; 20 &#183; &#216; 20 MM", 2.8, RED, "Silkscreen", "start")]
    for cx, cy in GRID:
        o.append(query_token_front(cx, cy))
    dy = 4 * 26 + 30
    o.append(text(12, 30 + dy, "BACKS &#215; 20 &#183; SAME ORDER AS THE FRONTS (Q-01 TOP LEFT)", 2.8, RED, "Silkscreen", "start"))
    for (cx, cy), code in zip(GRID, TOKEN_CODES):
        o.append(query_token_back(cx, cy + dy, code))
    o.append(text(12, 290, "Any back can go with any front: the code only matters on the back.", 2.6, "#333", "Archivo", "start"))
    return _page("The Last Query - query tokens A4 glue", [_sheet(o)])


def notebook():
    """Detective Notebook V2: A5, 2 pages (front: suspects x traits, back: my clues, accusation, table talk)."""
    W, H = 148, 210
    pw, ph = W + 2 * (bp.BLEED + bp.SLUG), H + 2 * (bp.BLEED + bp.SLUG)
    t = bp.BLEED + bp.SLUG
    traits = ["AGE", "HEIGHT", "SHOE", "HAND", "HAIR", "GLASSES", "SMELL"]
    head = "".join(f"<th>{x}</th>" for x in traits)
    rows = "".join(f"<tr><td class='n'>{n}</td>{'<td></td>' * len(traits)}<td class='x'></td></tr>" for n in SUSPECTS)
    clue_rows = "".join("<tr><td></td><td></td><td></td><td class='s'><i></i><i></i><i></i></td></tr>" for _ in range(9))
    tok = (f'<svg viewBox="0 0 24 24" style="width:3.4mm;height:3.4mm;vertical-align:-.7mm"><circle cx="12" cy="12" r="11" fill="{NOIR}"/>'
           f'<path d="{SEMI}" fill="{RED}"/></svg>')
    css = f"""
    .bleed {{ position:absolute; left:{bp.SLUG}mm; top:{bp.SLUG}mm; width:{W + 2 * bp.BLEED}mm; height:{H + 2 * bp.BLEED}mm; background:{PAPER}; }}
    .trim {{ position:absolute; left:{t}mm; top:{t}mm; width:{W}mm; height:{H}mm; padding:8.5mm 9mm 8mm 11mm; color:{NOIR}; }}
    .margin {{ position:absolute; left:{t + 6}mm; top:{bp.SLUG}mm; height:{H + 6}mm; width:.3mm; background:{RED}; opacity:.5; }}
    .hd {{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:.6mm solid {NOIR}; padding-bottom:1.5mm; }}
    .hd h1 {{ font-family:Bungee; font-weight:400; font-size:14pt; line-height:1; }}
    .hd .pix {{ font-size:6pt; color:{RED}; text-align:right; }}
    .fields {{ display:flex; gap:4mm; margin:2.6mm 0 3mm; font:600 8pt Archivo; }}
    .fields span {{ flex:1; border-bottom:.3mm solid {NOIR}; padding-bottom:2.6mm; }}
    table {{ width:100%; border-collapse:collapse; font:400 7.4pt Archivo; }}
    th {{ font-family:Silkscreen; font-weight:400; font-size:5.2pt; background:{NOIR}; color:{BONE}; padding:1.3mm .4mm; letter-spacing:.02em; }}
    td {{ border:.25mm solid {NOIR}; height:8.2mm; }}
    td.n {{ font-weight:600; padding-left:1.4mm; width:37mm; font-size:7.2pt; line-height:1.1; }}
    td.x {{ width:6mm; background:#E6DCC4; }}
    th.x {{ background:{RED}; }}
    h2 {{ font-family:Silkscreen; font-weight:400; font-size:7pt; color:{RED}; margin:3.6mm 0 1.4mm; letter-spacing:.05em; }}
    .help {{ font:400 7.4pt/1.35 Archivo; }}
    .gold {{ border-left:1mm solid {RED}; padding:.6mm 0 .6mm 2.4mm; font:italic 400 8pt/1.35 Archivo; margin-top:1.6mm; }}
    .clues td {{ height:8.2mm; }}
    .clues td.s {{ width:15mm; text-align:center; }}
    .clues td.s i {{ display:inline-block; width:3mm; height:3mm; border:.3mm solid {NOIR}; margin:0 .4mm; }}
    .acc {{ border:.5mm solid {NOIR}; padding:2.4mm 3mm; background:#F8F4EA; font:400 9pt/2 Archivo; }}
    .acc u {{ display:inline-block; border-bottom:.3mm solid {NOIR}; text-decoration:none; }}
    .say {{ font:italic 400 7.8pt/1.35 Archivo; margin:1.2mm 0; padding-left:2.4mm; border-left:.8mm solid {RED}; }}
    .code {{ font:400 7pt/1.45 'IBM Plex Mono'; background:{NOIR}; color:{BONE}; padding:1.8mm 2.4mm; margin-top:1.4mm; }}
    .code b {{ color:{RED}; }}
    .ft {{ position:absolute; left:11mm; right:9mm; bottom:5mm; display:flex; justify-content:space-between; font-family:Silkscreen; font-size:5.4pt; color:#6B665C; }}
    """

    def sheet(inner):
        return (f'<div class="sheet" style="width:{pw}mm;height:{ph}mm"><div class="bleed"></div><div class="margin"></div>'
                f'<div class="trim">{inner}</div>{bp.cropmarks(t, t, W, H)}</div>')
    front = f"""
      <div class="hd"><h1>Detective<br>Notebook</h1><span class="pix">CONFIDENTIAL<br>QUERY DIVISION</span></div>
      <div class="fields"><span>Detective:</span><span>Case:</span></div>
      <table><tr><th style="text-align:left;padding-left:1.4mm">SUSPECT</th>{head}<th class="x">&#10007;</th></tr>{rows}</table>
      <h2>&gt; HOW TO USE IT</h2>
      <div class="help">After each query, tick <b>&#10003;</b> the suspects who match a trait, cross out <b>&#10007;</b> the ones who don&#8217;t.
      The last suspect standing is your killer. <b>1 query per turn</b> = 1 {tok}.</div>
      <div class="gold">&#8220;Find the same clue <b>twice</b>, and it&#8217;s probably true.&#8221; &#183; &#8220;<b style="color:{RED}">0 suspects found?</b> One of your clues is fake!&#8221; &#183; &#8220;Two clues disagree? One is planted.&#8221;</div>
      <h2>&gt; W.A.T.S.O.N. UPDATES (TRUE TRAITS OF THE KILLER)</h2>
      <div style="display:flex;gap:2.5mm">{"".join(f"<div style='flex:1;border:.3mm solid {NOIR};padding:1.4mm 2mm;font:600 7.4pt Archivo;height:10mm;background:#F8F4EA'><span style='font-family:Silkscreen;font-size:5.6pt;color:{RED}'>ROUND {n}</span><br>+1 {tok}</div>" for n in (4, 8, 12))}</div>
      <div class="ft"><span>THE LAST QUERY</span><span>SIDE 1 / 2</span></div>"""
    back = f"""
      <div class="hd"><h1>My Clues</h1><span class="pix">SEEN TWICE?<br>PROBABLY TRUE</span></div>
      <table class="clues" style="margin-top:3mm"><tr><th style="text-align:left;padding-left:1.4mm">OBJECT</th><th>ROOM</th><th>WHAT IT REVEALS</th><th>SEEN</th></tr>{clue_rows}</table>
      <h2>&gt; MY ACCUSATION (IN THE LIBRARY)</h2>
      <div class="acc">&#8220;The killer is <u style="width:42mm"></u>:<br><u style="width:9mm"></u> years old, <u style="width:10mm"></u> m tall,
      size <u style="width:8mm"></u> shoes, <u style="width:14mm"></u>-handed!&#8221;</div>
      <h2>&gt; TABLE TALK</h2>
      <div class="say">&#8220;I found a muddy footprint in the Greenhouse.&#8221;</div>
      <div class="say">&#8220;Size 44 again! That&#8217;s the second time.&#8221;</div>
      <div class="say">&#8220;Zero suspects found&#8230; one of my clues must be fake.&#8221;</div>
      <div class="code"><b>SELECT</b> name <b>FROM</b> guests <b>WHERE</b> shoe = 44 <b>AND</b> height <b>BETWEEN</b> 1.85 <b>AND</b> 1.90;<br>
      <span style="color:#8C877D">&#8594; Find the guests whose shoe size is 44 and height is between 1.85 and 1.90 m.</span></div>
      <div class="ft"><span>THE LAST QUERY</span><span>SIDE 2 / 2</span></div>"""
    return bp.page("The Last Query - detective notebook A5", pw, ph, sheet(front) + sheet(back), css)


if __name__ == "__main__":
    (bp.SRC / "tokens_A4.html").write_text(tokens_sheet())
    (bp.SRC / "tokens_A4_glue.html").write_text(tokens_glue_sheet())
    (bp.SRC / "notebook_A5.html").write_text(notebook())
    print("tokens + notebook written")
