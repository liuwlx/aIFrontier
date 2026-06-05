# Source Time Rules

## 1. 为什么来源时间重要

日报不是普通收藏夹。每条快讯都必须回答：

- 这条信息来自哪里？
- 来源在什么时候披露？
- 如果来源没有披露时间，本系统是什么时候抓到的？
- 这个时间是否可核验，还是推断？

没有来源时间的条目不能进入合格日报。

## 2. 时间字段定义

| 字段 | 中文名 | 含义 | 是否必填 | 置信度 |
|---|---|---|---|---|
| `published_at` | 发布时间 | 来源页面、RSS/API、结构化数据或正文明确写出的首次发布时间 | 来源有则必填 | high |
| `updated_at` | 更新时间 | 来源页面、RSS/API、结构化数据或正文明确写出的更新或最后修改时间 | 来源有则必填 | high |
| `fetched_at` | 抓取时间 | 本系统抓到该条内容的时间 | 必填 | high |
| `inferred_at` | 推断时间 | 从 URL、列表页、搜索结果或上下文推断的时间 | 可选 | medium/low |

## 3. 展示优先级

默认优先级：

```text
published_at -> updated_at -> inferred_at -> fetched_at
```

长期文档、白皮书、架构指南、落地指南优先级：

```text
updated_at -> published_at -> inferred_at -> fetched_at
```

产品发布、新闻、博客优先级：

```text
published_at -> updated_at -> inferred_at -> fetched_at
```

## 4. 日报展示规则

来源有完整发布时间：

```text
来源时间：2026-06-02 09:30（北京时间）
```

来源只有日期：

```text
来源时间：2026-06-02（来源仅披露日期，北京时间）
```

来源有更新时间但无发布时间：

```text
来源更新时间：2026-06-02 09:30（北京时间）
```

来源无时间：

```text
来源时间：未披露，抓取时间：2026-06-02 09:30（北京时间）
```

时间从 URL、列表页或搜索结果推断：

```text
来源时间：推断为 2026-06-02（来源未直接披露）
```

来源时区不可识别：

```text
来源时间：2026-06-02（来源未披露时区）
```

## 5. 禁止事项

- 不得编造来源没有披露的具体时分秒。
- 来源只披露日期时，不得写成 `00:00`。
- 英文来源时间未转换前，不得直接标注为北京时间。
- 推断时间不得伪装成来源明确披露时间。
- 抓取时间不得伪装成发布时间。

## 6. 可接受的时间来源

- HTML metadata：`article:published_time`、`article:modified_time`、`datePublished`、`dateModified`。
- JSON-LD：`datePublished`、`dateModified`。
- RSS/API：`published`、`pubDate`、`updated`。
- 正文明确时间：例如 `Published Jun 2, 2026`、`2026年6月2日`。
- 列表页明确时间。
- URL 中清晰日期，仅可作为 `inferred_at`。

## 7. 校验规则

每条 normalized item 必须满足：

- `fetched_at` 非空。
- `time_display` 非空。
- `time_display_type` 属于 `published_at | updated_at | inferred_at | fetched_at`。
- `time_confidence` 属于 `high | medium | low`。

每条日报必须满足：

- 包含 `来源：[...] (...)` Markdown 链接。
- 包含 `来源时间`、`来源更新时间`、`抓取时间` 或 `推断为`。
- 日报末尾包含 `## 时间说明`。
