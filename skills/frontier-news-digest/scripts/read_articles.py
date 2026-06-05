#!/usr/bin/env python
"""Create article reading summaries before daily digest generation."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from datetime import date, datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path


BJ_TZ = timezone(timedelta(hours=8))
DROP_TAGS = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form"}
BOILERPLATE_PATTERNS = [
    r"skip to main content",
    r"x facebook linkedin instagram twitch youtube podcasts email",
    r"sign in to the console",
    r"create an aws account",
    r"contact us",
    r"privacy",
    r"cookie",
]
SIGNAL_TERMS = [
    "agent",
    "agents",
    "agentic",
    "bedrock",
    "rag",
    "generative ai",
    "llm",
    "foundation model",
    "security",
    "governance",
    "architecture",
    "data",
    "platform",
    "inference",
    "training",
    "evaluation",
    "deployment",
    "智能体",
    "大模型",
    "生成式",
    "治理",
    "架构",
    "数据",
]
GENERIC_TITLES = {
    "announcements",
    "artificial intelligence",
    "security & governance",
    "thought leadership",
    "aws news blog",
    "amazon bedrock",
    "amazon connect",
    "amazon quick suite",
    "investor relations",
    "overview",
    "resources",
    "getting started",
    "training",
    "what's new",
    "aws cloud security",
    "aws trust center",
    "executive insights",
    "explore all the guides",
    "explore the framework",
}
COLLECTION_URL_MARKERS = (
    "/category/",
    "/tag/",
    "/resources/",
    "/getting-started/",
    "/training",
    "/security/",
    "/trust-center/",
    "/overview/",
    "/what-is",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def today_bj() -> date:
    return datetime.now(BJ_TZ).date()


def parse_date_arg(value: str | None) -> date:
    if not value:
        return today_bj()
    return datetime.strptime(value, "%Y-%m-%d").date()


def normalized_path(root: Path, day: date) -> Path:
    return root / "data" / "normalized" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.jsonl"


def raw_dir(root: Path, day: date) -> Path:
    return root / "data" / "raw" / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}"


def readings_path(root: Path, day: date) -> Path:
    return root / "data" / "readings" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.jsonl"


def compact(text: str) -> str:
    text = html.unescape(text or "")
    return re.sub(r"\s+", " ", text).strip()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.drop_stack: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in DROP_TAGS:
            self.drop_stack.append(tag)
        if tag == "title":
            self._in_title = True
        if tag in {"p", "br", "li", "h1", "h2", "h3", "article", "section"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.drop_stack and self.drop_stack[-1] == tag:
            self.drop_stack.pop()
        if tag == "title":
            self._in_title = False
        if tag in {"p", "li", "h1", "h2", "h3", "article", "section"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if not self.drop_stack:
            self.parts.append(data)

    @property
    def text(self) -> str:
        return compact("\n".join(self.parts))

    @property
    def title(self) -> str:
        return compact(" ".join(self.title_parts))


def extract_text(page_html: str) -> tuple[str, str]:
    parser = TextExtractor()
    try:
        parser.feed(page_html or "")
    except Exception:
        pass
    text = parser.text
    for pattern in BOILERPLATE_PATTERNS:
        text = re.sub(pattern, " ", text, flags=re.I)
    return compact(parser.title), compact(text)


def sentence_split(text: str) -> list[str]:
    text = compact(text)
    if not text:
        return []
    pieces = re.split(r"(?<=[.!?。！？])\s+|(?<=。)", text)
    return [compact(piece) for piece in pieces if len(compact(piece)) >= 20]


def score_sentence(sentence: str, title: str) -> int:
    lowered = sentence.lower()
    score = 0
    for term in SIGNAL_TERMS:
        if term.lower() in lowered:
            score += 2
    for term in re.findall(r"[A-Za-z][A-Za-z0-9+-]{2,}|[\u4e00-\u9fff]{2,}", title):
        if term.lower() in lowered:
            score += 1
    if 60 <= len(sentence) <= 220:
        score += 2
    if len(sentence) > 320:
        score -= 2
    return score


def best_sentences(text: str, title: str, limit: int = 4) -> list[str]:
    sentences = sentence_split(text)
    ranked = sorted(enumerate(sentences), key=lambda item: (-score_sentence(item[1], title), item[0]))
    selected = sorted(ranked[:limit], key=lambda item: item[0])
    return [sentence for _, sentence in selected]


def short(text: str, max_len: int = 180) -> str:
    text = compact(text)
    if len(text) > max_len:
        return text[: max_len - 3].rstrip() + "..."
    return text


def article_summary(title: str, evidence: list[str], fallback: str) -> str:
    if evidence:
        core = evidence[0]
    else:
        core = fallback or title
    core = short(core, 170)
    if re.search(r"[\u4e00-\u9fff]", core):
        return core
    return f"本文围绕“{title}”展开，核心信息是：{core}"


def why_it_matters(item: dict) -> str:
    source_type = item.get("source_type")
    topic = item.get("topic") or source_type or "该主题"
    if source_type in {"product_releases", "ai_ml_practice_blog"}:
        return f"这条信息可能影响你对 {topic} 的产品能力、工程实践和技术路线判断。"
    if source_type in {"implementation_guides", "genai_architecture", "production_architecture_check"}:
        return "这条信息适合沉淀为架构清单、落地步骤或生产级检查项。"
    if source_type in {"executive_insights", "company_strategy", "data_leader_view"}:
        return "这条信息适合用来观察企业战略、组织采用路径和高层判断。"
    return "这条信息适合进入前沿资讯库，后续可按主题继续追踪。"


def action_hint(item: dict) -> str:
    title = item.get("title") or item.get("summary") or "该条资讯"
    if item.get("source_type") in {"implementation_guides", "genai_architecture", "production_architecture_check"}:
        return f"建议点开原文，提取“{title}”中的架构步骤、前置条件、风险和检查清单。"
    if item.get("source_type") == "product_releases":
        return f"建议核对“{title}”是否带来新 API、新平台能力或竞品变化。"
    return f"建议将“{title}”归档到对应主题，并判断是否值得做专题深挖。"


def reading_quality(text: str, evidence: list[str]) -> str:
    if len(text) >= 1200 and len(evidence) >= 3:
        return "high"
    if len(text) >= 400 and len(evidence) >= 2:
        return "medium"
    return "low"


def content_hash(text: str) -> str | None:
    if not text:
        return None
    return "sha256:" + hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def is_collection_or_navigation(item: dict, raw: dict | None, title: str) -> tuple[bool, str | None]:
    url = item.get("source_url") or ""
    lowered_title = compact(title).lower()
    if lowered_title in GENERIC_TITLES:
        return True, "generic_or_navigation_title"
    if raw and raw.get("kind") == "source_page":
        return True, "source_index_page"
    for marker in COLLECTION_URL_MARKERS:
        if marker in url.lower():
            return True, "collection_or_navigation_url"
    return False, None


def find_raw_by_url(root: Path, day: date) -> dict[str, dict]:
    mapping: dict[str, dict] = {}
    directory = raw_dir(root, day)
    if not directory.exists():
        return mapping
    for path in sorted(directory.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        url = record.get("source_url")
        if url and record.get("html") and url not in mapping:
            record["_raw_path"] = str(path)
            mapping[url] = record
    return mapping


def build_reading(item: dict, raw: dict | None) -> dict:
    title = item.get("title") or item.get("summary") or ""
    text = ""
    page_title = ""
    if raw:
        page_title, text = extract_text(raw.get("html", ""))
    if page_title and len(page_title) > len(title):
        title = page_title

    is_collection, collection_reason = is_collection_or_navigation(item, raw, title)
    evidence = best_sentences(text, title)
    quality = reading_quality(text, evidence)
    reader_status = "read" if raw and text and quality in {"high", "medium"} else "partial" if raw and text else "blocked"
    if is_collection:
        reader_status = "blocked"
    summary = article_summary(title, evidence, item.get("summary", ""))
    ran_at = datetime.now(BJ_TZ).isoformat(timespec="seconds")

    return {
        **item,
        "title": title,
        "summary": summary,
        "article_summary": summary,
        "why_it_matters": why_it_matters(item),
        "action_hint": action_hint(item),
        "key_points": evidence[:3],
        "evidence_quotes": evidence[:3],
        "reader_status": reader_status,
        "reader_agent": "frontier-news-digest.article-reader",
        "reader_model": "local-extractive-reader",
        "reader_ran_at": ran_at,
        "summary_source": "article_reader_agent",
        "summary_language": "zh-CN",
        "summary_generated_at": ran_at,
        "summary_is_title_only": summary.strip().lower() == (item.get("title") or "").strip().lower(),
        "reading_quality": quality,
        "content_chars": len(text),
        "content_hash": content_hash(text),
        "content_source": raw.get("kind") if raw else None,
        "raw_path": raw.get("_raw_path") if raw else None,
        "reader_failure_reason": collection_reason if is_collection else None if raw and text else "missing_readable_raw_html",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read normalized items and create article summary records.")
    parser.add_argument("--root", default=str(repo_root()), help="frontier-data-hub root directory")
    parser.add_argument("--date", help="digest date, YYYY-MM-DD; defaults to today in Beijing time")
    parser.add_argument("--max-items", type=int, default=60)
    parser.add_argument("--require-readable", action="store_true", help="drop items without readable raw HTML")
    args = parser.parse_args()

    root = Path(args.root)
    day = parse_date_arg(args.date)
    items = [item for item in read_jsonl(normalized_path(root, day)) if item.get("status") == "accepted"]
    raw_by_url = find_raw_by_url(root, day)

    readings = []
    for item in items[: args.max_items]:
        reading = build_reading(item, raw_by_url.get(item.get("source_url")))
        if args.require_readable and reading["reader_status"] == "blocked":
            continue
        readings.append(reading)

    out_path = readings_path(root, day)
    write_jsonl(out_path, readings)
    counts: dict[str, int] = {}
    for row in readings:
        counts[row["reader_status"]] = counts.get(row["reader_status"], 0) + 1

    print(json.dumps({
        "status": "ok",
        "date": day.isoformat(),
        "input_items": len(items),
        "readings": len(readings),
        "reader_status_counts": counts,
        "output": str(out_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
