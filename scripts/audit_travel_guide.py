#!/usr/bin/env python3
"""Public-content and release-structure audit for static and Sites/Vinext travel guides."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from urllib.parse import unquote, urlsplit
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


def check_assets(root: Path, refs: set[str], deployed: bool = False):
    errors: list[str] = []
    for reference in sorted(refs):
        relative_reference = reference.lstrip("/")
        candidates = (root / relative_reference,) if deployed else (root / "public" / relative_reference, root / relative_reference)
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


def resolve_release(root: Path, public_dir: str | None = None):
    """Return the public deploy directory and optional required Worker entry."""
    if public_dir:
        public = (root / public_dir).resolve()
        if not public.is_relative_to(root):
            raise ValueError("Public output must stay inside the selected project")
        if not public.is_dir():
            raise ValueError("Selected public output does not exist")
        return public, None
    hosting = root / ".openai" / "hosting.json"
    if hosting.is_file():
        try:
            config = json.loads(hosting.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ValueError("Invalid hosting metadata JSON") from None
        if not isinstance(config, dict):
            raise ValueError("Invalid hosting metadata object")
        static = config.get("static")
        if isinstance(static, dict) and isinstance(static.get("directory"), str):
            return resolve_release(root, static["directory"])
    if (root / "dist" / "client").is_dir():
        return root / "dist" / "client", root / "dist" / "server" / "index.js"
    if (root / "client").is_dir():
        return root / "client", root / "server" / "index.js"
    return (root / "dist" if (root / "dist").is_dir() else root), None


def local_asset(root: Path, value: str):
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    url = urlsplit(value)
    if url.scheme or url.netloc or url.query or url.fragment:
        return None
    decoded = unquote(url.path).lstrip("/")
    if ".." in Path(decoded).parts:
        return None
    candidate = (root / decoded).resolve()
    return candidate if candidate.is_relative_to(root.resolve()) else None


def check_integrity(release: Path):
    path = release / "precache-manifest.json"
    if not path.is_file():
        return [], []  # A different worker may own its own explicit list.
    errors = []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return ["Invalid precache manifest JSON"], []
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list) or not isinstance(manifest.get("integrity"), dict):
        return ["Precache manifest must contain files and integrity"], []
    seen = set()
    for name in manifest["files"]:
        candidate = local_asset(release, name)
        if candidate is None:
            errors.append("Unsafe precache path")
            continue
        if name in seen:
            errors.append("Duplicate precache entry")
        seen.add(name)
        if not candidate.is_file():
            errors.append(f"Missing precache asset: {name}")
            continue
        digest = manifest["integrity"].get(name)
        if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            errors.append(f"Missing or invalid SHA-256: {name}")
        elif hashlib.sha256(candidate.read_bytes()).hexdigest() != digest:
            errors.append(f"Integrity mismatch: {name}")
    if not manifest["files"]:
        errors.append("Empty precache manifest")
    return errors, []


def check_release(root: Path, public_dir: str | None = None):
    errors: list[str] = []
    warnings: list[str] = []
    try:
        release, worker_entry = resolve_release(root, public_dir)
    except ValueError as error:
        return [str(error)], []
    label = relative(release, root) or "project root"
    if worker_entry is not None and not worker_entry.is_file():
        errors.append("Sites/Vinext Worker entry missing: " + relative(worker_entry, root))
    index_path = release / "index.html"
    if not index_path.is_file():
        if worker_entry is not None and worker_entry.is_file():
            warnings.append("Server-rendered entry: verify public HTML and offline launch through the deployed Worker")
        else:
            errors.append(f"Release entry missing from {label}")
    manifest_path = next((release / name for name in ("manifest.webmanifest", "manifest.json") if (release / name).is_file()), None)
    if manifest_path is None:
        errors.append(f"PWA manifest missing from {label}")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            manifest = None
        if not isinstance(manifest, dict):
            errors.append(f"Invalid PWA manifest JSON object in {label}")
        else:
            for field in ("start_url", "scope", "display", "icons"):
                if not manifest.get(field):
                    errors.append(f"PWA manifest missing {field} in {label}")
            if manifest.get("display") not in {"standalone", "fullscreen", "minimal-ui"}:
                warnings.append(f"PWA display is not install-oriented in {label}")
            icons = manifest.get("icons", [])
            if not isinstance(icons, list):
                errors.append("Invalid PWA manifest icons")
                icons = []
            for icon in icons:
                value = icon.get("src") if isinstance(icon, dict) else None
                candidate = local_asset(release, value)
                if candidate is None or not candidate.is_file():
                    errors.append("Missing or non-local manifest icon")
    worker_path = next((release / name for name in ("sw.js", "service-worker.js") if (release / name).is_file()), None)
    if worker_path is None:
        errors.append(f"Service worker missing from {label}")
    else:
        worker = worker_path.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"(?:addAll|precacheAndRoute|APP_SHELL|precache-manifest|\bCORE\b)", worker):
            warnings.append(f"No visible precache signal in {relative(worker_path, root)}")
        if "ignoreVary" not in worker and "workbox" not in worker.lower():
            warnings.append(f"Review public cache Vary behavior: {relative(worker_path, root)}")
    if index_path.is_file():
        index = index_path.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<(?:div|main)\s+[^>]*id=["\'](?:root|app)["\'][^>]*>\s*</(?:div|main)>', index):
            warnings.append(f"Entry HTML has an empty framework root and no visible launch shell in {label}")
    integrity_errors, integrity_warnings = check_integrity(release)
    return errors + integrity_errors, warnings + integrity_warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="travel-guide project root")
    parser.add_argument("--release", action="store_true", help="audit deployed public output and verify release structure")
    parser.add_argument("--public-dir", help="relative public output directory for a nonstandard layout; requires --release")
    parser.add_argument("--source", action="store_true", help="also scan the selected source tree; separate from public-release privacy")
    args = parser.parse_args()
    if args.public_dir and not args.release:
        parser.error("--public-dir requires --release")

    root = args.project.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: project directory not found: {root}", file=sys.stderr)
        return 2

    try:
        scan_root = resolve_release(root, args.public_dir)[0] if args.release and not args.source else root
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1
    errors, warnings, refs = scan_text(scan_root)
    errors.extend(check_assets(scan_root, refs, deployed=args.release and not args.source))
    for paths in find_duplicate_images(scan_root):
        warnings.append("Duplicate image content: " + ", ".join(paths))
    if args.release:
        release_errors, release_warnings = check_release(root, args.public_dir)
        errors.extend(release_errors)
        warnings.extend(release_warnings)
    print("Scope: " + ("source tree" if scan_root == root and args.source else "deployed public output" if args.release else "source tree"))
    print("Coverage: heuristic text/asset/layout checks; not authorization, browser or physical-device proof")

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
