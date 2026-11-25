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

## Step 3: game board (`DA/board/`) ✅ V2 validated on 2026-11-25

- `the-last-query_board_A2_bleed3mm_cropmarks.pdf`: **A2 landscape 594 × 420 mm**, 3 mm bleed, crop marks. Vector PDF, fonts embedded.
- `the-last-query_board_A2_300dpi.png`: same at 300 DPI (7325 × 5269 px, includes bleed and slug).
- **v3: floor plan of Ravenscroft Manor**, seen from above, flat noir style with depth:
  - **light**: moonlight falling through every outside window, amber lamp glows, vignetted rooms, a flat cast shadow under every wall and piece of furniture (light from the top-left);
  - **architecture**: thick bone walls, doors opening onto the hallways with wooden thresholds, windows with mullions, four corner towers, the front door with its steps and gravel path, a hedge around the house, a decorative frame;
  - **one floor per room**: star chart, parquet, stone, herringbone, marble, tiles, greenhouse glass, raised server floor, cellar brick;
  - **furniture and story clues**: Victor's armchair, his cold tea, his dropped phone, the chalk outline and evidence marker 1 (Library); telescope (Observatory); pews, altar, organ, stained-glass light (Chapel); grand piano, cello, gramophone (Music Room); staircase, chandelier (Grand Hall); range, sink, coffee machine, table (Kitchen); foxglove beds labelled *Digitalis purpurea* (Greenhouse); server racks, a red failing unit, a terminal showing `SELECT *` / `ERR` (Server Room); barrels, bottle racks, tasting table (Wine Cellar); a grandfather clock stopped at 11:45 and **muddy footprints "SIZE 44?" from the Greenhouse to the Library** in the hallway.
- Game info: name plates numbered N°01-09 with the room icon and power, a **88 × 63 mm deck zone** (corner brackets) on a rug or table in every searchable room, red trapdoors for the secret passages, P1-P4 start medallions in the Grand Hall.
- Sidebar: logo, story line, **clock dial** (hands stopped at 11:45, 8 round slots from 12:00 to 4:00 AM + dawn), turn summary with icons, *Solve the case* (Opportunity + Means + Motive), coffee bank.
- Source: `tools/build_board.py` (pure SVG in millimetres; gradients and shadows stay vector in the PDF).

## Step 4: cards (`DA/cards/`) ✅ V2 validated on 2026-11-25

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

- `the-last-query_query-tokens_pawns_A4.pdf` (1 page A4, print at 100 %): **20 Query Tokens** `;` (16 + 4 spare, Ø 20 mm, black disc with the logo's red block semicolon) and **4 pawns P1-P4** to fold into tents (amber, red, blue, bone). Glue on 1.5 mm card, cut on the dotted circles / grey lines.
- `the-last-query_detective-notebook_A5_2-sides_bleed3mm.pdf`: one A5 sheet per player, two sides. Side 1: 12 suspects × age / height / shoe / hand / hair / glasses / smell + ✗, golden rules, W.A.T.S.O.N. updates (rounds 4/8/12). Side 2: *My clues* (object, room, what it reveals, seen ×3), accusation template, table talk, example query with its SQL.
- Source: `tools/build_tokens.py`. V1 (coffee, clock, suspended tokens) is in `_archive_v1/`.

## Step 6: rules booklet (`DA/rules/`) V2

- **A5, 8 pages, in English** (saddle-stitch: 2 A4 sheets folded): cover, the story & the game in 30 seconds, components & setup, your turn (move, search / recharge / accuse, query), the clues & golden rules, the Police Console & W.A.T.S.O.N. updates, accuse & table talk, back cover.
- `the-last-query_rules_A5_bleed3mm_cropmarks.pdf` (print shop) · `the-last-query_rules_A5_screen.pdf` (screen / printer booklet mode) · `the-last-query_rules_overview.png`.
- The back cover still has a blank: **"A GAME BY TEAM ________"**. Source: `tools/build_rules.py`.

## Print rules (all print files)
- **Bleed**: 3 mm on every edge. The background goes all the way into it.
- **Safe area**: no text or important element closer than **5 mm** to the trim line (3 mm minimum).
- **Resolution**: vectors (SVG / PDF) whenever possible; raster images at **300 DPI** minimum at final size.
- **Real sizes in mm**: cards 63 × 88 mm (poker size), board A2 (594 × 420 mm), rules booklet A5.
- **Crop marks** on every print PDF, placed outside the bleed (10 mm slug).
- **CMYK**: files are made in RGB (sRGB). Convert to CMYK (profile *FOGRA39 / Coated*) at the print shop or in Illustrator/Affinity before sending, and check the red: bright screen reds lose some punch on paper.
- No fonts inside the logo: everything is shapes, so nothing needs outlining. Board, cards and brand sheet PDFs embed their fonts.
- Card stock: 300-350 g/m² coated, matt finish. Board: printed on paper and glued on 2 mm greyboard (or foam board).
