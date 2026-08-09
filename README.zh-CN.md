# 365Skill

[English](README.md) | [简体中文](README.zh-CN.md)

一个用于跨项目、跨 AI 客户端发现、验证和共享可复用 Agent Skills 的实验仓库。

本仓库使用开放的 `SKILL.md` 目录格式。每个技能保持独立、可审查、可测试，并把流程说明、确定性脚本和按需加载的参考资料放在同一个可移植目录中。

## 当前技能

| Skill | 状态 | 作用 |
|---|---|---|
| [`365-chatgpt-pro-delivery`](skills/365-chatgpt-pro-delivery/SKILL.md) | 实验中 | 通过隐私闸门、证据标签、单次发送和 Codex 独立验收，完成一次边界清晰的 ChatGPT Pro 协作 |
| [`365-five-step-dev`](skills/365-five-step-dev/SKILL.md) | 实验中 | 帮助业务用户确定范围与风险、保护工作区归属、用证据验收并完成闭环，无需用户掌握开发流程 |
| [`365-session-rotation-maintainer`](skills/365-session-rotation-maintainer/SKILL.md) | 实验中 | 通过持久检查点、唯一且已验证的继任任务、工作区归属保护和最后归档机制，安全轮换长期任务 |
| [`discover-project-skills`](skills/discover-project-skills/SKILL.md) | Experimental | 盘点项目现有技能，发现可复用候选，并在明确授权后把成熟实践提炼成标准技能包 |
| [`shopify-theme-delivery`](skills/shopify-theme-delivery/SKILL.md) | 实验中 | Shopify Online Store 2.0 主题草稿优先交付：覆盖架构、内容保留、远程回读、浏览器验收和动态 DOM 稳定性验证 |
| [`gws-workspace`](skills/gws-workspace/SKILL.md) | 实验中 | 通过 gws CLI 操作 Gmail、日历、Drive、Sheets、Docs、Slides、Chat、Tasks：默认只读的安全边界、辅助命令速查、从零 OAuth 配置指南 |
| [`gws-weekly-digest`](skills/gws-weekly-digest/SKILL.md) | 实验中 | 用邮件和日历生成每周晨报：上周邮件统计、本周日程按天分组、markdown 晨报加会话摘要，严格只读 |
| [`parallel-sessions-protocol`](skills/parallel-sessions-protocol/SKILL.md) | 实验中 | 协调任意数量的会话并行开发同一仓库：Draft PR 公告板登记、资源认领、记账只在合并前写、合并纪律、三时点刷新 |

| [`discover-project-skills`](skills/discover-project-skills/SKILL.md) | Experimental | 盘点项目现有技能，发现可复用候选，并在明确授权后把成熟实践提炼成标准技能包 |
| [`shopify-theme-delivery`](skills/shopify-theme-delivery/SKILL.md) | 实验中 | Shopify Online Store 2.0 主题草稿优先交付：覆盖架构、内容保留、远程回读、浏览器验收和动态 DOM 稳定性验证 |
| [`gws-workspace`](skills/gws-workspace/SKILL.md) | 实验中 | 通过 gws CLI 操作 Gmail、日历、Drive、Sheets、Docs、Slides、Chat、Tasks：默认只读的安全边界、辅助命令速查、从零 OAuth 配置指南 |
| [`gws-weekly-digest`](skills/gws-weekly-digest/SKILL.md) | 实验中 | 用邮件和日历生成每周晨报：上周邮件统计、本周日程按天分组、markdown 晨报加会话摘要，严格只读 |
| [`parallel-sessions-protocol`](skills/parallel-sessions-protocol/SKILL.md) | 实验中 | 协调任意数量的会话并行开发同一仓库：Draft PR 公告板登记、资源认领、记账只在合并前写、合并纪律、三时点刷新 |
### 从 [mattpocock/skills](https://github.com/mattpocock/skills) 同步（MIT 协议）

Matt Pocock 生产环境技能的逐字同步——来源与版权见各技能目录内 `THIRD-PARTY.md`。

**工程**

| [`ask-matt`](skills/ask-matt/SKILL.md) | 稳定 | 本仓库用户主动调用技能的路由器：问哪个技能或流程适合当前场景 |
| [`code-review`](skills/code-review/SKILL.md) | 稳定 | 双轴评审（标准轴 vs 规格轴）自固定基准点以来的改动，并行子代理评审并排展示 |
| [`codebase-design`](skills/codebase-design/SKILL.md) | 稳定 | 设计深度模块的共享词汇：接口、接缝、可测试性、AI 可导航性 |
| [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md) | 稳定 | 疑难 bug 与性能回退的诊断循环 |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | 稳定 | 构建并打磨项目领域模型：统一语言与 ADR 架构决策记录 |
| [`grill-with-docs`](skills/grill-with-docs/SKILL.md) | 稳定 | 连环拷问的同时产出文档（ADR 与术语表） |
| [`implement`](skills/implement/SKILL.md) | 稳定 | 基于规格或一组 ticket 实现一项工作 |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | 稳定 | 扫描「深化」机会、生成可视化 HTML 报告，再针对选中的一项连环拷问 |
| [`prototype`](skills/prototype/SKILL.md) | 稳定 | 构建一次性原型回答设计问题 |
| [`research`](skills/research/SKILL.md) | 稳定 | 对照高可信一手资料调研，结论沉淀为仓库内 Markdown |
| [`resolving-merge-conflicts`](skills/resolving-merge-conflicts/SKILL.md) | 稳定 | 解决进行中的 git merge/rebase 冲突 |
| [`setup-matt-pocock-skills`](skills/setup-matt-pocock-skills/SKILL.md) | 稳定 | 工程技能的一次性仓库配置：issue 追踪器、分流标签、领域文档 |
| [`tdd`](skills/tdd/SKILL.md) | 稳定 | 测试驱动开发：红绿重构、集成测试 |
| [`to-spec`](skills/to-spec/SKILL.md) | 稳定 | 把当前会话整理成规格并发布到 issue 追踪器 |
| [`to-tickets`](skills/to-tickets/SKILL.md) | 稳定 | 把计划或规格拆解为带阻塞边界的曳光弹 ticket |
| [`triage`](skills/triage/SKILL.md) | 稳定 | 让 issue/PR 走完分流状态机并撰写 agent 可直接执行的简报 |
| [`wayfinder`](skills/wayfinder/SKILL.md) | 稳定 | 把大型工作规划为决策 ticket 地图，逐个解决 |
| [`wizard`](skills/wizard/SKILL.md) | 稳定 | 生成交互式 bash 向导，引导人类完成只有他们能做的步骤 |

**效率**

| [`grill-me`](skills/grill-me/SKILL.md) | 稳定 | 对计划或设计不留情面的连环拷问 |
| [`grilling`](skills/grilling/SKILL.md) | 稳定 | 对计划、决策或想法连环拷问——压力测试思考 |
| [`handoff`](skills/handoff/SKILL.md) | 稳定 | 把当前会话压缩成交接文档交给另一个 agent |
| [`teach`](skills/teach/SKILL.md) | 稳定 | 在工作区内教用户新技能或概念 |
| [`to-questionnaire`](skills/to-questionnaire/SKILL.md) | 稳定 | 把无法自行回答的决策转成问卷请他人填写 |
| [`wait-what`](skills/wait-what/SKILL.md) | 稳定 | 停下——刚才那条信息没传达清楚，重新讲 |
| [`writing-for-agents`](skills/writing-for-agents/SKILL.md) | 稳定 | 为 agent 写作：技能文件、AGENTS.md、CLAUDE.md |

**杂项**

| [`git-guardrails-claude-code`](skills/git-guardrails-claude-code/SKILL.md) | 稳定 | Claude Code hooks：在执行前拦截危险 git 命令 |
| [`migrate-to-shoehorn`](skills/migrate-to-shoehorn/SKILL.md) | 稳定 | 把测试从 `as` 断言迁移到 @total-typescript/shoehorn |
| [`scaffold-exercises`](skills/scaffold-exercises/SKILL.md) | 稳定 | 搭建练习目录：小节、题目、解答、讲解 |
| [`setup-pre-commit`](skills/setup-pre-commit/SKILL.md) | 稳定 | Husky pre-commit 钩子：lint-staged、类型检查与测试 |

**进行中（Beta）**

| [`claude-handoff`](skills/claude-handoff/SKILL.md) | Beta | 把会话交给全新后台 agent 立即接续 |
| [`loop-me`](skills/loop-me/SKILL.md) | Beta | 多会话循环拷问，把工作流规格打磨到可落地 |
| [`setup-ts-deep-modules`](skills/setup-ts-deep-modules/SKILL.md) | Beta | 把 dependency-cruiser 接入 TypeScript 仓库实现深度模块 |
| [`writing-beats`](skills/writing-beats/SKILL.md) | Beta | 把素材组装成「节拍」之旅，术语先落地定义 |
| [`writing-fragments`](skills/writing-fragments/SKILL.md) | Beta | 挖掘写作碎片——尚无结构 |
| [`writing-shape`](skills/writing-shape/SKILL.md) | Beta | 把素材逐段塑造成文章，逐步论证格式选择 |

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
./install.sh 365-five-step-dev codex
./install.sh 365-session-rotation-maintainer codex
./install.sh 365-chatgpt-pro-delivery codex
```

```text
使用 $365-five-step-dev 按五步法完整交付这个业务需求。
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
python3 -m json.tool evals/365-five-step-dev/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-session-rotation-maintainer/trigger-cases.json >/dev/null
python3 -m json.tool evals/discover-project-skills/trigger-cases.json >/dev/null
python3 -m json.tool evals/shopify-theme-delivery/trigger-cases.json >/dev/null
python3 -m json.tool evals/gws-workspace/trigger-cases.json >/dev/null
python3 -m json.tool evals/gws-weekly-digest/trigger-cases.json >/dev/null
python3 -m json.tool evals/parallel-sessions-protocol/trigger-cases.json >/dev/null
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
