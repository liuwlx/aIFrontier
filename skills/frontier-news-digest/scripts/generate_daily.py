#!/usr/bin/env python
"""Generate a Chinese daily digest from real Article Reader Agent records only."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


BJ_TZ = timezone(timedelta(hours=8))
IMPORTANCE_RANK = {"high": 0, "medium": 1, "low": 2}
QUALITY_RANK = {"high": 0, "medium": 1, "medium-high": 1, "low": 2}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def today_bj() -> date:
    return datetime.now(BJ_TZ).date()


def parse_date_arg(value: str | None) -> date:
    if not value:
        return today_bj()
    return datetime.strptime(value, "%Y-%m-%d").date()


def agent_readings_path(root: Path, day: date) -> Path:
    return root / "data" / "agent-readings" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.article-reader-agent.jsonl"


def daily_path(root: Path, day: date) -> Path:
    return root / "reports" / "daily" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.md"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def clean_text(text: str | None, max_len: int = 320) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    text = text.replace("x facebook linkedin instagram twitch youtube podcasts email", "").strip()
    if len(text) > max_len:
        return text[: max_len - 3].rstrip() + "..."
    return text


def sentence(text: str | None, max_len: int = 420) -> str:
    text = clean_text(text, max_len=max_len)
    if not text:
        return "待确认。"
    if text[-1] in "。！？!?":
        return text
    return text + "。"


def date_only(display: str) -> bool:
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", display or ""))


def source_time_clause(item: dict[str, Any]) -> str:
    display = clean_text(item.get("time_display"), max_len=120)
    display_type = item.get("time_display_type")

    if not display:
        return "来源时间：未披露，抓取时间：待确认"

    if display.startswith(("来源时间", "来源更新时间")):
        return display

    if display_type == "updated_at":
        if date_only(display):
            return f"来源更新时间：{display}（来源仅披露日期，北京时间）"
        return f"来源更新时间：{display}"

    if display_type == "inferred_at":
        if date_only(display):
            return f"来源时间：推断为 {display}（来源未直接披露）"
        return f"来源时间：推断为 {display}"

    if display_type == "fetched_at":
        return f"来源时间：未披露，抓取时间：{display}"

    if date_only(display):
        return f"来源时间：{display}（来源仅披露日期，北京时间）"
    return f"来源时间：{display}"


def quality_value(item: dict[str, Any]) -> str:
    raw = item.get("reading_quality")
    if isinstance(raw, str):
        if raw.startswith("high"):
            return "high"
        if raw.startswith("medium"):
            return "medium"
        if raw.startswith("low"):
            return "low"
        return raw
    if isinstance(raw, dict):
        quality = raw.get("quality") or raw.get("status") or raw.get("confidence")
        if isinstance(quality, str):
            if quality in {"medium-high", "sufficient", "medium_high"}:
                return "medium"
            return quality
    return "unknown"


def item_sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
    quality = quality_value(item)
    return (
        IMPORTANCE_RANK.get(item.get("importance"), 9),
        0 if item.get("time_display_type") in {"published_at", "updated_at"} else 1,
        QUALITY_RANK.get(quality, 9),
        item.get("source_name") or item.get("provider") or "",
        item.get("title") or "",
    )


def eligible_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted: list[dict[str, Any]] = []
    for item in items:
        quality = quality_value(item)
        if (
            item.get("reader_status") == "read"
            and item.get("reader_agent") == "Article Reader Agent"
            and item.get("summary_source") == "article_reader_agent"
            and quality in {"high", "medium", "medium-high"}
            and item.get("article_summary")
            and item.get("why_it_matters")
            and item.get("action_hint")
        ):
            accepted.append(item)
    return accepted


def build_digest(day: date, items: list[dict[str, Any]], max_items: int) -> str:
    accepted = eligible_items(items)
    accepted.sort(key=item_sort_key)
    accepted = accepted[:max_items]

    lines = [
        f"# 前沿资讯日报 {day:%Y-%m-%d}",
        "",
        f"{day:%m}.{day:%d}",
        "",
        "## 概要说明",
        "",
        "- 本日报条目必须经过 Article Reader Agent 阅读正文后生成，不直接把标题或列表页摘要当成正文概要。",
        "- 正式日报只使用 `data/agent-readings` 中 `reader_agent = Article Reader Agent` 且 `summary_source = article_reader_agent` 的结果。",
        "- 每条快讯包含正文概要、为什么重要、行动启发、来源链接、来源时间和阅读状态。",
        "- 若来源未披露发布时间，会展示本系统抓取时间；不会编造具体发布时间。",
        "",
    ]

    if not accepted:
        lines.append("暂无经过 Article Reader Agent 阅读且校验合格的快讯条目。")
        lines.append("")
    else:
        for index, item in enumerate(accepted, start=1):
            title = clean_text(item.get("title") or item.get("summary"), max_len=180)
            source_name = clean_text(item.get("source_name") or item.get("provider") or "来源", max_len=80)
            source_url = clean_text(item.get("source_url"), max_len=500)
            quality = quality_value(item)
            lines.append(f"{index}. **{title}**")
            lines.append(f"   - 概要：{sentence(item.get('article_summary'))}")
            lines.append(f"   - 为什么重要：{sentence(item.get('why_it_matters'))}")
            lines.append(f"   - 行动启发：{sentence(item.get('action_hint'))}")
            lines.append(
                f"   - 来源：[{source_name}]({source_url})；{source_time_clause(item)}；"
                f"阅读状态：{item.get('reader_status')}；阅读质量：{quality}"
            )
            lines.append("")

    lines.extend(
        [
            "## 时间说明",
            "",
            "- “来源时间”优先使用来源页面、RSS/API 或可核验元数据中明确披露的发布时间。",
            "- 若来源只披露日期，则按来源日期展示，不补造具体时分。",
            "- 若来源未披露时间，则展示本系统抓取时间。",
            "- 若时间由 URL、列表页或搜索结果推断，会明确标注“推断”。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily frontier news digest.")
    parser.add_argument("--root", default=str(repo_root()), help="frontier-data-hub root directory")
    parser.add_argument("--date", help="digest date, YYYY-MM-DD; defaults to today in Beijing time")
    parser.add_argument("--max-items", type=int, default=30)
    args = parser.parse_args()

    root = Path(args.root)
    day = parse_date_arg(args.date)
    in_path = agent_readings_path(root, day)
    rows = read_jsonl(in_path)
    out_path = daily_path(root, day)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_digest(day, rows, args.max_items), encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "ok",
                "date": day.isoformat(),
                "input": str(in_path),
                "items_loaded": len(rows),
                "items_eligible": len(eligible_items(rows)),
                "output": str(out_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
