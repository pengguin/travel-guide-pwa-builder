#!/usr/bin/env python3
"""Create a dependency-free travel-guide PWA from the bundled starter."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "travel-guide"


def js_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'").replace("\r", "").replace("\n", " ")


def json_escape(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)[1:-1]


def replace_tokens(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    for token, value in replacements.items():
        text = text.replace(token, value)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="new project directory")
    parser.add_argument("--title", required=True, help="full guide title")
    parser.add_argument("--short-title", help="short PWA/app title")
    parser.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--origin", required=True, help="trip origin")
    parser.add_argument("--destinations", nargs="+", required=True, help="ordered destination names")
    parser.add_argument("--trip-id", help="stable ASCII identifier")
    args = parser.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.start_date) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.end_date):
        parser.error("start and end dates must use YYYY-MM-DD")
    if args.start_date > args.end_date:
        parser.error("start date must not be after end date")

    output = args.output.expanduser().resolve()
    if output.exists():
        print(f"ERROR: output already exists; refusing to overwrite: {output}", file=sys.stderr)
        return 2

    starter = Path(__file__).parents[1] / "assets" / "starter"
    if not starter.is_dir():
        print(f"ERROR: bundled starter missing: {starter}", file=sys.stderr)
        return 2

    short_title = args.short_title or args.title[:8]
    trip_id = args.trip_id or slugify(args.title)
    destinations = " → ".join(args.destinations)
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(starter, output)

    replace_tokens(output / "index.html", {
        "__TITLE__": html.escape(args.title),
    })
    replace_tokens(output / "manifest.webmanifest", {
        "__TITLE__": json_escape(args.title),
        "__SHORT_TITLE__": json_escape(short_title),
    })
    replace_tokens(output / "service-worker.js", {
        "__CACHE_NAME__": f"{trip_id}-v1",
    })
    replace_tokens(output / "data" / "trip-data.js", {
        "__TRIP_ID__": js_escape(trip_id),
        "__TITLE__": js_escape(args.title),
        "__SHORT_TITLE__": js_escape(short_title),
        "__START_DATE__": js_escape(args.start_date),
        "__END_DATE__": js_escape(args.end_date),
        "__ORIGIN__": js_escape(args.origin),
        "__DESTINATIONS__": js_escape(destinations),
    })

    print(f"Created travel-guide PWA: {output}")
    print("Next: replace the scaffold content in data/trip-data.js, then run the audit and browser QA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
