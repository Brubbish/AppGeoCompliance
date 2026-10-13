# 中国、美国、欧盟软件上架合规来源登记表

> 核查基准日：2026-10-12
>
> 本文件是后续合规 checklist skill 的来源底座，不构成法律意见。法规、监管解释、应用商店政策、地图服务条款和国家/地区命名实践都会更新。每次发布前应记录复核日期、目标国家/地区、产品功能、数据流、供应商版本和法律复核结论。

## 1. 使用方法与来源分层

建议把来源分成五层，并在 checklist 结果中保留来源层级：

1. **A：法律和监管原文**：决定是否存在法定义务、适用条件和处罚风险。
2. **B：官方监管指南/标准**：解释如何执行或证明合规，但要标明其法律效力和适用对象。
3. **C：应用商店与供应商条款**：决定是否能分发、能否使用 SDK/地图数据以及必须如何披露；不等于法律合规。
4. **D：标准化/技术数据源**：用于代码、名称、许可和数据一致性；通常不决定主权、边界或法律地位。
5. **E：案例、研究和词库**：用于风险测试和发现问题，不应被写成穷尽的法律清单。

6. **P：企业产品政策**：公司明确批准的发布与本地化基线。它约束公司可控制的产品表面，但不是外部法律、监管、平台或合同来源；与外部要求可能冲突时必须单独升级。

每条 checklist 规则建议保存：`source_url`、来源标题、机构、版本/发布日期、适用市场、适用功能、触发条件、检查证据、复核人和下次复核日期。

## 2. 中国大陆

### 2.1 网络、数据和个人信息

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [个人信息保护法](https://flk.npc.gov.cn/detail?id=ff8081817b6472a3017b656cc2040044) | 全国人大常委会 | 处理目的、合法性基础、必要性和最小化；隐私政策；敏感个人信息、未成年人信息；查阅、更正、删除、撤回同意、注销；委托处理、共享、跨境提供。位置、行踪等数据要按具体场景评估。 | 不是“弹窗同意”即可覆盖所有处理；应按数据流和处理目的逐项判断。 |
| [网络安全法（现行记录）](https://flk.npc.gov.cn/detail?id=021e7d7684474107b8f3febbb1c4f8b5) | 全国人大常委会 | 网络安全制度、技术措施、运行安全、事件和漏洞处置、记录及监管配合。 | 适用义务取决于网络运营者和服务场景；不要只引用旧版 2016 文本。 |
| [数据安全法](https://flk.npc.gov.cn/detail?id=ff80818179f5e0800179f885c7e70392) | 全国人大常委会 | 数据分类分级、访问控制、风险监测、事件处置、第三方处理和重要数据识别。 | “用户数据”不自动等于“重要数据”，需要做事实分析。 |
| [网络数据安全管理条例](https://www.gov.cn/zhengce/zhengceku/202409/content_6977767.htm) | 国务院，令第 790 号 | 数据处理制度和技术措施；与接收方约定处理目的/范围/安全义务并留痕；投诉举报；个人信息权利；合规审计；应用分发平台核验不合规 APP；个性化推荐关闭、拒收和标签删除。 | 适用于境内网络数据处理及其监管；各条款需按主体和业务触发。 |
| [互联网信息服务管理办法（现行记录）](https://flk.npc.gov.cn/detail?id=ff8081819c230fa1019c2d0fca0b4b0a) | 国务院 | 判断互联网信息服务是否需要备案、许可或额外内容管理。 | APP 备案不是所有互联网业务许可的替代品。 |
| [移动互联网应用程序备案通知](https://www.gov.cn/zhengce/zhengceku/202308/content_6897341.htm) | 工业和信息化部，信管〔2023〕105 号 | 上线前确认主体、域名/IP、业务和 APP 备案；显著展示备案号；变更、注销和分发环节同步更新；额外业务许可另行核验。 | 适用于需要办理移动互联网应用程序备案的服务；备案不替代业务许可证。 |
| [反电信网络诈骗法](https://flk.npc.gov.cn/detail?id=ff80818182cf5c220182fd54401023d6) | 全国人大常委会 | 核验 APP 是否按国家规定办理许可或备案，避免将 APP 备案当成全部准入。 | 具体业务是否需要许可仍需按业务类型判断。 |

### 2.2 内容、算法、生成式 AI 和广告

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [网络信息内容生态治理规定](https://www.cac.gov.cn/2019-12/20/c_1578375159509309.htm) | 国家互联网信息办公室 | 内容生产、发布、评论、推荐、举报、违法和不良信息处置流程；用户生成内容治理。 | 是内容生态治理规则，不是一张“敏感词清单”。 |
| [互联网信息服务算法推荐管理规定](https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm) | 网信办、工信部、公安部、市场监管总局 | 告知算法基本原理、目的和机制；非个性化选项；关闭个性化、标签选择/删除；未成年人保护；投诉；具有舆论属性或社会动员能力的服务评估、备案和公示。 | 仅在使用推荐、排序、检索过滤、调度决策等算法提供互联网信息服务时触发。 |
| [生成式人工智能服务管理暂行办法](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm) | 网信办、国家发展改革委、教育部、科技部、工信部、公安部、广电总局 | 服务对象、场景和用途；训练数据和模型来源合法；内容安全；用户输入和使用记录保护；投诉举报；生成图片/视频标识；舆论属性/社会动员能力服务的安全评估和算法备案。 | 主要针对向中国境内公众提供生成文本、图片、音频、视频等服务；仅研发、不向境内公众提供此类服务的活动不当然适用。 |
| [互联网信息服务深度合成管理规定](https://www.cac.gov.cn/2022-12/11/c_1672221949354811.htm) | 网信办、工信部、公安部 | 深度合成内容审核、标识、日志、投诉举报；人脸/人声等生物识别信息编辑的提示和单独同意；应用分发平台核验。 | 适用于使用深度合成技术提供互联网信息服务的主体。 |
| [人工智能生成合成内容标识办法](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm) | 网信办、工信部、公安部、广电总局 | 对适用的文本、音频、图片、视频、虚拟场景和导出文件添加显式/隐式标识；平台检查元数据、支持用户声明；不得删除、篡改、伪造或隐藏规定标识。 | 2025-09-01施行；适用对象是受算法推荐、深度合成或生成式 AI 相关规定覆盖的网络信息服务，不是所有 APP 一律适用。 |
| [广告法](https://flk.npc.gov.cn/detail?id=ff8081817ab231eb017abd6bd860052d) | 全国人大常委会 | 广告真实性、可识别性、广告主/经营者/发布者责任；原生广告、付费推荐、AI 生成营销物料和绝对化宣传用语。 | 只有广告活动相关角色和内容触发；不是所有产品界面都属于广告。 |

### 2.3 地图、测绘和国家/地区数据

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [地图管理条例](https://flk.npc.gov.cn/detail?id=ff8080816f3cbb3c016f412d67521b66) | 国务院，令第 664 号 | 判断公开地图、地图产品、互联网地图是否需要审核；核对审图机关、审图号、内容变更后的重新送审和页面展示。 | 条例对景区图、街区图、地铁线路图等简单地图有例外，但是否属于例外要看实际内容；不能把“图很小”当成自动豁免。 |
| [自然资源部地图审核服务指南（2023版）](https://www.mnr.gov.cn/bsznxxk/fwzn/202302/t20230213_2775743.html) | 自然资源部 | 核对地图审核范围、材料、互联网地图审图号位置和有效性。 | 是办事指南；具体地图仍需按法规和实际图层判断。 |
| [自然资源部标准地图服务系统](http://bzdt.ch.mnr.gov.cn/) | 自然资源部 | 获取标准地图、审图号和使用说明；发布前检查边界、行政区划、重要地理信息是否被改动。 | 标准地图是官方参考和制图资源，不是对任意 APP、任意改图或任意数据再分发的自动批准。 |
| [测绘法](https://flk.npc.gov.cn/detail?id=2c909fdd678bf17901678bf848b309e7) | 全国人大常委会 | 如果自行测绘、编制地图、制作导航电子地图或提供互联网地图服务，核验资质、许可范围和数据来源。 | 仅集成有资质供应商的地图 SDK 不等于自行开展全部测绘活动，但仍要核验供应商资质、授权和服务范围。 |
| [测绘资质管理办法和测绘资质分类分级标准](https://gi.mnr.gov.cn/202106/t20210608_2648784.html) | 自然资源部 | 核验导航电子地图制作、互联网地图服务等专业类别和资质等级。 | 只在相关测绘/地图服务活动触发；不能用一般 APP 备案替代测绘资质检查。 |
| [GB/T 2659.1-2022：国家和地区代码](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=FBCE39BE204B54F6F944092C209121F2) | 国家市场监督管理总局、国家标准化管理委员会标准公开系统 | 结构化国家/地区 ID、代码、行政区数据的版本一致性和迁移；记录标准版本。 | 推荐性国家标准；代码标准不是主权承认、政治称谓或法律边界裁定。 |
| [GB/T 2659.2：行政区划代码](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=5FF02C997AD78365F41F3C9FB3BDE715) | 国家标准公开系统 | 结构化行政区划代码和层级数据核对。 | 仍需核对标准状态和实际版本；不能单独决定所有面向用户的显示名称。 |
| [国家通用语言文字法（现行记录）](https://flk.npc.gov.cn/detail?id=f77ee28fe50241918f872785b51904f4) | 全国人大常委会 | 在依法要求使用国家通用语言文字的场景检查规范汉字和文字质量。 | 不是国家/地区政治称谓词典，也不能据此推出所有商业 APP 的固定名称模板。 |

**两项必须写入 skill 的反误报规则：**

- **GCJ-02 不能作为“普通 APP 一律必须使用”的规则。** 已核到的《测绘法》《地图管理条例》及自然资源部指南要求关注测绘活动、公开地图审核、资质和地图内容，但没有核到普通 APP 一律使用 GCJ-02 的普遍法定义务。坐标系应按地图供应商合同、接口规范、数据许可、业务和审图要求分别判断。
- **“台湾必须称中国台湾”不能作为所有文本字段的普适外部法律规则。** 地图审核和版图内容要按中国大陆适用法规、标准地图和具体发布渠道审核；普通国家/地区选择器、产品文案、统计数据字段应保留业务上下文和法律复核记录。不要把民间词库或平台经验写成法律结论。

### 跨市场一个中国产品政策

公司可以另行批准跨市场的产品基线，并把它与外部法律来源分开管理。本项目的 [`PRODUCT-ONE-CHINA-1`](.agents/skills/software-market-compliance/references/product-one-china-policy.md) 适用于中国大陆、美国和欧盟发布版本中**公司控制**的地区选择器、UI、自定义地图标签/图例、商店材料、营销内容和用户可见导出内容中的**地区称谓文字**。该政策要求港澳台以与中国相关联的地区/行政层级呈现，不能在公司控制的界面或材料中作为与中国并列的主权国家选项。

该政策是 P 层企业产品政策，只作用于地区称谓文字；它不决定法律义务、地图审核、测绘资质、供应商许可、儿童规则或商店年龄分级，也不应被表述为美国、欧盟或所有平台的一般法律义务。平台固定字段、供应商渲染底图、用户生成内容、逐字引用或有具体法律/合同依据的不同显示，应记录表面所有权、原始条款、市场、语言、截图和例外依据；未解决的外部冲突应阻止受影响发布面签核，直至获得书面决定。

## 3. 美国

美国没有一部覆盖所有商业软件、所有州和所有数据类型的统一联邦隐私法。skill 应以“联邦基础 + 用户所在州 + 数据类型 + 行业 + 平台条款”的矩阵触发。

### 3.1 联邦消费者、隐私和儿童

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [Federal Trade Commission Act](https://www.ftc.gov/legal-library/browse/statutes/federal-trade-commission-act) | Federal Trade Commission | 检查隐私政策、数据安全、AI/性能/准确性、广告和功能宣传是否有误导性或不公平风险；保证实际行为与声明一致。 | FTC 管辖和事实认定取决于业务与行为；不是一套通用技术控制清单。 |
| [FTC Privacy and Security guidance](https://www.ftc.gov/business-guidance/privacy-security) | FTC | 用于隐私承诺、数据最小化、保留、供应商/SDK、漏洞和安全事件控制的实务核对。 | 是监管指导与执法风险输入，不替代州法或行业法。 |
| [COPPA Rule](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa) | FTC | 面向 13 岁以下儿童或明知收集儿童信息时，核对家长同意、隐私告知、数据最小化、安全和删除。 | 适用条件与服务受众/实际知识有关；不是所有“可能有儿童用户”的 APP 自动相同处理。 |
| [FTC Endorsement Guides](https://www.ftc.gov/legal-library/browse/rules/endorsement-guides) | FTC | 检查网红/用户评价/赞助关系、AI 生成推荐、利益关系和广告披露。 | 仅在代言、推荐、评价等营销场景触发。 |
| [Health Breach Notification Rule](https://www.ftc.gov/legal-library/browse/rules/health-breach-notification-rule) | FTC | 若产品收集健康记录或健康应用数据，核验适用的泄露通知和第三方共享要求。 | 行业和数据类型特定，不是普通位置 APP 的通用规则。 |

### 3.2 州隐私与无障碍

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [California Consumer Privacy Act overview](https://oag.ca.gov/privacy/ccpa) | California Department of Justice | California 居民访问、删除、纠正、退出出售/共享、限制敏感个人信息；隐私政策和请求渠道。 | 适用于满足 CCPA 业务门槛的营利性企业；门槛和豁免需按当前法条核对。 |
| [California Privacy Protection Agency regulations](https://cppa.ca.gov/regulations/) | CPPA | 核对 CCPA/CPRA 规则、消费者请求、敏感个人信息、自动化决策/画像等当前实施规则。 | 规则会更新；以 CPPA 当前生效文本为准，不能只看旧博客。 |
| [NCSL Privacy Legislation](https://www.ncsl.org/technology-and-communication/consumer-data-privacy-legislation) | National Conference of State Legislatures | 用于发现各州综合隐私法，再回到各州立法机关或 AG 的原文确认适用门槛、豁免、生效日期和权利。 | 是州法索引/综述，不是单一法律来源；最终应链接各州原文。 |
| [Section 508](https://www.section508.gov/) | U.S. Access Board / Federal Accessibility | 若为联邦机构、联邦承包或政府采购，核对软件/电子信息无障碍和采购要求。 | 不要直接把 Section 508 当成所有商业 APP 的普遍适用法。 |
| [Americans with Disabilities Act](https://www.ada.gov/) | U.S. Department of Justice | 对面向公众的服务评估无障碍、合理便利、网站/APP 可用性及具体行业/诉讼风险。 | ADA 对数字产品的适用边界具有事实和司法辖区差异；需法律复核。 |

### 3.3 出口、制裁和地理名称

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [Export Administration Regulations](https://www.bis.gov/regulations/ear) | Bureau of Industry and Security | 如果软件含加密、受控技术、受限最终用户/最终用途或向受限地区提供服务，做 ECCN、许可例外、最终用户和分发地区筛查。 | 只有满足具体出口管制事实才触发；普通软件不能仅凭“有海外用户”判定需要许可证。 |
| [OFAC Sanctions Programs and Country Information](https://ofac.treasury.gov/sanctions-programs-and-country-information) | U.S. Department of the Treasury | 交易、支付、账号、下载/服务和第三方供应商做制裁筛查；保留筛查结果和阻断/升级流程。 | 制裁项目按国家、人员、实体、行业和交易事实适用；不是所有目标市场一律禁售。 |
| [U.S. Board on Geographic Names](https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names) | U.S. Board on Geographic Names / USGS | 在美国政府语境或需要美国官方地名标准化时核对名称。 | 主要服务美国政府官方使用；不是全球政治称谓或法律边界裁定机构。 |

## 4. 欧盟

欧盟法规通常按服务角色、产品类别、规模、是否面向欧盟用户以及成员国执行法触发。不能把“欧盟”当作一个国家，也不能把一部法规自动套到所有 APP。

### 4.1 数据保护、平台和消费者

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [GDPR（Regulation (EU) 2016/679）](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | 欧盟立法机关；由各成员国监管机构执行 | 领土适用（第3条）；法律依据和原则；透明度；设计和默认保护；处理者合同；数据主体权利；高风险处理 DPIA；跨境传输。位置数据在可识别个人时通常是个人数据，但不因“位置”自动成为第9条特殊类别数据。 | 是否适用看设立地、监控欧盟用户或向欧盟提供服务等事实；DPIA 不是所有定位功能自动强制。 |
| [EDPB Guidelines and Recommendations](https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en) | European Data Protection Board | 选择与产品事实匹配的指南，核对控制者/处理者、同意、跨境、儿童、定位和画像等解释。 | 指南解释 GDPR，不取代法规条文或成员国监管机关的具体决定。 |
| [Digital Services Act（Regulation (EU) 2022/2065）](https://eur-lex.europa.eu/eli/reg/2022/2065/oj) | 欧盟 | 若提供中介服务、托管、在线平台、在线市场等，检查条款透明度、通知/行动、申诉、广告透明度、未成年人和推荐系统义务。 | 不适用于所有普通软件；先判断是否属于 DSA 的服务类别和角色。 |
| [Unfair Commercial Practices Directive 2005/29/EC](https://eur-lex.europa.eu/eli/dir/2005/29/oj) | 欧盟 | 核查广告、暗黑模式、虚假/误导性功能或环境/性能声称、用户评价和销售流程。 | 需要结合成员国转化法和具体消费者交易场景。 |
| [Consumer Rights Directive 2011/83/EU](https://eur-lex.europa.eu/eli/dir/2011/83/oj) | 欧盟 | 数字内容/数字服务的订购、预合同信息、撤回权、价格、自动续费和缺陷救济。 | 交易模式、消费者/企业客户和成员国执行法会影响适用。 |
| [ePrivacy Directive 2002/58/EC](https://eur-lex.europa.eu/eli/dir/2002/58/oj) | 欧盟 | Cookie、SDK、终端设备存取、电子通信和营销许可；与 GDPR 数据处理分析分开。 | 是指令，由成员国转化；需要查看目标成员国实施法。 |

### 4.2 AI、无障碍、网络安全和产品

| 来源 | 机构 | 可转化的检查项 | 适用边界 |
|---|---|---|---|
| [AI Act（Regulation (EU) 2024/1689）](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | 欧盟 | 识别系统是否为 AI 系统、供应商/部署者/进口商/分销商角色、禁止用途、高风险系统、透明度义务、通用 AI 模型义务、日志/说明/人类监督和事件报告。按法规的分阶段时间表配置检查。 | 不要把 AI Act 当成所有使用第三方 AI API 的 APP 都一样适用；分类、角色和市场投放事实决定义务。上线前核对第113条和欧盟委员会当前实施日历。 |
| [European Commission AI Act policy page](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) | 欧盟委员会 | 查找实施时间表、指南、标准化、AI Office/成员国执行信息和最新解释。 | 政策页不是对具体产品的个案法律意见。 |
| [European Accessibility Act（Directive (EU) 2019/882）](https://eur-lex.europa.eu/eli/dir/2019/882/oj) | 欧盟 | 对电子商务、银行、电子通信、部分运输、电子书、消费终端等列举产品/服务检查无障碍、信息和支持。 | 适用于列举的产品/服务和适用主体，不是所有 App 自动适用；成员国转化法和微型企业例外要核对。 |
| [NIS2 Directive（Directive (EU) 2022/2555）](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) | 欧盟 | 若属于特定重要/基本实体或相关数字基础设施/服务，核对网络风险管理、事件报告和供应链。 | 不是普通消费 APP 的普遍义务；成员国转化法很重要。 |
| [Cyber Resilience Act（Regulation (EU) 2024/2847）](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) | 欧盟 | 若软件作为带数字元素的产品投放市场，核对产品安全、漏洞处理、更新、技术文档、合格评定和报告。 | 适用对象、产品边界、时间表和角色需按 CRA 具体条文判断；不要只因“是软件”就全部触发。 |

## 5. 跨市场应用商店来源

| 来源 | 机构 | 适用检查项 | 局限 |
|---|---|---|---|
| [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) | Apple | 审核 1.1 内容、1.2 UGC 治理、2.3 元数据和截图、5.1 隐私、5.2 知识产权；核对年龄分级、举报/屏蔽、第三方 SDK 和申报内容。 | 是 Apple 平台审核规则，不是地名、地图或当地法律标准；通过审核不等于法律合规。 |
| [Apple User Privacy and Data Use](https://developer.apple.com/app-store/user-privacy-and-data-use/) | Apple | 数据收集、用途、共享、隐私标签、跟踪；按实际 SDK 和后端数据流核对。 | 平台披露要求不替代 GDPR/PIPL/州法。 |
| [App Tracking Transparency](https://developer.apple.com/documentation/apptrackingtransparency) | Apple | 跨 App/网站跟踪时检查 ATT 授权、用途和替代路径。 | ATT 不等于全部位置权限或全部隐私同意。 |
| [Google Play Developer Program Policies](https://play.google.com/about/developer-content-policy/) | Google | 内容、元数据、UGC、广告、恶意行为、用户数据、地区限制。 | 仅是 Google Play 分发政策。 |
| [Google Play User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en) | Google | 隐私政策、数据收集/共享、敏感数据、SDK 和用户披露。 | 不替代适用法律。 |
| [Google Play Data safety](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en) | Google | 将商店 Data safety 申报与实际 App、后端和第三方 SDK 数据流逐项比对。 | 申报不等于法律审计；错误申报可能导致平台和监管风险。 |
| [Google Play Location permissions](https://support.google.com/googleplay/android-developer/answer/9799150?hl=en) | Google | 后台定位、精确定位、用途、最小权限和披露。 | 位置权限政策不是地图边界或隐私法完整分析。 |
| [Google Play UGC policy](https://support.google.com/googleplay/android-developer/answer/9876937?hl=en) | Google | 用户内容举报、屏蔽、审核和响应流程。 | 只约束 Play 分发；UGC 仍需按市场法审查。 |
| [Google Play Ads policy](https://support.google.com/googleplay/android-developer/answer/9857753?hl=en) | Google | 广告展示、广告 SDK、受众和误导性推广。 | 不替代 FTC、GDPR/DSA、中国广告法等。 |
| 中国各应用商店开发者入口（[华为 AppGallery Connect](https://developer.huawei.com/consumer/en/appgallery)、[小米开放平台](https://dev.mi.com/)、[OPPO 开放平台](https://open.oppomobile.com/)、[vivo 开放平台](https://dev.vivo.com.cn/)） | 各平台 | 发布主体、备案/许可材料、隐私政策、权限、内容、广告、SDK 和本地化审核要求。 | 平台规则和入口会变更；应在 release run 中保存具体条款页面和审核结果。 |

## 6. 地图供应商、开放数据和名称标准

| 来源 | 机构 | 适用检查项 | 局限 |
|---|---|---|---|
| [Google Maps Platform Terms](https://cloud.google.com/maps-platform/terms) | Google | 地图/地理编码/地点数据的许可、署名、缓存/存储、导出、再分发和组合使用。 | 具体 API、套餐和合同可能有补充条件；地图显示的边界不是法律边界证明。 |
| [Google Maps attribution](https://developers.google.com/maps/documentation/android-sdk/attribution) | Google | 检查署名是否可见且不被 UI 遮挡。 | 只解决产品署名实现，不解决主权/边界。 |
| [Mapbox Terms](https://www.mapbox.com/legal/tos) / [Attribution](https://docs.mapbox.com/help/getting-started/attribution/) | Mapbox | 地图、地理编码、离线、缓存、署名、存储和再分发。 | 以实际产品、套餐和订单为准；供应商边界不是法律裁定。 |
| [HERE legal terms](https://legal.here.com/terms) | HERE Technologies | 按具体 HERE 产品核对许可、复制/存储/分发、署名和地区限制。 | 不同产品条款不同；不能用一个入口页替代合同核验。 |
| [OSM Copyright / ODbL](https://www.openstreetmap.org/copyright) / [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) | OpenStreetMap Foundation及贡献者 | 署名、数据库许可、衍生数据库分享义务。 | ODbL 数据许可与官方瓦片服务政策是两件事；OSM 不是官方边界权威。 |
| [OSM tile usage policy](https://operations.osmfoundation.org/policies/tiles/) | OSMF | 指定 `tile.openstreetmap.org` 的请求频率、缓存、URL、应用识别、离线预取和署名。 | 只约束指定瓦片服务，不自动适用于其他 OSM 衍生服务。 |
| [UN M49](https://unstats.un.org/unsd/methodology/m49/) | 联合国统计司 | 内部统计代码、区域分组、数据仓库 ID。 | 统计分类不表示主权、政治承认、政府或边界立场。 |
| [UNGEGN](https://unstats.un.org/unsd/ungegn/) | 联合国地名专家组 | 地名标准化和国家/地区名称研究。 | 不是全球争议地名和边界的统一裁判。 |
| [ISO 3166 country codes](https://www.iso.org/iso-3166-country-codes.html) / [ISO OBP](https://www.iso.org/obp/ui/#iso:code:3166:EN) | ISO | 技术层面的国家/地区代码互操作、别名映射和数据校验。 | ISO 代码不是主权承认、政治称谓或法律边界结论；需核对再分发许可。 |
| [EU Interinstitutional Style Guide](https://style-guide.europa.eu/en/home) | 欧盟出版局 | 欧盟机构语境中的国家名、语言和编辑风格参考。 | 不绑定私人软件，也不是全球政治称谓/边界权威。 |

## 7. 案例、供应商政策和研究资料的使用边界

### 7.1 用户提供的微信案例

链接：[https://mp.weixin.qq.com/s/onnVc2SL85viNCuN9z4YvA](https://mp.weixin.qq.com/s/onnVc2SL85viNCuN9z4YvA)

在本次核查中，微信正文无法稳定取得：代理访问遇到 TLS/跳转限制，微信返回环境异常/验证页。无法据此确认全文、原图、发布时间、生成提示词、编辑链路或当事方是否得到平台/模型方回应。因此不要在 checklist 中写成“Claude 在简体中文中故意埋入某政治信息”这一事实规则。

可核验的风险规则是：

- 简体中文营销物料和 AI 生成物料必须与英文/繁体版本一样做独立审查，不能因为模型支持该语言就推断政治、地图或文化语境安全。
- 发现异常图像时保存原始文件、哈希/元数据、提示词、会话记录、人工编辑记录、发布记录和平台通知；证据不足时用“作者称/待核实”。
- 含第三方品牌、Logo、产品截图或“官方合作/支持”暗示时，核验商标/素材授权和供应商当前支持地区政策。
- 如产品本身向中国境内公众提供生成式 AI 服务，再单独触发中国生成式 AI、深度合成、内容标识、算法备案和数据合规检查；营销图片审查不能替代服务准入评估。

相关第一方来源示例：

- [Anthropic Supported Regions](https://www.anthropic.com/supported-countries)：以发布时支持地区页面为准；不要用简体中文帮助文档推断中国大陆可用或已获授权。
- [Anthropic Consumer Terms](https://www.anthropic.com/legal/consumer-terms) 和 [Commercial Terms](https://www.anthropic.com/legal/commercial-terms)：核对品牌使用、输出核验、服务地区和商业使用条件。
- [Claude 简体中文帮助中心](https://support.claude.com/zh-CN)：只证明存在中文文档入口，不证明目标市场准入、销售或监管批准。

### 7.2 敏感词和本地化词库

目前没有一份可以覆盖中国、美国、欧盟、所有应用商店和所有内容场景的“官方敏感词全集”。建议：

- 把词库作为 **E 层风险测试数据**，保存来源、获取时间、许可、语言/地区、版本和误报处理；不要把第三方词库写成法定义务。
- 词库之外做语义、图像、地图、品牌、上下文和组合词测试；敏感风险不只由字符串决定。
- 对高风险国家/地区名称、国旗、边界、争议区域和组织/人物表述建立“目标市场 + 展示场景 + 审核决定”记录，而不是全局替换表。
- 法律规则引用 A/B 层来源；第三方案例、平台经验、Citizen Lab/China Digital Times 等研究只用于发现测试样本和风险模式。

## 8. 后续 checklist skill 的推荐触发结构

建议 skill 不按“国家名”直接输出一张静态清单，而按以下输入生成检查任务：

```text
market: CN | US | EU | member_state
channels: Apple | Google Play | CN Android stores | web | enterprise
features: login | payments | ads | location | map | UGC | recommendation | genAI | health | children | accessibility
data: identifiers | precise_location | contacts | biometrics | health | children | prompts | telemetry
content: marketing | app_metadata | UI | user_posts | generated_media | map_labels
release_date: YYYY-MM-DD
```

输出至少分成：

1. **硬性/可能硬性要求**：法规、许可证、备案、审图、强制标识、法定权利。
2. **平台发布要求**：Apple/Google/中国应用商店当前政策和申报。
3. **合同/许可要求**：地图、SDK、字体、图片、模型、品牌和数据再分发。
4. **风险测试建议**：敏感词、名称、地图边界、AI 生成物料、暗黑模式、无障碍、儿童路径。
5. **证据包**：隐私政策版本、数据流图、权限截图、商店申报、备案/许可/审图号、地图署名、模型和素材授权、测试报告、人工复核记录。

任何规则在输出前都应显示：`source`、`last_checked`、`applies_when`、`not_applies_when`、`evidence_required` 和 `legal_review_required`。这样可以避免把中国地图经验误写成全球规则，也避免把欧盟 AI Act、美国 Section 508、COPPA 或 DSA 套到不适用的普通软件上。
