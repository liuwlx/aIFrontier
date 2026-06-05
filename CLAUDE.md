# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

frontier-data-hub is a daily AI/tech frontier news aggregation pipeline. It crawls configured sources, normalizes items, uses an Article Reader Agent to read full article bodies and produce Chinese summaries, then generates and validates a Chinese Markdown daily digest report.

## Commands

All scripts live under `skills/frontier-news-digest/scripts/` and expect to be run from the repo root. Python 3.11+ with `pyyaml` is required.

```powershell
# ── Pipeline Orchestrator (recommended) ──
# Run all Python stages (1→2→4→5) with status tracking
python .\skills\frontier-news-digest\scripts\pipeline.py --date 2026-06-05

# Check pipeline state for today
python .\skills\frontier-news-digest\scripts\pipeline.py --date 2026-06-05 --status

# Run only crawl + normalize (skip if already done)
python .\skills\frontier-news-digest\scripts\pipeline.py --date 2026-06-05 --stages 1-2 --skip-if-done

# ── Individual Stage Scripts ──
# Crawl sources (source pages + candidate detail pages)
python .\skills\frontier-news-digest\scripts\crawl_sources.py --limit 12 --items-per-source 5 --fetch-candidates

# Normalize raw crawl records into JSONL
python .\skills\frontier-news-digest\scripts\normalize_items.py --date 2026-06-02

# (Optional) Local extractive reading — for diagnostics only, NOT for the official digest
python .\skills\frontier-news-digest\scripts\read_articles.py --date 2026-06-02

# Generate the daily digest Markdown (reads from data/agent-readings/)
python .\skills\frontier-news-digest\scripts\generate_daily.py --date 2026-06-02

# Validate a generated digest
python .\skills\frontier-news-digest\scripts\validate_digest.py --date 2026-06-02
```

## Pipeline Architecture

The pipeline has five stages, each producing data at a specific path:

```
config/                    → YAML configs (sources, source_types, topics, filters, digest)
  ↓ crawl_sources.py
data/raw/YYYY/MM/DD/*.json → one JSON file per fetched page (source pages + candidate detail pages)
  ↓ normalize_items.py
data/normalized/YYYY/MM/YYYY-MM-DD.jsonl   → accepted items
data/rejected/YYYY/MM/YYYY-MM-DD.jsonl     → rejected items
  ↓ Article Reader Agent (reads raw JSON html fields, runs per data/raw/ file)
data/agent-readings/YYYY/MM/YYYY-MM-DD.article-reader-agent.jsonl → official reader output
  ↓ generate_daily.py
reports/daily/YYYY/MM/YYYY-MM-DD.md → final Chinese Markdown digest
  ↓ validate_digest.py
(validation report to stdout)
```

**Critical architectural rule:** The pipeline enforces a hard separation between local extractive scripts and the Article Reader Agent. `read_articles.py` is a local extractive script that can be used for development diagnostics but its output (`data/readings/`) must **never** feed the final digest. Only `data/agent-readings/` — populated by a real Article Reader Agent (a Claude Code sub-agent) — is valid input for `generate_daily.py`.

## Article Reader Agent

This is the most important architectural constraint. Before running `generate_daily.py`, each candidate article must be read by a real Article Reader Agent:

1. Locate the article's raw JSON file under `data/raw/YYYY/MM/DD/`.
2. Spawn a sub-agent using the prompt in `skills/frontier-news-digest/references/article-reader-agent-prompt.md`.
3. The agent reads the `html` field from the raw JSON and returns a structured Chinese JSON result.
4. Write that result to `data/agent-readings/YYYY/MM/YYYY-MM-DD.article-reader-agent.jsonl`.

Every valid digest item requires: `reader_status = read`, `reader_agent = Article Reader Agent`, `summary_source = article_reader_agent`, `reading_quality` in `high | medium`, and non-empty `article_summary`, `why_it_matters`, `action_hint`.

## Source Time Rules (non-negotiable)

Every item in the final digest must include a source time. The time display priority chain is:

- **Blogs/news/releases:** `published_at` → `updated_at` → `inferred_at` → `fetched_at`
- **Long-lived docs (whitepapers, guides, architecture):** `updated_at` → `published_at` → `inferred_at` → `fetched_at`

Forbidden actions:
- Never fabricate `HH:mm` when a source only discloses a date.
- Never present fetched-at time as publication time.
- Never present inferred time (from URL) as explicit source time.
- Always convert recognizable foreign timezones to Beijing time (UTC+8).

## Config Files

| File | Purpose |
|------|---------|
| `config/sources.yaml` | 27+ sources from AWS, OpenAI, Anthropic, Google, NVIDIA, Meta, HuggingFace, Stanford, a16z, McKinsey, and Chinese tech media |
| `config/source_types.yaml` | 11 universal source types (not AWS-specific) |
| `config/topics.yaml` | Topic taxonomy with bilingual keywords |
| `config/filters.yaml` | Accept/reject keyword filters and priority rules |
| `config/digest.yaml` | Digest generation settings: timezone, output paths, required fields, validation rules |

## Run State

- `runs/state/crawl_state.json` — last crawl summary (attempted/succeeded/failed counts)
- `runs/state/source_health.json` — per-source health (last attempt, status, error)
- `runs/state/seen_urls.json` — previously seen URLs for dedup
