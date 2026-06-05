#!/usr/bin/env python
"""Orchestrate the daily digest pipeline – crawl, normalize, generate, validate."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Any

BJ_TZ = timezone(timedelta(hours=8))

STAGE_NAMES = {
    "1": "crawl",
    "2": "normalize",
    "3": "agent_read",
    "4": "generate",
    "5": "validate",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def today_bj() -> date:
    return datetime.now(BJ_TZ).date()


def parse_date_arg(value: str | None) -> date:
    if not value:
        return today_bj()
    return datetime.strptime(value, "%Y-%m-%d").date()


def state_path(root: Path) -> Path:
    return root / "runs" / "state" / "pipeline_state.json"


def read_state(root: Path) -> dict[str, Any]:
    sp = state_path(root)
    if sp.exists():
        return json.loads(sp.read_text(encoding="utf-8"))
    return {}


def write_state(root: Path, state: dict[str, Any]) -> None:
    sp = state_path(root)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def python_exe() -> str:
    return sys.executable


def run_script(script_name: str, *args: str, root: str | None = None) -> dict[str, Any]:
    """Run a pipeline script and return its JSON output."""
    root = root or str(repo_root())
    cmd = [python_exe(), f"skills/frontier-news-digest/scripts/{script_name}"]
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(repo_root()))
    stdout = result.stdout.strip()
    if result.returncode != 0 and result.stderr:
        print(f"[pipeline] {script_name} stderr: {result.stderr[:500]}", file=sys.stderr)
    try:
        return json.loads(stdout.split("EXIT:")[0].strip()) if stdout else {}
    except json.JSONDecodeError:
        return {"error": stdout[:200], "script": script_name}


def raw_count(root: Path, day: date) -> int:
    raw_dir = root / "data" / "raw" / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}"
    if not raw_dir.exists():
        return 0
    return len(list(raw_dir.glob("*.json")))


def normalized_count(root: Path, day: date) -> int:
    path = root / "data" / "normalized" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.jsonl"
    if not path.exists():
        return 0
    return sum(1 for _ in path.read_text(encoding="utf-8").splitlines() if _.strip())


def agent_readings_count(root: Path, day: date) -> int:
    path = root / "data" / "agent-readings" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.article-reader-agent.jsonl"
    if not path.exists():
        return 0
    return sum(1 for _ in path.read_text(encoding="utf-8").splitlines() if _.strip())


def agent_eligible_count(root: Path, day: date) -> int:
    """Count agent readings that are high/medium quality and status=read."""
    path = root / "data" / "agent-readings" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.article-reader-agent.jsonl"
    if not path.exists():
        return 0
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            if row.get("reader_status") == "read" and row.get("reading_quality") in ("high", "medium"):
                count += 1
        except json.JSONDecodeError:
            pass
    return count


def cmd_status(root: Path, day: date) -> None:
    print(f"Pipeline status for {day:%Y-%m-%d}")
    print("-" * 40)
    raw = raw_count(root, day)
    norm = normalized_count(root, day)
    agent_total = agent_readings_count(root, day)
    agent_good = agent_eligible_count(root, day)
    digest_path = root / "reports" / "daily" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.md"
    digest_exists = digest_path.exists()

    print(f"  Stage 1 (crawl):      {raw} raw files")
    print(f"  Stage 2 (normalize):  {norm} accepted items")
    print(f"  Stage 3 (agent read): {agent_total} total / {agent_good} eligible (read+high/medium)")
    print(f"  Stage 4 (generate):   {'done' if digest_exists else 'pending'}")
    print(f"  Stage 5 (validate):   {'done' if digest_exists else 'pending'}")

    state = read_state(root)
    if state.get("date") == str(day):
        stages = state.get("stages", {})
        for s in ["1", "2", "3", "4", "5"]:
            info = stages.get(s, {})
            if info:
                print(f"  Stage {s} ({STAGE_NAMES[s]}): {info.get('status', '?')} at {info.get('at', '?')[:19]}")
            else:
                print(f"  Stage {s} ({STAGE_NAMES[s]}): no record")

    remaining = norm - agent_total
    if remaining > 0:
        print(f"\n  >>> {remaining} articles need Article Reader Agent processing <<<")
    elif norm > 0 and agent_good == 0:
        print("\n  >>> Agent readings exist but none are eligible (read+high/medium). Check quality. <<<")
    elif norm > 0 and agent_good > 0:
        print(f"\n  >>> Ready for generate: {agent_good} eligible articles <<<")


def stage_is_done(root: Path, day: date, stage: str) -> bool:
    """Check if a stage is already done (idempotency check)."""
    day_str = str(day)
    if stage == "1":
        return raw_count(root, day) > 0
    if stage == "2":
        return normalized_count(root, day) > 0
    if stage == "4":
        digest = root / "reports" / "daily" / f"{day:%Y}" / f"{day:%m}" / f"{day:%Y-%m-%d}.md"
        return digest.exists()
    if stage == "5":
        return False  # Always re-validate
    if stage == "3":
        norm = normalized_count(root, day)
        agent = agent_readings_count(root, day)
        return agent >= norm and norm > 0
    return False


def update_stage_state(root: Path, day: date, stage: str, status: str, **extra) -> None:
    state = read_state(root)
    state["date"] = str(day)
    if "stages" not in state:
        state["stages"] = {}
    state["stages"][stage] = {"status": status, "at": datetime.now(BJ_TZ).isoformat(), **extra}
    write_state(root, state)


def cmd_run(root: Path, day: date, stages: str, skip_if_done: bool) -> int:
    day_str = day.strftime("%Y-%m-%d")
    stage_nums = [s.strip() for s in stages.split(",")]

    exit_code = 0
    for sn in stage_nums:
        if sn == "1":
            if skip_if_done and stage_is_done(root, day, "1"):
                print(f"[pipeline] Stage 1 (crawl) already done, skipping.")
                continue
            print("[pipeline] Stage 1: crawl_sources.py")
            r = run_script("crawl_sources.py", "--limit", "32", "--items-per-source", "5",
                           "--fetch-candidates", "--timeout", "30")
            status = "ok" if r.get("succeeded", 0) > 0 else "failed"
            update_stage_state(root, day, "1", status,
                               attempted=r.get("attempted", 0),
                               succeeded=r.get("succeeded", 0),
                               failed=r.get("failed", 0))
            print(f"  attempted={r.get('attempted')}, succeeded={r.get('succeeded')}, failed={r.get('failed')}")
            if status == "failed":
                exit_code = 1

        elif sn == "2":
            if skip_if_done and stage_is_done(root, day, "2"):
                print(f"[pipeline] Stage 2 (normalize) already done, skipping.")
                continue
            print("[pipeline] Stage 2: normalize_items.py")
            r = run_script("normalize_items.py", "--date", day_str)
            status = "ok" if r.get("accepted", 0) > 0 else "failed"
            update_stage_state(root, day, "2", status,
                               raw_records=r.get("raw_records", 0),
                               accepted=r.get("accepted", 0),
                               rejected=r.get("rejected", 0))
            print(f"  raw={r.get('raw_records')}, accepted={r.get('accepted')}, rejected={r.get('rejected')}")
            if status == "failed":
                exit_code = 1

        elif sn == "3":
            print("[pipeline] Stage 3: Article Reader Agent (manual step)")
            norm = normalized_count(root, day)
            agent = agent_readings_count(root, day)
            eligible = agent_eligible_count(root, day)
            print(f"  normalized={norm}, agent readings={agent}, eligible={eligible}")
            remaining = norm - agent
            if remaining > 0:
                print(f"  >>> {remaining} articles still need Agent processing <<<")
            elif eligible > 0:
                print(f"  All articles processed. {eligible} eligible for digest.")
            update_stage_state(root, day, "3", "checked",
                               normalized=norm, agent_readings=agent, eligible=eligible)

        elif sn == "4":
            if skip_if_done and stage_is_done(root, day, "4"):
                print(f"[pipeline] Stage 4 (generate) already done, skipping.")
                continue
            eligible = agent_eligible_count(root, day)
            if eligible == 0:
                print("[pipeline] Stage 4: No eligible articles. Run Stage 3 (Article Reader Agent) first.")
                update_stage_state(root, day, "4", "skipped", reason="no_eligible_articles")
                continue
            print("[pipeline] Stage 4: generate_daily.py")
            r = run_script("generate_daily.py", "--date", day_str)
            status = "ok" if r.get("items_eligible", 0) > 0 else "failed"
            update_stage_state(root, day, "4", status,
                               items_loaded=r.get("items_loaded", 0),
                               items_eligible=r.get("items_eligible", 0))
            print(f"  loaded={r.get('items_loaded')}, eligible={r.get('items_eligible')}")
            if status == "failed":
                exit_code = 1

        elif sn == "5":
            print("[pipeline] Stage 5: validate_digest.py")
            r = run_script("validate_digest.py", "--date", day_str)
            valid = r.get("valid", False)
            errors = len(r.get("errors", []))
            warnings = len(r.get("warnings", []))
            update_stage_state(root, day, "5", "ok" if valid else "invalid",
                               errors=errors, warnings=warnings)
            print(f"  valid={valid}, errors={errors}, warnings={warnings}")
            if not valid:
                exit_code = 1

        else:
            print(f"[pipeline] Unknown stage: {sn}")

    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Orchestrate the frontier-data-hub daily digest pipeline.")
    parser.add_argument("--root", default=str(repo_root()), help="frontier-data-hub root directory")
    parser.add_argument("--date", help="digest date, YYYY-MM-DD; defaults to today in Beijing time")
    parser.add_argument("--stages", default="1,2,3,4,5",
                        help="stages to run, comma-separated (1=crawl,2=normalize,3=agent_check,4=generate,5=validate)")
    parser.add_argument("--status", action="store_true", help="show pipeline status and exit")
    parser.add_argument("--skip-if-done", action="store_true", help="skip stages that already have output data")
    args = parser.parse_args()

    root = Path(args.root)
    day = parse_date_arg(args.date)

    if args.status:
        cmd_status(root, day)
        return 0

    return cmd_run(root, day, args.stages, args.skip_if_done)


if __name__ == "__main__":
    sys.exit(main())
