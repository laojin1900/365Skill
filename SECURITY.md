# Security Policy

[English](#english) | [简体中文](#简体中文)

## English

### Supported versions

365Skill is experimental. Security fixes are applied to the current `main` branch; older commits and copied skill versions are not maintained.

### Reporting a vulnerability

Please use GitHub's **Report a vulnerability** form in this repository's Security tab. Do not disclose exploit details, credentials, personal data, or suspected secrets in a public issue.

If private vulnerability reporting is unavailable, open a minimal public issue asking the maintainer to establish a private contact channel. Do not include sensitive technical details in that issue.

Include the affected file or skill, reproduction steps, potential impact, and a suggested mitigation when possible. You may submit reports in English or Chinese.

### Scanner data boundary

The project scanner excludes common secret files and does not intentionally read credential values. Its reports can still contain repository paths, filenames, commands, dependency names, skill descriptions, and recent commit subjects. Review reports before sharing them outside your organization.

## 简体中文

### 支持范围

365Skill 目前处于实验阶段。安全修复只应用于当前 `main` 分支；历史提交以及复制到其他位置的旧版技能不在维护范围内。

### 报告安全问题

请使用本仓库 Security 页面中的 **Report a vulnerability** 私密报告入口。不要在公开 Issue 中披露漏洞利用细节、凭证、个人数据或疑似密钥。

如果私密漏洞报告暂不可用，请只创建一个最简短的公开 Issue，请求维护者建立私密沟通渠道；不要在该 Issue 中填写敏感技术细节。

报告中建议包含受影响的文件或技能、复现步骤、潜在影响以及可行的缓解建议。可以使用中文或英文提交。

### 扫描数据边界

项目扫描器会排除常见敏感文件，也不会有意读取凭证值。但扫描报告仍可能包含仓库路径、文件名、命令、依赖名称、技能描述和近期提交主题。向组织外分享前请先审阅报告。
