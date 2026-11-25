#!/usr/bin/env python3
"""Rules booklet for The Last Query: A5 portrait, 12 pages (saddle-stitch ready).

Run:  python3 DA/tools/build_rules.py
Writes print_src/rules_A5_print.html (3 mm bleed + crop marks) and rules_A5_screen.html (trim size, for reading).
"""
import build_print as bp
import build_tokens as bt
import build_board  # noqa: F401  (registers the extra icons: poison, heart, terminal, steps)

C = bp.C
NOIR, BONE, RED, OX, AMBER, BLUE, ASH, GRAPH = (C[k] for k in ("noir", "bone", "red", "oxblood", "amber", "blue", "ash", "graphite"))
BRASS, PAPER = "#C9923A", "#EFE8D8"
W, H, B, S = 148, 210, bp.BLEED, bp.SLUG
CARDS = "../../cards/png/"
LOGO = bp.LOGO
cup = bp.cup


def ic(name, size="5mm", sw=2, colour=None):
    return bp.icon(name, size, sw, f"color:{colour}" if colour else "")


def tok(svg_inner, w, h, vb):
    return f'<svg viewBox="{vb}" style="width:{w}mm;height:{h}mm;display:block">{svg_inner}</svg>'


CSS = f"""
.pg {{ position:relative; width:{W + 2 * B}mm; height:{H + 2 * B}mm; background:{PAPER}; color:{NOIR}; overflow:hidden; }}
.pg.dark {{ background:{NOIR}; color:{BONE}; }}
.pg .mg {{ position:absolute; left:{B + 6}mm; top:0; bottom:0; width:.3mm; background:{RED}; opacity:.45; }}
.pg .in {{ position:absolute; left:{B + 13}mm; top:{B + 12}mm; width:{W - 26}mm; height:{H - 24}mm; }}
.run {{ position:absolute; left:{B + 13}mm; right:{B + 13}mm; top:{B + 5.5}mm; display:flex; justify-content:space-between;
        font-family:Silkscreen; font-size:6pt; color:#6B665C; letter-spacing:.06em; }}
.folio {{ position:absolute; bottom:{B + 5}mm; left:0; right:0; text-align:center; font-family:Bungee; font-size:8pt; color:{RED}; }}
h1 {{ font-family:Bungee; font-weight:400; font-size:21pt; line-height:1; margin-bottom:1.5mm; }}
h1 small {{ display:block; font-family:Silkscreen; font-size:7pt; color:{RED}; letter-spacing:.08em; margin-bottom:1.6mm; }}
h2 {{ font-family:Silkscreen; font-weight:400; font-size:8pt; color:{RED}; letter-spacing:.06em; margin:4mm 0 1.6mm; }}
h3 {{ font-family:Bungee; font-weight:400; font-size:11pt; margin:0 0 .8mm; }}
p, li, td {{ font-size:9pt; line-height:1.38; }}
p + p {{ margin-top:1.8mm; }}
b {{ font-weight:700; }}
.lead {{ font-size:10pt; line-height:1.4; }}
.rule {{ height:.6mm; background:{NOIR}; margin:2.5mm 0 3mm; }}
.box {{ border:.4mm solid {NOIR}; padding:2.6mm 3mm; margin-top:3mm; background:#F8F4EA; }}
.box.red {{ border-color:{RED}; }}
.box .t {{ font-family:Silkscreen; font-size:7pt; color:{RED}; margin-bottom:1mm; letter-spacing:.06em; }}
.stamp {{ display:inline-block; border:.6mm solid {RED}; color:{RED}; font-family:Bungee; font-size:8pt; padding:.5mm 2mm; transform:rotate(-6deg); }}
ol.steps {{ list-style:none; counter-reset:s; }}
ol.steps li {{ counter-increment:s; position:relative; padding-left:9mm; margin-bottom:2.4mm; }}
ol.steps li::before {{ content:counter(s); position:absolute; left:0; top:-.4mm; width:6mm; height:6mm; background:{NOIR}; color:{BONE};
  font-family:Bungee; font-size:8.5pt; display:flex; align-items:center; justify-content:center; }}
table.t {{ width:100%; border-collapse:collapse; margin-top:1.5mm; }}
table.t td {{ border-bottom:.25mm solid #B9B09D; padding:1.3mm 1mm; vertical-align:top; font-size:8.4pt; }}
table.t td:first-child {{ font-family:Bungee; font-size:7.6pt; white-space:nowrap; width:28mm; }}
.mono {{ font-family:'IBM Plex Mono'; }}
.code {{ font-family:'IBM Plex Mono'; font-size:8.2pt; background:{NOIR}; color:{BONE}; padding:2.4mm 3mm; line-height:1.45; margin-top:2mm; }}
.code .k {{ color:{RED}; font-weight:700; }} .code .c {{ color:{ASH}; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:3mm; }}
.turn {{ display:grid; grid-template-columns:14mm 1fr; gap:3mm; align-items:start; margin-bottom:3.2mm; }}
.turn .ico {{ width:14mm; height:14mm; background:{NOIR}; color:{BONE}; display:flex; align-items:center; justify-content:center; border-left:2mm solid {RED}; }}
.cardrow {{ display:grid; grid-template-columns:18mm 1fr; gap:3.5mm; align-items:center; margin-bottom:1.8mm; }}
.cardrow img {{ width:18mm; display:block; box-shadow:.4mm .6mm 0 rgba(0,0,0,.25); }}
.comp {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:3mm 3mm; }}
.comp .it {{ border:.3mm solid #B9B09D; padding:2mm; display:flex; flex-direction:column; align-items:center; gap:1.4mm; text-align:center; background:#F8F4EA; }}
.comp .it span {{ font-size:7.6pt; line-height:1.25; }}
.comp .it b {{ font-family:Bungee; font-weight:400; font-size:8pt; }}
.say {{ border-left:1.2mm solid {RED}; padding:1mm 0 1mm 2.6mm; margin:1.6mm 0; font-style:italic; font-size:9pt; }}
"""


def page(n, title, body, dark=False):
    run = (f'<div class="run"><span>&gt; THE LAST QUERY &#183; RULES</span><span>{title}</span></div>' if not dark else "")
    folio = f'<div class="folio">{n:02d}</div>' if not dark else ""
    return (f'<div class="pg{" dark" if dark else ""}">{"" if dark else "<div class=mg></div>"}{run}'
            f'<div class="in">{body}</div>{folio}</div>')


SEMI = "M10 4h4v4h-4z M10 12h4v4l-2 4h-2.6l1.6-4h-1z"


def tk(size="3.6mm"):
    """Inline Query Token for running text."""
    return (f'<svg viewBox="0 0 24 24" style="width:{size};height:{size};vertical-align:-.7mm;display:inline-block">'
            f'<circle cx="12" cy="12" r="11" fill="{NOIR}" stroke="{RED}" stroke-width="1"/><path d="{SEMI}" fill="{RED}"/></svg>')


def pages():
    """Rules V2 (2026-11-25): 8 pages A5."""
    P = []
    # 1 ---------------------------------------------------------------- cover
    P.append(f"""<div class="pg dark">{bp.RAIN}
      <div style="position:absolute;inset:{B + 8}mm;border:.5mm solid {RED}"></div>
      <div style="position:absolute;inset:{B + 9.5}mm;border:.2mm solid {RED}"></div>
      <div style="position:absolute;left:0;right:0;top:{B + 30}mm;display:flex;flex-direction:column;align-items:center;gap:7mm">
        <span class="pix" style="font-size:7.5pt;color:{RED};letter-spacing:.1em">CASE FILE N&#176; 1123 &#183; RAVENSCROFT MANOR</span>
        <img src="{LOGO}" style="width:118mm">
        <div style="font-family:Bungee;font-size:26pt;letter-spacing:.04em">OFFICIAL RULES</div>
        <div class="pix" style="font-size:7.5pt;color:{BONE};letter-spacing:.08em">2-4 PLAYERS &#183; AGE 10+ &#183; 25-40 MIN &#183; 1 PHONE EACH</div>
      </div>
      <div style="position:absolute;left:{B + 16}mm;right:{B + 16}mm;bottom:{B + 22}mm;text-align:center;font:italic 400 10.5pt Archivo;color:{ASH}">
        &#8220;The house remembers everything.<br>The killer made it forget.&#8221;</div>
    </div>""")
    # 2 ---------------------------------------------------------------- story + 30 seconds
    P.append(page(2, "THE STORY", f"""
      <h1><small>&gt; 11:45 PM, A STORMY NIGHT</small>The Story</h1><div class="rule"></div>
      <p class="lead"><b>Sir Victor Ravenscroft</b>, 70, is found dead in his armchair, in the <b>Library</b> of his manor, next to a cold cup of tea.</p>
      <p>His house is a smart house. Its AI, <b>W.A.T.S.O.N.</b>, keeps a file on each of the <b>12 guests</b>: age, height, shoe size,
      which hand they write with&#8230; The storm has cut the bridge. The killer is still inside, and has left traces all over the manor.
      Some of them are <b>fake clues, planted to trick you</b>.</p>
      <h2>&gt; THE GAME IN 30 SECONDS</h2>
      <div class="box red" style="margin-top:1mm"><p style="font-size:10pt"><b>Explore the manor, collect clues, and use your phone to search the guest database.
      The first detective to name the killer wins.</b></p></div>
      <ol class="steps" style="margin-top:3.5mm">
        <li>Every room has a deck of <b>clue cards</b>. Walk there to draw them.</li>
        <li>Some clues describe <b>the killer</b>. Some are <b>dead ends</b>. A few are <b>fakes</b>.</li>
        <li>On your phone, <b>filter the 12 suspects</b> with your clues. Each search costs <b>1 Query Token</b> {tk()}.</li>
        <li>Recharge your tokens in the <b>Server Room</b>, then <b>accuse</b> in the Library.</li>
      </ol>
      <p style="margin-top:2mm;color:#6B665C">No SQL needed: the phone shows simple sentences&#8230; and the real SQL under each result.</p>
    """))
    # 3 ---------------------------------------------------------------- components + setup
    qt = tok(bt.query_token(12, 12, 10, False), 12, 12, "0 0 24 24")
    pawn = tok(bt.detective_figure(0, 0, 24, NOIR, RED), 6, 16, "0 0 10 25")
    P.append(page(3, "SETUP", f"""
      <h1><small>&gt; WHAT&#8217;S IN THE BOX</small>Components</h1><div class="rule"></div>
      <div class="comp">
        <div class="it" style="grid-column:span 3;flex-direction:row;gap:3mm;text-align:left"><img src="board_thumb.png" style="width:50mm;display:block">
          <span><b>1 GAME BOARD</b><br>Ravenscroft Manor: 9 rooms. 7 have a deck. The Server Room recharges your tokens.</span></div>
        <div class="it"><img src="{CARDS}lib-01.png" style="width:14mm"><span><b>40 CLUE CARDS</b><br>34 evidence to scan, 6 bonus</span></div>
        <div class="it">{qt}<span><b>16 QUERY TOKENS</b><br>3 each + spares</span></div>
        <div class="it">{pawn}<span><b>4 PAWNS</b><br>P1 to P4</span></div>
      </div>
      <p style="margin-top:2mm">Plus <b>1 Detective Notebook pad</b> (one sheet each) and <b>1 smartphone per player</b> (not included).</p>
      <h2>&gt; SETUP (3 MINUTES)</h2>
      <ol class="steps">
        <li>The <b>host</b> starts a game in the Police Console app. Everyone joins with their phone.</li>
        <li><b>Shuffle each room deck</b> (the room is on the back) and put it face down on its room.</li>
        <li>Everyone puts their pawn in the <b>Grand Hall</b> and takes <b>3 Query Tokens</b> {tk()} and a notebook sheet.</li>
        <li>The <b>youngest</b> player starts. Play goes clockwise.</li>
      </ol>
    """))
    # 4 ---------------------------------------------------------------- your turn
    P.append(page(4, "YOUR TURN", f"""
      <h1><small>&gt; MOVE, ACT, QUERY</small>Your Turn</h1><div class="rule"></div>
      <div class="turn"><div class="ico">{ic("steps", "8mm", 2)}</div><div><h3>1. Move</h3>
        <p>Move your pawn <b>up to 2 rooms</b> through the doors. You may also stay.</p></div></div>
      <div class="turn"><div class="ico">{ic("magnifier", "8mm", 2)}</div><div><h3>2. Act: one of these</h3>
        <p><b>Search</b>: draw the top card of the room deck. Scan it (or read it) <b>secretly</b> and keep it face down in front of you.
        An empty deck means the room has been searched clean.</p>
        <p><b>Recharge</b> <i>(Server Room only)</i>: refill up to <b>3 tokens</b>. You can never have more than 3.</p>
        <p><b>Accuse</b> <i>(Library only)</i>: see page 7.</p></div></div>
      <div class="turn"><div class="ico" style="background:{RED};border-left-color:{NOIR}">{ic("terminal", "8mm", 2)}</div><div><h3>Anytime: Query</h3>
        <p>During your turn, pay <b>1 {tk()}</b> to run one search on your phone, with <b>up to 2 conditions</b>. You can query several times if you have the tokens.</p></div></div>
      <div class="box"><div class="t">&gt; THE SERVER ROOM</div><p>It is in the corner <b>opposite the Library</b> and has no cards. Going there to recharge costs you a search: choose the right moment!</p></div>
    """))
    # 5 ---------------------------------------------------------------- clues
    def crow(img, title, txt):
        return f'<div class="cardrow"><img src="{CARDS}{img}"><div><h3>{title}</h3><p>{txt}</p></div></div>'
    P.append(page(5, "THE CLUES", f"""
      <h1><small>&gt; 40 CARDS</small>The Clues</h1><div class="rule"></div>
      <p>Evidence cards all look the same: an object, its room and a QR code. <b>Scan</b> one to see what it reveals in this case. Behind it there can be:</p>
      <table class="t" style="margin:2mm 0 1mm">
        <tr><td>True clue</td><td>A real trait of the killer. Each one is hidden in <b>3 different rooms</b>.</td></tr>
        <tr><td>Dead end</td><td>True, but useless to find the killer.</td></tr>
        <tr><td style="color:{RED}">Fake clue</td><td>Planted by the killer. Only <b>1 copy</b>, and it contradicts the real clues.</td></tr>
      </table>
      {crow("gre-01.png", "Evidence &#215; 34", "Scan it secretly in the Police Console, then keep it face down. Write what you learn in your notebook.")}
      {crow("obs-06-bonus.png", "Bonus &#215; 6", f"Printed, never scanned. Spare Battery: +1 {tk()}. Running Shoes: move again. Master Key: peek at the top card of any deck.")}
      <h2>&gt; GOLDEN RULES</h2>
      <div class="say" style="font-size:10.5pt">&#8220;Find the same clue <b>twice</b>, and it&#8217;s probably true.&#8221;</div>
      <div class="say" style="font-size:10.5pt">&#8220;<b style="color:{RED}">0 suspects found?</b> One of your clues is fake!&#8221;</div>
    """))
    # 6 ---------------------------------------------------------------- the phone + watson
    P.append(page(6, "THE PHONE", f"""
      <h1><small>&gt; NO SQL NEEDED</small>The Police Console</h1><div class="rule"></div>
      <p>The query screen is a sentence with blanks. Fill them with the menus, then run it for <b style="white-space:nowrap">1 {tk()}</b>.</p>
      <div class="code" style="font-size:8.6pt">FIND guests WHERE [shoe size] <span class="k">is</span> [44]<br>&#8195;&#8195;&#8195;&#8195;&#8195;&#8195;<span class="k">AND</span> [height] <span class="k">between</span> [1.85] and [1.90]
      <br><span class="c">&#8594; 2 suspects found: Oscar Lindqvist, Hugo Ravenscroft</span><br>
      <span class="c">SQL: SELECT name FROM guests WHERE shoe = 44 AND height BETWEEN 1.85 AND 1.90;</span></div>
      <p style="margin-top:2.4mm">You only see the <b>names that match</b>, never the whole table. That is why one query is not enough:
      with 3 or 4 clues you need several queries and your notebook to cross-check.</p>
      <div class="box red"><div class="t">&gt; 0 SUSPECTS FOUND</div><p>Nobody matches both conditions: <b>one of your two clues is fake</b>. Try them separately to find which one.</p></div>
      <h2>&gt; W.A.T.S.O.N. UPDATES</h2>
      <p>Every <b>4 rounds</b> (rounds 4, 8 and 12) the host taps <b>End round</b> and the app:</p>
      <ul style="margin:1.5mm 0 0 5mm"><li>reveals <b>one true trait of the killer</b> to everyone;</li><li>gives every detective <b>+1 {tk()}</b> (max 3).</li></ul>
    """))
    # 7 ---------------------------------------------------------------- accuse + table talk
    P.append(page(7, "ACCUSE", f"""
      <h1><small>&gt; HOW TO WIN</small>Accuse</h1><div class="rule"></div>
      <ol class="steps">
        <li>Go to the <b>Library</b>. Accusing is your action.</li>
        <li>Say the killer&#8217;s <b>full profile</b> out loud, in English:</li>
      </ol>
      <div class="say" style="font-size:10pt">&#8220;The killer is <b>___</b>: 47 years old, 1.86 m tall, size 44 shoes, left-handed!&#8221;</div>
      <ol class="steps" start="3" style="counter-reset:s 2"><li>Type the name in the app.</li></ol>
      <div class="grid2" style="margin-top:2mm">
        <div class="box" style="margin:0"><div class="t">&gt; RIGHT</div><p><b>You win!</b> Read the solution in the app together.</p></div>
        <div class="box red" style="margin:0"><div class="t">&gt; WRONG</div><p>Go back to the <b>Grand Hall</b> and lose all your {tk()}. You stay in the game.</p></div>
      </div>
      <h2>&gt; TABLE TALK (SAY IT IN ENGLISH)</h2>
      <div class="say">&#8220;I found a muddy footprint in the Greenhouse.&#8221;</div>
      <div class="say">&#8220;Size 44 again! That&#8217;s the second time.&#8221;</div>
      <div class="say">&#8220;Zero suspects found&#8230; one of my clues must be fake.&#8221;</div>
      <div class="say">&#8220;I&#8217;m going to the Server Room to recharge.&#8221;</div>
      <h2>&gt; WHAT YOU LEARNED</h2>
      <p class="mono" style="font-size:8pt">SELECT &#183; WHERE &#183; AND &#183; BETWEEN &#183; an empty result means a false condition.</p>
    """))
    # 8 ---------------------------------------------------------------- back cover
    P.append(f"""<div class="pg dark">{bp.RAIN}
      <div style="position:absolute;inset:{B + 8}mm;border:.5mm solid {RED}"></div>
      <div style="position:absolute;left:{B + 18}mm;right:{B + 18}mm;top:{B + 30}mm;text-align:center">
        <div class="pix" style="font-size:7pt;color:{RED};letter-spacing:.1em;margin-bottom:5mm">&gt; CASE CLOSED?</div>
        <p style="font:400 10.5pt/1.5 Archivo;color:{BONE}">A storm. A smart manor. A dead billionaire.<br>Twelve guests, one killer, and fake clues everywhere.<br><br>
        Search the rooms, query the guest database and <b>name the killer</b> before the others.
        Without even noticing, you will learn how databases think.</p>
        <div style="display:flex;justify-content:center;gap:3mm;margin-top:8mm">
          <span class="stamp" style="transform:none;color:{BONE};border-color:{BONE}">2-4 PLAYERS</span>
          <span class="stamp" style="transform:none;color:{BONE};border-color:{BONE}">10+</span>
          <span class="stamp" style="transform:none;color:{BONE};border-color:{BONE}">25-40 MIN</span></div>
      </div>
      <div style="position:absolute;left:0;right:0;bottom:{B + 22}mm;display:flex;flex-direction:column;align-items:center;gap:4mm">
        <img src="{LOGO}" style="width:62mm">
        <div class="pix" style="font-size:6pt;color:{ASH};letter-spacing:.08em">A GAME BY TEAM ________ &#183; ENGLISH GAME WEEK 2026</div>
      </div>
    </div>""")
    return P


def build(which):
    pp = pages()
    if which == "print":
        pw, ph = W + 2 * (B + S), H + 2 * (B + S)
        body = "".join(f'<div class="sheet" style="width:{pw}mm;height:{ph}mm"><div style="position:absolute;left:{S}mm;top:{S}mm">{p}</div>'
                       f'{bp.cropmarks(S + B, S + B, W, H)}</div>' for p in pp)
    else:
        pw, ph = W, H
        body = "".join(f'<div class="sheet" style="width:{pw}mm;height:{ph}mm"><div style="position:absolute;left:-{B}mm;top:-{B}mm">{p}</div></div>' for p in pp)
    return bp.page(f"The Last Query - rules ({which})", pw, ph, body, CSS)


if __name__ == "__main__":
    (bp.SRC / "rules_A5_print.html").write_text(build("print"))
    (bp.SRC / "rules_A5_screen.html").write_text(build("screen"))
    print(f"rules written ({len(pages())} pages)")
