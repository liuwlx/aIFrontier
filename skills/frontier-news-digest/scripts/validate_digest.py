#!/usr/bin/env python
"""Validate daily digest links, source-time display, and Article Reader Agent provenance."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


BJ_TZ = timezone(timedelta(hours=8))
MOJIBAKE_MARKERS = ("姒傝", "鏉ユ簮", "闃呰", "锛", "銆", "鈥", "涓轰粈")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def today_bj() -> date:
    return datetime.now(BJ_TZ).date()


def parse_date_arg(value: str | None) -> date:
    if not value:
        return today_bj()
    return datetime.strptime(value, "%Y-%m-%d").date()


def daily_path(root: Path, day: date) -> Path:
    return root / "reports" / "daily" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.md"


def agent_readings_path(root: Path, day: date) -> Path:
    return root / "data" / "agent-readings" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.article-reader-agent.jsonl"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def numbered_blocks(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    blocks: list[tuple[str, str]] = []
    current_id: str | None = None
    current_lines: list[str] = []
    for line in lines:
        match = re.match(r"^(\d+)\.\s+", line.strip())
        if match:
            if current_id is not None:
                blocks.append((current_id, "\n".join(current_lines)))
            current_id = match.group(1)
            current_lines = [line]
        elif current_id is not None:
            if line.startswith("   - ") or not line.strip():
                current_lines.append(line)
            else:
                blocks.append((current_id, "\n".join(current_lines)))
                current_id = None
                current_lines = []
    if current_id is not None:
        blocks.append((current_id, "\n".join(current_lines)))
    return blocks


def source_urls_from_digest(text: str) -> list[str]:
    return re.findall(r"来源：\[[^\]]+\]\((https?://[^)]+)\)", text)


def normalized_text(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def chinese_char_count(text: str | None) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text or ""))


def has_garbled_text(text: str | None) -> bool:
    text = text or ""
    return "???" in text or "\ufffd" in text or any(marker in text for marker in MOJIBAKE_MARKERS) or text.count("?") >= 6


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


def validate_text(text: str, readings: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    blocks = numbered_blocks(text)
    by_url = {row.get("source_url"): row for row in readings if row.get("source_url")}

    if has_garbled_text(text):
        errors.append({"scope": "digest", "issue": "digest_contains_mojibake", "message": "日报正文包含乱码或疑似错误编码字符。"})

    if not blocks:
        errors.append({"scope": "digest", "issue": "no_numbered_items", "message": "日报没有编号快讯条目。"})

    if "## 时间说明" not in text:
        errors.append({"scope": "digest", "issue": "missing_time_explanation", "message": "日报缺少 ## 时间说明 小节。"})

    if "## 概要说明" not in text:
        errors.append({"scope": "digest", "issue": "missing_summary_explanation", "message": "日报缺少 ## 概要说明 小节。"})

    source_link_re = re.compile(r"来源：\[[^\]]+\]\(https?://[^)]+\)")
    time_re = re.compile(r"(来源时间：|来源更新时间：|抓取时间：|推断为)")

    for item_id, block in blocks:
        if not source_link_re.search(block):
            errors.append({"scope": f"item_{item_id}", "issue": "missing_source_link", "message": block})
        if not time_re.search(block):
            errors.append({"scope": f"item_{item_id}", "issue": "missing_source_time", "message": block})
        for label, issue in [
            ("概要：", "missing_article_summary"),
            ("为什么重要：", "missing_why_it_matters"),
            ("行动启发：", "missing_action_hint"),
            ("阅读状态：", "missing_reader_status"),
        ]:
            if label not in block:
                errors.append({"scope": f"item_{item_id}", "issue": issue, "message": block})

        urls = source_urls_from_digest(block)
        if not urls:
            continue
        row = by_url.get(urls[0])
        if not row:
            errors.append({"scope": f"item_{item_id}", "issue": "missing_article_reader_record", "message": urls[0]})
            continue

        if row.get("reader_status") != "read":
            errors.append({"scope": f"item_{item_id}", "issue": "article_reader_not_successful", "message": urls[0]})
        if row.get("reader_agent") != "Article Reader Agent":
            errors.append({"scope": f"item_{item_id}", "issue": "not_real_article_reader_agent", "message": urls[0]})
        if row.get("summary_source") != "article_reader_agent":
            errors.append({"scope": f"item_{item_id}", "issue": "summary_not_from_reader", "message": urls[0]})
        if not row.get("reader_ran_at"):
            errors.append({"scope": f"item_{item_id}", "issue": "missing_reader_ran_at", "message": urls[0]})
        if not row.get("content_hash") and row.get("reader_status") == "read":
            warnings.append({"scope": f"item_{item_id}", "issue": "missing_reader_content_hash", "message": urls[0]})
        if not row.get("time_display") or not row.get("time_display_type"):
            errors.append({"scope": f"item_{item_id}", "issue": "missing_source_time_fields", "message": urls[0]})

        summary = normalized_text(row.get("article_summary") or row.get("summary"))
        title = normalized_text(row.get("title"))
        if summary and title and summary == title:
            errors.append({"scope": f"item_{item_id}", "issue": "title_only_summary", "message": urls[0]})

        quality = quality_value(row)
        if quality not in {"high", "medium", "medium-high"}:
            errors.append({"scope": f"item_{item_id}", "issue": "reader_quality_not_accepted", "message": urls[0]})

        for field in ["article_summary", "why_it_matters", "action_hint"]:
            value = row.get(field) or ""
            if has_garbled_text(value):
                errors.append({"scope": f"item_{item_id}", "issue": f"garbled_{field}", "message": urls[0]})
            if chinese_char_count(value) < 10:
                errors.append({"scope": f"item_{item_id}", "issue": f"not_enough_chinese_{field}", "message": urls[0]})

    return {
        "valid": len(errors) == 0,
        "items": len(blocks),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a daily digest Markdown file.")
    parser.add_argument("--root", default=str(repo_root()), help="frontier-data-hub root directory")
    parser.add_argument("--date", help="digest date, YYYY-MM-DD; defaults to today in Beijing time")
    parser.add_argument("--path", help="explicit digest Markdown path")
    args = parser.parse_args()

    root = Path(args.root)
    day = parse_date_arg(args.date)
    path = Path(args.path) if args.path else daily_path(root, day)
    if not path.exists():
        result = {
            "valid": False,
            "path": str(path),
            "errors": [{"scope": "digest", "issue": "file_not_found", "message": "日报文件不存在。"}],
            "warnings": [],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    readings = read_jsonl(agent_readings_path(root, day))
    result = validate_text(path.read_text(encoding="utf-8"), readings)
    result["path"] = str(path)
    result["agent_readings_path"] = str(agent_readings_path(root, day))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
