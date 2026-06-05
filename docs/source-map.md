# Source Map

## 1. 首批来源策略

首批来源以一手官方来源、工程实践博客、行业报告和中文科技媒体为主。AWS 作为重点样例覆盖较多信息类型，但分类体系对所有来源通用。

## 2. AWS / Amazon

| provider | source_name | source_type | url | 用途 |
|---|---|---|---|---|
| AWS | AWS Executive Insights | `executive_insights` | https://aws.amazon.com/executive-insights/ | 高管和行业洞察 |
| AWS | AWS CDO Agenda | `data_leader_view` | https://aws.amazon.com/data/cdo-report/ | 数据负责人视角 |
| AWS | AWS Prescriptive Guidance | `implementation_guides` | https://docs.aws.amazon.com/prescriptive-guidance/ | 落地指南 |
| AWS | Enterprise-ready GenAI Platform | `enterprise_genai_platform` | https://docs.aws.amazon.com/prescriptive-guidance/latest/enterprise-ready-generative-ai-platform/welcome.html | 企业 GenAI 平台 |
| AWS | AWS Whitepapers | `whitepapers` | https://aws.amazon.com/whitepapers/ | 白皮书 |
| AWS | AWS Well-Architected Generative AI Lens | `production_architecture_check` | https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/welcome.html | 生产级架构检查 |
| AWS | AWS Machine Learning Blog | `ai_ml_practice_blog` | https://aws.amazon.com/blogs/machine-learning/ | AI/ML 实战博客 |
| AWS | AWS News Blog | `product_releases` | https://aws.amazon.com/blogs/aws/ | 产品发布 |
| AWS | AWS re:Invent | `annual_conference` | https://reinvent.awsevents.com/ | 年度大会 |
| Amazon | Amazon Shareholder Letters | `company_strategy` | https://ir.aboutamazon.com/annual-reports-proxies-and-shareholder-letters/default.aspx | 公司战略 |
| AWS | AWS GenAI Architecture | `genai_architecture` | https://aws.amazon.com/architecture/generative-ai/ | GenAI 架构 |

## 3. 国际 AI 公司和云厂商

| provider | source_name | source_type | url |
|---|---|---|---|
| OpenAI | OpenAI News | `product_releases` | https://openai.com/news/ |
| OpenAI | OpenAI Research | `ai_ml_practice_blog` | https://openai.com/research/ |
| Anthropic | Anthropic News | `product_releases` | https://www.anthropic.com/news |
| Anthropic | Anthropic Research | `ai_ml_practice_blog` | https://www.anthropic.com/research |
| Anthropic | Anthropic Economic Index | `executive_insights` | https://www.anthropic.com/economic-index |
| Google DeepMind | Google DeepMind Blog | `ai_ml_practice_blog` | https://deepmind.google/discover/blog/ |
| Google | Google AI Blog | `ai_ml_practice_blog` | https://research.google/blog/ |
| Google Cloud | Google Cloud Blog AI | `ai_ml_practice_blog` | https://cloud.google.com/blog/topics/ai-machine-learning |
| Google Cloud | Google Cloud Architecture Center | `genai_architecture` | https://cloud.google.com/architecture |
| Microsoft | Microsoft AI Blog | `executive_insights` | https://blogs.microsoft.com/ai/ |
| Microsoft | Azure AI Blog | `ai_ml_practice_blog` | https://techcommunity.microsoft.com/category/azure-ai-services/blog/azure-ai-services-blog |
| Microsoft | Microsoft WorkLab | `executive_insights` | https://www.microsoft.com/en-us/worklab |
| NVIDIA | NVIDIA Blog | `product_releases` | https://blogs.nvidia.com/ |
| NVIDIA | NVIDIA Technical Blog | `ai_ml_practice_blog` | https://developer.nvidia.com/blog/ |
| NVIDIA | NVIDIA GTC | `annual_conference` | https://www.nvidia.com/gtc/ |
| Meta | Meta AI Blog | `ai_ml_practice_blog` | https://ai.meta.com/blog/ |
| Meta | Meta Engineering Blog | `ai_ml_practice_blog` | https://engineering.fb.com/ |
| Hugging Face | Hugging Face Blog | `ai_ml_practice_blog` | https://huggingface.co/blog |
| Hugging Face | Hugging Face Papers | `whitepapers` | https://huggingface.co/papers |

## 4. 研究机构、咨询机构和投资机构

| provider | source_name | source_type | url |
|---|---|---|---|
| Stanford HAI | Stanford AI Index | `whitepapers` | https://hai.stanford.edu/ai-index |
| State of AI | State of AI Report | `whitepapers` | https://www.stateof.ai/ |
| a16z | a16z AI | `executive_insights` | https://a16z.com/category/ai/ |
| McKinsey | QuantumBlack AI Insights | `executive_insights` | https://www.mckinsey.com/capabilities/quantumblack/our-insights |
| Deloitte | Deloitte Applied AI | `implementation_guides` | https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence.html |
| Menlo Ventures | Menlo Ventures AI Perspectives | `executive_insights` | https://menlovc.com/perspective/ |
| CB Insights | CB Insights AI Research | `executive_insights` | https://www.cbinsights.com/research/artificial-intelligence/ |

## 5. 中文科技和行业来源

| provider | source_name | source_type | url |
|---|---|---|---|
| IT之家 | IT之家 | `product_releases` | https://www.ithome.com/ |
| 机器之心 | 机器之心 | `ai_ml_practice_blog` | https://www.jiqizhixin.com/ |
| 量子位 | 量子位 | `ai_ml_practice_blog` | https://www.qbitai.com/ |
| 36氪 | 36氪 | `executive_insights` | https://36kr.com/ |
| 新浪财经 | 新浪财经科技 | `product_releases` | https://finance.sina.com.cn/tech/ |
| 中国信通院 | 中国信通院 | `whitepapers` | http://www.caict.ac.cn/ |
| CNNIC | CNNIC | `whitepapers` | https://www.cnnic.net.cn/ |

## 6. 后续扩展建议

- 对 RSS 友好的来源优先接入 RSS。
- 对官网列表页先抓取标题、链接、发布时间，再进入详情页提取元数据。
- 对社区来源先做低频扫描，避免噪音污染日报。
- 对报告类来源单独生成 `reports/source-briefs`，避免日报过度展开。
