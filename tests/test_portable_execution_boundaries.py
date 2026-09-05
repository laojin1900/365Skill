"""Regression guards for portable instructions; not a live execution/behavior claim."""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = (
    "365-chatgpt-pro-delivery",
    "365-session-rotation-maintainer",
    "project-health-check",
    "shopify-theme-delivery",
)


def skill(name):
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


class PortableExecutionBoundaries(unittest.TestCase):
    def test_theme_contracts_run_through_existing_repository_gate(self):
        # The mirror's existing credential can publish skills, not workflow edits.
        # Keep its workflow unchanged and run package tests from the Python gate
        # already used by both source validation and public export.
        scripts = sorted((ROOT / "skills" / "shopify-theme-delivery" / "scripts").glob("*.test.mjs"))
        self.assertTrue(scripts)
        result = subprocess.run(
            ["node", "--test", *map(str, scripts)], cwd=ROOT,
            capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_updated_entries_have_no_host_or_project_private_contracts(self):
        for name in PACKAGES:
            with self.subTest(package=name):
                text = skill(name)
                for forbidden in ("/Users/", "365nails", "MODULE_CONTEXT_V1", "Registry/Binding"):
                    self.assertNotIn(forbidden, text)
                self.assertLess(len(text.splitlines()), 500)
                for link in re.findall(r"\]\((references/[^)]+)\)", text):
                    self.assertTrue((ROOT / "skills" / name / link).is_file())

    def test_rotation_chooses_one_contract_and_reuses_evidence(self):
        text = skill("365-session-rotation-maintainer")
        for required in ("Select one implementation", "advertised but unreadable",
                         "Never switch an in-flight rotation", "unchanged verified evidence",
                         "preserving its", "cursor", "Create at most one successor"):
            self.assertIn(required, text)

    def test_rotation_audit_fallback_does_not_silently_write(self):
        text = skill("365-session-rotation-maintainer")
        self.assertIn("without writing files or changing tasks", text)
        self.assertIn("checkpoint only when the requested boundary separately includes that local write", text)
        self.assertIn("complete owner-facing kickoff is visible in its final answer", text)

    def test_pro_payload_is_capacity_based_not_complexity_based(self):
        text = skill("365-chatgpt-pro-delivery")
        for required in ("observed channel capacity and fidelity", "do not mandate an attachment",
                         "Never truncate", "current callable browser API", "verify the complete payload"):
            self.assertIn(required, text)

    def test_pro_retry_stays_in_same_conversation_without_duplicate_send(self):
        text = skill("365-chatgpt-pro-delivery")
        for required in ("After one attachment upload failure", "confirmed unsent",
                         "marker is already present", "do not resend", "same tab"):
            self.assertIn(required, text)
        self.assertIn("Never send the same", text)
        self.assertIn("minimum sanitized context", text)
        self.assertIn("manual dispatch only when the original is confirmed unsent", text)
        self.assertIn("recovery, not instructions to resend", text)
        self.assertNotIn("stop with the exact transport state and give the user", text)

    def test_health_scope_and_identity_are_bounded(self):
        text = skill("project-health-check")
        for required in ("不默认递归扫描", "common directory", "独立克隆仍分别",
                         "提交日期不等于任务活动时间", "缓存 ref 不是远端实时证明",
                         "NOT_CHECKED", "不盲跑 package script"):
            self.assertIn(required, text)
        self.assertNotIn('find "$HOME"', text)

    def test_health_findings_are_not_authority_or_mandatory_new_tasks(self):
        text = skill("project-health-check")
        self.assertIn("发现问题不等于获得修复授权", text)
        self.assertIn("普通修复不强制五步法、另建任务或重复确认", text)
        self.assertIn("不叠加本技能的第二套流程", text)


if __name__ == "__main__":
    unittest.main()
