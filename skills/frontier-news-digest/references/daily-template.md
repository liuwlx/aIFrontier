# Daily Template

```markdown
# 前沿资讯日报 {date}

{mm}.{dd}

## 概要说明

- 本日报条目必须经过 Article Reader Agent 阅读正文后生成，不直接把标题或列表页摘要当成正文概要。
- 每条快讯包含正文概要、为什么重要、行动启发、来源链接和来源时间。
- 若来源未披露发布时间，会展示本系统抓取时间；不会编造具体发布时间。

{items}

## 时间说明

- “来源时间”优先使用来源页面、RSS/API 或可核验元数据中明确披露的发布时间。
- 若来源只披露日期，则按来源日期展示，不补造具体时分。
- 若来源未披露时间，则展示本系统抓取时间。
- 若时间由 URL、列表页或搜索结果推断，会明确标注“推断”。
```

Item format:

```markdown
1. **{title}**
   - 概要：{article_summary}
   - 为什么重要：{why_it_matters}
   - 行动启发：{action_hint}
   - 来源：[{source_name}]({source_url})；{time_display}；阅读状态：{reader_status}；阅读质量：{reading_quality}
```
