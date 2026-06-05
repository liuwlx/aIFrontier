# Operating Guide

## 1. 日常使用

进入仓库：

```powershell
cd E:\workerspace\daily\frontier-data-hub
```

抓取来源和候选详情页：

```powershell
python .\skills\frontier-news-digest\scripts\crawl_sources.py --limit 12 --items-per-source 5 --fetch-candidates
```

归一化数据：

```powershell
python .\skills\frontier-news-digest\scripts\normalize_items.py --date 2026-06-02
```

启动 Article Reader Agent 阅读文章并生成概要：

```text
使用 skills/frontier-news-digest/references/article-reader-agent-prompt.md。
优先每篇文章启动一个 Article Reader Agent，或者给同一个 Article Reader Agent 分配小批量 raw JSON 文件。
Agent 必须读取 data/raw/YYYY/MM/DD 下本地 raw JSON 的 html 字段。
正式输出必须写入 data/agent-readings/YYYY/MM/YYYY-MM-DD.article-reader-agent.jsonl。
本地脚本只能做抓取、归一化、校验和日报排版，不能冒充 Article Reader。
```

生成日报：

```powershell
python .\skills\frontier-news-digest\scripts\generate_daily.py --date 2026-06-02
```

校验日报：

```powershell
python .\skills\frontier-news-digest\scripts\validate_digest.py --date 2026-06-02
```

## 2. 推荐工作流

1. 更新 `config/sources.yaml`，补充新来源。
2. 运行抓取脚本，确认 `data/raw` 有数据。
3. 运行归一化脚本，确认 `data/normalized/YYYY/MM/YYYY-MM-DD.jsonl` 有数据。
4. 为候选文章启动 Article Reader Agent，读取本地 raw HTML。
5. 确认 `data/agent-readings/YYYY/MM/YYYY-MM-DD.article-reader-agent.jsonl` 有数据。
6. 生成日报。
7. 校验日报。
8. 将高价值条目沉淀到 `knowledge`。

## 3. 添加来源

每个来源必须包含：

```yaml
provider: "AWS"
source_name: "AWS Machine Learning Blog"
source_type: "ai_ml_practice_blog"
url: "https://aws.amazon.com/blogs/machine-learning/"
priority: "high"
crawl_frequency: "daily"
topics:
  - bedrock
  - rag
  - agents
language: "en"
access: "public"
time_extraction:
  preferred_fields:
    - "published_at"
    - "updated_at"
    - "article_meta_time"
  fallback: "fetched_at"
```

## 4. 阅读质量检查

生成日报前要重点检查：

- 每条是否有 `article_summary`。
- 每条是否有 `why_it_matters`。
- 每条是否有 `action_hint`。
- 每条是否有 `reader_status` 和 `reader_ran_at`。
- `reader_agent` 是否为 `Article Reader Agent`。
- `summary_source` 是否为 `article_reader_agent`。
- 是否还有标题原样进入概要。
- 是否还有本地抽取脚本结果混入正式 reader 输出。

## 5. 时间质量检查

生成日报后要重点检查：

- 每条是否有来源链接。
- 每条是否有来源时间、来源更新时间、推断时间或抓取时间。
- 来源只有日期时是否没有补造时分。
- 英文来源是否在可识别时区时转换为北京时间。
- 未披露时间的来源是否写了抓取时间。

## 6. 后续自动化建议

后续可增加：

- Windows Task Scheduler 每天定时运行抓取和归一化。
- Codex automation 定期触发 Article Reader Agent 任务。
- RSS/API 专用抓取器。
- Playwright 动态页面抓取器。
- 每周/每月趋势报告。

注意：自动化只能调度 Article Reader Agent，不能用本地抽取脚本替代阅读阶段。

## 7. 故障处理

如果抓取失败：

- 查看 `runs/logs`。
- 查看 `runs/state/source_health.json`。
- 单个来源失败不应影响整体日报。
- 失败来源应在 `source_health.json` 中记录最近错误和时间。

如果阅读失败：

- 查看 `data/agent-readings` 中 `reader_status = blocked` 的条目。
- 优先为高价值来源增加详情页抓取、RSS/API 或 Playwright 解析。
- 不要把标题当作最终概要。
- 不要用本地脚本“抽一段文字”替代 Article Reader Agent。

如果日报校验失败：

- 优先检查缺失 Article Reader 输出、来源链接或时间字段的条目。
- 不要手动编造来源时间。
- 如果来源确实没有披露时间，使用抓取时间并明确说明。
