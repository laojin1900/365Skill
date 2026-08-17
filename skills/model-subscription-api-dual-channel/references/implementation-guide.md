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

---

## 7. 额度/使用量可视化（订阅 vs API 的差异化）

前端在模型选择器上显示每个 provider 的额度状态（会变成绿色/琥珀色/红色的状态点）：

| Provider 类型 | 数据来源 | unavailable 提示文案 |
|---|---|---|
| OpenAI Codex (订阅) | 官方 `/wham` quota | 实时余量 |
| Kimi Coding (订阅) | Kimi quota 接口 | 实时余量 |
| DeepSeek / OpenRouter (API) | 各自 balance 接口 | 实时余额 |
| **google-vip / kimi-vip (网关订阅)** | **网关只读 quota** | `unavailable`（如实说"网关未提供上游只读 quota；不会用网关 token 余额冒充订阅余量"） |
| 原生 Google API | 无公开余额接口 | 引导去 AI Studio 看配额 |

**设计要点**：不要用"网关总 token 余额"冒充"固定订阅余量"——那是两个不同概念，会误导用户。没有真接口就诚实标 unavailable，并给出跳转。

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

---

## 8. 落地方案：给"其它 agent"的最小实现清单

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

## 9. 常见坑

- **不要把 gweb/网页模拟塞进主力通道**：网页端无 Tool Calling、长上下文崩溃（你已踩过）。
- **订阅 catalog 没更新的模型别硬造**：`antigravity/gemini-3.7-flash` 现在 404（Google 开发者端未开放），直接从网关列表里拿真实的，才能测出 `model_not_found`。
- **权重表别写死成不可配置**：不同 agent 的"主力模型"不同。把优先表放进配置。
- **`input:["text","image"]` 会同时满足文本和图像**；需要纯文本再写 `["text"]`。
- **ID 前缀必须与网关路由一致**：`antigravity/`、`kimi-coding/` 是 OmniRoute 的约定，换网关就换前缀。

---

*文档生成于 pi-web / models.json 现状。落任何其它系统时，以你的网关实际返回的模型 ID 为准。*
