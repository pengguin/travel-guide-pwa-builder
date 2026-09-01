from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CREATE = ROOT / "scripts" / "create_project.py"
AUDIT = ROOT / "scripts" / "audit_travel_guide.py"
SPEC = importlib.util.spec_from_file_location("travel_guide_builder", CREATE)
BUILDER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BUILDER)


def luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(first: str, second: str) -> float:
    first_luminance, second_luminance = luminance(first), luminance(second)
    return (max(first_luminance, second_luminance) + 0.05) / (min(first_luminance, second_luminance) + 0.05)


class CreateProjectTests(unittest.TestCase):
    def test_theme_text_contrast_meets_aa(self):
        for name, theme in BUILDER.THEMES.items():
            with self.subTest(theme=name, role="primary"):
                self.assertGreaterEqual(contrast(theme["primary"], theme["on_primary"]), 4.5)
            with self.subTest(theme=name, role="secondary"):
                self.assertGreaterEqual(contrast(theme["secondary"], theme["on_secondary"]), 4.5)
            with self.subTest(theme=name, role="body"):
                self.assertGreaterEqual(contrast(theme["paper"], theme["ink"]), 4.5)

    def create(
        self, output: Path, destinations: tuple[str, ...] = ("Stop A", "Stop B"),
        theme: str = "auto",
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable, str(CREATE),
                "--output", str(output),
                "--title", "Example Journey",
                "--short-title", "Journey",
                "--start-date", "2030-01-02",
                "--end-date", "2030-01-05",
                "--origin", "Origin City",
                "--destinations", *destinations,
                "--theme", theme,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_creates_complete_static_pwa(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "guide"
            result = self.create(output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for relative in (
                "index.html", "styles.css", "app.js", "data/trip-data.js",
                "manifest.webmanifest", "service-worker.js", "icons/app-icon.svg",
            ):
                self.assertTrue((output / relative).is_file(), relative)
            index = (output / "index.html").read_text(encoding="utf-8")
            data = (output / "data" / "trip-data.js").read_text(encoding="utf-8")
            styles = (output / "styles.css").read_text(encoding="utf-8")
            manifest = (output / "manifest.webmanifest").read_text(encoding="utf-8")
            self.assertIn("Example Journey", index)
            self.assertIn("Origin City", data)
            self.assertIn("Stop A → Stop B", data)
            self.assertNotIn("__TITLE__", index)
            self.assertNotIn("__THEME_", index + styles + manifest)
            self.assertIn("Theme: heritage (auto)", result.stdout)

    def test_auto_theme_uses_destination_hints(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "guide"
            result = self.create(output, destinations=("Sahara Desert",))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            styles = (output / "styles.css").read_text(encoding="utf-8")
            self.assertIn("--primary: #322d29", styles)
            self.assertIn("Theme: desert (auto)", result.stdout)

    def test_explicit_theme_overrides_destination_hints(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "guide"
            result = self.create(output, destinations=("Sahara Desert",), theme="coast")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            styles = (output / "styles.css").read_text(encoding="utf-8")
            self.assertIn("--primary: #123c50", styles)
            self.assertIn("Theme: coast (selected)", result.stdout)

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "guide"
            output.mkdir()
            result = self.create(output)
            self.assertEqual(result.returncode, 2)
            self.assertIn("refusing to overwrite", result.stderr)

    def test_scaffold_must_be_finalized_before_release(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "guide"
            self.assertEqual(self.create(output).returncode, 0)
            unfinished = subprocess.run(
                [sys.executable, str(AUDIT), str(output), "--release"],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(unfinished.returncode, 1)
            self.assertIn("unfinished scaffold", unfinished.stdout)

            data_path = output / "data" / "trip-data.js"
            scaffold_marker = "__REPLACE_WITH_" + "FINAL_ITINERARY__"
            data_path.write_text(
                data_path.read_text(encoding="utf-8").replace(
                    scaffold_marker, "final"
                ),
                encoding="utf-8",
            )
            complete = subprocess.run(
                [sys.executable, str(AUDIT), str(output), "--release"],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(complete.returncode, 0, complete.stdout + complete.stderr)


if __name__ == "__main__":
    unittest.main()
