import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNNER = SKILL_ROOT / "scripts" / "run_checks.py"
CHECKLIST = SKILL_ROOT / "references" / "code-review-checklist.md"
SKILL_MARKDOWN = SKILL_ROOT / "SKILL.md"


class SoftwareMarketComplianceSkillTests(unittest.TestCase):
    def write_project(self, root: Path, files: dict[str, str]) -> None:
        for relative_path, content in files.items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def run_json(self, root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--project-root",
                str(root),
                "--format",
                "json",
                *extra,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def report(self, result: subprocess.CompletedProcess[str]) -> dict:
        self.assertTrue(result.stdout, result.stderr)
        return json.loads(result.stdout)

    def findings(self, report: dict, status: str) -> list[dict]:
        return [item for item in report["findings"] if item["status"] == status]

    def test_help_is_available(self) -> None:
        result = subprocess.run(
            [sys.executable, str(RUNNER), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode)
        self.assertIn("--markets", result.stdout)

    def test_unknown_market_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_json(Path(temp_dir), "--markets", "mars")
        self.assertEqual(2, result.returncode)
        self.assertIn("unknown market", result.stderr)

    def test_markets_are_read_from_minimal_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_project(root, {"compliance-input.yaml": "markets:\n  - us\n"})
            result = self.run_json(root)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["us"], self.report(result)["markets"])

    def test_country_region_name_is_candidate_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_project(root, {"locales/en.json": '{"label":"Taiwan"}\n'})
            result = self.run_json(root, "--markets", "cn-mainland")
        report = self.report(result)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(any(item["id"] == "NAME-REVIEW-TAIWAN" for item in self.findings(report, "candidate")))
        self.assertNotIn("confirmed_violation", report["summary"])

    def test_plain_json_location_field_conflict_is_generic_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_project(
                root,
                {"location-field-candidate.json": '{"releaseStatus":"submitted", "locationCollected":false, "locationShared":true}\n'},
            )
            result = self.run_json(root, "--markets", "us")
        report = self.report(result)
        self.assertEqual(0, result.returncode, result.stderr)
        finding = next(item for item in report["findings"] if item["id"] == "REG-PRIVACY-METADATA-CANDIDATE")
        self.assertEqual("candidate", finding["status"])
        self.assertNotIn("confirmed_violation", report["summary"])

    def test_location_code_and_notice_are_candidates_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_project(
                root,
                {
                    "privacy.md": "We do not collect precise location.\n",
                    "src/location.js": "navigator.geolocation.getCurrentPosition(onSuccess);\nfetch('/telemetry', {body: JSON.stringify({location: position.coords})});\n",
                },
            )
            result = self.run_json(root, "--markets", "us")
        report = self.report(result)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(any(item["id"] == "REG-PRIVACY-LOCATION-CANDIDATE" for item in self.findings(report, "candidate")))
        self.assertFalse(self.findings(report, "candidate")[0]["status"] == "confirmed_violation")

    def test_map_signals_are_candidates_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_project(
                root,
                {"src/map.ts": "import mapboxgl from 'mapbox-gl';\nconst source = 'WGS-84';\nconst map = mapboxgl.Map;\n"},
            )
            result = self.run_json(root, "--markets", "cn-mainland")
        report = self.report(result)
        self.assertEqual(0, result.returncode, result.stderr)
        candidates = self.findings(report, "candidate")
        self.assertTrue(any(item["id"] == "MAP-ATTRIBUTION-VERIFY" for item in candidates))
        self.assertTrue(any(item["id"] == "MAP-COORDINATE-REVIEW" for item in candidates))
        self.assertTrue(any(item["id"] == "CN-MAP-PUBLIC-REVIEW" for item in candidates))
        self.assertNotIn("confirmed_violation", report["summary"])

    def test_plain_json_age_rating_and_content_flags_are_generic_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_project(
                root,
                {
                    "store-metadata.json": '{"ageRating":"everyone", "containsAdultContent":true}\n',
                    "src/audience.ts": "export const audience = 'children';\n",
                },
            )
            result = self.run_json(root, "--markets", "us", "eu")
        report = self.report(result)
        self.assertEqual(0, result.returncode, result.stderr)
        candidates = self.findings(report, "candidate")
        self.assertTrue(any(item["id"] == "AGE-STORE-RATING-CANDIDATE" for item in candidates))
        self.assertEqual({"us", "eu"}, {item["market"] for item in candidates if item["id"] == "AGE-CHILD-SIGNAL"})
        self.assertNotIn("confirmed_violation", report["summary"])

    def test_empty_project_reports_all_domains_as_no_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_json(Path(temp_dir), "--markets", "cn-mainland")
        report = self.report(result)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"candidate": 0, "not_detected": 4, "scan_incomplete": 0}, report["summary"])
        self.assertEqual({"naming", "regulation", "maps", "age"}, {item["domain"] for item in self.findings(report, "not_detected")})

    def test_missing_market_input_is_scan_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_json(Path(temp_dir))
        report = self.report(result)
        self.assertEqual(2, result.returncode)
        self.assertEqual("scan_incomplete", report["findings"][0]["status"])

    def test_candidate_scan_output_and_model_checklist_are_reported_separately(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = root / "report.md"
            self.write_project(root, {"locales/en.json": '{"label":"Taiwan"}\n'})
            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--project-root",
                    str(root),
                    "--markets",
                    "cn-mainland",
                    "--format",
                    "both",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            markdown = output.read_text(encoding="utf-8")
            report = json.loads(output.with_suffix(".json").read_text(encoding="utf-8"))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Candidate Scan", markdown)
        self.assertIn("not a compliance decision", markdown)
        self.assertIn("NAME-REVIEW-TAIWAN", markdown)
        self.assertEqual(1, report["summary"]["candidate"])
        self.assertNotIn("confirmed_violation", report["summary"])
        self.assertTrue(report["sources"])

    def test_skill_requires_model_checklist_even_without_scanner_matches(self) -> None:
        skill = SKILL_MARKDOWN.read_text(encoding="utf-8")
        checklist = CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("Track 2: 模型代码审查", skill)
        self.assertIn("即使脚本没有命中也要完成", skill)
        for domain in ("Country and region naming", "Legal and regulatory triggers", "Maps and geospatial information", "Age, children, and age ratings"):
            self.assertIn(domain, checklist)
        for status in ("confirmed_issue", "candidate", "not_found", "not_reviewable"):
            self.assertIn(status, checklist)


if __name__ == "__main__":
    unittest.main()
