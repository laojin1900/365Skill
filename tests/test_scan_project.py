import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY / "skills" / "discover-project-skills" / "scripts" / "scan_project.py"


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_project", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ScanProjectTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "skills" / "sample-skill").mkdir(parents=True)
        (self.root / "scripts").mkdir()
        (self.root / "node_modules" / "ignored").mkdir(parents=True)
        (self.root / "AGENTS.md").write_text("Follow project rules.\n", encoding="utf-8")
        (self.root / "skills" / "sample-skill" / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: Use when testing sample repositories.\n---\n",
            encoding="utf-8",
        )
        (self.root / "scripts" / "deploy-check.py").write_text("print('ok')\n", encoding="utf-8")
        (self.root / "package.json").write_text(
            json.dumps({"name": "fixture", "scripts": {"test": "python -m unittest"}}),
            encoding="utf-8",
        )
        (self.root / ".env.local").write_text("SENSITIVE_VALUE=redacted-fixture\n", encoding="utf-8")
        (self.root / "node_modules" / "ignored" / "SKILL.md").write_text(
            "---\nname: ignored\ndescription: ignored\n---\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temporary.cleanup()

    def test_inventory_finds_skills_and_excludes_sensitive_content(self):
        scanner = load_scanner()
        inventory = scanner.collect_inventory(self.root, git_history=0)
        serialized = json.dumps(inventory)

        self.assertEqual(["sample-skill"], [item["name"] for item in inventory["existing_skills"]])
        self.assertIn("AGENTS.md", inventory["agent_instructions"])
        self.assertIn("scripts/deploy-check.py", inventory["scripts"])
        self.assertNotIn("redacted-fixture", serialized)
        self.assertNotIn(".env.local", serialized)
        self.assertNotIn("node_modules", serialized)

    def test_package_scripts_are_collected(self):
        scanner = load_scanner()
        inventory = scanner.collect_inventory(self.root, git_history=0)
        package = inventory["files"]["package_json"][0]

        self.assertEqual("fixture", package["name"])
        self.assertEqual("python -m unittest", package["scripts"]["test"])

    def test_cli_emits_valid_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), "--git-history", "0"],
            check=True,
            capture_output=True,
            text=True,
        )
        inventory = json.loads(result.stdout)
        self.assertEqual(str(self.root.resolve()), inventory["root"])


if __name__ == "__main__":
    unittest.main()
