#!/bin/zsh
# Export every logo SVG to PNG with headless Google Chrome.
# Scale x3 of the 1150 x 655 artboard = 3450 x 1965 px
# = 29.2 x 16.6 cm at 300 DPI.
# Usage: zsh DA/tools/render.sh
set -e
DIR="${0:A:h}/../logo"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$DIR/png"
for f in "$DIR"/*.svg; do
  name="${f:t:r}"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --default-background-color=00000000 \
    --force-device-scale-factor=3 --window-size=1150,655 \
    --screenshot="$DIR/png/$name.png" "file://$f" >/dev/null 2>&1
  echo "rendered $name.png"
done
