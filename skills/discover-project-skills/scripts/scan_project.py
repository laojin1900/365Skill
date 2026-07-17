#!/usr/bin/env python3
"""Build a secret-aware structural inventory for project-skill discovery."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".codegraph",
    ".next",
    ".nuxt",
    ".output",
    ".playwright-cli",
    ".playwright-mcp",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".worktrees",
    "$codex_home",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "logs",
    "node_modules",
    "out",
    "output",
    "secrets",
    "target",
    "tmp",
    "vendor",
    "venv",
}

ALLOWED_HIDDEN_DIRS = {
    ".agent",
    ".agents",
    ".claude",
    ".codex",
    ".cursor",
    ".gemini",
    ".github",
    ".windsurf",
}

SENSITIVE_DIRS = {".aws", ".azure", ".gcp", ".ssh", "credentials", "secrets"}
SENSITIVE_NAMES = {
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "id_dsa",
    "id_ed25519",
    "id_rsa",
}
SENSITIVE_SUFFIXES = {".key", ".p12", ".pem", ".pfx"}

MANIFEST_NAMES = {
    "Cargo.toml",
    "Gemfile",
    "go.mod",
    "package.json",
    "pnpm-workspace.yaml",
    "pyproject.toml",
    "requirements.txt",
}

ROOT_INSTRUCTION_NAMES = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "PROJECT_CONTROLLER.md",
}

AUTOMATION_NAMES = {
    "Dockerfile",
    "Justfile",
    "Makefile",
    "Taskfile.yml",
    "Taskfile.yaml",
    "compose.yaml",
    "docker-compose.yml",
}

EVIDENCE_TERMS = re.compile(
    r"(?:audit|checklist|controller|deploy|guide|governance|migration|ops|playbook|"
    r"policy|process|report|review|runbook|template|training|workflow)",
    re.IGNORECASE,
)

GENERIC_EVIDENCE_TOKENS = {
    "approval",
    "batch",
    "completion",
    "current",
    "final",
    "governance",
    "hardening",
    "implement",
    "implementation",
    "live",
    "mvp",
    "owner",
    "phase",
    "plan",
    "readiness",
    "record",
    "review",
    "source",
}

LANGUAGE_BY_SUFFIX = {
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
    ".css": "CSS",
    ".go": "Go",
    ".html": "HTML",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".kt": "Kotlin",
    ".lua": "Lua",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scss": "SCSS",
    ".sh": "Shell",
    ".sql": "SQL",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".vue": "Vue",
}


def run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return subprocess.CompletedProcess(
            args=["git", "-C", str(root), *args],
            returncode=127,
            stdout="",
            stderr=str(error),
        )


def git_root(root: Path) -> Path | None:
    result = run_git(root, ["rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def is_sensitive(relative: Path) -> bool:
    lowered_parts = {part.lower() for part in relative.parts}
    name = relative.name.lower()
    if lowered_parts & SENSITIVE_DIRS:
        return True
    if name.startswith(".env") or name in SENSITIVE_NAMES:
        return True
    if relative.suffix.lower() in SENSITIVE_SUFFIXES:
        return True
    return False


def is_excluded(relative: Path) -> bool:
    for part in relative.parts[:-1]:
        lowered = part.lower()
        if lowered in EXCLUDED_DIRS:
            return True
        if part.startswith(".") and part not in ALLOWED_HIDDEN_DIRS:
            return True
    return is_sensitive(relative)


def collect_git_files(root: Path, repository_root: Path) -> list[Path]:
    result = run_git(root, ["ls-files", "--cached", "--others", "--exclude-standard", "-z"])
    if result.returncode != 0:
        return []
    collected: list[Path] = []
    for item in result.stdout.split("\0"):
        if not item:
            continue
        absolute = (repository_root / item).resolve()
        try:
            relative = absolute.relative_to(root)
        except ValueError:
            continue
        if absolute.is_file() and not is_excluded(relative):
            collected.append(relative)
    return collected


def collect_walk_files(root: Path) -> list[Path]:
    collected: list[Path] = []
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        current_relative = current_path.relative_to(root)
        kept_directories: list[str] = []
        for directory in directories:
            candidate = current_relative / directory
            lowered = directory.lower()
            if lowered in EXCLUDED_DIRS:
                continue
            if directory.startswith(".") and directory not in ALLOWED_HIDDEN_DIRS:
                continue
            if is_sensitive(candidate / "placeholder"):
                continue
            kept_directories.append(directory)
        directories[:] = kept_directories
        for filename in files:
            relative = current_relative / filename
            if not is_excluded(relative):
                collected.append(relative)
    return collected


def collect_files(root: Path, maximum: int) -> tuple[list[Path], bool, Path | None]:
    repository_root = git_root(root)
    files = collect_git_files(root, repository_root) if repository_root else collect_walk_files(root)
    unique = sorted(set(files), key=lambda item: item.as_posix().lower())
    truncated = len(unique) > maximum
    return unique[:maximum], truncated, repository_root


def read_text(path: Path, limit: int = 131_072) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return handle.read(limit)
    except (OSError, UnicodeError):
        return ""


def strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_skill(root: Path, relative: Path) -> dict[str, Any]:
    text = read_text(root / relative)
    name = ""
    description = ""
    valid_frontmatter = False
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            valid_frontmatter = True
            for line in parts[1].splitlines():
                match = re.match(r"^(name|description)\s*:\s*(.+?)\s*$", line)
                if not match:
                    continue
                key, value = match.groups()
                if key == "name":
                    name = strip_yaml_scalar(value)
                else:
                    description = strip_yaml_scalar(value)
    return {
        "path": relative.as_posix(),
        "name": name,
        "description": description,
        "valid_frontmatter": valid_frontmatter and bool(name and description),
    }


def parse_package_json(root: Path, relative: Path) -> dict[str, Any]:
    try:
        data = json.loads(read_text(root / relative, 1_048_576))
    except (json.JSONDecodeError, OSError):
        return {"path": relative.as_posix(), "parse_error": True}
    scripts = data.get("scripts") if isinstance(data, dict) else None
    return {
        "path": relative.as_posix(),
        "name": data.get("name", "") if isinstance(data, dict) else "",
        "scripts": dict(sorted(scripts.items())) if isinstance(scripts, dict) else {},
    }


def is_instruction_file(relative: Path) -> bool:
    path = relative.as_posix()
    if relative.name in ROOT_INSTRUCTION_NAMES:
        return True
    if path == ".github/copilot-instructions.md":
        return True
    return path.startswith((".cursor/rules/", ".windsurf/rules/"))


def is_documentation(relative: Path) -> bool:
    path = relative.as_posix()
    if relative.name == "SKILL.md":
        return False
    if relative.suffix.lower() not in {".md", ".mdx", ".rst", ".txt"}:
        return False
    return len(relative.parts) == 1 or path.startswith(("docs/", "documentation/"))


def is_script(relative: Path) -> bool:
    if any(part.lower() in {"bin", "scripts", "tools"} for part in relative.parts[:-1]):
        return True
    return len(relative.parts) == 1 and relative.suffix.lower() in {".bash", ".py", ".sh"}


def is_skill_resource(relative: Path) -> bool:
    parts = [part.lower() for part in relative.parts]
    if "skills" not in parts or "scripts" not in parts:
        return False
    return parts.index("skills") < parts.index("scripts")


def is_skill_package_path(relative: Path) -> bool:
    parts = [part.lower() for part in relative.parts]
    return "skills" in parts and parts.index("skills") < len(parts) - 1


def is_automation(relative: Path) -> bool:
    path = relative.as_posix()
    return relative.name in AUTOMATION_NAMES or path.startswith(".github/workflows/")


def recent_git_history(root: Path, count: int) -> list[str]:
    if count <= 0 or git_root(root) is None:
        return []
    result = run_git(root, ["log", f"-n{count}", "--pretty=format:%s"])
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def current_branch(root: Path) -> str:
    result = run_git(root, ["branch", "--show-current"])
    return result.stdout.strip() if result.returncode == 0 else ""


def limited(items: Iterable[Path], maximum: int = 200) -> list[str]:
    return [item.as_posix() for item in list(items)[:maximum]]


def evidence_clusters(paths: Iterable[Path], maximum: int = 30) -> list[dict[str, Any]]:
    clusters: dict[str, list[Path]] = {}
    for path in paths:
        tokens = [
            token.lower()
            for token in re.findall(r"[A-Za-z]+", path.stem)
            if token.lower() not in GENERIC_EVIDENCE_TOKENS and len(token) > 1
        ]
        if not tokens:
            continue
        scope = path.parts[0] if len(path.parts) > 1 else "root"
        key = f"{scope}:{'-'.join(tokens[:4])}"
        clusters.setdefault(key, []).append(path)

    ranked = sorted(clusters.items(), key=lambda item: (-len(item[1]), item[0].lower()))
    return [
        {
            "topic": topic,
            "count": len(examples),
            "examples": limited(sorted(examples, key=lambda item: item.as_posix().lower()), 3),
        }
        for topic, examples in ranked[:maximum]
        if len(examples) >= 2
    ]


def collect_inventory(root: Path, maximum: int = 50_000, git_history: int = 20) -> dict[str, Any]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Repository root is not a directory: {root}")

    files, truncated, repository_root = collect_files(root, maximum)
    skills = [parse_skill(root, path) for path in files if path.name == "SKILL.md"]
    manifests = [path for path in files if path.name in MANIFEST_NAMES]
    package_json = [parse_package_json(root, path) for path in manifests if path.name == "package.json"]
    instructions = [path for path in files if is_instruction_file(path)]
    documentation = [path for path in files if is_documentation(path)]
    all_scripts = [path for path in files if is_script(path)]
    skill_resource_scripts = [path for path in all_scripts if is_skill_resource(path)]
    project_scripts = [path for path in all_scripts if not is_skill_resource(path)]
    automation = [path for path in files if is_automation(path)]

    evidence_set = {
        path
        for path in files
        if not is_skill_package_path(path)
        and (
            EVIDENCE_TERMS.search(path.name)
            or path in instructions
            or path in project_scripts
            or path in automation
        )
    }
    evidence_paths = sorted(evidence_set, key=lambda item: item.as_posix().lower())

    languages = Counter(
        LANGUAGE_BY_SUFFIX[path.suffix.lower()]
        for path in files
        if path.suffix.lower() in LANGUAGE_BY_SUFFIX
    )

    warnings: list[str] = []
    if truncated:
        warnings.append(f"File inventory was truncated at {maximum} paths.")
    if not skills:
        warnings.append("No SKILL.md files were found in the scanned repository scope.")

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "git": {
            "is_repository": repository_root is not None,
            "repository_root": str(repository_root) if repository_root else "",
            "branch": current_branch(root) if repository_root else "",
            "recent_commit_subjects": recent_git_history(root, git_history),
        },
        "files": {
            "considered": len(files),
            "truncated": truncated,
            "languages": dict(languages.most_common()),
            "documentation_count": len(documentation),
            "project_script_count": len(project_scripts),
            "skill_resource_script_count": len(skill_resource_scripts),
            "manifests": limited(manifests),
            "package_json": package_json[:30],
        },
        "existing_skills": skills,
        "agent_instructions": limited(instructions),
        "automation": limited(automation),
        "scripts": limited(project_scripts, 120),
        "skill_resource_scripts": limited(skill_resource_scripts, 80),
        "documentation": limited(documentation, 120),
        "candidate_evidence": limited(evidence_paths, 120),
        "candidate_evidence_clusters": evidence_clusters(evidence_paths),
        "excluded_content": [
            "secret values and credential files",
            "dependency and build directories",
            "generated browser artifacts",
            "VCS internals and worktrees",
        ],
        "warnings": warnings,
    }


def markdown_list(values: list[str]) -> str:
    if not values:
        return "- None found"
    return "\n".join(f"- `{value}`" for value in values)


def render_markdown(inventory: dict[str, Any]) -> str:
    lines = [
        "# Structural Project Inventory",
        "",
        f"- Root: `{inventory['root']}`",
        f"- Files considered: {inventory['files']['considered']}",
        f"- Git repository: {inventory['git']['is_repository']}",
        "",
        "## Existing Skills",
        "",
    ]
    skills = inventory["existing_skills"]
    if skills:
        lines.extend(["| Name | Description | Path | Valid |", "|---|---|---|---|"])
        for skill in skills:
            description = skill["description"].replace("|", "\\|")
            lines.append(
                f"| {skill['name'] or 'Unknown'} | {description} | `{skill['path']}` | "
                f"{skill['valid_frontmatter']} |"
            )
    else:
        lines.append("None found.")

    sections = [
        ("Agent Instructions", inventory["agent_instructions"]),
        ("Automation", inventory["automation"]),
        ("Scripts", inventory["scripts"][:60]),
        ("Candidate Evidence", inventory["candidate_evidence"][:60]),
    ]
    for title, values in sections:
        lines.extend(["", f"## {title}", "", markdown_list(values)])
    clusters = inventory["candidate_evidence_clusters"]
    if clusters:
        lines.extend(
            [
                "",
                "## Candidate Evidence Clusters",
                "",
                "| Topic | Count | Examples |",
                "|---|---:|---|",
            ]
        )
        for cluster in clusters:
            examples = ", ".join(f"`{value}`" for value in cluster["examples"])
            lines.append(f"| {cluster['topic']} | {cluster['count']} | {examples} |")
    if inventory["warnings"]:
        lines.extend(["", "## Warnings", "", markdown_list(inventory["warnings"])])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to scan (default: current directory)")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--max-files", type=int, default=50_000)
    parser.add_argument("--git-history", type=int, default=20)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        inventory = collect_inventory(Path(args.root), args.max_files, args.git_history)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"scan_project: {error}", file=sys.stderr)
        return 2

    if args.format == "markdown":
        sys.stdout.write(render_markdown(inventory))
    else:
        json.dump(inventory, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
