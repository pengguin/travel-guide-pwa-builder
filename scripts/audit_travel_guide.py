#!/usr/bin/env python3
"""Privacy and release audit for a static travel-guide project."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".js", ".json", ".jsx", ".md", ".mjs",
    ".svg", ".toml", ".ts", ".tsx", ".txt", ".yaml", ".yml",
}
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
SKIP_DIRS = {".git", ".vite", "coverage", "node_modules"}
SKIP_FILES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}

ERROR_PATTERNS = {
    "macOS home path": re.compile(r"/Users/[^/\s'\"<>]+/"),
    "Windows home path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s'\"<>]+\\"),
    "file URL": re.compile(r"file://[^\s'\"<>]+"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "common secret assignment": re.compile(
        r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"
    ),
    "unfinished scaffold": re.compile(r"__REPLACE_WITH_" r"FINAL_ITINERARY__"),
}
WARNING_PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "placeholder": re.compile(r"\b(?:TODO|FIXME|CHANGEME)\b"),
    "local host URL": re.compile(r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?"),
}
ASSET_REF = re.compile(
    r"(?:src|href)\s*=\s*['\"`](/?(?:images|icons)/[^'\"`?#]+)['\"`]|"
    r"['\"`](/?(?:images|icons)/[^'\"`?#]+)['\"`]"
)


def iter_files(root: Path):
    for path in root.rglob("*"):
        relative_path = path.relative_to(root).as_posix()
        if (
            not path.is_file()
            or path.name in SKIP_FILES
            or any(part in SKIP_DIRS for part in path.parts)
            or relative_path.startswith("assets/starter/")
        ):
            continue
        yield path


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def scan_text(root: Path):
    errors: list[str] = []
    warnings: list[str] = []
    refs: set[str] = set()
    for path in iter_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            warnings.append(f"Unreadable text encoding: {relative(path, root)}")
            continue
        for label, pattern in ERROR_PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{label}: {relative(path, root)}:{line}")
        for label, pattern in WARNING_PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                warnings.append(f"{label}: {relative(path, root)}:{line}")
        for match in ASSET_REF.finditer(text):
            refs.add(match.group(1) or match.group(2))
    return errors, warnings, refs


def check_assets(root: Path, refs: set[str]):
    errors: list[str] = []
    for reference in sorted(refs):
        relative_reference = reference.lstrip("/")
        candidates = (root / "public" / relative_reference, root / relative_reference)
        if not any(candidate.is_file() for candidate in candidates):
            errors.append(f"Missing referenced asset: {reference}")
    return errors


def find_duplicate_images(root: Path):
    by_hash: dict[str, list[str]] = {}
    image_roots = [
        candidate
        for candidate in (
            root / "public" / "images",
            root / "src" / "assets" / "images",
            root / "assets" / "images",
        )
        if candidate.is_dir()
    ]
    candidates = (
        (path for image_root in image_roots for path in image_root.rglob("*"))
        if image_roots
        else iter_files(root)
    )
    for path in candidates:
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        by_hash.setdefault(digest, []).append(relative(path, root))
    return [paths for paths in by_hash.values() if len(paths) > 1]


def check_release(root: Path):
    errors: list[str] = []
    warnings: list[str] = []
    release = root / "dist" if (root / "dist").is_dir() else root
    label = "dist/" if release.name == "dist" else "project root"
    index_path = release / "index.html"
    if not index_path.is_file():
        errors.append(f"Release entry missing from {label}")
    manifest_path = next(
        (release / name for name in ("manifest.webmanifest", "manifest.json") if (release / name).is_file()),
        None,
    )
    if manifest_path is None:
        errors.append(f"PWA manifest missing from {label}")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            errors.append(f"Invalid PWA manifest JSON in {label}")
        else:
            for field in ("start_url", "scope", "display", "icons"):
                if not manifest.get(field):
                    errors.append(f"PWA manifest missing {field} in {label}")
            if manifest.get("display") not in {"standalone", "fullscreen", "minimal-ui"}:
                warnings.append(f"PWA display is not install-oriented in {label}")

    worker_path = next(
        (release / name for name in ("sw.js", "service-worker.js") if (release / name).is_file()),
        None,
    )
    if worker_path is None:
        errors.append(f"Service worker missing from {label}")
    else:
        worker = worker_path.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"(?:addAll|precacheAndRoute|APP_SHELL|\bCORE\b)", worker):
            warnings.append(f"No visible precache signal in {relative(worker_path, root)}")
        if "ignoreVary" not in worker and "workbox" not in worker.lower():
            warnings.append(f"Service worker cache matching does not visibly handle Vary headers: {relative(worker_path, root)}")

    if index_path.is_file():
        index = index_path.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<(?:div|main)\s+[^>]*id=["\'](?:root|app)["\'][^>]*>\s*</(?:div|main)>', index):
            warnings.append(f"Entry HTML has an empty framework root and no visible launch shell in {label}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="travel-guide project root")
    parser.add_argument("--release", action="store_true", help="also verify dist output")
    args = parser.parse_args()

    root = args.project.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: project directory not found: {root}", file=sys.stderr)
        return 2

    errors, warnings, refs = scan_text(root)
    errors.extend(check_assets(root, refs))
    for paths in find_duplicate_images(root):
        warnings.append("Duplicate image content: " + ", ".join(paths))
    if args.release:
        release_errors, release_warnings = check_release(root)
        errors.extend(release_errors)
        warnings.extend(release_warnings)

    print(f"Travel guide audit: {root}")
    print(f"Referenced local assets checked: {len(refs)}")
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
