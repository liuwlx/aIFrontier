# Source Policy

## 1. Source Principles

- Prefer first-party sources over second-hand summaries.
- Prefer pages with explicit publication or update time.
- Prefer sources that provide actionable AI, data, product, architecture, strategy, or implementation value.
- Treat AWS as a rich provider, not as the classification model.
- Classify every source with the common `source_type` taxonomy.

## 2. Required Source Config

Every source in `config/sources.yaml` must include:

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

## 3. Priority

Use `high` for sources that are first-party, strategically important, or directly useful for product and architecture decisions.

Use `medium` for useful sources that require filtering.

Use `low` for exploratory or noisy sources.

## 4. Rejection Rules

Reject or downrank items when:

- No source URL is available.
- No useful AI/tech/product/data/architecture signal exists.
- The item is promotional noise without implementation or strategic value.
- Time cannot be verified and the content is not important enough to preserve with fetched time.
