# Daily Digest Format

## 1. 输出路径

日报固定输出到：

```text
reports/daily/YYYY/MM/YYYY-MM-DD.md
```

示例：

```text
reports/daily/2026/06/2026-06-02.md
```

## 2. 标题格式

```markdown
# 前沿资讯日报 2026-06-02

06.02
```

## 3. 条目格式

每条必须是一句话摘要 + 来源链接 + 时间展示：

```markdown
1. AWS 发布企业级生成式 AI 平台落地指南，覆盖安全、治理、数据和模型评估架构。来源：[AWS Prescriptive Guidance](https://docs.aws.amazon.com/...)；来源时间：2026-06-02 09:30（北京时间）
```

## 4. 时间展示示例

完整发布时间：

```markdown
1. OpenAI 发布某项产品更新。来源：[OpenAI News](https://openai.com/news/)；来源时间：2026-06-02 09:30（北京时间）
```

只有日期：

```markdown
2. 某研究机构发布 AI 行业年度报告。来源：[State of AI](https://www.stateof.ai/)；来源时间：2026-06-02（来源仅披露日期，北京时间）
```

更新时间：

```markdown
3. AWS 更新企业级 GenAI 平台落地指南。来源：[AWS Prescriptive Guidance](https://docs.aws.amazon.com/...)；来源更新时间：2026-05-20（来源仅披露日期，北京时间）
```

无来源时间：

```markdown
4. 某来源发布 Bedrock Agents 案例文章，但页面未披露发布时间。来源：[AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/...)；来源时间：未披露，抓取时间：2026-06-02 09:30（北京时间）
```

推断时间：

```markdown
5. 某页面 URL 暗示发布日期为 2026-06-02。来源：[Example](https://example.com/2026/06/02/item)；来源时间：推断为 2026-06-02（来源未直接披露）
```

## 5. 必备时间说明

每份日报必须包含：

```markdown
## 时间说明

- “来源时间”优先使用来源页面明确披露的发布时间。
- 若来源只披露日期，则按来源日期展示，不补造具体时分。
- 若来源未披露时间，则展示本系统抓取时间。
- 若时间由 URL 或搜索结果推断，会明确标注“推断”。
```

## 6. 不合格条目

以下条目不合格：

```markdown
1. 某公司发布新模型。
```

原因：没有来源链接，没有来源时间。

```markdown
1. 某公司发布新模型。来源：[Example](https://example.com/)
```

原因：没有来源时间或抓取时间。

```markdown
1. 某公司发布新模型。来源：[Example](https://example.com/)；来源时间：2026-06-02 00:00（北京时间）
```

原因：如果来源只披露日期，不能补造 `00:00`。
