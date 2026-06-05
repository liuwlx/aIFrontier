# AIFrontier

每日 AI 前沿技术资讯聚合 Pipeline。自动爬取 27+ 全球 AI 来源 → Claude Code Agent 阅读正文 → 生成中文日报。

## Pipeline 架构

```
config/ → crawl → data/raw/ → normalize → data/normalized/
    → Article Reader Agent → data/agent-readings/
    → generate → reports/daily/ → validate
```

## 数据来源

**国际：** OpenAI, Anthropic, Google DeepMind, NVIDIA, Meta, Hugging Face, AWS, Microsoft, a16z, McKinsey, Stanford HAI

**中文：** 量子位, IT之家, 机器之心, 新浪财经, 中国信通院

## 每日自动化

服务器 crond 每日 9:57 CST 自动执行全流程：
1. 爬取 27+ 源 → 2. 标准化 → 3. AI Agent 阅读正文并生成中文摘要 → 4. 生成 Markdown 日报 → 5. 验证 → 自动推送到 GitHub

## 目录

| 目录 | 内容 |
|------|------|
| `config/` | 源配置、话题分类、筛选规则 |
| `skills/` | Pipeline 脚本和参考文档 |
| `data/raw/` | 爬虫原始 HTML |
| `data/normalized/` | 标准化条目 JSONL |
| `data/agent-readings/` | AI Agent 阅读结果 |
| `reports/daily/` | 每日中文 Markdown 日报 |
| `docs/` | 操作指南和架构文档 |

## 环境要求

- Python 3.11+ with `pyyaml`
- Claude Code CLI (for Article Reader Agent)
- crond (for daily automation)
