# Source Taxonomy

## 1. 设计原则

`source_type` 是通用信息类型，不绑定某个 provider。AWS、OpenAI、Anthropic、Google、Microsoft、NVIDIA、Meta、Hugging Face、咨询机构、中文科技媒体、行业协会和社区来源都使用同一套分类。

分类的目标不是给来源贴品牌标签，而是回答：

- 这条信息能帮助我理解什么？
- 它更适合进入日报、专题研究、架构检查、产品跟踪，还是战略判断？
- 后续应该由什么 Skill 或研究流程消费？

## 2. 通用来源类型

| source_type | 中文标签 | 适合内容 | 典型用途 |
|---|---|---|---|
| `executive_insights` | 高管/行业洞察 | CEO、CTO、CPO、首席科学家、行业负责人观点 | 判断战略方向、组织变化、行业共识 |
| `data_leader_view` | 数据负责人视角 | CDO、数据平台负责人、数据治理负责人观点 | 理解数据平台、数据治理、数据产品落地 |
| `implementation_guides` | 落地指南 | 实施手册、迁移指南、最佳实践、参考路径 | 转化为产品需求、架构清单、执行步骤 |
| `enterprise_genai_platform` | 企业 GenAI 平台 | 企业级 GenAI 平台、Agent 平台、AI Studio、MLOps/LLMOps 平台 | 研究平台能力边界和产品化路径 |
| `whitepapers` | 白皮书 | 研究报告、技术白皮书、行业报告 | 建立方法论和长期知识库 |
| `production_architecture_check` | 生产级架构检查 | Well-Architected、生产检查清单、可靠性/安全/成本框架 | 做架构评审、上线检查、生产风险分析 |
| `ai_ml_practice_blog` | AI/ML 实战博客 | 工程实践、模型评测、RAG、Agent、训练/推理优化案例 | 抽取实战经验和工程模式 |
| `product_releases` | 产品发布 | 新产品、新模型、新功能、API 更新 | 跟踪能力变化、竞品动态、机会窗口 |
| `annual_conference` | 年度大会 | re:Invent、GTC、Build、Google Cloud Next、DevDay 等 | 总结年度路线、生态变化、重大发布 |
| `company_strategy` | 公司战略 | 财报、股东信、战略文章、组织路线、生态合作 | 判断企业长期方向和商业模式 |
| `genai_architecture` | GenAI 架构 | RAG、Agent、多模态、评估、安全、治理、部署架构 | 形成架构范式和系统设计模板 |

## 3. 分类注意事项

- 同一个 provider 可以有多个来源，每个来源配置一个主 `source_type`。
- 同一个条目可以通过 `topics` 和 `entities` 记录更细粒度主题。
- 如果来源既像博客又像产品发布，优先按条目本身的主要价值分类。
- 如果来源是长期指南，优先关注 `updated_at`。
- 如果来源是新闻、博客或发布稿，优先关注 `published_at`。

## 4. 推荐优先级

高优先级来源通常满足至少两个条件：

- 一手来源。
- 能披露产品、模型、平台或战略变化。
- 能给出可落地架构或操作指南。
- 能反映企业实际采用路径。
- 能帮助建立可复用方法论。

低优先级来源通常满足以下特征：

- 二手转述且无原始链接。
- 标题党或缺少可核验信息。
- 与 AI、数据、产品、架构、科技前沿无关。
- 时间、来源、作者都不可核验。
