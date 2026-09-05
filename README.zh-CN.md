# 365Skill

[English](README.md) | [简体中文](README.zh-CN.md)

一个用于跨项目、跨 AI 客户端发现、验证和共享可复用 Agent Skills 的实验仓库。

本仓库使用开放的 `SKILL.md` 目录格式。每个技能保持独立、可审查、可测试，并把流程说明、确定性脚本和按需加载的参考资料放在同一个可移植目录中。

## 当前技能

| Skill | 状态 | 作用 |
|---|---|---|
| [`365-chatgpt-pro-delivery`](skills/365-chatgpt-pro-delivery/SKILL.md) | 实验中 | 通过隐私闸门、证据标签、单次发送和 Codex 独立验收，完成一次边界清晰的 ChatGPT Pro 协作 |
| [`365-five-step-dev-codex`](skills/365-five-step-dev-codex/SKILL.md) | 实验中 | 365五步法（Codex版）：以轻量、比例化的业务治理管理目标级授权、风险、证据、工作区归属、进度和闭环，不重复 Codex 原生开发流程 |
| [`365-five-step-dev-claude`](skills/365-five-step-dev-claude/SKILL.md) | 实验中 | 365五步法（Claude Code 版）：同一套治理理念，用 A/B/C 三级风险分级、动手前需求碰撞、证据验收闭环，经十轮真实运行复盘打磨 |
| [`365-five-step-retro-claude`](skills/365-five-step-retro-claude/SKILL.md) | 实验中 | Claude Code 版五步法的自我迭代复盘技能——六维度分析真实日志、用 git 记录交叉核对漏记，只在逐条获批后才升级流程本身 |
| [`365-session-rotation-maintainer`](skills/365-session-rotation-maintainer/SKILL.md) | 实验中 | 通过持久检查点、唯一且已验证的继任任务、工作区归属保护和最后归档机制，安全轮换长期任务 |
| [`discover-project-skills`](skills/discover-project-skills/SKILL.md) | 实验中 | 盘点项目现有技能，发现可复用候选，并在明确授权后把成熟实践提炼成标准技能包 |
| [`shopify-theme-delivery`](skills/shopify-theme-delivery/SKILL.md) | 实验中 | Shopify Online Store 2.0 主题按范围交付：本地工作本地闭环；已授权发布复用项目路由，保留回读、浏览器验收和动态 DOM 稳定性验证 |
| [`gws-workspace`](skills/gws-workspace/SKILL.md) | 实验中 | 通过 gws CLI 操作 Gmail、日历、Drive、Sheets、Docs、Slides、Chat、Tasks：默认只读的安全边界、辅助命令速查、从零 OAuth 配置指南 |
| [`gws-weekly-digest`](skills/gws-weekly-digest/SKILL.md) | 实验中 | 用邮件和日历生成每周晨报：上周邮件统计、本周日程按天分组、markdown 晨报加会话摘要，严格只读 |
| [`parallel-sessions-protocol`](skills/parallel-sessions-protocol/SKILL.md) | 实验中 | 协调任意数量的会话并行开发同一仓库：Draft PR 公告板登记、资源认领、记账只在合并前写、合并纪律、收工登记（会话中断/暂停时的对称收尾）、三时点刷新 |
| [`project-health-check`](skills/project-health-check/SKILL.md) | 实验中（早期） | 有界只读项目/worktree 巡检：优先项目入口、明确覆盖限制，不默认扫描主目录或清理；已授权修复转具体实现路由 |

## 发布模型

公共仓库由私有源仓库确定性导出。发布策略默认私有：只有 `catalog/publication-policy.json` 白名单中的技能 ID 才会复制到公共镜像。CI 会拒绝任何未列入白名单的技能目录、评测、目录条目和文本引用。

## 快速体验

### 在 Codex 中安装

克隆仓库后，把技能链接到个人技能目录：

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/discover-project-skills" ~/.codex/skills/discover-project-skills
```

在任意项目的新任务中调用：

```text
使用 $discover-project-skills 扫描当前仓库，输出项目技能地图。
```

三个 365 核心技能也可以用同样方式安装和调用：

```bash
./install.sh 365-five-step-dev-codex codex
./install.sh 365-session-rotation-maintainer codex
./install.sh 365-chatgpt-pro-delivery codex
```

安装脚本会把 Codex 链接到当前仓库。后续升级应修改并更新这个唯一仓库源，不直接编辑全局安装副本，
避免本机运行版与公开版再次漂移。

```text
使用 $365-five-step-dev-codex 按 365五步法（Codex版）完整交付这个业务需求。
使用 $365-session-rotation-maintainer 把这个长期任务安全交给一个已验证的继任任务。
使用 $365-chatgpt-pro-delivery 获取一次 Pro 审查，并由 Codex 独立验收。
```

进行 Shopify 主题工作时，可链接并调用主题交付技能：

```bash
ln -s "$PWD/skills/shopify-theme-delivery" ~/.codex/skills/shopify-theme-delivery
```

```text
使用 $shopify-theme-delivery 先规划并验证这次主题草稿修改，不要直接写入 Shopify。
```

不同客户端版本使用独立技能 ID。本包是 Codex 版；Claude Code 版已发布为
[`365-five-step-dev-claude`](skills/365-five-step-dev-claude/SKILL.md)
（配套复盘技能 [`365-five-step-retro-claude`](skills/365-five-step-retro-claude/SKILL.md)）——
同一套治理理念，在 Claude Code 侧独立打磨了十轮真实运行复盘，两个版本互不触发冲突。

只运行结构扫描器：

```bash
python3 skills/discover-project-skills/scripts/scan_project.py \
  --root /path/to/project \
  --format markdown
```

### 其他 Agent 客户端

技能采用标准 `SKILL.md` 格式。将 `skills/discover-project-skills/` 复制或链接到客户端支持的个人或项目技能目录即可。随着实验扩展，仓库会增加不同客户端的安装适配器。

## 工作模式

- **Inventory**：列出并总结已有 `SKILL.md`。
- **Discover**：识别重复流程、业务知识和候选技能，默认只读。
- **Extract**：用户明确选择候选后，生成可移植技能包。
- **Audit**：检查已有技能的触发、结构、资源、安全边界和验证覆盖。

## 语言支持

仓库文档同时提供英文和简体中文。技能会识别用户使用的语言，并使用相同语言回答；用户明确要求时，也可以输出中英双语项目技能报告。

技能 ID、路径、命令和机器可读字段继续使用英文，保证跨客户端可移植性。

## 安全边界

项目扫描器不会读取或输出 `.env*`、凭证、私钥和 Secrets 内容，并排除依赖目录、构建产物、浏览器生成数据及版本控制内部文件。

Discovery 和 Audit 默认只读。只有用户明确要求提炼技能并提供或确认目标目录后，才允许写入。

扫描报告仍可能包含仓库路径、文件名、命令、依赖名称、技能描述和近期提交主题。向组织外分享或公开发布前，请先审阅生成的报告。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 -m json.tool evals/365-chatgpt-pro-delivery/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-codex/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-codex/workflow-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-codex/regression-cases.json >/dev/null
python3 -m json.tool evals/365-session-rotation-maintainer/trigger-cases.json >/dev/null
python3 -m json.tool evals/discover-project-skills/trigger-cases.json >/dev/null
python3 -m json.tool evals/shopify-theme-delivery/trigger-cases.json >/dev/null
python3 -m json.tool evals/gws-workspace/trigger-cases.json >/dev/null
python3 -m json.tool evals/gws-weekly-digest/trigger-cases.json >/dev/null
python3 -m json.tool evals/parallel-sessions-protocol/trigger-cases.json >/dev/null
python3 -m json.tool evals/project-health-check/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-claude/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-retro-claude/trigger-cases.json >/dev/null
node --test skills/shopify-theme-delivery/scripts/*.test.mjs
node --test scripts/publication/*.test.mjs
```

每个触发评测集包含 10 个应触发请求和 10 个不应触发请求，覆盖中英文。格式验证、脚本单元测试和真实仓库扫描已经通过；独立模型触发率评测仍属于后续实验。

## 开源许可证

本仓库采用 [Apache License 2.0](LICENSE) 开源许可证。

## 参考

- [Agent Skills specification](https://github.com/agentskills/agentskills)
- [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- [Superpowers writing-skills](https://github.com/obra/superpowers-skills/tree/main/skills/meta/writing-skills)
