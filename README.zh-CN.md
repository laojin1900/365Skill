# 365Skill

[English](README.md) | [简体中文](README.zh-CN.md)

一个用于跨项目、跨 AI 客户端发现、验证和共享可复用 Agent Skills 的实验仓库。

本仓库使用开放的 `SKILL.md` 目录格式。每个技能保持独立、可审查、可测试，并把流程说明、确定性脚本和按需加载的参考资料放在同一个可移植目录中。

## 当前技能

| Skill | 状态 | 作用 |
|---|---|---|
| [`discover-project-skills`](skills/discover-project-skills/SKILL.md) | Experimental | 盘点项目现有技能，发现可复用候选，并在明确授权后把成熟实践提炼成标准技能包 |
| [`five-step-dev`](skills/five-step-dev/SKILL.md) | Experimental | 面向业务型开发者的风险分级五步开发流程（Research→Plan→Implement→Review→Verify）：用计划审批和证据验收把控质量，用模型切换提醒把最强模型额度只花在高危决策点 |
| [`five-step-retro`](skills/five-step-retro/SKILL.md) | 实验中 | five-step-dev 的自我迭代循环：运行日志 + 六维度复盘 + 有证据的改进提案，人工批准后升级技能并提交本仓库 |

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
python3 -m json.tool evals/discover-project-skills/trigger-cases.json >/dev/null
node --test scripts/publication/*.test.mjs
```

每个触发评测集包含 10 个应触发请求和 10 个不应触发请求，覆盖中英文。格式验证、脚本单元测试和真实仓库扫描已经通过；独立模型触发率评测仍属于后续实验。

## 开源许可证

本仓库采用 [Apache License 2.0](LICENSE) 开源许可证。

## 参考

- [Agent Skills specification](https://github.com/agentskills/agentskills)
- [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- [Superpowers writing-skills](https://github.com/obra/superpowers-skills/tree/main/skills/meta/writing-skills)
