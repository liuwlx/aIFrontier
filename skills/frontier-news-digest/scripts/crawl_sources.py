#!/usr/bin/env python
"""Fetch configured frontier sources and save raw crawl records."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path

import yaml


BJ_TZ = timezone(timedelta(hours=8))
SKIP_LINK_WORDS = {
    "privacy",
    "terms",
    "contact",
    "subscribe",
    "sign in",
    "login",
    "careers",
    "about",
    "cookie",
    "cookies",
    "feedback",
    "中文",
    "登录",
    "注册",
    "隐私",
    "广告",
    "marketplace",
    "overview",
    "resources",
    "what is",
}
GENERIC_LINK_TITLES = {
    "skip to main content",
    "learn more",
    "read more",
    "watch now",
    "listen now",
    "download",
    "download now",
    "access the ebook",
    "access the e-book",
    "read the full report",
    "view all",
    "explore",
    "overview",
    "resources",
}
BLOCKED_PATH_PREFIXES = (
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


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def now_bj() -> datetime:
    return datetime.now(BJ_TZ)


def now_iso() -> str:
    return now_bj().isoformat(timespec="seconds")


def safe_slug(text: str, max_len: int = 80) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return (text or "item")[:max_len]


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class PageParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.links: list[dict] = []
        self._href: str | None = None
        self._link_parts: list[str] = []
        self._in_title = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag.lower() == "a":
            href = attrs_dict.get("href")
            if href:
                self._href = urllib.parse.urljoin(self.base_url, href)
                self._link_parts = []
        elif tag.lower() == "title":
            self._in_title = True

    def handle_data(self, data):
        if self._href is not None:
            self._link_parts.append(data)
        if self._in_title:
            self._title_parts.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "a" and self._href is not None:
            text = " ".join(" ".join(self._link_parts).split())
            self.links.append({"url": self._href, "title": text})
            self._href = None
            self._link_parts = []
        elif tag == "title":
            self._in_title = False

    @property
    def title(self) -> str:
        return " ".join(" ".join(self._title_parts).split())


def extract_page_info(page_html: str, base_url: str, items_per_source: int) -> tuple[str, list[dict]]:
    parser = PageParser(base_url)
    try:
        parser.feed(page_html)
    except Exception:
        pass

    seen: set[str] = set()
    candidates: list[dict] = []
    for link in parser.links:
        url = link.get("url", "")
        title = html.unescape(link.get("title", "")).strip()
        title = re.sub(r"\s+", " ", title)
        if not should_keep_link(url, title, base_url):
            continue
        clean_url = url.split("#", 1)[0]
        if clean_url in seen:
            continue
        seen.add(clean_url)
        candidates.append({"title": title, "url": clean_url})
        if len(candidates) >= items_per_source:
            break
    return parser.title, candidates


def should_keep_link(url: str, title: str, base_url: str) -> bool:
    if not url.startswith(("http://", "https://")):
        return False
    if len(title) < 8 or len(title) > 180:
        return False
    parsed_url = urllib.parse.urlparse(url)
    parsed_base = urllib.parse.urlparse(base_url)
    normalized_url = parsed_url._replace(query="", fragment="").geturl().rstrip("/")
    normalized_base = parsed_base._replace(query="", fragment="").geturl().rstrip("/")
    if normalized_url == normalized_base:
        return False
    if parsed_url.netloc and parsed_base.netloc and parsed_url.netloc != parsed_base.netloc:
        # Keep the first crawler conservative; cross-domain targets need source-specific extractors.
        return False
    if parsed_url.path.lower().startswith(BLOCKED_PATH_PREFIXES):
        return False
    lowered = title.lower()
    if lowered in GENERIC_LINK_TITLES:
        return False
    if any(word in lowered for word in SKIP_LINK_WORDS):
        return False
    if re.search(r"\.(jpg|jpeg|png|gif|svg|css|js|ico)(\?|$)", url, re.I):
        return False
    return True


def fetch_url(url: str, timeout: int, max_bytes: int) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "frontier-news-digest/1.0 (+local research crawler)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status_code = getattr(response, "status", 200)
            content_type = response.headers.get("content-type", "")
            raw = response.read(max_bytes + 1)
            truncated = len(raw) > max_bytes
            raw = raw[:max_bytes]
            charset = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
            return {
                "status": "success",
                "status_code": status_code,
                "content_type": content_type,
                "html": text,
                "truncated": truncated,
                "elapsed_ms": int((time.time() - started) * 1000),
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(4096).decode("utf-8", errors="replace") if exc.fp else ""
        return {
            "status": "failed",
            "status_code": exc.code,
            "content_type": "",
            "html": body,
            "truncated": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "error": f"HTTPError: {exc}",
        }
    except Exception as exc:
        return {
            "status": "failed",
            "status_code": None,
            "content_type": "",
            "html": "",
            "truncated": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "error": f"{exc.__class__.__name__}: {exc}",
        }


def load_sources(root: Path) -> list[dict]:
    config_path = root / "config" / "sources.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return data.get("sources", [])


def source_key(source: dict) -> str:
    return safe_slug(f"{source.get('provider', '')}_{source.get('source_name', '')}")


def raw_dir(root: Path, stamp: datetime) -> Path:
    return root / "data" / "raw" / f"{stamp:%Y}" / f"{stamp:%m}" / f"{stamp:%d}"


def build_record(source: dict, url: str, kind: str, fetch_result: dict, fetched_at: str, title_hint: str | None = None, parent_url: str | None = None, items_per_source: int = 3) -> dict:
    page_title = ""
    candidates: list[dict] = []
    if fetch_result.get("html"):
        page_title, candidates = extract_page_info(fetch_result["html"], url, items_per_source)
    return {
        "kind": kind,
        "provider": source.get("provider"),
        "source_name": source.get("source_name"),
        "source_type": source.get("source_type"),
        "source_url": url,
        "parent_source_url": parent_url,
        "configured_source_url": source.get("url"),
        "priority": source.get("priority"),
        "crawl_frequency": source.get("crawl_frequency"),
        "topics": source.get("topics", []),
        "language": source.get("language"),
        "access": source.get("access"),
        "time_extraction": source.get("time_extraction", {}),
        "fetched_at": fetched_at,
        "status": fetch_result.get("status"),
        "status_code": fetch_result.get("status_code"),
        "content_type": fetch_result.get("content_type"),
        "elapsed_ms": fetch_result.get("elapsed_ms"),
        "truncated": fetch_result.get("truncated"),
        "error": fetch_result.get("error"),
        "title": title_hint or page_title,
        "page_title": page_title,
        "candidates": candidates,
        "html": fetch_result.get("html", ""),
    }


def save_raw_record(root: Path, record: dict, index: int) -> Path:
    fetched = datetime.fromisoformat(record["fetched_at"])
    directory = raw_dir(root, fetched)
    directory.mkdir(parents=True, exist_ok=True)
    stamp = fetched.strftime("%Y%m%d_%H%M%S")
    slug = safe_slug(f"{record.get('provider')}_{record.get('source_name')}_{record.get('kind')}_{index}")
    path = directory / f"{stamp}_{slug}.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def update_health(root: Path, key: str, record: dict) -> None:
    path = root / "runs" / "state" / "source_health.json"
    health = read_json(path, {"sources": {}})
    health.setdefault("sources", {})[key] = {
        "last_attempt_at": record.get("fetched_at"),
        "last_status": record.get("status"),
        "last_status_code": record.get("status_code"),
        "last_error": record.get("error"),
        "last_elapsed_ms": record.get("elapsed_ms"),
        "source_url": record.get("source_url"),
    }
    write_json(path, health)


def update_crawl_state(root: Path, run_started_at: str, attempted: int, succeeded: int, failed: int) -> None:
    path = root / "runs" / "state" / "crawl_state.json"
    state = read_json(path, {})
    state.update(
        {
            "last_run_at": run_started_at,
            "last_success_at": now_iso() if succeeded else state.get("last_success_at"),
            "sources_attempted": attempted,
            "sources_succeeded": succeeded,
            "sources_failed": failed,
        }
    )
    write_json(path, state)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch configured frontier sources.")
    parser.add_argument("--root", default=str(repo_root()), help="frontier-data-hub root directory")
    parser.add_argument("--limit", type=int, default=5, help="maximum configured sources to fetch")
    parser.add_argument("--items-per-source", type=int, default=3, help="candidate links to keep from each source page")
    parser.add_argument("--fetch-candidates", action="store_true", help="also fetch candidate article/detail pages")
    parser.add_argument("--timeout", type=int, default=20, help="request timeout seconds")
    parser.add_argument("--max-bytes", type=int, default=1_000_000, help="maximum bytes to read per response")
    parser.add_argument("--provider", help="optional provider filter")
    args = parser.parse_args()

    root = Path(args.root)
    sources = load_sources(root)
    if args.provider:
        sources = [source for source in sources if source.get("provider", "").lower() == args.provider.lower()]
    if args.limit > 0:
        sources = sources[: args.limit]

    run_started_at = now_iso()
    attempted = succeeded = failed = 0
    saved_paths: list[str] = []

    for idx, source in enumerate(sources, start=1):
        attempted += 1
        fetched_at = now_iso()
        result = fetch_url(source["url"], args.timeout, args.max_bytes)
        record = build_record(source, source["url"], "source_page", result, fetched_at, items_per_source=args.items_per_source)
        path = save_raw_record(root, record, idx)
        saved_paths.append(str(path))
        update_health(root, source_key(source), record)
        if record["status"] == "success":
            succeeded += 1
        else:
            failed += 1

        if args.fetch_candidates and record["status"] == "success":
            for cand_idx, candidate in enumerate(record.get("candidates", [])[: args.items_per_source], start=1):
                candidate_result = fetch_url(candidate["url"], args.timeout, args.max_bytes)
                candidate_record = build_record(
                    source,
                    candidate["url"],
                    "candidate_page",
                    candidate_result,
                    now_iso(),
                    title_hint=candidate.get("title"),
                    parent_url=source["url"],
                    items_per_source=0,
                )
                candidate_path = save_raw_record(root, candidate_record, idx * 100 + cand_idx)
                saved_paths.append(str(candidate_path))

    update_crawl_state(root, run_started_at, attempted, succeeded, failed)

    print(json.dumps({
        "status": "ok",
        "root": str(root),
        "attempted": attempted,
        "succeeded": succeeded,
        "failed": failed,
        "saved": saved_paths,
    }, ensure_ascii=False, indent=2))
    return 0 if succeeded or attempted == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
