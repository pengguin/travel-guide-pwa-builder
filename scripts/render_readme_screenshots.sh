#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
CHROME=${CHROME:-/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome}
PAGE="file://${ROOT}/docs/demo-screenshots.html"
OUT="${ROOT}/docs/images"

mkdir -p "$OUT"

capture() {
  lang="$1"
  shot="$2"
  width="$3"
  height="$4"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size="${width},${height}" \
    --screenshot="${OUT}/${shot}-${lang}.png" \
    "${PAGE}?lang=${lang}&shot=${shot}"
}

for lang in zh en; do
  capture "$lang" chat 1600 1000
  capture "$lang" home 1600 1000
  capture "$lang" map 1600 900
done
