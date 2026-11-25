#!/bin/zsh
# Render the print sources (built by build_print.py) to PDF and PNG with headless Chrome.
# Usage: zsh DA/tools/render_print.sh [quick]
#   quick = low-res PNG previews only (for checking the layout)
set -e
T="${0:A:h}"
DA="$T/.."
SRC="$T/print_src"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MM=3.7795275591   # CSS px per mm
DPI300=3.125      # device scale factor for 300 DPI (96 * 3.125 = 300)

pdf() {  # pdf <html> <out.pdf>
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=20000 \
    --run-all-compositor-stages-before-draw --print-to-pdf="$2" "file://$1" >/dev/null 2>&1
  echo "pdf  ${2:t}"
}
png() {  # png <html> <out.png> <width mm> <height mm> <scale>
  local w=$(( int(ceil($3 * MM)) )) h=$(( int(ceil($4 * MM)) ))
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=20000 \
    --force-device-scale-factor=$5 --window-size=$w,$h --screenshot="$2" "file://$1" >/dev/null 2>&1
  echo "png  ${2:t}"
}
zmodload zsh/mathfunc

mkdir -p "$DA/palette-typo" "$DA/board" "$DA/cards/png" "$DA/cards/print"

if [[ "$1" == "quick" ]]; then
  png "$SRC/brand_sheet.html" "$DA/palette-typo/preview.png" 343 256 1
  png "$SRC/board_A2.html" "$DA/board/preview.png" 620 446 0.6
  png "$SRC/cards_overview.html" "$DA/cards/preview.png" 400 210 1
  exit 0
fi

# brand sheet
pdf "$SRC/brand_sheet.html" "$DA/palette-typo/the-last-query_brand-sheet_A4_bleed3mm.pdf"
png "$SRC/brand_sheet.html" "$DA/palette-typo/the-last-query_brand-sheet.png" 343 256 $DPI300

# board (PNG = trim + bleed + slug at 300 DPI)
pdf "$SRC/board_A2.html" "$DA/board/the-last-query_board_A2_bleed3mm_cropmarks.pdf"
png "$SRC/board_A2.html" "$DA/board/the-last-query_board_A2_300dpi.png" 620 446 $DPI300

# cards
pdf "$SRC/cards_faces_bleed.html" "$DA/cards/print/the-last-query_cards_faces_63x88_bleed3mm.pdf"
pdf "$SRC/cards_backs_bleed.html" "$DA/cards/print/the-last-query_cards_backs_63x88_bleed3mm.pdf"
pdf "$SRC/cards_faces_A4.html" "$DA/cards/print/the-last-query_cards_faces_A4-home.pdf"
pdf "$SRC/cards_backs_A4.html" "$DA/cards/print/the-last-query_cards_backs_A4-home_duplex.pdf"
png "$SRC/cards_overview.html" "$DA/cards/the-last-query_cards_overview.png" 400 210 2
for f in "$SRC"/cards/*.html; do
  png "$f" "$DA/cards/png/${f:t:r}.png" 69 94 $DPI300 >/dev/null
done
echo "png  cards/png/*.png ($(ls "$DA/cards/png" | wc -l | tr -d ' ') files)"
