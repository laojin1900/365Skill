import json
import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
PUBLIC_CORE_SKILLS = (
    "365-chatgpt-pro-delivery",
    "365-five-step-dev",
    "365-session-rotation-maintainer",
)
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "laojin1900",
    "365nails",
    "ops-center",
    "Project Controller",
    "chatgpt-pro-delivery/SKILL.md",
    "session-rotation-maintainer/SKILL.md",
)
THREAD_ID = re.compile(r"\b019f[0-9a-f-]{20,}\b", re.IGNORECASE)
REQUIRED_TRIGGER_BOUNDARIES = {
    "365-five-step-dev": (
        ("发布授权流程", True),
        ("完成这个普通本地功能", False),
        ("普通修复提交", False),
        ("编写迁移文件", False),
    ),
    "365-chatgpt-pro-delivery": (
        ("review this local diff", True),
        ("本地 TypeScript", False),
    ),
    "365-session-rotation-maintainer": (
        ("rotate this long-running Codex task", True),
        ("Archive this completed Codex task", False),
    ),
}


class PublicCoreSkillTests(unittest.TestCase):
    def test_packages_are_self_contained_and_portable(self):
        for skill_id in PUBLIC_CORE_SKILLS:
            with self.subTest(skill=skill_id):
                root = REPOSITORY / "skills" / skill_id
                skill = root / "SKILL.md"
                agent = root / "agents" / "openai.yaml"
                self.assertTrue(skill.is_file())
                self.assertTrue(agent.is_file())

                text = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in root.rglob("*")
                    if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".json"}
                )
                self.assertIn(f"name: {skill_id}", skill.read_text(encoding="utf-8"))
                self.assertIn(f"${skill_id}", agent.read_text(encoding="utf-8"))
                self.assertLessEqual(len(skill.read_text(encoding="utf-8").splitlines()), 500)
                for forbidden in FORBIDDEN_PUBLIC_TEXT:
                    self.assertNotIn(forbidden, text)
                self.assertIsNone(THREAD_ID.search(text))

    def test_trigger_evaluations_are_bilingual_and_balanced(self):
        for skill_id in PUBLIC_CORE_SKILLS:
            with self.subTest(skill=skill_id):
                path = REPOSITORY / "evals" / skill_id / "trigger-cases.json"
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                self.assertIn('"should_trigger": true', text)
                self.assertIn('"should_trigger": false', text)
                self.assertRegex(text, r"[\u4e00-\u9fff]")
                self.assertRegex(text, r"[A-Za-z]{4,}")

    def test_important_trigger_boundaries_do_not_regress(self):
        for skill_id, boundaries in REQUIRED_TRIGGER_BOUNDARIES.items():
            cases = json.loads(
                (REPOSITORY / "evals" / skill_id / "trigger-cases.json").read_text(
                    encoding="utf-8"
                )
            )
            for needle, expected in boundaries:
                with self.subTest(skill=skill_id, query=needle):
                    matches = [case for case in cases if needle in case["query"]]
                    self.assertEqual(len(matches), 1)
                    self.assertIs(matches[0]["should_trigger"], expected)


if __name__ == "__main__":
    unittest.main()
