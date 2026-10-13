---
name: software-market-compliance
description: 检查软件、网站、移动应用或 AI 产品面向中国大陆、美国或欧盟发布时的国家地区称谓、法律监管触发项、地图地理信息、年龄与儿童问题。用户提到上架、市场合规、地区称谓、地图、儿童、年龄分级、APP 备案或发布前审查时使用。
---

# Software Market Compliance

对项目做范围有限、证据驱动的发布前检查，只覆盖：

1. 国家/地区称谓
2. 法律监管触发项
3. 地图与地理信息
4. 年龄、儿童与年龄分级

不要扩展为通用安全扫描、供应链审计、出口管制、无障碍审计或全面广告合规检查。

## 输入

只需要目标市场。优先读取项目根目录的 `compliance-input.yaml`：

```yaml
markets:
  - cn-mainland
  - us
  - eu
```

支持 `cn-mainland`、`us`、`eu`。若文件不存在，只询问目标市场；不要要求开发者预先填写功能、数据类型、渠道或法律适用结论。对于欧盟，若成员国会影响结论，再在对应检查项询问目标成员国。

## 两轨检查流程

两轨都是必需的，不可只运行扫描器然后结束。

### Track 1: Python 候选扫描

在 skill 目录运行：

```bash
python scripts/run_checks.py --project-root /path/to/project --input compliance-input.yaml --format markdown
```

没有输入文件时：

```bash
python scripts/run_checks.py --project-root /path/to/project --markets cn-mainland us eu --format markdown
```

需要机器可读 JSON 时用 `--format json`；`--format both --output compliance-report.md` 会同时写 Markdown 和 JSON。

扫描器只做轻量规则匹配，输出 `candidate`、`not_detected` 或 `scan_incomplete`，用于定位文件、代码行、配置和来源。它不会给出最终法律、平台或合同判断。退出码只表示扫描是否成功，不表示合规结论。

### Track 2: 模型代码审查

扫描后必须逐项执行 [`references/code-review-checklist.md`](code-review-checklist.md)，即使脚本没有命中也要完成。独立检查项目代码、配置、依赖、调用路径和实际用户流程，不能把脚本结果复述一遍当作代码审查。

阅读并按市场选择 [`references/source-registry.json`](source-registry.json) 中的官方法律、监管、平台或合同来源。对适用规则说明触发条件；对代码事实引用具体文件、行号或配置。若证据在后端、构建产物、商店提交材料或供应商合同中而当前仓库不可见，应标记为待确认/无法检查，并向开发者提出具体问题。

## 结果语义

脚本结果和模型审查结果必须分开：

- **扫描器状态**：`candidate`、`not_detected`、`scan_incomplete`。
- **模型审查状态**：`confirmed_issue`、`candidate`、`not_found`、`not_reviewable`。

模型只有在目标市场、规则适用条件、实现行为和证据都足够明确时，才可报告 `confirmed_issue`。结论还要标明类型：法律要求、应用商店政策或供应商合同。该结论是基于可见材料的模型审查，不等于监管机构、法院或律师的正式认定。

不确定时不猜测，列出：已发现事实、无法确认的原因、缺失证据和开发者需要回答的问题。`not_detected` / `not_found` 只表示当前扫描/审阅范围内未发现问题，不代表整个产品全面合规。

## 反误报约束

- 不把敏感词词库当成穷尽的法律词表。国家/地区名称、旗帜、地图或争议地区静态命中只是一条线索。
- 不把“台湾必须称中国台湾”或其他单一政治称谓硬编码为所有 UI、市场和数据字段的普遍要求；按目标市场、展示位置、上下文和可引用规则审查。
- 不因没有 GCJ-02 就判定中国大陆违法；坐标系需结合数据源、供应商规范、地图业务和审核事实判断。
- 不因发现地图 SDK 就断言需要审图或测绘资质；需检查公开展示、图层、服务角色、供应商材料及可能的例外。
- 不假设欧盟各成员国有统一儿童同意年龄阈值。
- 不因发现 AI、UGC、推荐、儿童相关关键词就自动断言备案、许可、DSA、AI Act 或 COPPA 适用。
- 不因扫描器没有命中就跳过代码检查。

## 输出

最终结果必须包括：

1. **明确问题**：模型代码审查后成立的具体问题；逐项写市场、问题类型、实现证据、来源及整改建议。
2. **需开发者确认**：描述已观察到的事实和待确认问题。
3. **无法检查**：列出不可见的后端、运行时行为、最终截图/商店申报、合同或目标成员国等证据缺口。
4. **扫描器候选**：保留候选 ID 和位置，并说明模型复核后是确认、保留候选还是未发现。
5. **范围说明**：写明检查了哪些文件和未能覆盖哪些构建产物或市场材料。

每个目标市场在四个检查域中都必须有模型审查状态；不适用的项目说明不适用原因。不要用脚本退出码或零候选报告作为合规结论。

## 文件说明

- `rules/naming.json`：国家/地区称谓候选模式。
- `rules/regulation.json`：备案、AI/深度合成、隐私声明、UGC、GDPR/DSA/AI Act 相关信号。
- `rules/maps.json`：地图供应商、署名、公开地图、边界、坐标和离线数据线索。
- `rules/age.json`：年龄门槛、儿童、家长同意和商店年龄分级线索。
- `scripts/`：Track 1 候选扫描器和 Markdown/JSON 报告器。
- `references/code-review-checklist.md`：Track 2 必须完成的逐项代码审查清单。
- `references/source-registry.json`：来源 ID、URL、机构、核查日期和适用边界。
- 项目根目录的 `compliance-source-registry.md`：完整的人类可读研究底稿。
