from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_travel_guide.py"


class AuditTravelGuideTests(unittest.TestCase):
    def run_audit(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_clean_release_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "public" / "images").mkdir(parents=True)
            (root / "public" / "images" / "example.png").write_bytes(b"image-one")
            (root / "src").mkdir()
            (root / "src" / "page.tsx").write_text(
                "export const image = '/images/example.png';", encoding="utf-8"
            )
            (root / "dist").mkdir()
            (root / "dist" / "index.html").write_text("<main>Example Trip</main>", encoding="utf-8")
            (root / "dist" / "manifest.webmanifest").write_text(
                '{"start_url":"./","scope":"./","display":"standalone","icons":[{"src":"icon.png"}]}',
                encoding="utf-8",
            )
            (root / "dist" / "sw.js").write_text(
                "const APP_SHELL=[]; caches.match(request,{ignoreVary:true});",
                encoding="utf-8",
            )
            result = self.run_audit(root, "--release")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_private_path_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            private_path = "/Us" + "ers/example/Private/file.png"
            (root / "src" / "data.ts").write_text(private_path, encoding="utf-8")
            result = self.run_audit(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("macOS home path", result.stdout)

    def test_missing_asset_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "page.tsx").write_text(
                "export const image = '/images/missing.webp';", encoding="utf-8"
            )
            result = self.run_audit(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Missing referenced asset", result.stdout)

    def test_duplicate_images_warn_without_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "public" / "images").mkdir(parents=True)
            for name in ("one.jpg", "two.jpg"):
                (root / "public" / "images" / name).write_bytes(b"same-image")
            result = self.run_audit(root)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Duplicate image content", result.stdout)

    def test_release_requires_service_worker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("<main>Example</main>", encoding="utf-8")
            (root / "manifest.webmanifest").write_text(
                '{"start_url":"./","scope":"./","display":"standalone","icons":[{"src":"icon.png"}]}',
                encoding="utf-8",
            )
            result = self.run_audit(root, "--release")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Service worker missing", result.stdout)

    def test_empty_framework_root_warns(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<div id="root"></div>', encoding="utf-8")
            (root / "manifest.webmanifest").write_text(
                '{"start_url":"./","scope":"./","display":"standalone","icons":[{"src":"icon.png"}]}',
                encoding="utf-8",
            )
            (root / "sw.js").write_text(
                "const APP_SHELL=[]; caches.match(request,{ignoreVary:true});",
                encoding="utf-8",
            )
            result = self.run_audit(root, "--release")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("empty framework root", result.stdout)


if __name__ == "__main__":
    unittest.main()
