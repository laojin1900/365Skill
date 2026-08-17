# Pi 模型「订阅 + API」双通道设计 & 智能排序——可复用实现方案

> 目的：把 `pi-web`（Pi Coding Agent 网页版）里这套「订阅额度通道 + 按量 API 通道」的模型设计、注册、发现与智能排序方式抽象出来，让**任何其他 agent / 网关 / 前端**都能照着这套规范落地。
>
> 适用对象：需要在多通道（订阅 / 按量）下管理模型，并向用户提供"好用、有先后、能看懂"的模型选择器的任何系统。
>
> 源实现：`~/.pi/agent/models.json` + `pi-web/components/ChatInput.tsx` + `pi-web/app/api/models-config/discover/route.ts` + `app/api/model-usage/route.ts`。

---

## 0. 核心理念（先想清楚再动手）

1. **一条通道一个 Provider 实例**：订阅额度（如 Google AI Pro、Kimi Coding、xAI）和按量 API（如原生 Google、DeepSeek、OpenRouter）是**不同 provider**，绝不在同一个 provider 里混。
   - 订阅 → `google-vip`、`kimi-vip`、`xai-subscription`
   - 按量 → `google`、`deepseek`、`openrouter`
   - 用 `-vip` / `-subscription` 后缀表明"订阅"，`-api` / 裸名 = 按量。
2. **认证分开**：订阅通道走 OAuth 或固定免鉴权网关；按量通道走 API Key。
3. **统一 OpenAI 协议**：不管上游是什么，全部归一成 `openai-completions`，由网关（如 OmniRoute / new-api）做转换。
4. **模型是"可声明的对象"**：每个模型带 `id / name / reasoning / input / contextWindow / maxTokens / compat`，前端据此决定能不能选、怎么排序、怎么标徽章。
5. **排序 = 厂商权重 + 使用频率 + 自然语言排序**（见 §4）。

---

## 1. 数据模型（models.json 规范）

这是**声明式的、不含密钥的模型目录**。密钥另存（见 §5）。

```jsonc
{
  "providers": {
    "google-vip": {            // 1) Provider ID 即身份，全局唯一
      "baseUrl": "https://allmodelsapi.com/v1",
      "api": "openai-completions",
      "authHeader": true,
      "models": [
        {
          "id": "antigravity/gemini-3.5-flash-high",  // 2) 完整模型 ID（gateway 约定前缀）
          "name": "Gemini 3.5 Flash (High) (Google AI Pro订阅)", // 3) 展示名（含订阅标识）
          "reasoning": true,                           // 4) 是否推理模型
          "input": ["text", "image"],                  // 5) 输入模态
          "contextWindow": 1048576,                    // 6) 上下文窗口（token）
          "maxTokens": 65536,                          // 7) 最大输出
          "compat": {                                  // 8) 兼容性能力（驱动对话构造）
            "supportsDeveloperRole": false,
            "supportsReasoningEffort": false
          }
        }
        // ... 更多模型
      ]
    },
    "kimi-vip": {
      "baseUrl": "https://allmodelsapi.com/v1",
      "api": "openai-completions",
      "authHeader": true,
      "models": [
        {
          "id": "kimi-coding/k3",
          "name": "Kimi K3 (Kimi Coding订阅)",
          "reasoning": true,
          "input": ["text", "image"],
          "contextWindow": 1048576,
          "maxTokens": 131072,
          "compat": {
            "supportsDeveloperRole": false,
            "supportsReasoningEffort": true,
            "requiresReasoningContentOnAssistantMessages": true
          }
        }
      ]
    }
  }
}
```

### 字段语义（TypeBox 校验，供其它语言参考）

| 字段 | 类型 | 说明 |
|---|---|---|
| `providers.<id>` | ProviderConfig | Provider ID = 通道身份 |
| `.baseUrl` | string | 统一 OpenAI-compatible 端点 |
| `.apiKey` | string\|undefined | 可为空（走 auth.json / 网关） |
| `.api` | "openai-completions"\|… | 协议类型，此处统一 `openai-completions` |
| `.authHeader` | boolean | true = 用 `Authorization: Bearer` |
| `.models[]` | ModelDefinition[] | 该通道可用的模型（有序） |
| `models[].id` | string | **必须含 gateway 前缀**（`antigravity/`、`kimi-coding/`） |
| `models[].reasoning` | boolean | 决策/思考类模型 |
| `models[].input` | ("text"\|"image")[] | 支持文本/图像 |
| `models[].compat` | object | 对话构造兼容开关（见 §6） |

---

## 2. Provider 命名与分组（关键约定）

前端靠 **Provider ID 前缀/后缀** 决定如何分组、打徽章、排序。**这套约定必须在你的系统里保持一致。**

| Provider ID | 分类 | 徽章显示 |
|---|---|---|
| `google-vip` | 订阅 | `Google(订阅)` |
| `google` | 按量 API | `Google(API)` |
| `kimi-vip` | 订阅 | `Kimi(订阅)` |
| `kimi-coding` | 订阅 | `Kimi(Coding)` |
| `xai-subscription` | 订阅 | `xAI(订阅)` |
| `xai-api` | 按量 API | `xAI(API)` |
| `deepseek` | 按量 API | `DeepSeek` |
| `openrouter` | 按量 API | `OpenRouter` |
| `qwen-token-plan-cn` | 订阅 | `Qwen(包月)` |
| `qwen-dashscope-cn` | 按量 API | `Qwen(按量)` |
| `openai-codex` | 订阅 (OAuth) | `ChatGPT` |
| `omniroute` | 调度网关 | `OmniRoute` |

**规则**：
- 不要一个 provider 既当订阅又当按量——会污染排序和额度展示。
- 展示名与内部 ID 解耦：内部 `google-vip`，界面显示"Google (订阅)"。可读名映射集中在**一处**（`getProviderShortBadge` / `getProviderDisplayName`）。

---

## 3. 模型发现 / 同步（如何把"新模型"拉进目录）

Pi Web 用一个 discover 路由，对**订阅通道**从网关按"前缀规则"拉取并过滤。核心逻辑（伪代码 + 关键片段）：

```
discover(providerName):
  if kimi-vip:   endpoint = OMNIROUTE_CATALOG_URL
                 prefix = "kimi-coding/"
                 accept = id 以 "kimi-coding/" 开头
  if google-vip: endpoint = OMNIROUTE_CATALOG_URL
                 prefix = "antigravity/"
                 accept = id 以 "antigravity/gemini-" 开头
                          && 不含 "image" && 不含 "agent"
                         && type 不是 image/embedding
  else: 原生 provider → 走 runtime catalog（内置厂商模型表）
```

**关键安全约束**（务必抄这条）：
> 固定订阅规则**只接受来自自己 catalog 的、带正确前缀的 ID**。绝不从宽泛的 `auto/*` 或公共总目录凭空制造 `antigravity/*`、`kimi-coding/*` —— 否则会落到别的厂商或运行时 404。

新拉到的模型会合并进 providers 的 `models` 数组（去重、保留已有用户改过的 name/排序）。用户可一键"拉取最新模型"刷新。

---

## 4. 智能排序（"Smart Three-Tier Gold Sorting"）

这是这套系统的**灵魂**，直接决定用户体验。三层权重，权重高者排前面。

### 4.1 权重计算

```ts
const MODEL_PRIORITY_WEIGHTS: Record<string, number> = {
  "deepseek-v4-pro": 100,           // 旗舰强模型，给最高分
  "deepseek-chat": 99,
  "claude-3.5-sonnet": 96,
  "gpt-4o": 95,
  "k3": 94,
  "gemini-3.6-flash": 92,
  "gemini-2.5-pro": 91,
  "auto/best-coding": 89,
  "qwen3.7-max": 87,
  "qwen-coder-plus": 86,
};

function getSmartSortWeight(modelId, provider): number {
  const normId = modelId.toLowerCase();

  // 1) 使用频率加成（本机持久化）——用户用的越多越靠前
  let usageBonus = 0;
  const usageMap = JSON.parse(localStorage.getItem("pi-model-usage-counts") || "{}");
  usageBonus = Math.min(100, (usageMap[`${provider}:${modelId}`] || 0) * 10);

  // 2) 旗舰权重——精确/子串匹配，取最大
  let baseWeight = 5;
  for (const [k, w] of Object.entries(MODEL_PRIORITY_WEIGHTS)) {
    if (normId.includes(k.toLowerCase()) || k.toLowerCase().includes(normId)) {
      baseWeight = Math.max(baseWeight, w);
    }
  }
  return baseWeight + usageBonus;
}
```

### 4.2 排序比较器

```ts
const COLLATOR = new Intl.Collator(undefined, { numeric: true, sensitivity: "base" });

function compareModelOptions(a, b): number {
  return COLLATOR.compare(a.name || a.modelId, b.name || b.modelId)
    || COLLATOR.compare(a.provider, b.provider)
    || COLLATOR.compare(a.modelId, b.modelId);
}

const sorted = rawOptions.sort((a, b) => {
  const wa = getSmartSortWeight(a.modelId, a.provider);
  const wb = getSmartSortWeight(b.modelId, b.provider);
  if (wa !== wb) return wb - wa;   // 高权重在前
  return compareModelOptions(a, b); // 同权重 → 自然排序
});
```

### 4.3 按 Provider 分组（保持排序后插入顺序）

```ts
const modelsByProvider = [];
for (const opt of sortedOptions) {
  const g = modelsByProvider.find(x => x.provider === opt.provider);
  g ? g.options.push(opt) : modelsByProvider.push({ provider: opt.provider, options: [opt] });
}
// 渲染时：每组打 Provider 徽章 + 组标题
```

### 4.4 其它环境的可选排序（保持一致心智）

- **CLI / 终端**：`当前选中的模型置顶 → 按 provider 名自然排序 → 按 model id 自然排序`（`ModelSelectorComponent.sortModels`）。
- **表格输出**：`provider → model id` 字典序，列 = provider / model / context / maxOut / thinking / images。

> 建议：网页端用"权重+分组"，终端用"当前置顶+字典序"——两者都基于同一份 models.json，只是渲染语境不同。

---

## 5. 凭据管理（订阅 vs API 分开）

把 **模型目录（models.json，无密钥）** 与 **凭据（auth.json，有密钥）** 分离：

```jsonc
// ~/.pi/agent/auth.json
{
  "google-vip":     { "type": "api_key", "key": "sk-…（订阅网关共享 key）" },
  "kimi-vip":       { "type": "api_key", "key": "sk-…" },
  "deepseek":       { "type": "api_key", "key": "sk-…" },
  "openai-codex":   { "type": "oauth", "accessToken": "…" }  // OAuth 订阅
}
```

**规则**：
- 目录文件不含密钥，可安全入库/共享。
- 订阅通道 key 是**网关的统一 key**（如 `allmodelsapi.com` 签发），不暴露上游厂商 key。
- OAuth 订阅（ChatGPT、xAI、Antigravity）走 token 刷新，与 API Key 分列。

---

## 6. 兼容性（compat）字段——决定对话怎么构造

不同厂商的 OpenAI-compatible 行为差异，全部收敛到 `compat`，不散落在调用点。实现时**在协议适配层按这些开关分派**：

| 字段 | 含义 |
|---|---|
| `supportsDeveloperRole` | 是否支持 `developer` 角色（否则用 `system`） |
| `supportsReasoningEffort` | 是否支持 `reasoning_effort` 参数 |
| `requiresReasoningContentOnAssistantMessages` | assistant 回复是否必须回传 reasoning content（Kimi 需要） |
| `supportsThinkingAsText` / `thinkingFormat` | 思考内容以何形式呈现（deepseek/openai/qwen…） |
| `supportsUsageInStreaming` | 流式是否带 usage |
| `maxTokensField` | `max_completion_tokens` vs `max_tokens` |

> 这样 `google-vip`（Antigravity）与 `kimi-vip`（Kimi）虽然都走 `openai-completions`，但对话构造细节靠 `compat` 自动适配。

## 6.1 高级模型字段（可选的性能/成本/思维控制）

除 compat 外的可选字段，模型目录 schema 也支持，且会影响选择器/成本展示/推理力度：

| 字段 | 类型 | 含义 | 影响 |
|---|---|---|---|
| `reasoning` | boolean | 是否推理模型 | 决定思考级别可选范围、是否推导 token |
| `thinkingLevelMap` | `Record<"off\|minimal\|low\|medium\|high\|xhigh\|max", string\|null>` | 把七个思考级别映射到厂商字符串；`null`=该级别不可用 | `getSupportedThinkingLevels()`：非推理模型只有 `["off"]`；按 `thinkingLevelMap[level]===null` 过滤；xhigh/max 仅在显式映射时可用 |
| `cost` | `{ input, output, cacheRead, cacheWrite, tiers? }` | 每百万 token 单价（input/output/cacheRead/cacheWrite）+ 可选按用量分档 `tiers[]`（每个 `{ inputTokensAbove, ...rates }`） | `calculateCost()` 按 `inputTokens > tier.inputTokensAbove` 选档，算出会话 `$` 成本；前端 MessageView 显示 `$0.1234` |
| `headers` | `Record<string,string>` | 模型级覆写请求头 | `getAuth()` 里 `mergeHeaders(providerHeaders, model.headers)`——单个模型可走不同端点/鉴权头 |
| `api`（模型级） | `openai-completions`\|… | 覆盖 provider 级协议 | 同一 provider 内可混不同 API 的实现分发 |
| 每模型 `baseUrl` / `apiKey` | string | 模型级端点/凭据覆写 | 部分模型走专用网关 |

**思考级别落地**：选择器里给推理模型提供思考级别切换；非推理模型固定 `off`。

## 6.2 可见模型过滤 + 默认模型持久化

- **可见白名单**：单独的 `pi-web-model-preferences.json`（`{ visibleModels: ["provider/model", ...] }`）存用户主动勾选可见的模型引用。`visibleModels` 为空 = 全部显示。`/api/models` 用 `filterByVisibleModels()` 按 `provider/model` 精确引用过滤。
- **默认模型持久化**：`settings.getDefaultProvider()/getDefaultModel()`——上次选中的 provider+模型作为默认；前端用 `settingsManager.setDefaultModelAndProvider()` 写入。
- **硬约束**：UI 能显示/选择的**只有 runtime `getAvailable()` 能解析的模型**——绝不能从 UI 文件凭空注入 runtime 不认的模型，否则运行时 `getModel()` 拿不到。

---

## 7. 额度/使用量可视化（订阅 vs API 的差异化）

前端在模型选择器上显示每个 provider 的额度状态（会变成绿色/琥珀色/红色的状态点）。

### 7.0 各平台额度接口速查表（真实实现，来自 Pi Web `app/api/model-usage/route.ts`）

每个 provider 走一个**独立的只读 GET 接口**，带 `Bearer` 令牌，单请求超时 12s，服务器端带内存缓存：live 60s / 错误 15s / 静态 5min。

| Provider | 数据源 | scope | reliability | 接口 & 关键字段 | 展示仪表盘 |
|---|---|---|---|---|---|
| `openai-codex` (订阅) | `chatgpt.com/backend-api/wham/usage` | subscription | provider_reported_private | header `Bearer <OAuth>` + `chatgpt-account-id`（从 JWT payload `https://api.openai.com/auth.chatgpt_account_id` 解出）；字段 `rate_limit.primary_window/secondary_window` (`used_percent`→剩余%)、`additional_rate_limits[]`、`credits.balance` | chatgpt.com/codex/settings/usage |
| `kimi-coding` (订阅) | `api.kimi.com/coding/v1/usages` | subscription | official | header `Bearer <OAuth>`；字段 `usage`(每周窗口) + `limits[]`(各周期 limit/used/remaining/resetTime) | kimi.com/code/console |
| `deepseek` (API) | `api.deepseek.com/user/balance` | api_balance | official | header `Bearer <key>`；字段 `balance_infos[]`(currency,total_balance)、`is_available`；is_available=false ⇒ message “余额不足” | platform.deepseek.com/usage |
| `openrouter` (API) | `openrouter.ai/api/v1/key` | api_key_limit | official | header `Bearer <key>`；字段 `data.usage/limit/limit_remaining/limit_reset`；无额度则退化成 spend | openrouter.ai/activity |
| `google-vip`/`kimi-vip`/`omniroute` (网关订阅) | `PI_OMNIROUTE_USAGE_URL` (env) + `?provider=` | gateway_subscription | gateway | GET，可选 `Bearer PI_OMNIROUTE_USAGE_TOKEN`；字段 `metrics[]`(normalize→window/balance/spend)、`plan`、`source` | (env 未配则 unavailable) |

**无公开额度接口的 provider → `unavailable`**（如实文案，绝不编造数字）：

| Provider | message | 跳转 |
|---|---|---|
| `google` (API) | “没有可直接查询剩余额度的接口；请在.Google Cloud / AI Studio 查看项目配额。” | aistudio.google.com/usage |
| `qwen-token-plan-cn` (订阅) | “仅在 Token Plan 控制台展示订阅余量，推理 Key 不能直接查询。” | — |
| `qwen-dashscope-cn` (API) | “没有统一的余额查询端点；可显示调用 token，不能冒充账户余额。” | — |
| `xai` (订阅) | OAuth 无公开订阅余量接口 | console.x.ai |
| `xai-api` (API) | 余额需独立 Management Key，推理 Key 不能查 | console.x.ai |

**额度可信度分级（reliability）**——额度数据的可靠性要随数据一起传进类型系统并展示：

| 等级 | 含义 | 例子 |
|---|---|---|
| `official` | 官方公开稳定 API | Kimi / DeepSeek / OpenRouter |
| `provider_reported_private` | 是厂商返回、但非公开稳定接口，可能变 | OpenAI Codex `/wham/usage` |
| `gateway` | 来自网关（上游聚合） | google-vip/kimi-vip/omniroute |
| `none` | 无数据（unavailable） | google/qwen/xai |

> 前端据此在 tooltip 标注“实时厂商数据；接口不是公开稳定 API”，不把它当作铁定的公开配额。

**通用额度数据契约**（`ProviderModelUsage`）：`status(live/unavailable/auth_error/error)` + `scope(subscription/api_balance/api_key_limit/gateway_subscription/unknown)` + `reliability` + `source` + `plan?` + `metrics[]`（每条 `kind: window/balance/spend`、`used/limit/remaining/remainingPercent/unit/resetsAt`）+ `message?` + `dashboardUrl?`。


**设计要点**：不要用“网关总 token 余额”冒充“固定订阅余量”——那是两个不同概念，会误导用户。没有真接口就诚实标 unavailable，并给出跳转。

### 7.1 额度徽章（每个 Provider 组头显示一个，不逐行）

在**每个 Provider 分组头部**渲染一个胶囊徽章：小圆点 + 简短文字。

```
[Google(订阅)      ● 93%            前 4/9]
```

- **文字**：`93%`、`13.2M`、`余量不可查`；加载中灰色 `额度…`；auth 失效红色 `凭证失效`。
- **颜色**：按阈值绿/琥珀/红（对应 Pi Web 的 `modelUsageText` / `modelUsageColor` / `modelUsageTooltip`）。
- **title-tooltip**：`source · plan` + 每条指标 remaining/used/percent + message + reliability。
- **规则**：provider 未加载时根本不显示徽章；unavailable 只显示 `余量不可查`+链接，绝不造假数字。
- **不要逐行打额度徽章**——大型目录会刷屏；额度属于 Provider 维度。

### 7.2 长模型组折叠（前 4 + 展开）

**未搜索时**，某个 provider 模型数 > 4，则只显示前 4 个，组头给 `前 4/N` 提示，底部给通栏切换按钮：

```
[Google(订阅)      ● 93%            前 4/9]
  Gemini 3.5 Flash (High) (✓ 当前选择)   [Google(订阅)]
  Gemini 3.5 Flash (Low)                [Google(订阅)]
  Gemini 3.1 Flash Lite                 [Google(订阅)]
  Gemini 2.5 Pro                        [Google(订阅)]
[▼ 展开更多 (还有 5 个模型)]
```

点击展开后变 `▲ 折叠收起`；**每次重新打开选择器时把各 Provider 的展开态重置为折叠**。搜索时旁路折叠（直接显示全部匹配项，匹配集本身已变小）。

> 折叠上限和额度徽章都是**前端 UI 关注点**，与排序权重、额度数据层解耦，任一方可独立调整。

## 8. 落地 UI：思考级别选择器 + 成本/额度显示（已存在于 Pi Web，直接复用契约）

这两套 UI 在 Pi Web **已经实现**。做“其它 agent 版本”时按下列契约复刻即可（对齐现有实现，不要重复造）。

### 9.1 思考级别选择器

- 级别列表：`["auto","off","minimal","low","medium","high","xhigh","max"]`（Pi Web 用 `THINKING_LEVELS` 常量）。
- 每个级别的展示文案（`THINKING_LEVEL_DESC`）：`auto:"Use pi default"`、`off:"Reasoning off"`、`minimal:"Minimal reasoning"`、`low:"Low reasoning"`、`medium:"Medium reasoning"`、`high:"High reasoning"`、`xhigh:"Extra-high reasoning"`、`max:"Max reasoning"`。
- **级别可用性**完全由模型驱动（`getSupportedThinkingLevels(model)`）：
  - 非 `reasoning` 模型 → 只有 `["off"]`；
  - 推理模型 → 在 `off..high` 选区上，只要 `thinkingLevelMap[level] !== null`；
  - `xhigh/max` 仅在 `thinkingLevelMap` 里**显式映射**时才可用。
- **下拉 UI**（Pi Web）：按钮显示当前 `thinkingDisplayLabel`；打开后列出 `THINKING_LEVELS`，按 `availableThinkingLevels` 过滤（`auto` 总是保留）；每个选项若 `thinkingLevelMap[lvl]` 映射到了厂商特定值，则显示**映射后的值**并保留原值于 title。
- **实际请求构造**（`ChatInput`）：`const lvl = thinkingLevel ?? "auto"; if (lvl === "auto" || !thinkingLevelMap) return lvl; return thinkingLevelMap[lvl] ?? lvl;`——映射到厂商字符串；`auto` 交给 provider 默认。

### 9.2 成本显示

- models.json 的 `cost` 字段（每百万 token：`input/output/cacheRead/cacheWrite`，可选 `tiers[]`）由 `calculateCost(model, usage)` 求出会话成本（`tiers` 按 `inputTokens > tier.inputTokensAbove` 选档）。
- 会话统计（`AppShell`）显示 `Cost: $X.XXXX`（仅当 `sessionStats.cost > 0`）。
- 每条消息的 usage 格式化（`MessageView` 的 `formatUsage`）：
  ```
  "1,234 in · 567 out · 89 cache · $0.0123"
  input → `${input.toLocaleString()} in`; output → `${output.toLocaleString()} out`;
  cacheRead → `${cacheRead.toLocaleString()} cache`; cost?.total → `$${total.toFixed(4)}`
  ```

### 9.3 额度文案/格式化（额度徽章用）

- `formatTokenCount`：≥1M → `1.2M`；≥1k → `123k`；否则 `1,234`。
- `formatUsageValue(value, unit?)`：`USD`→`$…`，`CNY`→`¥…`，`requests`→`N 次`，`credits`→`N credits`；小数位按绝对值（≥100→0 位，≥1→2 位，否则 4 位）。
- 徽章精简标签：`5 小时`→`5h`、`每周`→`周`、`Spark…`→`Spark`，超 9 字符截断加 `…`。
- `modelUsageText`：加载中→`额度…`，`auth_error`→`凭证失效`，`error`→`获取失败`，`unavailable`→`余量不可查`，否则取百分比/余额的缩略文案。

---

## 9. 落地方案：给“其它 agent”的最小实现清单

要在别的 agent/系统里复刻这套，你需要：

1. **一份 models.json**（§1）——复制你的 `google-vip` / `kimi-vip` 结构，改 `baseUrl` 指向你的网关。
2. **Provider 命名规范**（§2）——订阅/API 分开，统一徽章映射表。
3. **发现路由**（§3）——订阅通道按前缀过滤，绝不造假 ID。
4. **排序器**（§4）——权重表 + 使用频率 + 自然排序，按 provider 分组。
5. **凭据分离**（§5）——目录无密钥。
6. **compat 适配层**（§6）——按开关构造请求体。
7. **额度面板**（§7）——订阅/API 差异化，诚实的 unavailable。

### 通用代码骨架（任意语言）

```
# models.json
{ "providers": { "<provider-id>": {
    baseUrl, api, apiKey?, models: [
      { id:"<gw-prefix>/<model>", name, reasoning, input[], contextWindow, maxTokens, compat{} }
]}}}
```

```
# 排序伪代码
def sort_models(models, usage_counts):
    return sorted(models, key=lambda m: (
        -(_weight(m.id) + min(100, usage_counts[m.id]*10)),  # 高权重在前
        collator(m.name or m.id),
        collator(m.provider),
        collator(m.id),
    ))
```

---

## 10. 常见坑

- **不要把 gweb/网页模拟塞进主力通道**：网页端无 Tool Calling、长上下文崩溃（你已踩过）。
- **订阅 catalog 没更新的模型别硬造**：`antigravity/gemini-3.7-flash` 现在 404（Google 开发者端未开放），直接从网关列表里拿真实的，才能测出 `model_not_found`。
- **权重表别写死成不可配置**：不同 agent 的"主力模型"不同。把优先表放进配置。
- **`input:["text","image"]` 会同时满足文本和图像**；需要纯文本再写 `["text"]`。
- **ID 前缀必须与网关路由一致**：`antigravity/`、`kimi-coding/` 是 OmniRoute 的约定，换网关就换前缀。

---

*文档生成于 pi-web / models.json 现状。落任何其它系统时，以你的网关实际返回的模型 ID 为准。*
