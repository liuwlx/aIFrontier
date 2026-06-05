# Source Time Rules

## 1. Time Fields

Every normalized item must include:

- `published_at`: explicit source publication time, nullable.
- `updated_at`: explicit source update time, nullable.
- `fetched_at`: system fetch time, always required.
- `inferred_at`: date/time inferred from URL, list page, or search result, nullable.
- `time_display`: final digest time text, always required.
- `time_display_type`: `published_at | updated_at | inferred_at | fetched_at`.
- `time_confidence`: `high | medium | low`.

## 2. Display Priority

Default:

```text
published_at -> updated_at -> inferred_at -> fetched_at
```

Long-lived docs, whitepapers, architecture checks, implementation guides:

```text
updated_at -> published_at -> inferred_at -> fetched_at
```

News, releases, blogs:

```text
published_at -> updated_at -> inferred_at -> fetched_at
```

## 3. Display Text

Full source publication time:

```text
来源时间：YYYY-MM-DD HH:mm（北京时间）
```

Date only:

```text
来源时间：YYYY-MM-DD（来源仅披露日期，北京时间）
```

Updated time:

```text
来源更新时间：YYYY-MM-DD HH:mm（北京时间）
```

No source time:

```text
来源时间：未披露，抓取时间：YYYY-MM-DD HH:mm（北京时间）
```

Inferred time:

```text
来源时间：推断为 YYYY-MM-DD（来源未直接披露）
```

## 4. Forbidden

- Do not invent hour/minute/second.
- Do not convert date-only source times into exact datetimes.
- Do not label an unconverted foreign time as Beijing time.
- Do not present fetched time as publication time.
- Do not present inferred time as explicit source time.
