# Quality Rules

## 1. Digest Validation

A daily digest is valid only if:

- Every numbered item has a Markdown source link.
- Every numbered item has source time, source update time, inferred time, or fetched time.
- Every numbered item has Article Reader Agent output:
  - `概要`
  - `为什么重要`
  - `行动启发`
  - `阅读状态`
- The report contains `## 概要说明`.
- The report contains `## 时间说明`.
- No item uses a fabricated exact time.
- No item uses a title-only summary as the final digest summary.
- No item uses a local extractive script as official reader output.

## 2. Reader Validation

Every item entering the final digest must have:

- `reader_status = read`
- `reader_agent = Article Reader Agent`
- `reading_quality` in `high | medium`
- `reader_ran_at`
- `article_summary`
- `why_it_matters`
- `action_hint`
- `summary_source = article_reader_agent`
- `summary_language = zh-CN`

## 3. Normalized Item Validation

Required time fields:

- `source_url`
- `source_name`
- `published_at`
- `updated_at`
- `fetched_at`
- `inferred_at`
- `time_display`
- `time_display_type`
- `time_confidence`

Allowed `time_display_type`:

- `published_at`
- `updated_at`
- `inferred_at`
- `fetched_at`

Allowed `time_confidence`:

- `high`
- `medium`
- `low`

## 4. Failure Handling

- If source time is absent, use fetched time and say it is fetched time.
- If exact time is not available, keep date-only display.
- If source timezone cannot be determined, mark timezone unknown.
- If Article Reader Agent cannot read the item, exclude it from the final digest.
- If validation fails, do not call the digest complete.
