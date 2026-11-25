"""Card illustrations V2.1: painted-look vector scenes (60 x 48 units).

Each picture = a room surface (rug, parquet, stone, tiles...) + the object with
material gradients, highlights, a soft contact shadow, a lamp light from the
top-left and a photo vignette. Everything stays vector (print-safe).
"""
NOIR, BONE, RED, OX, AMBER, BLUE, ASH = "#0B0B0C", "#F4F0E6", "#E31B3B", "#7E0C1F", "#F2A93B", "#5B7C99", "#8C877D"

DEFS = f"""<defs>
<radialGradient id="aLight" cx=".25" cy=".15" r=".9"><stop offset="0" stop-color="#FFD9A0" stop-opacity=".32"/><stop offset=".55" stop-color="#FFD9A0" stop-opacity=".06"/><stop offset="1" stop-color="#FFD9A0" stop-opacity="0"/></radialGradient>
<radialGradient id="aVig" cx=".5" cy=".5" r=".72"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient>
<radialGradient id="aShadow"><stop offset="0" stop-color="#000" stop-opacity=".65"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="aGlowR"><stop offset="0" stop-color="{RED}" stop-opacity=".9"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<linearGradient id="aBone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFDF6"/><stop offset=".6" stop-color="#E9E1CC"/><stop offset="1" stop-color="#B9AE94"/></linearGradient>
<linearGradient id="aPaper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6EFDC"/><stop offset="1" stop-color="#CDBF9C"/></linearGradient>
<linearGradient id="aWood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8A5A40"/><stop offset=".5" stop-color="#5A3A2C"/><stop offset="1" stop-color="#2E1C16"/></linearGradient>
<linearGradient id="aWoodV" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3A2621"/><stop offset=".35" stop-color="#7A5240"/><stop offset=".6" stop-color="#5A3A2C"/><stop offset="1" stop-color="#2A1A16"/></linearGradient>
<linearGradient id="aBrass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7D58A"/><stop offset=".45" stop-color="#C9923A"/><stop offset="1" stop-color="#6E4A16"/></linearGradient>
<linearGradient id="aRed" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0566F"/><stop offset=".5" stop-color="#C21732"/><stop offset="1" stop-color="#5A0916"/></linearGradient>
<linearGradient id="aLeather" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A33A3A"/><stop offset=".5" stop-color="#6E1620"/><stop offset="1" stop-color="#330A10"/></linearGradient>
<linearGradient id="aBrownL" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B07A52"/><stop offset=".6" stop-color="#7A4E2E"/><stop offset="1" stop-color="#3E2414"/></linearGradient>
<linearGradient id="aMetal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C9CDD3"/><stop offset=".5" stop-color="#6E737B"/><stop offset="1" stop-color="#2A2C31"/></linearGradient>
<linearGradient id="aGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3E6E58"/><stop offset=".5" stop-color="#173828"/><stop offset="1" stop-color="#07140E"/></linearGradient>
<linearGradient id="aLeaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E9C72"/><stop offset="1" stop-color="#22402E"/></linearGradient>
<linearGradient id="aTweed" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6A645A"/><stop offset=".6" stop-color="#46423C"/><stop offset="1" stop-color="#26231F"/></linearGradient>
<linearGradient id="aVelvet" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4A0A14"/><stop offset=".25" stop-color="#B0203A"/><stop offset=".45" stop-color="#6E0E1E"/><stop offset=".7" stop-color="#C02640"/><stop offset="1" stop-color="#4A0A14"/></linearGradient>
<linearGradient id="aNavy" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22324A"/><stop offset="1" stop-color="#0C1422"/></linearGradient>
<linearGradient id="aTea" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B0703A"/><stop offset="1" stop-color="#4A2610"/></linearGradient>
<linearGradient id="aTerra" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C46A44"/><stop offset="1" stop-color="#6A2C18"/></linearGradient>
<pattern id="sParquet" width="20" height="5" patternUnits="userSpaceOnUse"><rect width="20" height="5" fill="#3E281F"/><rect y="2.5" width="20" height="2.5" fill="#35221A"/><path d="M0 0H20M0 2.5H20M0 0V2.5M12 2.5V5" stroke="#21140F" stroke-width=".3"/><path d="M3 1.2H8M14 3.8H18" stroke="#4E3428" stroke-width=".2"/></pattern>
<pattern id="sRug" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#5E0A18"/><path d="M4 .8L7.2 4 4 7.2 .8 4Z" fill="none" stroke="#B0203A" stroke-width=".35"/><circle cx="4" cy="4" r=".7" fill="#C9923A"/><circle cx="0" cy="0" r=".4" fill="#C9923A"/><circle cx="8" cy="8" r=".4" fill="#C9923A"/></pattern>
<pattern id="sStone" width="16" height="9" patternUnits="userSpaceOnUse"><rect width="16" height="9" fill="#34343A"/><rect x="8" y="4.5" width="8" height="4.5" fill="#3B3B42"/><path d="M0 0H16M0 4.5H16M0 0V4.5M8 4.5V9" stroke="#1E1E22" stroke-width=".5"/></pattern>
<pattern id="sTiles" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#23323E"/><rect width="4" height="4" fill="#2B3C4A"/><rect x="4" y="4" width="4" height="4" fill="#2B3C4A"/><path d="M0 0H8M0 4H8M0 0V8M4 0V8" stroke="#141B21" stroke-width=".25"/></pattern>
<pattern id="sSoil" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#2C211B"/><circle cx="1" cy="1.5" r=".35" fill="#3E2E24"/><circle cx="4" cy="4" r=".4" fill="#1F1712"/><circle cx="4.6" cy="1" r=".25" fill="#4A372A"/></pattern>
<pattern id="sDark" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#1C1A1E"/><path d="M0 0H10" stroke="#25222A" stroke-width=".4"/></pattern>
<pattern id="sHerring" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#3E281F"/><rect width="6" height="3" fill="#35221A"/><path d="M0 0H6M0 3H6M3 0V3M0 3V6" stroke="#21140F" stroke-width=".25"/></pattern>
<pattern id="sCellar" width="12" height="7" patternUnits="userSpaceOnUse"><rect width="12" height="7" fill="#2A2527"/><rect y="3.5" width="6" height="3.5" fill="#302A2C"/><path d="M0 0H12M0 3.5H12M0 0V3.5M6 3.5V7" stroke="#151213" stroke-width=".45"/></pattern>
</defs>"""

SURF = {"LIBRARY": "url(#sParquet)", "GREENHOUSE": "url(#sSoil)", "OBSERVATORY": "url(#sDark)", "CHAPEL": "url(#sStone)",
        "MUSIC ROOM": "url(#sHerring)", "KITCHEN": "url(#sTiles)", "WINE CELLAR": "url(#sCellar)"}


def sh(cx, cy, rx, ry, op=1):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#aShadow)" opacity="{op}"/>'


def p(d, f="none", s="none", w=0, extra=""):
    return f'<path d="{d}" fill="{f}" stroke="{s}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def r(x, y, w, h, f, rx=0, s="none", sw=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="{sw}" {extra}/>'


def c(cx, cy, rr, f, s="none", sw=0, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{f}" stroke="{s}" stroke-width="{sw}" {extra}/>'


def e(cx, cy, rx, ry, f, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{f}" {extra}/>'


def hl(d, op=.55, w=.6):
    """Specular highlight stroke."""
    return p(d, "none", "#FFFFFF", w, f'opacity="{op}"')


def write(x, y, w, n, gap=2.6, col="#3A3530", sw=.45, wav=.5):
    """Handwritten lines."""
    out = []
    for k in range(n):
        yy = y + k * gap
        ww = w * (.6 if k == n - 1 else 1)
        segs = int(ww / 2.4)
        d = f"M{x} {yy}" + "".join(f" q1.2 {-wav if j % 2 else wav} 2.4 0" for j in range(segs))
        out.append(p(d, "none", col, sw))
    return "".join(out)


def dust(pts, col="#9A948A"):
    return "".join(c(x, y, .35, col, extra='opacity=".7"') for x, y in pts)


# ------------------------------------------------------------------ objects (drawn in the 60 x 48 frame)
A = {}
A["sock"] = (e(31, 33, 17, 8, "#1A2A38", 'opacity=".55"') + sh(32, 34, 16, 5)
             + p("M24 8h11v20l8.5 7.5a5.8 5.8 0 0 1-8 8.4L24 32z", "url(#aBone)")
             + p("M24 8h11v5H24z", "url(#aRed)") + p("M24 15h11v1.6H24z", "#C21732")
             + "".join(p(f"M{25.5 + k * 1.9} 8v7", "none", "#C9BFA8", .3) for k in range(5))
             + p("M38 37a5.8 5.8 0 0 0-4 7l2-.4a4 4 0 0 1 3-5z", "#B8AC92") + p("M24 27c3 1 8 1 11 0v3c-3 1-8 1-11 0z", "#7E8FA0", extra='opacity=".45"')
             + hl("M26 17v12") + "".join(c(x, y, rr, "#9FB6CC", extra='opacity=".85"') + c(x - .3, y - .3, rr * .35, "#FFF")
                                          for x, y, rr in [(17, 26, 1.1), (14, 31, .8), (47, 24, 1), (20, 39, .7)]))
A["teacup"] = (sh(31, 28, 19, 15) + c(30, 25, 17, "url(#aBone)") + c(30, 25, 16.2, "none", "#C9923A", .5) + c(30, 25, 12.5, "#E4DCC8")
               + c(30, 25, 11, "url(#aBone)") + c(30, 25, 9.6, "#C9923A", extra='opacity=".7"') + c(30, 25, 9, "url(#aTea)")
               + e(27, 22, 4, 2, "#E8B57A", 'opacity=".35"') + p("M19.6 25a5.5 5.5 0 0 1-7.5 0", "none", "url(#aBone)", 3)
               + p("M19.6 25a5.5 5.5 0 0 1-7.5 0", "none", "#C9923A", .4) + p("M40 12l9-6", "none", "url(#aMetal)", 1.6) + e(38.6, 13.2, 2.4, 1.4, "url(#aMetal)", 'transform="rotate(-33 38.6 13.2)"')
               + hl("M21 17a12 12 0 0 1 9-4", .6, .8))
A["ashtray"] = (sh(30, 30, 19, 12) + p("M12 26a18 13 0 0 0 36 0a18 13 0 0 0-36 0z", "#3A4450", "#9FB6CC", .4, 'opacity=".9"')
                + p("M16 26a14 9 0 0 0 28 0a14 9 0 0 0-28 0z", "#1E262E") + "".join(p(f"M{x} {y1}L{x + 2} {y2}", "none", "#B8C8D8", .3, 'opacity=".5"') for x, y1, y2 in [(14, 22, 30), (22, 15, 18), (38, 15, 18), (45, 22, 30)])
                + p("M20 25l15-2 1.5 4-15 2z", "url(#aBrownL)") + p("M30 23.6l2.6-.4 1.4 4.2-2.6.4z", "url(#aRed)") + p("M31 23.4l.6 4.3", "none", "#C9923A", .4)
                + p("M35 23l3.6-.6 1.2 3.8-3.4.6z", "#8C877D") + dust([(36, 24), (37.5, 25), (38, 23.6)], "#C9C3B8")
                + p("M40 21c3-3-1-5 2-8c2-2 0-4 2-6", "none", "#DADADA", .7, 'opacity=".35"') + p("M43 19c2-2-1-4 1-6", "none", "#DADADA", .5, 'opacity=".25"')
                + hl("M15 22a15 10 0 0 1 12-7", .5, .7))
A["diary"] = (sh(31, 37, 20, 6) + p("M47 14l4 1-12 30-4-1z", "url(#aMetal)") + p("M46 15l2 .6", "none", "#C9923A", 1)
              + r(12, 6, 30, 36, "url(#aLeather)", 2) + r(12, 6, 4.5, 36, "#3E0A12", 1) + r(41, 8, 2, 33, "#E9E1CC") + p("M41.4 9v31M42.2 9v31", "none", "#B9AE94", .2)
              + r(18, 14, 18, 9, "none", 0, "url(#aBrass)", .7) + f'<text x="27" y="21" font-family="Bungee" font-size="5.2" fill="url(#aBrass)" text-anchor="middle">V.R.</text>'
              + p("M12 6h5l-5 5zM42 6h-5l5 5zM12 42h5l-5-5zM42 42h-5l5-5z", "url(#aBrass)") + p("M33 42v6l2-2 2 2v-6", "url(#aRed)")
              + hl("M17 8v32", .25, 1.2) + hl("M20 9h17", .35, .5))
A["jacket"] = (sh(30, 40, 22, 6) + p("M8 46L14 6l16 12 16-12 6 40z", "url(#aTweed)")
               + "".join(p(f"M{x} 10l3 4-3 4 3 4-3 4 3 4-3 4 3 4", "none", "#5A554C", .25, 'opacity=".6"') for x in range(12, 50, 5))
               + p("M14 6l16 26L46 6l-6 1-10 17L20 7z", "#2E2B27") + p("M30 32v14", "none", "#1E1C19", .8)
               + c(30, 35, 1.3, "url(#aBrass)") + c(30, 41, 1.3, "url(#aBrass)") + p("M36 24l7-1 .5 3-7 1z", "url(#aRed)")
               + p("M18 20c4 2 7 0 11 3c3 2 5 0 8 2", "none", "#E8E2D2", .45) + c(28, 22, 4.2, "none", "#FFFFFF", .3, 'opacity=".35"')
               + hl("M15 9l-4 34", .2, 1.4))
A["footprint"] = (p("M20 6c8-5 17 0 15 12c-1 8-4 11-4 18c0 4-2 8-8 8c-5 0-8-4-6-9c1-6-3-11-3-18c0-5 2-8 6-11z", "#4A3220", extra='opacity=".9"')
                  + "".join(p(f"M{21 + (k % 2)} {9 + k * 3}h{10 - (k % 2) * 2}", "none", "#6B4A32", 1) for k in range(6))
                  + "".join(p(f"M{22} {33 + k * 2.6}h7", "none", "#6B4A32", .9) for k in range(4))
                  + "".join(c(x, y, rr, "#5A3E2A", extra='opacity=".8"') for x, y, rr in [(42, 36, 2), (45, 31, 1), (12, 12, 1.4), (9, 18, .8), (40, 8, .9)])
                  + p("M20 6c8-5 17 0 15 12", "none", "#8A6448", .5, 'opacity=".6"'))
A["branch"] = (sh(30, 34, 22, 6) + p("M4 40L26 25l6 1", "none", "url(#aBrownL)", 3.6) + p("M26 25l4-7", "none", "url(#aBrownL)", 3)
               + p("M29.6 18.6l3-2.2-.6 3 2.6.4-3 1.4.8 2.2z", "#E9D9B8") + p("M31 26l6 3", "none", "url(#aBrownL)", 2.4) + p("M36.4 28.6l2.6-1-1 2.6z", "#E9D9B8")
               + "".join(p(f"M{x} {y}c3-5 10-5 11 0c-4 4-9 4-11 0z", "url(#aLeaf)", extra=f'transform="rotate({a} {x} {y})"') + p(f"M{x} {y}h10", "none", "#8FB890", .3, f'transform="rotate({a} {x} {y})"')
                       for x, y, a in [(12, 33, -40), (18, 29, 20), (22, 33, 60), (8, 36, 10), (33, 20, -70)])
               + "".join(e(x, y, 1.4, 2, "#B05A8C") + e(x, y + 1.2, .9, .6, "#5A1E44") for x, y in [(40, 14), (43, 18), (46, 13)]))
A["clipboard"] = (sh(30, 40, 18, 5) + r(15, 5, 30, 39, "url(#aWood)", 2) + r(18, 11, 24, 30, "url(#aPaper)")
                  + f'<text x="30" y="16.5" font-family="Bungee" font-size="3" fill="#3A3530" text-anchor="middle">WATERING</text>'
                  + write(20, 21, 20, 6, 3) + r(24, 3, 12, 6, "url(#aMetal)", 1.5) + c(30, 4.6, 1, "#2A2C31")
                  + e(38, 36, 3.4, 2.4, "#5B7C99", 'opacity=".35"') + p("M47 30c0-3 3-6 3-6s3 3 3 6a3 3 0 0 1-6 0z", "#7FA3C2") + hl("M48.5 30c0-1 .8-2.4 1.4-3", .7, .5))
A["label"] = (sh(30, 44, 18, 4) + p("M12 34h36l-3 14H15z", "url(#aTerra)") + r(10, 31, 40, 5, "#C46A44", 1) + r(12, 32, 36, 3, "url(#sSoil)")
              + p("M30 33V16", "none", "#C9B48A", 1.6) + r(19, 6, 22, 13, "url(#aPaper)", 1.5) + c(22, 9, .9, "#3A3530")
              + f'<text x="30" y="12.6" font-family="IBM Plex Mono" font-size="2.6" font-weight="700" fill="{OX}" text-anchor="middle">DIGITALIS</text>' + write(23, 15.6, 14, 1)
              + p("M30 31c-8-1-12-6-11-11c6 0 11 4 11 11zM30 32c7-1 11-5 10-10c-6 0-10 4-10 10z", "url(#aLeaf)") + p("M30 31c-4-3-7-6-8-9M30 32c3-3 6-6 7-8", "none", "#8FB890", .3))
A["petals"] = "".join(p(f"M{x} {y}c3-5 9-4 9 1c-3 4-8 4-9-1z", col, extra=f'transform="rotate({a} {x} {y})"') + p(f"M{x + 1} {y}c2-2 5-2 6 0", "none", "#FFFFFF", .3, f'opacity=".4" transform="rotate({a} {x} {y})"')
                      for x, y, a, col in [(14, 14, 20, "#A77AA0"), (30, 9, -30, "#8E6488"), (38, 25, 50, "#B48AAE"), (16, 31, -10, "#8E6488"),
                                           (27, 38, 80, "#A77AA0"), (44, 39, 10, "#8E6488"), (24, 22, 140, "#B48AAE")]) + p("M8 44c6-6 10-8 14-16", "none", "#3E6A46", .8)
A["eyepiece"] = (sh(31, 30, 19, 14) + c(30, 24, 17, "url(#aBrass)") + "".join(p(f"M{30 + 17 * __import__('math').cos(k * .2)} {24 + 17 * __import__('math').sin(k * .2)}L{30 + 15.3 * __import__('math').cos(k * .2)} {24 + 15.3 * __import__('math').sin(k * .2)}", "none", "#6E4A16", .35) for k in range(32))
                 + c(30, 24, 14.6, "#6E4A16") + c(30, 24, 13.2, "url(#aBrass)") + c(30, 24, 9.8, "#2A2A30") + c(30, 24, 8.4, "#0B1722")
                 + c(30, 24, 8.4, "url(#aNavy)", extra='opacity=".6"') + p("M24 19a8 8 0 0 1 8-3", "none", "#CFE2F2", 1, 'opacity=".7"') + c(34, 28, 1.2, "#CFE2F2", extra='opacity=".4"')
                 + hl("M17 15a17 17 0 0 1 12-7", .55, .9))
A["telescope"] = (sh(32, 42, 20, 4) + p("M24 30L19 47M24 30L30 47M24 30l-1 17", "none", "url(#aMetal)", 1.2)
                  + p("M6 38L44 12l5 7-38 26z", "url(#aBone)") + p("M6 38l5 7", "none", "#B9AE94", 1) + p("M40 14.6l5 7-2.6 1.8-5-7z", "url(#aBrass)")
                  + p("M44 12l5 7 3-2-5-7z", "url(#aBrass)") + c(24, 30, 2.4, "url(#aBrass)") + hl("M9 37L45 12.6", .7, .7)
                  + p("M16 32c3-3 6 0 9-3c2-2 5 0 7-2", "none", "#2A2A2A", .45))
A["starchart"] = (sh(31, 40, 22, 5) + r(6, 8, 48, 32, "url(#aNavy)", 1) + e(8, 24, 2.6, 16, "#1A2638") + e(52, 24, 2.6, 16, "#1A2638")
                  + c(30, 24, 12, "none", "#5B7C99", .5) + c(30, 24, 9, "none", "#5B7C99", .25, 'stroke-dasharray="1 1"')
                  + p("M16 14L22 11L27 16L35 12M31 31L38 28L42 34", "none", "#9FB6CC", .45)
                  + "".join(c(x, y, rr, "#F4F0E6") for x, y, rr in [(16, 14, .8), (22, 11, .6), (27, 16, .9), (35, 12, .6), (31, 31, .7), (38, 28, .8), (42, 34, .6), (14, 32, .4), (46, 16, .5)])
                  + p("M37 38l9-24M37 38l13-20", "none", "url(#aBrass)", 1) + c(37, 38, 1.6, "url(#aBrass)"))
A["camera"] = (r(4, 4, 52, 40, "#1E2228") + "".join(p(f"M{x} {y}l-2 {L}", "none", "#9FB6CC", .5, 'opacity=".5"') for x, y, L in [(10, 6, 6), (20, 12, 5), (48, 8, 7), (52, 30, 5), (14, 34, 6), (36, 4, 5)])
               + r(42, 18, 4, 18, "url(#aMetal)") + p("M14 16h26l4 4v12l-4 4H14z", "url(#aMetal)") + r(16, 18, 22, 14, "#2A2C31", 2)
               + c(16, 25, 7, "#16181C", "url(#aMetal)", 1.2) + c(16, 25, 4.4, "#0B1722") + p("M13 22a4 4 0 0 1 4-2", "none", "#CFE2F2", .8, 'opacity=".7"')
               + c(36, 21, 3, "url(#aGlowR)") + c(36, 21, .9, "#FF5C70") + e(16, 25, 7, 7, "#9FB6CC", 'opacity=".12"'))
A["glasses"] = (sh(30, 34, 22, 5) + c(19, 26, 8.6, "#8FA9BF", extra='opacity=".25"') + c(41, 26, 8.6, "#8FA9BF", extra='opacity=".25"')
                + c(19, 26, 8.6, "none", "url(#aBrownL)", 1.8) + c(41, 26, 8.6, "none", "url(#aBrownL)", 1.8)
                + p("M27.6 24.6c1.4-2.4 3.4-2.4 4.8 0", "none", "url(#aBrownL)", 1.6) + p("M10.6 23L4 15M49.4 23L56 15", "none", "url(#aBrownL)", 1.3)
                + "".join(c(x, y, .5, "#2A1608") for x, y in [(13, 21), (24, 31), (36, 20), (47, 30)])
                + p("M14 21a7 7 0 0 1 5-3M36 21a7 7 0 0 1 5-3", "none", "#FFFFFF", .8, 'opacity=".6"'))
A["glove"] = (r(0, 26, 60, 22, "url(#aWoodV)") + "".join(p(f"M0 {y}H60", "none", "#2A1A16", .4) for y in (31, 37, 43)) + sh(30, 34, 15, 4)
              + p("M18 33V17c0-2.4 3.6-2.4 3.6 0v-5c0-2.4 3.6-2.4 3.6 0v-1.4c0-2.4 3.6-2.4 3.6 0v2.4c0-2.4 3.6-2.4 3.6 0V28l3.4-4.6c1.4-2 4.6 0 3.4 2.4L34 36H18z", "url(#aBrownL)")
              + p("M21.6 17v10M25.2 12v14M28.8 11v15M32.4 13v14", "none", "#3E2414", .35, 'stroke-dasharray=".8 .6"') + r(17, 33, 18, 4, "#5A3420", 1)
              + hl("M19 30V18", .4, .7))
A["confessional"] = (r(8, 2, 44, 46, "url(#aWood)", 1) + p("M8 2h44v4H8z", "url(#aBrass)") + p("M12 10h20v26H12z", "#120A08")
                     + "".join(p(f"M{12 + k * 4} 10v26", "none", "#7A5240", .6) for k in range(6)) + "".join(p(f"M12 {10 + k * 4.3}h20", "none", "#7A5240", .6) for k in range(7))
                     + p("M36 10h12v34H36z", "url(#aVelvet)") + p("M12 36h20v2H12z", "url(#aBrass)") + p("M30 8a8 6 0 0 0-16 0", "none", "url(#aBrass)", .8) + hl("M9 4v42", .2, 1.2))
A["hymn"] = (sh(30, 40, 24, 5) + p("M4 12c8-3 18-3 26 0v30c-8-3-18-3-26 0z", "url(#aPaper)") + p("M56 12c-8-3-18-3-26 0v30c8-3 18-3 26 0z", "url(#aPaper)")
             + p("M30 12v30", "none", "#9A8E70", .6) + write(7, 16, 19, 8, 2.6, "#4A4238", .35, .3)
             + p("M33 15l2 3-1 3 2 3-1 3 2 3-1 3 2 3-1 3 2 3", "none", "#C9BC98", .7) + p("M35 14h18", "none", "#4A4238", .35)
             + p("M3 44h54v2H3z", "url(#aLeather)") + f'<text x="45" y="22" font-family="Bungee" font-size="4" fill="#B9AE94" text-anchor="middle">42?</text>')
A["photo"] = (sh(31, 44, 18, 4) + r(13, 4, 34, 40, "url(#aBrass)", 1.2) + r(16, 7, 28, 34, "#6E4A16") + r(17.4, 8.4, 25.2, 31.2, "#C9B48A")
              + r(17.4, 8.4, 25.2, 31.2, "#8A6A3A", extra='opacity=".35"') + c(25, 19, 3.4, "#5A4028") + p("M19 39c0-9 3-13 6-13s6 4 6 13z", "#3A2818")
              + c(35, 19, 3.4, "#5A4028") + p("M29 39c1-9 3-13 6-13s6 4 7 13z", "#F4EAD0") + p("M33 12c1-3 4-3 5 0", "none", "#F4EAD0", .6)
              + p("M18 9l14 0-14 14z", "#FFFFFF", extra='opacity=".18"') + p("M30 4l-4 4M34 4l-4 4", "none", "#F7D58A", .5))
A["bench"] = (sh(30, 40, 24, 5) + r(6, 16, 48, 18, "url(#aWood)", 2) + r(8, 18, 44, 14, "url(#aLeather)", 2)
              + "".join(c(x, y, .9, "#3E0A12") for x in (16, 24, 32, 40, 48 - 4) for y in (22, 28)) + p("M8 34v12M52 34v12", "none", "url(#aWoodV)", 3)
              + p("M18 24c4-3 7 2 11-1c3-2 5 1 8-1", "none", "#F2E6B8", .4) + hl("M10 19h38", .35, .7))
A["sheet"] = (sh(30, 42, 22, 5) + p("M10 8l28-3 4 36-28 3z", "#D9CFB8") + r(16, 5, 30, 38, "url(#aPaper)")
              + "".join("".join(p(f"M19 {y + k * 1.4}h24", "none", "#4A4238", .3) for k in range(5)) for y in (10, 21, 32))
              + "".join(c(x, y, 1, "#1E1A16") + p(f"M{x + .9} {y}v-4", "none", "#1E1A16", .35) for x, y in [(22, 13.5), (27, 12.2), (32, 14.8), (24, 24), (30, 22.6), (37, 25.4), (22, 35)])
              + p("M30 33c5-2 10 0 11 5c-4 3-10 2-11-5z", "#2E2A30", extra='opacity=".7"') + "".join(p(f"M{32 + k} {35 - k * .3}c1.5-1 3.5-.6 4 1", "none", "#57505C", .25) for k in range(4)))
A["programme"] = (sh(31, 42, 18, 5) + p("M44 10c3 0 5 3 4 6c-2 0-5-2-4-6z", "url(#aRed)") + p("M44 16l-2 8", "none", "#3E6A46", .7)
                  + r(14, 5, 28, 38, "url(#aLeather)", .5) + r(16.5, 7.5, 23, 33, "none", 0, "url(#aBrass)", .6)
                  + p("M21 17c3-4 11-4 14 0c-1 6-13 6-14 0z", "url(#aBone)") + e(25, 17.4, 1.6, 1, "#1E1A16") + e(31, 17.4, 1.6, 1, "#1E1A16") + p("M24 22c2 1 5 1 7 0", "none", "#1E1A16", .5)
                  + f'<text x="28" y="31" font-family="Bungee" font-size="3.2" fill="url(#aBrass)" text-anchor="middle">TONIGHT</text>'
                  + p("M21 34h14M23 36.6h10", "none", "#C9923A", .5) + hl("M16 8v34", .2, 1))
A["metronome"] = (sh(30, 44, 16, 4) + p("M19 46L25 5h10l6 41z", "url(#aWood)") + p("M22 30h16l2 14H20z", "#2A1A16") + p("M25 8h10", "none", "#C9923A", .6)
                  + p("M30 38L44 12", "none", "url(#aMetal)", 1.1) + p("M37.6 22l3.4 1.6-1.4 3-3.4-1.6z", "url(#aBrass)") + c(30, 38, 1.2, "url(#aBrass)")
                  + p("M24 16l3 4-2 3 3 3", "none", "#1A0E0A", .6) + p("M46 8l3-3M47 13l4-1", "none", "#E31B3B", .8) + hl("M25.6 7l-5 36", .3, .8))
A["curtains"] = (r(0, 0, 60, 48, "#0E1218") + "".join(p(f"M{x} {y}l-2 4", "none", "#5B7C99", .4, 'opacity=".5"') for x, y in [(28, 10), (32, 20), (30, 32), (27, 40)])
                 + r(2, 3, 56, 3, "url(#aBrass)", 1.5) + c(3, 4.5, 2, "url(#aBrass)") + c(57, 4.5, 2, "url(#aBrass)")
                 + p("M4 6h20c-3 10 3 18-1 30l1 10H4z", "url(#aVelvet)") + p("M56 6H36c3 10-3 18 1 30l-1 10h20z", "url(#aVelvet)")
                 + p("M18 28c3 0 5 1 6 2M42 28c-3 0-5 1-6 2", "none", "url(#aBrass)", 1.6) + e(24, 31, 1.6, 2.4, "url(#aBrass)") + e(36, 31, 1.6, 2.4, "url(#aBrass)"))
A["flour"] = (p("M8 32c3-8 14-10 22-7c8-5 19 0 18 8c5 5-3 13-11 10c-7 5-19 4-23-1c-8-1-9-8-6-10z", "#E9E4D8") + p("M8 32c3-8 14-10 22-7", "none", "#FFFFFF", 1.2, 'opacity=".5"')
              + p("M27 27c4-2 8 0 8 4c0 4-1 5-1 9c0 3-2 4-4 4s-4-2-3-5c0-4-3-6-2-9z", "#BDB49F") + "".join(p(f"M28 {30 + k * 2.4}h5", "none", "#A89E86", .6) for k in range(5))
              + p("M36 4h16l2 20H34z", "url(#aPaper)") + p("M34 24l-6 4", "none", "#CDBF9C", 1) + f'<text x="44" y="15" font-family="Bungee" font-size="3.4" fill="{OX}" text-anchor="middle">FLOUR</text>'
              + dust([(14, 22), (20, 18), (48, 28), (52, 36), (10, 40)], "#F4F0E6"))
A["cupboard"] = (r(0, 0, 60, 48, "#1E2830") + r(8, 2, 44, 26, "url(#aWood)", 1) + r(11, 5, 17, 20, "#1A100C") + p("M28 5l14 4v14l-14 2z", "url(#aWoodV)")
                 + c(38, 16, .9, "url(#aBrass)") + r(13, 15, 5, 10, "#D9E4EA", extra='opacity=".85"') + r(13, 13, 5, 2, "#8C877D") + r(19.5, 17, 6, 8, "#C9923A") + r(19.5, 15.5, 6, 1.5, "#5A3A2C")
                 + p("M14 11h12", "none", "#5A3A2C", .8) + p("M30 34v12M26 38l4-4 4 4", "none", "#E31B3B", 1) + p("M10 46h40", "none", "#3A3A40", 1)
                 + f'<text x="45" y="40" font-family="Silkscreen" font-size="3" fill="#8C877D">2.1 m</text>')
A["menu"] = (sh(30, 42, 18, 5) + r(15, 4, 30, 40, "url(#aPaper)", 1) + r(17.5, 6.5, 25, 35, "none", 0, "url(#aBrass)", .6)
             + p("M24 9c2-2 10-2 12 0", "none", "#C9923A", .5) + f'<text x="30" y="15.6" font-family="Bungee" font-size="5" fill="{OX}" text-anchor="middle">MENU</text>'
             + p("M23 18h14", "none", "#C9923A", .4) + write(21, 22, 18, 6, 3.2, "#3A3530", .4, .35) + c(30, 40, .9, "url(#aBrass)") + hl("M16 6v36", .3, .8))
A["grocery"] = (sh(30, 42, 18, 5) + r(14, 6, 28, 38, "url(#aPaper)", .5) + "".join(c(16 + k * 3.4, 6, .9, "none", "url(#aMetal)", .6) for k in range(8))
                + "".join(r(17, 12 + k * 6.6, 3.2, 3.2, "none", 0, "#3A3530", .45) + write(22.5, 14 + k * 6.6, 15, 1, col="#3A3530") for k in range(4))
                + p("M17.6 13.6l1.2 1.3 2.2-2.6M17.6 20.2l1.2 1.3 2.2-2.6", "none", "#E31B3B", .7)
                + p("M40 44l12-16", "none", "url(#aBrass)", 2.2) + p("M52 28l1.4-2", "none", "#F4C2A0", 2) + p("M39.4 44.8l.8-1.2", "none", "#2A2A2A", 2))
A["sugar"] = (sh(28, 36, 20, 7) + p("M10 26c0 10 8 16 18 16s18-6 18-16z", "url(#aBone)") + e(28, 26, 18, 6, "#F8F4EA") + e(28, 26, 15, 4.6, "#E4DCC8")
              + "".join(r(x, y, 3.2, 3.2, "#FFFFFF", .3, "#C9C3B8", .3) for x, y in [(19, 23), (24, 24.6), (29, 23), (33, 25), (25, 21.6)])
              + p("M10 26c0 10 8 16 18 16", "none", "#C9923A", .4) + p("M42 18l12-12", "none", "url(#aMetal)", 1.6) + e(40.4, 19.8, 3.2, 1.8, "url(#aMetal)", 'transform="rotate(-45 40.4 19.8)"')
              + e(48, 38, 6, 2, "#E4DCC8") + hl("M13 29c2 6 7 10 14 11", .6, .8))
A["barrels"] = (c(16, 24, 14, "url(#aWood)", "#1A100C", .6) + c(16, 24, 11.6, "none", "url(#aMetal)", 1.2) + c(16, 24, 6, "none", "#2A1A16", .6) + c(16, 24, 1.6, "#2A1A16")
                + c(44, 26, 13, "url(#aWood)", "#1A100C", .6) + c(44, 26, 10.6, "none", "url(#aMetal)", 1.2) + c(44, 26, 5.4, "none", "#2A1A16", .6) + c(44, 26, 1.4, "#2A1A16")
                + sh(30, 44, 8, 3) + p("M24 43l9-1.4.8 2.4-9 1.4z", "url(#aBrownL)") + p("M33 41.6l2.2-.3.8 2.4-2.2.3z", "#8C877D") + p("M27.6 42.5l1.4-.2.5 1.5-1.4.2z", "url(#aRed)")
                + hl("M8 16a12 12 0 0 1 8-4", .35, .8) + hl("M36 18a11 11 0 0 1 8-4", .35, .8))
A["barrel"] = (sh(30, 46, 18, 3) + p("M12 6c12-4 24-4 36 0c3 14 3 28 0 40c-12 4-24 4-36 0c-3-12-3-26 0-40z", "url(#aWoodV)")
               + "".join(p(f"M{x} 5c-1 14-1 28 0 42", "none", "#2A1A16", .35) for x in (18, 24, 30, 36, 42))
               + p("M11 13c12 3 26 3 38 0M10 26c13 2 27 2 40 0M11 39c12 3 26 3 38 0", "none", "url(#aMetal)", 1.6)
               + p("M10 3l14 10M10 3c4 5 4 10 2 16M10 3l10 3M14 6c2 1 4 0 6-1M12 10c2 1 4 1 6-1", "none", "#E8E2D2", .3, 'opacity=".65"')
               + dust([(20, 18), (34, 20), (40, 32), (26, 34), (44, 16)], "#B9B2A6") + c(30, 26, 1.4, "#1A100C"))
A["iou"] = (sh(30, 42, 22, 5) + r(6, 12, 20, 28, "#FFFFFF", 1.5, "#C9C3B8", .4, 'transform="rotate(-14 16 26)"')
            + f'<text x="12" y="22" font-family="Bungee" font-size="6" fill="{RED}" transform="rotate(-14 16 26)">A</text>' + p("M14 30l2-4 2 4-2 4z", RED, extra='transform="rotate(-14 16 26)"')
            + r(20, 8, 26, 30, "url(#aPaper)", .5) + f'<text x="33" y="17" font-family="Bungee" font-size="6" fill="{NOIR}" text-anchor="middle">IOU</text>'
            + f'<text x="33" y="25" font-family="IBM Plex Mono" font-size="3.6" font-weight="700" fill="{OX}" text-anchor="middle">&#163;200,000</text>'
            + write(24, 30, 18, 2, 2.6) + c(50, 38, 5, RED, "#FFFFFF", .8, 'stroke-dasharray="1.2 1.2"') + c(50, 38, 3, "#C21732") + c(46, 43, 4, "#1E1A16", "#FFFFFF", .7, 'stroke-dasharray="1 1"'))
A["bottle"] = (sh(30, 46, 12, 3) + p("M27 4h6v12c6 3 8 7 8 12v18H19V28c0-5 2-9 8-12z", "url(#aGlass)") + r(26, 2, 8, 6, "url(#aRed)", 1)
               + p("M26 6c2 2 6 2 8 0", "none", "#5A0916", .6) + r(19, 28, 22, 12, "url(#aPaper)") + r(20.5, 29.5, 19, 9, "none", 0, "#C9923A", .4)
               + f'<text x="30" y="33.6" font-family="Bungee" font-size="2.6" fill="{OX}" text-anchor="middle">CH&#194;TEAU</text>'
               + f'<text x="30" y="37.4" font-family="Bungee" font-size="3.2" fill="#3A3530" text-anchor="middle">1956</text>'
               + hl("M22 22c0-3 2-6 5-7", .4, 1) + p("M22 30v14", "none", "#FFFFFF", .7, 'opacity=".2"') + dust([(25, 20), (34, 22), (23, 44), (37, 43), (31, 18), (28, 25)], "#C9C3B8"))
A["dustprint"] = (r(0, 0, 60, 48, "#4A4440") + "".join(c((k * 37) % 60, (k * 23) % 48, .4 + (k % 3) * .15, "#6E6862", extra='opacity=".8"') for k in range(70))
                  + p("M24 6c8-5 15 0 13 11c-1 7-3 10-3 16c0 4-2 7-6 7c-5 0-7-3-6-8c1-5-3-10-3-16c0-4 1-7 5-10z", "#38332F")
                  + "".join(p(f"M{25 + (k % 2)} {9 + k * 3}h{8 - (k % 2) * 2}", "none", "#4A4440", .9) for k in range(5))
                  + "".join(p(f"M{26} {31 + k * 2.4}h5", "none", "#4A4440", .8) for k in range(3)))
# bonus
A["battery"] = (sh(30, 44, 14, 3) + r(17, 12, 26, 33, "url(#aMetal)", 3) + r(19, 14, 22, 29, "#16181C", 2) + r(25, 7, 10, 6, "url(#aBrass)", 1.5)
                + r(21, 28, 18, 13, "url(#aRed)", 1) + p("M32 16l-7 10h5.6l-3 8 8-11h-5.6z", "#F2A93B", "#FFF2C8", .3) + hl("M20 16v26", .4, 1))
A["shoes"] = (sh(32, 42, 24, 4) + p("M6 34c7 0 12-8 17-12l8 2c3 5 10 7 17 7c4 0 6 3 6 7v4H6z", "url(#aBone)") + p("M6 40h48v5H6z", "url(#aRed)")
              + p("M23 22l8 2c-1 4-3 6-6 7", "none", "#C9BFA8", .5) + "".join(p(f"M{24 + k * 2} {26 + k}l3 1", "none", "#1E1A16", .7) for k in range(3))
              + p("M2 26h10M4 31h8M1 36h6", "none", "#8C877D", 1) + hl("M10 34c6-1 10-6 13-9", .6, .7))
A["key"] = (sh(32, 30, 24, 6) + c(14, 24, 9, "none", "url(#aBrass)", 3.6) + c(14, 24, 3.6, "none", "url(#aBrass)", 1.2) + r(22, 22, 28, 4, "url(#aBrass)", 1)
            + p("M42 26v8h3v-3h2v5h3V26z", "url(#aBrass)") + r(26, 21, 2, 6, "#8A5E1E") + hl("M8 19a8 8 0 0 1 8-3", .6, .8) + hl("M24 22.8h24", .5, .5))


def art(key, room):
    return (f'<svg viewBox="0 0 60 48" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block">{DEFS}'
            f'<rect width="60" height="48" fill="{SURF[room]}"/>{A[key]}'
            f'<rect width="60" height="48" fill="url(#aLight)"/><rect width="60" height="48" fill="url(#aVig)"/></svg>')
