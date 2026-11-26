# THE LAST QUERY — Art Direction

Style: graphic film noir × terminal. Black night, warm paper white, one blood red.
Geometric block letters, flat colours, no gradients. Board-game finish: every shape has a solid 45° extrusion (like a die-cut token) and the tagline sits on a ribbon in a pixel "terminal" font. "Corrupted data" is shown with glitch slices.

## Logo (step 1, v6: board-game finish) ✅ validated on 2026-11-24

| Detail | Meaning |
|---|---|
| `>` before THE | terminal prompt: the police console |
| Sliced R with red offset | a corrupted record (`████`) |
| Red `;` at the end | the end of the query: the *last* one |
| Red 3D extrusion (oxblood under red shapes) | box-art depth, like a printed game token |
| Ribbon "A MURDER MYSTERY BOARD GAME" in pixel font | says what it is, with the terminal flavour |
| Q = magnifying glass | the investigation |
| Detective in a trench coat, red hat band, phone glowing red | the player and the Police Console app |

### Files (`DA/logo/`)
| File | Use |
|---|---|
| `the-last-query_logo_dark.svg` | **main version**, on black |
| `the-last-query_logo_light.svg` | on paper white |
| `*_transparent.svg` | no background (web / app). Cuts are an SVG mask: use the opaque or PNG versions for print. |
| `the-last-query_logo_mono_white.svg` / `_mono_black.svg` | 1 colour, no extrusion (stamp, laser engraving, B&W print) |
| `png/*.png` | 3450 × 1965 px = 29.2 × 16.6 cm at 300 DPI. Transparent PNGs keep alpha. |
| `print/the-last-query_logo_A4_bleed3mm_cropmarks.pdf` | A4 landscape print test: 3 mm bleed, crop marks, logo inside the safe area |

Regenerate everything: `python3 DA/tools/build_logo.py && zsh DA/tools/render.sh` (needs Google Chrome).

### Clear space and minimum size
- **Clear space**: keep empty space around the logo equal to the **height of "THE"** (called *x*) on every side. The SVG artboards already include it.
- **Minimum size**: **50 mm wide** with the tagline (pixel text ≈ 1.5 mm high), **40 mm wide** in print (thinnest line ≈ 0.5 mm), **240 px wide** on screen. Below this, use the mono version or the symbol alone (the Q).

## Step 2: palette & typography (`DA/palette-typo/`) ✅ validated on 2026-11-24

Brand sheet: `the-last-query_brand-sheet_A4_bleed3mm.pdf` (print, crop marks) and `.png` (300 DPI).

| Name | HEX | RGB | CMYK (approx., coated paper) | Role |
|---|---|---|---|---|
| Noir | `#0B0B0C` | 11 11 12 | **Rich black** C60 M40 Y40 K100 (large areas) / K100 (small text) | backgrounds, night |
| Graphite | `#232327` | 35 35 39 | C70 M60 Y55 K75 | panels, room tiles |
| Bone | `#F4F0E6` | 244 240 230 | C3 M4 Y9 K0 | text, lines, Table cards |
| Ash | `#8C877D` | 140 135 125 | C40 M35 Y45 K15 | secondary text |
| Query Red | `#E31B3B` | 227 27 59 | C0 M95 Y75 K0 · Pantone ≈ 1925 C | accent, Keyword cards |
| Oxblood | `#7E0C1F` | 126 12 31 | C20 M100 Y80 K45 | 3D depth, Twist cards |
| Lamp Amber | `#F2A93B` | 242 169 59 | C0 M38 Y85 K0 | Coffee cards and tokens |
| Storm Blue | `#5B7C99` | 91 124 153 | C65 M35 Y20 K15 | Evidence cards, rain |
| Brass | `#C9923A` | 201 146 58 | C15 M45 Y85 K5 | board details, medallions |
| Case Paper | `#EFE8D8` | 239 232 216 | C5 M7 Y15 K0 | card faces |
| Kraft | `#C9A46E` | 201 164 110 | C20 M35 Y60 K5 | card backs (folder) |

| Use | Font (Google Fonts, SIL OFL: free for print) | Sizes |
|---|---|---|
| Titles | **Bungee** | 14-40 pt |
| Body / rules | **Archivo** | 7.5-10 pt, never under 7 pt on cards |
| Data / SQL / codes | **IBM Plex Mono** | 7-24 pt |
| Labels | **Silkscreen** (pixel, caps only) | 6-12 pt |

Icons: 24 px grid, 2 px stroke, square ends (room icons + card-type icons), drawn in `tools/build_print.py`.

## Step 3: game board (`DA/board/`) ✅ V3 validated on 2026-11-25

The V2 board (A2 with a side panel) was replaced by the **V3 board**: the manor only, no side panel,
**394 × 539 mm (portrait) printed on 2 A3 landscape sheets** stacked top / bottom and glued together.
The logo is a rug in the Grand Hall. Clean case-file style (aged paper, typewriter text, black and red accents).

| File | Use |
|---|---|
| `the-last-query_board-V3_sheet-1-of-2_A3_print.pdf` | **print**: top half, A3 landscape at 100 % |
| `the-last-query_board-V3_sheet-2-of-2_A3_print.pdf` | **print**: bottom half + 10 mm glue tab |
| `the-last-query_board-V3_assembled_preview_394x539.pdf` / `_preview.png` | preview of the glued board |
| `png/*_300dpi.png` | both sheets and the assembled board at 300 DPI |

How to print, cut and glue, and the source scripts: see `DA_V3/README.md` (`DA_V3/tools/build_board_v3.py`).

## Step 4: cards (`DA/cards/`) ✅ V2 validated on 2026-11-25

> **Current print files** = 40 clue cards V2, **63 × 88 mm**, made by `tools/build_cards.py` (34 Evidence + 6 Bonus, codes `LIB-01` … `CEL-06`). Updated after playtest 1: Bonus cards now carry a QR too (*"Keep it face up · play it on your turn"*). The **V3 cards, 50 × 85 mm**, with the same codes, are being made in `DA_V3/` and will replace them.
> The description below (64 cards, Keyword, Table…) is the older V1 set, kept for reference.

**Style: B "Case File"** (chosen on 2026-11-24 among 3 proposals in `cards/proposals/`): square corners, cream paper with a red margin line, paper clip, black header with the type colour on the left, a red rubber stamp per type (ACCESS GRANTED, RECORDS, EVIDENCE, BREAK TIME, URGENT, CLASSIFIED); backs = kraft folder with a "CASE FILE N° 1123" tab, a typed room label and a CONFIDENTIAL stamp. The other styles stay available in `tools/build_print.py` (`THEME = "noir" | "dossier" | "deco"`).

**64 cards, 63 × 88 mm**: 16 Keyword, 8 Table, 12 Evidence, 12 Coffee, 12 Twist, 4 Detectives.
Clue cards are dealt into the 7 searchable rooms (the back shows the room). Keyword, Table and Evidence cards carry a **real QR code** (`TLQ:<code>`, e.g. `TLQ:KW-WHR1`) and the same backup code in text, ready for the app.

| File | Use |
|---|---|
| `print/the-last-query_cards_faces_63x88_bleed3mm.pdf` | **print shop**: 1 card per page, 69 × 94 mm with bleed, crop marks |
| `print/the-last-query_cards_backs_63x88_bleed3mm.pdf` | matching backs, same order |
| `print/the-last-query_cards_faces_A4-home.pdf` | **home / school printer**: 9 cards per A4 page, crop marks |
| `print/the-last-query_cards_backs_A4-home_duplex.pdf` | backs, mirrored for duplex (flip on long edge) |
| `png/*.png` | every face + the 8 backs, 300 DPI with bleed (816 × 1113 px) |
| `the-last-query_cards_overview.png` | one card of each type |

Regenerate board, cards and brand sheet: `python3 DA/tools/build_print.py && zsh DA/tools/render_print.sh` (needs Google Chrome and an internet connection for the fonts and the QR library).

## Step 5: tokens, pawns & notebook (`DA/tokens/`) ✅ V2 validated on 2026-11-25

- **Query Tokens are physical since playtest 1 (T1)**: the app no longer counts them. 20 tokens Ø 20 mm, front = black disc with the logo's red `;`, **back = unique QR `TLQ:Q-01` … `TLQ:Q-20` + backup code** (scanned in the Police Console to pay a query; a token works once per round). Bleed 3 mm, cut along the dotted circles. QR checked with the app's reader (jsQR).
  - **`the-last-query_query-tokens_A4_duplex-grid.pdf` (recommended, easy cut)**: 2 pages, double-sided, flip on the long edge, 100 %, 250-350 g/m² card. The 20 tokens are **20 × 20 mm squares in a gapless 4 × 5 grid**: cut straight along the crop marks with a ruler or a guillotine (5 vertical + 6 horizontal cuts). One solid colour per side, so a small duplex shift never shows; 3 mm bleed around the block; backs mirrored. QR decoded at their mirrored places (Q-01, Q-07, Q-20).
  - `the-last-query_query-tokens_pawns_A4_duplex.pdf` (2 pages, double-sided, flip on long edge, 250-350 g/m² card): page 1 = token fronts + **4 pawns P1-P4** to fold into tents, page 2 = token backs, mirrored.
  - `the-last-query_query-tokens_A4_glue.pdf` (1 page, one-sided): fronts on top, backs below. Glue the fronts on one side of a 1.5 mm card and the backs on the other side, then cut. No duplex alignment problem.
  - `*_300dpi.png`: previews.
- `the-last-query_detective-notebook_A5_2-sides_bleed3mm.pdf`: one A5 sheet per player, two sides (updated after playtest 1: 1 query per turn, "two clues disagree" rule, example query in real SQL). Side 1: 12 suspects × age / height / shoe / hand / hair / glasses / smell + ✗, golden rules, W.A.T.S.O.N. updates (rounds 4/8/12). Side 2: *My clues* (object, room, what it reveals, seen ×3), accusation template, table talk, example query with its SQL.
- Source: `tools/build_tokens.py`. V1 (coffee, clock, suspended tokens) is in `_archive_v1/`.

## Step 6: rules booklet (`DA/rules/`) V2

- Updated after playtest 1 (2026-11-25): 1 card per turn during the move, 1 query per turn, Bonus cards kept and played later, what to do with drawn cards, "two clues disagree" golden rule, block-by-block Police Console.
- **A5, 8 pages, in English** (saddle-stitch: 2 A4 sheets folded): cover, the story & the game in 30 seconds, components & setup, your turn (move, search / recharge / accuse, query), the clues & golden rules, the Police Console & W.A.T.S.O.N. updates, accuse & table talk, back cover.
- `the-last-query_rules_A5_bleed3mm_cropmarks.pdf` (print shop) · `the-last-query_rules_A5_screen.pdf` (screen / printer booklet mode) · `the-last-query_rules_overview.png`.
- The back cover still has a blank: **"A GAME BY TEAM ________"**. Source: `tools/build_rules.py`.

## Print rules (all print files)
- **Bleed**: 3 mm on every edge. The background goes all the way into it.
- **Safe area**: no text or important element closer than **5 mm** to the trim line (3 mm minimum).
- **Resolution**: vectors (SVG / PDF) whenever possible; raster images at **300 DPI** minimum at final size.
- **Real sizes in mm**: cards 63 × 88 mm (V2, poker size; V3 = 50 × 85 mm), board V3 2 × A3 (394 × 539 mm assembled), rules booklet A5.
- **Crop marks** on every print PDF, placed outside the bleed (10 mm slug).
- **CMYK**: files are made in RGB (sRGB). Convert to CMYK (profile *FOGRA39 / Coated*) at the print shop or in Illustrator/Affinity before sending, and check the red: bright screen reds lose some punch on paper.
- No fonts inside the logo: everything is shapes, so nothing needs outlining. Board, cards and brand sheet PDFs embed their fonts.
- Card stock: 300-350 g/m² coated, matt finish. Board: printed on paper and glued on 2 mm greyboard (or foam board).
