#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
# Requires Node.js and Playwright. CHROME optionally selects an existing browser.
exec "${NODE:-node}" "$ROOT/scripts/render_readme_screenshots.cjs"
