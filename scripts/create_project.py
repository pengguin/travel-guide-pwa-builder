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


THEMES: dict[str, dict[str, str]] = {
    "heritage": {
        "paper": "#f6f1e7", "surface": "#fffdf8", "ink": "#182626",
        "muted": "#64706e", "line": "#ddd6c8", "primary": "#173f3b",
        "secondary": "#a94f35", "highlight": "#e7ad4f", "soft": "#e7efeb",
        "danger": "#a33f34", "on_primary": "#ffffff", "on_primary_muted": "#d7e4df",
        "on_secondary": "#ffffff", "metric_surface": "#fffaf0", "map_surface": "#dde8e2",
        "shadow_rgb": "23, 63, 59", "icon_mid": "#72a49b",
    },
    "desert": {
        "paper": "#f5efe3", "surface": "#fffaf2", "ink": "#2b241d",
        "muted": "#71665b", "line": "#dfd1bf", "primary": "#322d29",
        "secondary": "#a4472d", "highlight": "#d79a35", "soft": "#eee2d2",
        "danger": "#9b332d", "on_primary": "#fffaf2", "on_primary_muted": "#ddd2c5",
        "on_secondary": "#ffffff", "metric_surface": "#fff5e5", "map_surface": "#e8d7bd",
        "shadow_rgb": "50, 45, 41", "icon_mid": "#c9874f",
    },
    "mountain": {
        "paper": "#f1f4f2", "surface": "#fbfdfc", "ink": "#172724",
        "muted": "#5e706d", "line": "#cfdad6", "primary": "#163f38",
        "secondary": "#256383", "highlight": "#d79b36", "soft": "#dfeae6",
        "danger": "#9c3f35", "on_primary": "#ffffff", "on_primary_muted": "#cfe1db",
        "on_secondary": "#ffffff", "metric_surface": "#f5f9f7", "map_surface": "#d8e7e3",
        "shadow_rgb": "22, 63, 56", "icon_mid": "#6eaaa1",
    },
    "coast": {
        "paper": "#eef4f3", "surface": "#fbfefd", "ink": "#142a33",
        "muted": "#60747b", "line": "#ccdcdd", "primary": "#123c50",
        "secondary": "#087879", "highlight": "#e28b63", "soft": "#dceceb",
        "danger": "#a23e3a", "on_primary": "#ffffff", "on_primary_muted": "#cce0e7",
        "on_secondary": "#ffffff", "metric_surface": "#f1faf8", "map_surface": "#d3e8e8",
        "shadow_rgb": "18, 60, 80", "icon_mid": "#58aeb0",
    },
    "forest": {
        "paper": "#f2f1e8", "surface": "#fcfbf5", "ink": "#20291f",
        "muted": "#677063", "line": "#d5d8c8", "primary": "#25452f",
        "secondary": "#4f6f3c", "highlight": "#bd753d", "soft": "#e2e8d9",
        "danger": "#973d35", "on_primary": "#ffffff", "on_primary_muted": "#d4e0d5",
        "on_secondary": "#ffffff", "metric_surface": "#f7f6ec", "map_surface": "#dce5d3",
        "shadow_rgb": "37, 69, 47", "icon_mid": "#7d9a68",
    },
    "tropical": {
        "paper": "#f4f2df", "surface": "#fffdf2", "ink": "#153129",
        "muted": "#62756c", "line": "#d7dcc6", "primary": "#174c3d",
        "secondary": "#087f86", "highlight": "#d9912f", "soft": "#dcebdc",
        "danger": "#a23c37", "on_primary": "#ffffff", "on_primary_muted": "#cee4dc",
        "on_secondary": "#ffffff", "metric_surface": "#fff8df", "map_surface": "#d1e7dc",
        "shadow_rgb": "23, 76, 61", "icon_mid": "#49a795",
    },
    "polar": {
        "paper": "#eef3f6", "surface": "#fbfdff", "ink": "#172631",
        "muted": "#647682", "line": "#cfdae0", "primary": "#173b59",
        "secondary": "#176d83", "highlight": "#dc694f", "soft": "#dce9ef",
        "danger": "#a43b3b", "on_primary": "#ffffff", "on_primary_muted": "#d0e0ea",
        "on_secondary": "#ffffff", "metric_surface": "#f3f8fb", "map_surface": "#d8e8ef",
        "shadow_rgb": "23, 59, 89", "icon_mid": "#6cb4c7",
    },
    "urban": {
        "paper": "#f1f2f3", "surface": "#fcfcfd", "ink": "#202329",
        "muted": "#6a6f78", "line": "#d7d9de", "primary": "#292e38",
        "secondary": "#315ca8", "highlight": "#bd6d87", "soft": "#e5e8ef",
        "danger": "#a33c42", "on_primary": "#ffffff", "on_primary_muted": "#d8dce4",
        "on_secondary": "#ffffff", "metric_surface": "#f6f7fa", "map_surface": "#dfe4ec",
        "shadow_rgb": "41, 46, 56", "icon_mid": "#7387ad",
    },
}

THEME_HINTS: dict[str, tuple[str, ...]] = {
    "desert": ("desert", "sahara", "gobi", "dune", "canyon", "荒漠", "沙漠", "戈壁", "峡谷"),
    "mountain": ("mountain", "alps", "himalaya", "highland", "lake", "山", "高原", "雪", "湖"),
    "coast": ("coast", "island", "ocean", "sea", "beach", "海岸", "海岛", "海洋", "海滩"),
    "forest": ("forest", "woodland", "rainforest", "森林", "林地"),
    "tropical": ("tropical", "jungle", "equator", "热带", "雨林"),
    "polar": ("arctic", "antarctic", "polar", "glacier", "冰川", "极地", "北极", "南极"),
    "urban": ("city", "metropolis", "urban", "城市", "都市"),
    "heritage": ("heritage", "historic", "ancient", "old town", "古城", "历史", "遗产"),
}


def choose_theme(requested: str, destinations: list[str]) -> tuple[str, dict[str, str]]:
    if requested != "auto":
        return requested, THEMES[requested]
    haystack = " ".join(destinations).casefold()
    scores = {
        name: sum(1 for hint in hints if hint.casefold() in haystack)
        for name, hints in THEME_HINTS.items()
    }
    best = max(scores, key=scores.get)
    selected = best if scores[best] else "heritage"
    return selected, THEMES[selected]


def theme_replacements(theme: dict[str, str]) -> dict[str, str]:
    return {f"__THEME_{key.upper()}__": value for key, value in theme.items()}


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
    parser.add_argument(
        "--theme", default="auto", choices=("auto", *THEMES),
        help="destination-aware color family; auto uses destination-name hints",
    )
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
    theme_name, theme = choose_theme(args.theme, args.destinations)
    colors = theme_replacements(theme)
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(starter, output)

    replace_tokens(output / "index.html", {
        "__TITLE__": html.escape(args.title),
        **colors,
    })
    replace_tokens(output / "manifest.webmanifest", {
        "__TITLE__": json_escape(args.title),
        "__SHORT_TITLE__": json_escape(short_title),
        **colors,
    })
    replace_tokens(output / "styles.css", colors)
    replace_tokens(output / "icons" / "app-icon.svg", colors)
    replace_tokens(output / "service-worker.js", {
        "__CACHE_PREFIX__": f"{trip_id}-",
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
    print(f"Theme: {theme_name} ({'auto' if args.theme == 'auto' else 'selected'})")
    print("Next: replace the scaffold content in data/trip-data.js, then run the audit and browser QA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
