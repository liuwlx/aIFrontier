# Frontier Data Hub Requirement

## 1. 背景

用户希望在 `E:\workerspace\daily` 下建立一个长期维护的前沿数据仓库，用来持续跟踪 AI、科技、企业 GenAI、数据平台、产品发布、架构实践、行业报告和公司战略等信息。

过去的问题是：资讯来源分散，看到后没有结构化沉淀；日报条目容易只有一句话和链接，缺少标准来源时间，后续无法判断信息新鲜度、可信度和追踪价值。

## 2. 目标

- 建立长期目录 `E:\workerspace\daily\frontier-data-hub`。
- 配套 `frontier-news-digest` Codex Skill，支持抓取、归一化、过滤、日报生成和质量校验。
- 所有来源统一使用通用 `source_type` 分类，不为 AWS 单独设计分类。
- 每条日报必须包含一句话摘要、标准来源链接、标准来源时间或抓取时间。
- 时间统一展示为北京时间，不编造来源没有披露的具体时分秒。

## 3. 核心使用场景

### 3.1 每日前沿快讯

每天从配置的数据源中抓取最新条目，按重要性筛选后生成：

```text
reports/daily/YYYY/MM/YYYY-MM-DD.md
```

条目格式：

```markdown
1. AWS 发布企业级生成式 AI 平台落地指南，覆盖安全、治理、数据和模型评估架构。来源：[AWS Prescriptive Guidance](https://docs.aws.amazon.com/...)；来源时间：2026-06-02 09:30（北京时间）
```

### 3.2 长期报告和白皮书追踪

对长期文档、白皮书、架构指南和落地指南，优先关注更新时间。如果来源没有更新时间，再使用发布时间或抓取时间。

### 3.3 知识库沉淀

将高价值来源沉淀到：

```text
knowledge/entities
knowledge/topics
knowledge/trends
knowledge/followups
knowledge/source-guides
```

后续可以扩展为专题报告、趋势图谱和个人研究助手。

## 4. 范围

本期实现：

- 目录结构初始化。
- 来源分类和来源清单配置。
- 来源时间规则文档。
- `frontier-news-digest` Skill。
- 轻量脚本：
  - `crawl_sources.py`
  - `normalize_items.py`
  - `generate_daily.py`
  - `validate_digest.py`

本期不实现：

- 浏览器登录态抓取。
- 付费报告下载。
- 大规模分布式爬虫。
- 自动翻译或大模型摘要 API 调用。
- 定时任务系统。可后续通过 Codex automation、Windows Task Scheduler 或 GitHub Actions 扩展。

## 5. 信息类型

所有来源统一按 `source_type` 分类：

- `executive_insights`
- `data_leader_view`
- `implementation_guides`
- `enterprise_genai_platform`
- `whitepapers`
- `production_architecture_check`
- `ai_ml_practice_blog`
- `product_releases`
- `annual_conference`
- `company_strategy`
- `genai_architecture`

AWS 是重要来源之一，但不是分类体系的中心。其他公司、研究机构、社区、中文科技媒体和咨询机构也使用同一套分类。

## 6. 标准来源时间

每条资讯必须包含以下时间字段：

```json
{
  "published_at": "来源明确披露的发布时间，允许为空",
  "updated_at": "来源明确披露的更新时间，允许为空",
  "fetched_at": "系统抓取时间，必填",
  "inferred_at": "从 URL、列表页或上下文推断的时间，允许为空",
  "time_display": "日报直接展示的时间文本，必填",
  "time_display_type": "published_at | updated_at | inferred_at | fetched_at",
  "time_confidence": "high | medium | low"
}
```

时间展示优先级：

```text
published_at -> updated_at -> inferred_at -> fetched_at
```

长期文档类来源可优先使用 `updated_at`。

## 7. Normalized Item Schema

标准归一化数据结构：

```json
{
  "id": "2026-06-02_aws_ml_blog_0001",
  "title": "AWS 发布企业级生成式 AI 平台落地指南",
  "summary": "AWS 发布企业级生成式 AI 平台落地指南，覆盖安全、治理、数据和模型评估架构。",
  "provider": "AWS",
  "source_name": "AWS Prescriptive Guidance",
  "source_type": "implementation_guides",
  "source_url": "https://docs.aws.amazon.com/prescriptive-guidance/latest/enterprise-ready-generative-ai-platform/welcome.html",
  "published_at": "2026-06-02T09:30:00+08:00",
  "updated_at": null,
  "fetched_at": "2026-06-02T10:15:00+08:00",
  "inferred_at": null,
  "time_display": "2026-06-02 09:30（北京时间）",
  "time_display_type": "published_at",
  "time_confidence": "high",
  "topic": "enterprise_genai_platform",
  "entities": ["AWS", "Generative AI Platform"],
  "importance": "high",
  "business_relevance": "high",
  "architecture_relevance": "high",
  "product_relevance": "medium",
  "dedupe_key": "aws_enterprise_genai_platform",
  "status": "accepted"
}
```

## 8. 验收标准

- `config/source_types.yaml` 包含 11 个通用来源类型。
- `config/sources.yaml` 每个来源包含 `time_extraction`。
- `docs/source-time-rules.md` 存在并说明发布时间、更新时间、抓取时间、推断时间。
- `skills/frontier-news-digest/references/source-time-rules.md` 存在。
- 日报每条包含来源 Markdown 链接和时间展示。
- 日报包含 `## 时间说明`。
- 校验脚本能发现缺来源、缺时间、缺时间说明的问题。
- 不编造具体时间，不把来源仅披露日期伪装成精确时间。
