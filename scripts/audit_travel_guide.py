#!/usr/bin/env python3
"""Privacy and release audit for a static travel-guide project."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".js", ".json", ".jsx", ".md", ".mjs",
    ".svg", ".toml", ".ts", ".tsx", ".txt", ".yaml", ".yml",
}
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
SKIP_DIRS = {".git", ".vite", "coverage", "node_modules"}

ERROR_PATTERNS = {
    "macOS home path": re.compile(r"/Users/[^/\s'\"<>]+/"),
    "Windows home path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s'\"<>]+\\"),
    "file URL": re.compile(r"file://[^\s'\"<>]+"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "common secret assignment": re.compile(
        r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"
    ),
}
WARNING_PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "placeholder": re.compile(r"\b(?:TODO|FIXME|CHANGEME)\b"),
    "local host URL": re.compile(r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?"),
}
ASSET_REF = re.compile(
    r"(?:src|href)\s*=\s*['\"](/(?:images|icons)/[^'\"?#]+)['\"]|"
    r"['\"](/(?:images|icons)/[^'\"?#]+)['\"]"
)


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
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
        candidate = root / "public" / reference.lstrip("/")
        if not candidate.is_file():
            errors.append(f"Missing referenced asset: {reference}")
    return errors


def find_duplicate_images(root: Path):
    by_hash: dict[str, list[str]] = {}
    for path in iter_files(root):
        if path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        by_hash.setdefault(digest, []).append(relative(path, root))
    return [paths for paths in by_hash.values() if len(paths) > 1]


def check_release(root: Path):
    errors: list[str] = []
    dist = root / "dist"
    if not dist.is_dir():
        return ["Release directory missing: dist/"]
    if not (dist / "index.html").is_file():
        errors.append("Release entry missing: dist/index.html")
    if not any((dist / name).is_file() for name in ("manifest.webmanifest", "manifest.json")):
        errors.append("PWA manifest missing from dist/")
    return errors


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
        errors.extend(check_release(root))

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
