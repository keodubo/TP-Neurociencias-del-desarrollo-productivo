#!/bin/bash
# Renderiza cada diapositiva como PNG (cada una como slide "presente",
# de modo que el centrado vertical y las ondas salen correctos).
# Perfil único + watchdog por slide para evitar cuelgues de Chrome headless.
set -u
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML="$1"      # ruta absoluta a index.html
OUT="$2"       # carpeta de salida
NSLIDES="${3:-25}"
mkdir -p "$OUT"
rm -f "$OUT"/slide_*.png

last=$((NSLIDES - 1))
for i in $(seq 0 "$last"); do
  N=$(printf '%02d' "$i")
  PROF="/tmp/cep_$i"
  rm -rf "$PROF"
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --no-first-run --no-default-browser-check \
    --user-data-dir="$PROF" --window-size=1280,720 --force-device-scale-factor=2 \
    --virtual-time-budget=4500 \
    --screenshot="$OUT/slide_$N.png" \
    "file://$HTML?export#/$i" >/dev/null 2>&1 &
  CPID=$!
  ( sleep 18; kill -9 "$CPID" 2>/dev/null ) &
  WPID=$!
  wait "$CPID" 2>/dev/null
  kill "$WPID" 2>/dev/null
  rm -rf "$PROF"
done
echo "DONE: $(ls "$OUT"/slide_*.png 2>/dev/null | wc -l | tr -d ' ') PNGs"
