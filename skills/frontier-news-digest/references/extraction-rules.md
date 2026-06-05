# Extraction Rules

## 1. Raw Crawl

For each configured source:

- Fetch the configured URL.
- Prefer `--fetch-candidates` so article/detail pages are available for reading.
- Save raw payload under `data/raw/YYYY/MM/DD`.
- Record provider, source name, source type, source URL, status code, fetched time, and extraction notes.
- A single source failure must not stop the whole run.

## 2. Time Extraction Order

Try these fields:

- HTML meta: `article:published_time`, `article:modified_time`, `datePublished`, `dateModified`.
- JSON-LD: `datePublished`, `dateModified`.
- RSS/API: `published`, `pubDate`, `updated`.
- Visible text patterns: `Published`, `Updated`, `YYYY-MM-DD`, `YYYY年M月D日`.
- URL date patterns as `inferred_at` only.

## 3. Normalization

Every normalized item should contain:

- `id`
- `title`
- `summary`
- `provider`
- `source_name`
- `source_type`
- `source_url`
- `published_at`
- `updated_at`
- `fetched_at`
- `inferred_at`
- `time_display`
- `time_display_type`
- `time_confidence`
- `topic`
- `entities`
- `importance`
- `business_relevance`
- `architecture_relevance`
- `product_relevance`
- `dedupe_key`
- `status`

## 4. Article Reader Summary

Title-only summaries are not valid final digest summaries.

Before `generate_daily.py`, run:

```powershell
python .\skills\frontier-news-digest\scripts\read_articles.py --date YYYY-MM-DD
```

The reader output must include:

- `article_summary`
- `why_it_matters`
- `action_hint`
- `reader_status`
- `reader_ran_at`
- `summary_source`

If no model summarizer is available, the fallback reader may create an extractive summary from readable article text, but it must still record reader status and evidence fields. It must not silently use the title as the final summary.

## 5. Rejection

Write rejected records to `data/rejected` when:

- Missing URL.
- Missing title and no usable page title.
- Irrelevant to configured topics.
- Duplicate URL already seen.
- Missing Article Reader record before final digest generation.
