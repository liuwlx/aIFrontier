#!/usr/bin/env python
"""Normalize raw crawl records into JSONL records with strict source-time fields."""

from __future__ import annotations

import argparse
import email.utils
import html
import json
import re
import sys
import urllib.parse
from datetime import date, datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path


BJ_TZ = timezone(timedelta(hours=8))
LONG_LIVED_TYPES = {
    "implementation_guides",
    "enterprise_genai_platform",
    "whitepapers",
    "production_architecture_check",
    "genai_architecture",
}
HIGH_VALUE_TYPES = {
    "implementation_guides",
    "enterprise_genai_platform",
    "production_architecture_check",
    "company_strategy",
    "genai_architecture",
}
NOISE_TITLES = {
    "skip to main content",
    "aws marketplace",
    "learn more",
    "read more",
    "watch now",
    "listen now",
    "download",
    "read the full report",
    "overview",
    "resources",
    "what is aws?",
    "what is cloud computing?",
    "what is agentic ai?",
}
NOISE_URL_PATH_PREFIXES = (
    "/marketplace",
    "/contact-us",
    "/contact",
    "/privacy",
    "/terms",
    "/careers",
    "/login",
    "/account",
    "/what-is",
)
MONTHS = "jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def today_bj() -> date:
    return datetime.now(BJ_TZ).date()


def safe_slug(text: str, max_len: int = 100) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return (text or "item")[:max_len]


def parse_date_arg(value: str | None) -> date:
    if not value:
        return today_bj()
    return datetime.strptime(value, "%Y-%m-%d").date()


def raw_date_dir(root: Path, day: date) -> Path:
    return root / "data" / "raw" / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}"


def normalized_path(root: Path, day: date) -> Path:
    return root / "data" / "normalized" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.jsonl"


def rejected_path(root: Path, day: date) -> Path:
    return root / "data" / "rejected" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.jsonl"


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta: list[dict] = []
        self.json_ld_parts: list[str] = []
        self.title_parts: list[str] = []
        self._in_title = False
        self._in_json_ld = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = {key.lower(): value for key, value in attrs}
        if tag == "meta":
            self.meta.append(attrs_dict)
        elif tag == "title":
            self._in_title = True
        elif tag == "script":
            script_type = (attrs_dict.get("type") or "").lower()
            self._in_json_ld = "ld+json" in script_type

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._in_json_ld:
            self.json_ld_parts.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._in_json_ld = False

    @property
    def title(self) -> str:
        return compact(" ".join(self.title_parts))


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


def parse_html_metadata(page_html: str) -> MetadataParser:
    parser = MetadataParser()
    try:
        parser.feed(page_html or "")
    except Exception:
        pass
    return parser


def meta_time_candidates(parser: MetadataParser) -> tuple[list[str], list[str]]:
    published_keys = {
        "article:published_time",
        "datepublished",
        "date",
        "dc.date",
        "dc.date.issued",
        "publishdate",
        "pubdate",
    }
    updated_keys = {
        "article:modified_time",
        "datemodified",
        "lastmod",
        "last-modified",
        "modified",
        "updated",
    }
    published: list[str] = []
    updated: list[str] = []
    for meta in parser.meta:
        key = (meta.get("property") or meta.get("name") or meta.get("itemprop") or "").lower()
        key = key.replace("_", "").replace("-", "")
        content = compact(meta.get("content") or "")
        if not content:
            continue
        normalized_keys = {item.replace("_", "").replace("-", "") for item in published_keys}
        if key in normalized_keys:
            published.append(content)
        normalized_updated = {item.replace("_", "").replace("-", "") for item in updated_keys}
        if key in normalized_updated:
            updated.append(content)
    return published, updated


def walk_json_dates(value, published: list[str], updated: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in {"datepublished", "publisheddate", "uploaddate"} and isinstance(child, str):
                published.append(child)
            elif lowered in {"datemodified", "dateupdated", "modifieddate", "updated"} and isinstance(child, str):
                updated.append(child)
            else:
                walk_json_dates(child, published, updated)
    elif isinstance(value, list):
        for child in value:
            walk_json_dates(child, published, updated)


def json_ld_time_candidates(parser: MetadataParser) -> tuple[list[str], list[str]]:
    published: list[str] = []
    updated: list[str] = []
    for raw in parser.json_ld_parts:
        try:
            data = json.loads(raw)
        except Exception:
            continue
        walk_json_dates(data, published, updated)
    return published, updated


def visible_time_candidates(page_html: str) -> list[str]:
    text = re.sub(r"<[^>]+>", " ", page_html or "")
    text = compact(text)
    candidates: list[str] = []
    patterns = [
        r"20\d{2}-\d{1,2}-\d{1,2}(?:[T\s]\d{1,2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)?",
        r"20\d{2}年\d{1,2}月\d{1,2}日(?:\s*\d{1,2}:\d{2})?",
        rf"(?:{MONTHS})\s+\d{{1,2}},\s+20\d{{2}}",
        rf"\d{{1,2}}\s+(?:{MONTHS})\s+20\d{{2}}",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.I):
            candidates.append(match.group(0))
            if len(candidates) >= 10:
                return candidates
    return candidates


def infer_date_from_url(url: str) -> dict | None:
    patterns = [
        r"/(20\d{2})/(\d{1,2})/(\d{1,2})(?:/|$)",
        r"(20\d{2})-(\d{1,2})-(\d{1,2})",
        r"(20\d{2})(\d{2})(\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if not match:
            continue
        year, month, day = map(int, match.groups())
        try:
            value = date(year, month, day).isoformat()
        except ValueError:
            continue
        return {
            "value": value,
            "precision": "date",
            "timezone_known": False,
            "confidence": "medium",
            "source_text": match.group(0),
        }
    return None


def parse_time(value: str) -> dict | None:
    value = compact(value)
    if not value:
        return None

    chinese = re.search(r"(20\d{2})年(\d{1,2})月(\d{1,2})日(?:\s*(\d{1,2}):(\d{2}))?", value)
    if chinese:
        year, month, day = map(int, chinese.group(1, 2, 3))
        hour = chinese.group(4)
        minute = chinese.group(5)
        try:
            if hour is None:
                return {"value": date(year, month, day).isoformat(), "precision": "date", "timezone_known": True, "confidence": "high", "source_text": value}
            dt = datetime(year, month, day, int(hour), int(minute), tzinfo=BJ_TZ)
            return {"value": dt.isoformat(timespec="seconds"), "precision": "datetime", "timezone_known": True, "confidence": "high", "source_text": value}
        except ValueError:
            return None

    iso_match = re.search(r"20\d{2}-\d{1,2}-\d{1,2}(?:[T\s]\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?", value)
    if iso_match:
        token = iso_match.group(0)
        has_time = bool(re.search(r"[T\s]\d{1,2}:\d{2}", token))
        if not has_time:
            try:
                parsed_date = datetime.strptime(token, "%Y-%m-%d").date()
            except ValueError:
                parts = token.split("-")
                parsed_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
            return {"value": parsed_date.isoformat(), "precision": "date", "timezone_known": True, "confidence": "high", "source_text": value}
        normalized = token.replace("Z", "+00:00")
        normalized = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", normalized)
        normalized = normalized.replace(" ", "T")
        try:
            dt = datetime.fromisoformat(normalized)
        except ValueError:
            return None
        timezone_known = dt.tzinfo is not None
        if timezone_known:
            dt = dt.astimezone(BJ_TZ)
        return {"value": dt.isoformat(timespec="seconds"), "precision": "datetime", "timezone_known": timezone_known, "confidence": "high", "source_text": value}

    try:
        dt = email.utils.parsedate_to_datetime(value)
    except Exception:
        dt = None
    if dt:
        if dt.tzinfo is not None:
            return {"value": dt.astimezone(BJ_TZ).isoformat(timespec="seconds"), "precision": "datetime", "timezone_known": True, "confidence": "high", "source_text": value}
        return {"value": dt.isoformat(timespec="seconds"), "precision": "datetime", "timezone_known": False, "confidence": "medium", "source_text": value}

    english_date = re.search(rf"((?:{MONTHS})\s+\d{{1,2}},\s+20\d{{2}}|\d{{1,2}}\s+(?:{MONTHS})\s+20\d{{2}})", value, flags=re.I)
    if english_date:
        for fmt in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y"):
            try:
                parsed = datetime.strptime(english_date.group(1), fmt).date()
                return {"value": parsed.isoformat(), "precision": "date", "timezone_known": False, "confidence": "high", "source_text": value}
            except ValueError:
                continue

    return None


def first_parsed(candidates: list[str]) -> dict | None:
    for candidate in candidates:
        parsed = parse_time(candidate)
        if parsed:
            return parsed
    return None


def display_from_parsed(parsed: dict, display_type: str) -> str:
    if parsed["precision"] == "date":
        if display_type == "inferred_at":
            return parsed["value"]
        if parsed.get("timezone_known"):
            return f"{parsed['value']}（来源仅披露日期，北京时间）"
        return f"{parsed['value']}（来源未披露时区）"
    try:
        dt = datetime.fromisoformat(parsed["value"])
    except ValueError:
        return parsed["value"]
    if dt.tzinfo is None or not parsed.get("timezone_known"):
        return f"{dt:%Y-%m-%d %H:%M}（来源未披露时区）"
    return f"{dt.astimezone(BJ_TZ):%Y-%m-%d %H:%M}（北京时间）"


def choose_time(source_type: str, published: dict | None, updated: dict | None, inferred: dict | None, fetched_at: str) -> tuple[str, str, str]:
    fetched_parsed = {"value": fetched_at, "precision": "datetime", "timezone_known": True, "confidence": "high", "source_text": fetched_at}
    if source_type in LONG_LIVED_TYPES:
        order = [("updated_at", updated), ("published_at", published), ("inferred_at", inferred), ("fetched_at", fetched_parsed)]
    else:
        order = [("published_at", published), ("updated_at", updated), ("inferred_at", inferred), ("fetched_at", fetched_parsed)]
    for display_type, parsed in order:
        if parsed:
            return display_from_parsed(parsed, display_type), display_type, parsed.get("confidence", "high")
    return display_from_parsed(fetched_parsed, "fetched_at"), "fetched_at", "high"


def extract_times(page_html: str, source_url: str) -> tuple[dict | None, dict | None, dict | None]:
    parser = parse_html_metadata(page_html)
    meta_published, meta_updated = meta_time_candidates(parser)
    json_published, json_updated = json_ld_time_candidates(parser)
    visible = visible_time_candidates(page_html)
    published = first_parsed(meta_published + json_published + visible)
    updated = first_parsed(meta_updated + json_updated)
    inferred = infer_date_from_url(source_url)
    return published, updated, inferred


def title_from_raw(raw: dict) -> str:
    title = compact(raw.get("title") or raw.get("page_title") or "")
    if title:
        return title
    parser = parse_html_metadata(raw.get("html", ""))
    return parser.title


def build_summary(title: str) -> str:
    title = compact(title)
    if not title:
        return ""
    title = re.sub(r"\s+[-|]\s+.*$", "", title) if len(title) > 60 else title
    return title[:180]


def is_noise_item(url: str, title: str) -> bool:
    lowered = compact(title).lower()
    if lowered in NOISE_TITLES:
        return True
    if lowered.startswith(("what is ", "什么是")):
        return True
    parsed = urllib.parse.urlparse(url or "")
    if parsed.path.lower().startswith(NOISE_URL_PATH_PREFIXES):
        return True
    return False


def importance_for(raw: dict) -> str:
    if raw.get("priority") == "high" or raw.get("source_type") in HIGH_VALUE_TYPES:
        return "high"
    if raw.get("priority") == "low":
        return "low"
    return "medium"


def relevance_for(source_type: str, dimension: str) -> str:
    if dimension == "architecture":
        return "high" if source_type in {"genai_architecture", "production_architecture_check", "implementation_guides", "enterprise_genai_platform"} else "medium"
    if dimension == "product":
        return "high" if source_type in {"product_releases", "enterprise_genai_platform"} else "medium"
    if dimension == "business":
        return "high" if source_type in {"executive_insights", "company_strategy", "data_leader_view"} else "medium"
    return "medium"


def item_id(day: date, raw: dict, url: str, index: int) -> str:
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    return f"{day:%Y-%m-%d}_{safe_slug(host, 40)}_{index:04d}"


def normalized_item(day: date, raw: dict, url: str, title: str, index: int) -> dict | None:
    title = compact(title)
    summary = build_summary(title)
    if not url or not summary:
        return None
    if is_noise_item(url, title):
        return None

    source_type = raw.get("source_type") or "ai_ml_practice_blog"
    published, updated, inferred = extract_times(raw.get("html", ""), url)
    fetched_at = raw.get("fetched_at")
    time_display, time_display_type, time_confidence = choose_time(source_type, published, updated, inferred, fetched_at)
    topics = raw.get("topics") or []

    return {
        "id": item_id(day, raw, url, index),
        "title": title,
        "summary": summary,
        "provider": raw.get("provider"),
        "source_name": raw.get("source_name"),
        "source_type": source_type,
        "source_url": url,
        "published_at": published["value"] if published else None,
        "updated_at": updated["value"] if updated else None,
        "fetched_at": fetched_at,
        "inferred_at": inferred["value"] if inferred else None,
        "time_display": time_display,
        "time_display_type": time_display_type,
        "time_confidence": time_confidence,
        "topic": topics[0] if topics else source_type,
        "entities": [raw.get("provider")] if raw.get("provider") else [],
        "importance": importance_for(raw),
        "business_relevance": relevance_for(source_type, "business"),
        "architecture_relevance": relevance_for(source_type, "architecture"),
        "product_relevance": relevance_for(source_type, "product"),
        "dedupe_key": safe_slug(f"{raw.get('provider')}_{url}", 160),
        "status": "accepted",
    }


def load_raw_records(root: Path, day: date) -> list[dict]:
    directory = raw_date_dir(root, day)
    if not directory.exists():
        return []
    records = []
    for path in sorted(directory.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            record["_raw_path"] = str(path)
            records.append(record)
        except Exception:
            continue
    # Candidate detail pages contain better metadata than source-list candidates.
    records.sort(key=lambda item: 0 if item.get("kind") == "candidate_page" else 1)
    return records


def append_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize raw crawl records.")
    parser.add_argument("--root", default=str(repo_root()), help="frontier-data-hub root directory")
    parser.add_argument("--date", help="raw crawl date, YYYY-MM-DD; defaults to today in Beijing time")
    parser.add_argument("--include-source-pages", action="store_true", help="also normalize source index pages")
    parser.add_argument("--max-candidates-per-source", type=int, default=5)
    args = parser.parse_args()

    root = Path(args.root)
    day = parse_date_arg(args.date)
    raw_records = load_raw_records(root, day)
    accepted: list[dict] = []
    rejected: list[dict] = []
    seen_urls: set[str] = set()
    index = 1

    for raw in raw_records:
        if raw.get("status") != "success":
            rejected.append({"reason": "raw_fetch_failed", "raw_path": raw.get("_raw_path"), "source_url": raw.get("source_url"), "error": raw.get("error")})
            continue

        if raw.get("kind") == "candidate_page":
            url = raw.get("source_url")
            if url in seen_urls:
                continue
            item = normalized_item(day, raw, url, title_from_raw(raw), index)
            if item:
                accepted.append(item)
                seen_urls.add(url)
                index += 1
            else:
                rejected.append({"reason": "missing_title_or_url", "raw_path": raw.get("_raw_path"), "source_url": url})
            continue

        candidates = raw.get("candidates") or []
        for candidate in candidates[: args.max_candidates_per_source]:
            url = candidate.get("url")
            if not url or url in seen_urls:
                continue
            item = normalized_item(day, raw, url, candidate.get("title") or title_from_raw(raw), index)
            if item:
                accepted.append(item)
                seen_urls.add(url)
                index += 1

        if args.include_source_pages or not candidates:
            url = raw.get("source_url")
            if url and url not in seen_urls:
                item = normalized_item(day, raw, url, title_from_raw(raw), index)
                if item:
                    accepted.append(item)
                    seen_urls.add(url)
                    index += 1
                else:
                    rejected.append({"reason": "missing_title_or_url", "raw_path": raw.get("_raw_path"), "source_url": url})

    out_path = normalized_path(root, day)
    rej_path = rejected_path(root, day)
    append_jsonl(out_path, accepted)
    append_jsonl(rej_path, rejected)

    print(json.dumps({
        "status": "ok",
        "date": day.isoformat(),
        "raw_records": len(raw_records),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "normalized_path": str(out_path),
        "rejected_path": str(rej_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
