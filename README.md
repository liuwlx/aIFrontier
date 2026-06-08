# AIFrontier

AIFrontier 是一个面向 AI 前沿技术资讯的自动化日报 Pipeline。项目会从全球 AI 信息源抓取内容，标准化为结构化数据，再通过 Claude Code Agent 阅读正文、提炼中文摘要，并生成每日 Markdown 日报。

这个仓库适合用来持续跟踪大模型、AI Agent、RAG、企业级 GenAI 平台、AI 治理、云厂商产品更新、研究机构观点和产业趋势。简单说，不用每天在信息海里“撒网捞鱼”，Pipeline 会先把鱼打上来，再帮你把刺挑了。

## 核心能力

- **多来源采集**：聚合 OpenAI、Anthropic、Google DeepMind、NVIDIA、Meta、Hugging Face、AWS、Microsoft、a16z、McKinsey、Stanford HAI 等国际来源，以及量子位、IT之家、机器之心、新浪财经、中国信通院等中文来源。
- **结构化处理**：将原始页面、文章元信息和抓取结果标准化，便于后续筛选、归档和生成报告。
- **Agent 阅读正文**：调用 Claude Code Agent 阅读文章正文，生成中文摘要、要点和判断。
- **中文日报生成**：自动输出 Markdown 格式的每日 AI 前沿技术日报。
- **自动化运行**：支持通过服务器 `crond` 定时执行全流程，并将结果推送回 GitHub。

## Pipeline 架构

```text
config/
  ↓
crawl
  ↓
data/raw/
  ↓
normalize
  ↓
data/normalized/
  ↓
Article Reader Agent
  ↓
data/agent-readings/
  ↓
generate
  ↓
reports/daily/
  ↓
validate
  ↓
GitHub
```

流程说明：

1. **配置数据源**：在 `config/` 中维护来源、话题分类、优先级和抓取频率。
2. **抓取原始内容**：将网页、元信息和正文内容保存到 `data/raw/`。
3. **标准化条目**：清洗并统一字段格式，输出到 `data/normalized/`。
4. **Agent 阅读**：让 Article Reader Agent 阅读正文，输出摘要与分析到 `data/agent-readings/`。
5. **生成日报**：根据标准化数据和 Agent 阅读结果，生成 `reports/daily/` 下的 Markdown 日报。
6. **结果校验**：校验日报结构、数据完整性和输出格式。
7. **自动推送**：由定时任务自动提交并推送到 GitHub。

## 目录结构

| 目录 | 说明 |
| --- | --- |
| `config/` | 数据源配置、话题分类、筛选规则、优先级和抓取频率 |
| `skills/` | Pipeline 脚本、执行逻辑和参考文档 |
| `data/raw/` | 爬虫抓取的原始 HTML、页面内容或中间文件 |
| `data/normalized/` | 标准化后的资讯条目，通常用于后续生成和分析 |
| `data/agent-readings/` | Claude Code Agent 阅读正文后的结构化结果 |
| `reports/daily/` | 每日中文 Markdown 日报输出目录 |
| `docs/` | 操作指南、架构说明和维护文档 |

## 数据来源

当前数据源覆盖国际和中文两个方向。

### 国际来源

- OpenAI
- Anthropic
- Google DeepMind
- NVIDIA
- Meta
- Hugging Face
- AWS
- Microsoft
- a16z
- McKinsey
- Stanford HAI

### 中文来源

- 量子位
- IT之家
- 机器之心
- 新浪财经
- 中国信通院

数据源的具体 URL、来源类型、优先级、抓取频率、话题标签和时间字段提取策略维护在 `config/` 下的配置文件中。

## 环境要求

- Python 3.11+
- `pyyaml`
- Claude Code CLI，用于 Article Reader Agent 阅读文章正文
- `crond`，用于服务器每日自动化调度
- Git，用于提交和推送生成结果

## 使用方式

### 1. 克隆仓库

```bash
git clone https://github.com/liuwlx/aIFrontier.git
cd aIFrontier
```

### 2. 准备 Python 环境

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml
```

### 3. 配置 Agent 运行环境

确保服务器或本地环境已经安装并登录 Claude Code CLI。Article Reader Agent 依赖 Claude Code CLI 读取正文并生成中文分析结果。

### 4. 执行 Pipeline

项目脚本集中在 `skills/` 目录中。建议按照 Pipeline 顺序执行：

```text
crawl → normalize → Article Reader Agent → generate → validate
```

如果仓库中提供了一键脚本或调度脚本，优先使用对应脚本执行完整流程。

## 每日自动化

服务器通过 `crond` 在每天 **09:57 CST** 自动执行全流程：

```text
爬取 27+ 数据源
  → 标准化资讯条目
  → Article Reader Agent 阅读正文并生成中文摘要
  → 生成 Markdown 日报
  → 校验输出结果
  → 自动提交并推送到 GitHub
```

建议在定时任务中记录日志，便于排查网络波动、来源页面结构变化、Agent 调用失败或日报生成异常等问题。

## 输出产物

| 产物 | 位置 | 用途 |
| --- | --- | --- |
| 原始抓取内容 | `data/raw/` | 便于回溯原始页面和调试抓取逻辑 |
| 标准化条目 | `data/normalized/` | 作为日报生成和后续分析的结构化输入 |
| Agent 阅读结果 | `data/agent-readings/` | 保存正文摘要、关键信息和分析判断 |
| 每日 Markdown 日报 | `reports/daily/` | 面向阅读和归档的最终输出 |

## 配置说明

数据源配置通常包含以下字段：

- `provider`：来源机构或平台
- `source_name`：来源名称
- `source_type`：来源类型，例如产品发布、研究观点、技术博客、架构指南等
- `url`：抓取入口地址
- `priority`：优先级
- `crawl_frequency`：抓取频率
- `topics`：话题标签
- `language`：内容语言
- `access`：访问方式
- `time_extraction`：发布时间或更新时间提取策略

新增数据源时，建议同步补充话题标签和时间字段策略，否则后面生成日报时容易“菜都买回来了，发现没贴价签”。

## 维护建议

- 定期检查数据源页面结构是否变化。
- 对高价值来源设置更高优先级和更高抓取频率。
- 保留原始数据，方便复盘抓取或摘要质量问题。
- 对日报输出做格式校验，避免自动化推送无效报告。
- 如果 Agent 输出质量下降，优先检查正文抽取质量、Prompt 和输入长度。

## 适用场景

- 每日 AI 技术趋势跟踪
- 企业 GenAI / Agent / RAG 技术雷达
- 云厂商 AI 产品更新观察
- AI 治理、架构、实施指南归档
- 中文 AI 日报自动生成

## License

当前仓库尚未声明 License。如需对外复用或分发，建议补充明确的开源许可证。