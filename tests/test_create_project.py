from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CREATE = ROOT / "scripts" / "create_project.py"
AUDIT = ROOT / "scripts" / "audit_travel_guide.py"


class CreateProjectTests(unittest.TestCase):
    def create(self, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable, str(CREATE),
                "--output", str(output),
                "--title", "Example Journey",
                "--short-title", "Journey",
                "--start-date", "2030-01-02",
                "--end-date", "2030-01-05",
                "--origin", "Origin City",
                "--destinations", "Stop A", "Stop B",
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
            self.assertIn("Example Journey", index)
            self.assertIn("Origin City", data)
            self.assertIn("Stop A → Stop B", data)
            self.assertNotIn("__TITLE__", index)

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
