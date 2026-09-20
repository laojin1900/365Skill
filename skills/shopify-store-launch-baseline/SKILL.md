---
name: shopify-store-launch-baseline
description: "Shopify 店铺从零到「看起来像真店、上手即可运营」的上线基线全流程，提炼自 knightlynails.com 一次完整整备（主题修复/品牌资产/合规政策/内容体系/后台核对 5 个阶段，每个坑都带根因与修法）。覆盖：Theme Access 部署通道、推送纪律、商品卡与 PDP 画廊修复、品牌图资产兜底接线、政策四件套、联系表单、页脚双菜单、Hero 轮播 split 布局、智能合集、品牌故事页、指南博客体系、双层 FAQ、后台运营核对清单。凡新店上线、老店整备、或评估「这个店还缺什么」时先加载本技能。"
whenToUse: Shopify 店铺上线、整备、验收，或需要把一套裸主题变成可运营店铺时；也适用于给其他服务/客户的店铺做出厂交付。
---

# Shopify 店铺上线基线（裸主题 → 可运营真店）

本技能沉淀自 knightlynails.com 一次完整整备（DS Nails 主题 + Shopify 店铺，从「商品卡样式错乱、无政策页、无联系表单、首页全占位符」到基线可运营）。**总原则：每个阶段都按「修主题 → 构建 → 精确推送 → curl 验证 → 截图亲眼看」闭环，不看不算完成。**

## 0. 阶段顺序（依赖关系决定的，不要乱）

```
1. 通道与备份      → 没有它后面都是空谈
2. 主题基线修复    → 商品卡/PDP 是转化主战场，先修 bug
3. 品牌资产        → favicon/logo/分享图/OG，一次接线永久生效
4. 合规与信任      → 政策页/联系表单/页脚，缺失直接掉转化
5. 内容体系        → 让店"看起来像真店"：轮播/合集/故事/指南/FAQ
6. 后台运营核对    → 非主题项，店主必须亲自确认（清单见 §7）
```

## 1. 通道与权限

- **首选部署通道：Theme Access 密码**。Partners 设备码授权经常撞「don't have access to this dev store」（CLI 只认 Partner 组织成员）。让有后台权限的人在店铺装官方 **Theme Access** 应用 → Create password（形如 `shptka_xxx`）→ `export SHOPIFY_CLI_THEME_TOKEN=...` 后 `shopify theme push/pull --store <shop>` 即可，与账号体系无关。
- **店铺 myshopify 域名不知道时**：`curl -s https://<域名> | grep -o 'Shopify.shop = "[^"]*"'`。
- **推任何东西之前先备份**：`shopify theme pull --theme <id> --path /tmp/backup`，并 `diff -rq` 确认线上与本地构建产物的差异——线上有商家在主题编辑器里的改动，全量推会清掉。**永远用 `--only <file>` 精确推送**，尤其是 JSON 模板和 settings_data。
- **CLI 设备码授权注意**：账号选择器第一项≠正确账号，必须按名字选。

## 2. 推送与验证纪律（每次推送都走这五步）

1. 改源码 → 构建（`ds-theme build`，产物在 dist）。
2. `diff` 待推文件 vs 线上备份，确认增量只有你的改动。
3. `shopify theme push --theme <id> --allow-live --only <每个文件>`。
4. **静默失败排查**：CLI 显示成功但页面没变时，立刻 `--verbose` 看有没有 `<file>: failure`。已知原因见 §8。
5. `curl -s <页面> | grep` 验证 HTML/CSS 落地 + 浏览器截图亲眼看。**字符串断言看不见嵌套，看过才算数。**

## 3. 主题基线修复清单（模板级，照单检查）

- **商品卡**：hover 浮层按钮（quickview 等）必须相对**图片容器**定位而不是整张卡——包一层 `media-wrap { position: relative }`，否则按钮盖住标题/价格。缩略图比例用参数化（合集页 `ratio: '1/1'`）。
- **白底产品图一律 `object-fit: contain`**（cover 会把横构图两侧内容切掉）；卡片/PDP/弹窗统一。
- **PDP 画廊**：`<img>` 的 `width/height` 属性必须写**真实尺寸**（`media.preview_image.width/height`），硬编码错误比例会让未加载的 lazy slide 预留错误空间，主图下方出现大空档。
- **hover 切换第二图**：用 `:has(.img--hover)` 判断存在性，否则单图商品 hover 时主图淡出成空白。
- **商家自填的标题不要接 `t` 过滤器**（`settings.heading | default: 'key' | t` 会把商家文案当翻译键 → "Translation missing"）。先判空再翻。
- **多行 textarea 不要继承单行输入的全圆角**（`--ds-radius-input: full` 只适配单行）。
- **OG/Twitter Card**：`theme.liquid` 加 `og:site_name/url/title/type/description/image` + `twitter:card`，图片链 `page_image → 主题自带 share-image.png(1200×628)`。

## 4. 品牌资产（打进主题 assets，模板兜底接线）

模式统一：**主题自带默认图放 `assets/`，模板里写「商家设置 > 主题资产」的兜底链**——商家后台传图自动覆盖，新装店铺开箱即有。

- `favicon.png`（512²）、`logo.png`（横版字标）、`share-image.png`（1200×628）——代码生成即可（Pillow + 品牌 token 配色 + 系统字体，本店用赤陶甲片图标 + Optima）。
- header：`settings.logo → assets/logo.png`；favicon 同理；OG image：`page_image → assets/share-image.png`。
- **场景/配图类内容位同理**：image-with-text 未传图时用 `assets/craft-scene.jpg`（真实产品图拼贴合成，白框圆角卡片 + 柔影 + 品牌色点缀）。
- 社媒链接：主题 settings 预留 Instagram/Facebook/TikTok/YouTube/Pinterest URL 字段，页脚按设置渲染图标；上线时先填平台首页占位，店主后续换真实账号。

## 5. 合规与信任（A 级优先级）

- **政策四件套**（Settings → Policies）：refund/privacy/terms 用 Shopify「Insert from template」生成后按业务改（**注意删 `[INSERT RETURN ADDRESS]` 占位**）；shipping 无官方模板需手写（写清：生产周期、免邮门槛、时效、追踪、关税、错地址责任）。四个 `/policies/*` 都要 200，结账页底部会自动引用。
- **联系表单**：`{% form 'contact' %}` section + `page.contact.json` 模板。Shopify 惯例：**handle 为 `contact` 的页面自动套用 page.contact 模板**；其他模板（如 faq）需在页面侧栏手动指派。
- **页脚**：菜单拆两列（Quick links / Policies），`footer-group.json` 出厂带 menu+newsletter blocks；栅格按块数响应式（4 块时宽屏四列、≤1200px 两列）。
- **店铺 SEO**：Online Store → Preferences 填 Home page title（≤70 字符）+ Meta description（≤320）。

## 6. 内容体系（"看起来像真店"的关键）

- **Hero 轮播 ≥3 张**：2 产品 + 1 品牌故事。滑块支持**选产品取图**（image_picker > product.featured_image 兜底，免上传）。**白底产品图用 split 布局（左文右图 contain），不要全幅 cover**（4:3 图 cover 成宽幅会裁成局部特写）。
- **智能合集**：New arrivals（条件 `Price > 0`，排序 Newest）+ Best sellers（同条件，排序 Best selling）。合集创建在 Products → Collections → Add condition（右侧 Products 卡，不是中间预览区）。
- **首页系列行**：两个 featured-collection section 分别挂这两个合集，消灭 "Example product" 占位符。
- **品牌故事页**：后台 Pages 建页（TinyMCE 填入技巧见 §8），主菜单加入口。
- **指南体系**：建 Guides 博客 + 4 篇核心指南（佩戴教程/尺码测量/卸除复用/甲型长度，内容与店铺政策、尺码表逐值一致）。首页 `blog-posts` section 出卡片区；文章配图走 `ds-guide-image` snippet（文章 featured image > handle 映射主题资产）。
- **双层 FAQ**：首页 6 问 + "View full FAQ →" 链到 FAQ 页；**PDP 底部加"Before you choose your set"**（能戴多久/选错尺码/破损错发/复用定制）。FAQ section 带 FAQPage JSON-LD。
- **页脚 Quick links** 挂：Our Story / FAQ / Guides / Contact。

## 7. 后台运营核对清单（非主题，必须店主确认）

- [ ] 配送费率与公告栏承诺一致（如"满 $50 免邮"必须有对应 shipping 规则）
- [ ] 退款政策删除 `[INSERT RETURN ADDRESS]` 占位
- [ ] 隐私政策按实际业务补充（邮箱/地区法规）
- [ ] 税务 / Markets / 币种策略
- [ ] 订单通知邮件品牌化、发件邮箱（非 myshopify 域）
- [ ] Cookie/GDPR 横幅（Settings → Customer privacy）
- [ ] 社媒占位链接换成真实账号
- [ ] Social sharing image（Online Store → Preferences，可选，主题 og 兜底已覆盖）

## 8. 坑位速查（都是实测踩出来的）

| 坑 | 根因 → 修法 |
|---|---|
| 推送显示成功但页面没变 | `themeFilesUpsert` 静默拒绝——`--verbose` 看 `failure`。**schema option label 限 50 字符** |
| 推 JSON 后自定义 setting 消失 | Shopify 会剥离 schema 未注册的 setting——**先推 section(schema) 再推 JSON 模板** |
| snippet 里 `article.handle` 匹配不上 | 它带博客前缀（`guides/slug`）——用 `handle \| split: '/' \| last` |
| 后台 TinyMCE 填长文失败/格式乱 | 用**单换行**分段（双换行会生成空 `<p><br></p>`）；fill 报"无法验证值"是正常的（编辑器会改写），先看内容再决定 |
| CodeMirror(Show HTML) fill 不上 | 放弃，回 TinyMCE 普通模式填 |
| 菜单 Link 校验不过 | 粘**完整 URL** 后**按 Enter** 确认（相对路径不收）；或从建议下拉选 |
| 误点 Discard 丢改动 | 菜单编辑页顶栏 Discard/Save 相邻，点 Save 前先看一眼；删项后必须 Save 才生效 |
| `page.contact` 模板没生效 | handle 为 contact 自动套用；其他 suffix（faq 等）要在页面侧栏 Theme template 手动选 |

## 9. 上线验收清单（最后一遍，逐项 curl/截图）

- [ ] 合集页：hover 商品卡按钮不压标题价格；缩略图正方形不裁内容
- [ ] PDP：画廊无空档、变体/数量/ATC 正常、PDP FAQ 出现
- [ ] 首页：轮播 3 张（split）、新品/热卖两行真实商品、场景图文、指南卡、FAQ、订阅、四列页脚
- [ ] `/policies/*` ×4 = 200；`/pages/contact` 有表单；`/pages/faq` 有问答；`/blogs/guides` 有文章
- [ ] 页头 logo、favicon、OG 标签（`curl | grep og:`）、社媒图标
- [ ] 主菜单含 Our Story；页脚 Quick links + Policies 双列
