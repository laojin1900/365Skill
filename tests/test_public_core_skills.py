import json
import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
PUBLIC_CORE_SKILLS = (
    "365-chatgpt-pro-delivery",
    "365-five-step-dev-codex",
    "365-session-rotation-maintainer",
)
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "laojin1900",
    "365nails",
    "ops-center",
    "Project Controller",
    "MODULE_CONTEXT_V1",
    "Registry/Binding",
    "chatgpt-pro-delivery/SKILL.md",
    "session-rotation-maintainer/SKILL.md",
)
THREAD_ID = re.compile(r"\b019f[0-9a-f-]{20,}\b", re.IGNORECASE)
REQUIRED_TRIGGER_BOUNDARIES = {
    "365-five-step-dev-codex": (
        ("365五步法（Codex版）", True),
        ("$365-five-step-dev-codex", True),
        ("365五步法（Claude版）", False),
        ("发布授权流程", True),
        ("完成这个普通本地功能", False),
        ("普通修复提交", False),
        ("编写迁移文件", False),
        ("already-approved permission check", False),
        ("生产环境切换支付回调", True),
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
                if skill_id == "365-five-step-dev-codex":
                    self.assertLessEqual(
                        len(skill.read_text(encoding="utf-8").splitlines()), 220
                    )
                    self.assertIn("allow_implicit_invocation: true", agent.read_text(encoding="utf-8"))
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

    def test_five_step_regression_metrics_are_bounded(self):
        path = REPOSITORY / "evals" / "365-five-step-dev-codex" / "regression-cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        metrics = [case["metric"] for case in cases]
        self.assertEqual(len(metrics), 6)
        self.assertEqual(len(metrics), len(set(metrics)))
        self.assertTrue(all(case["target"] == 0 for case in cases))

    def test_five_step_catalog_version_is_v05(self):
        catalog = (REPOSITORY / "catalog" / "skills.yaml").read_text(encoding="utf-8")
        entry = catalog.split("  - id: 365-five-step-dev-codex", 1)[1].split("\n  - id:", 1)[0]
        self.assertIn("version: 0.5.0", entry)
        self.assertIn("title_zh_cn: 365五步法（Codex版）", entry)
        self.assertIn("default_behavior: proportional-business-governance", entry)

    def test_five_step_conditional_references_are_direct_and_present(self):
        root = REPOSITORY / "skills" / "365-five-step-dev-codex"
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        links = set(re.findall(r"\]\((references/[^)]+)\)", text))
        self.assertEqual(len(links), 6)
        for link in links:
            with self.subTest(reference=link):
                self.assertTrue((root / link).is_file())


if __name__ == "__main__":
    unittest.main()
