# AppGeoCompliance

## 项目出发点

软件准备进入新市场时，风险不只来自功能本身，也可能藏在国家和地区名称、地图及边界展示、隐私和内容监管、儿童用户与年龄分级中。相同的代码、文案或地图素材，在不同市场可能受到不同规则或平台要求约束。

本项目希望把这些发布前检查整理成一个可由 agent 使用的 skill。目标不是自动替代律师或监管判断，而是帮助开发团队更早发现需要检查的代码和材料，提供来源和证据，并把无法确定的事项明确交回开发者确认。

本项目的地区称谓检查包含一项跨市场的公司产品政策：[`PRODUCT-ONE-CHINA-1`](.agents/skills/software-market-compliance/references/product-one-china-policy.md)。它要求中国大陆、美国和欧盟发布版本中由产品控制的地区称谓遵循批准的中国关联地区层级。该政策只作用于地区称谓文字，不决定法律义务、地图审核、测绘资质、供应商许可、儿童规则或商店年龄分级；法律监管、地图与年龄/儿童仍分别按目标市场判断。该政策是公司的产品立场，不声称美国或欧盟法律统一强制相同措辞；平台固定字段、供应商地图标签或具体外部要求如产生冲突，会单独标记并升级处理。

目前聚焦四个领域：

- **国家/地区称谓**：检查界面、语言包、商店资料和地图中的名称及使用上下文。
- **法律监管问题**：根据产品实际功能识别可能触发的备案、隐私、AI、内容治理等要求。
- **地图与地理信息**：检查地图服务、数据来源、署名、边界和中国大陆地图审核相关事项。
- **年龄与儿童**：检查目标受众、年龄门槛、家长流程、未成年人数据和商店年龄分级。

首批目标市场是中国大陆、美国和欧盟。欧盟成员国要求存在差异的地方，会要求进一步确认目标国家。

## 如何使用

在已加载本项目 skill 的 agent 中打开或指向本项目，然后说明目标市场并让它开始检查即可。例如：

> 请读取这个项目，按合规检查 skill 检查准备上架中国大陆、美国和欧盟的版本。先扫描，再按 checklist 阅读代码；不确定的事项列出来让我确认。

也可以只指定一个市场，例如：

> 请检查这个项目准备上架中国大陆时的地区称谓、监管、地图和年龄问题。

Agent 会读取本项目的 [`SKILL.md`](.agents/skills/software-market-compliance/SKILL.md)，运行轻量扫描脚本，再按 [`模型代码审查 checklist`](.agents/skills/software-market-compliance/references/code-review-checklist.md) 独立检查代码。通常不需要开发者预先整理完整的功能或数据清单；开始检查只需明确目标市场，检查过程中缺少的事实再逐项询问。

如果 agent 没有自动加载 skill，可以显式调用 `software-market-compliance`，或让 agent 先阅读上述 `SKILL.md` 再开始检查。

## 检查方式

检查分两条轨道：

1. **轻量扫描**：Python 脚本根据规则查找可能相关的文案、配置、权限、SDK 和代码片段，提供候选位置。扫描结果只是线索，不是合规结论。
2. **模型代码审查**：Agent 必须按四个检查领域阅读实现、调用路径和用户流程；即使扫描没有命中，也要完成 checklist。证据不足时，说明缺少什么并请开发者确认。

最终报告会区分模型审查确认的问题、待确认的候选、未发现问题和无法检查的部分，并附上代码证据与来源。未发现问题不代表整个产品已被证明合规。

## 项目资料

- [跨市场一个中国产品政策](.agents/skills/software-market-compliance/references/product-one-china-policy.md)：公司产品基线、默认名称映射和外部冲突升级流程。
- [Skill 使用说明](.agents/skills/software-market-compliance/SKILL.md)：Agent 的检查流程和判断边界。
- [模型代码审查 checklist](.agents/skills/software-market-compliance/references/code-review-checklist.md)：四个领域的必查项目。
- [候选扫描规则](.agents/skills/software-market-compliance/rules)：供轻量扫描使用的规则。
- [来源登记数据](.agents/skills/software-market-compliance/references/source-registry.json)：规则引用的来源 ID 和适用边界。

## 注意事项

法规、监管指南、商店政策和供应商条款会更新。项目来源登记表提供核查入口和适用边界，但每次实际发布仍应复核当前有效版本。地区称谓、地图边界、法律适用范围、产品受众和合同许可都依赖具体上下文；Agent 的输出用于辅助检查和整理证据，不构成法律意见或监管批准。
