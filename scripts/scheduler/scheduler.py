#!/usr/bin/env python3
"""
Scheduler for automated test failure analysis.

Polls Azure DevOps pipelines for new completed builds, checks for test failures,
and runs the analyze-failures skill via Claude CLI.
"""

import json
import logging
import subprocess
import shutil
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import yaml


SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.yaml"
HISTORY_FILE = SCRIPT_DIR / "build_history.json"
LOCK_FILE = SCRIPT_DIR / ".scheduler.lock"
FAILED_CLONE_RETENTION_DAYS = 7

ADO_RESOURCE_ID = "499b84ac-1321-427f-aa17-267ca6975798"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def load_config() -> dict:
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def load_history() -> dict:
    if not HISTORY_FILE.exists():
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history: dict):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def purge_history(history: dict, retention_days: int) -> dict:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=retention_days)).isoformat()
    purged = {}
    for pipeline, builds in history.items():
        kept = {
            bid: info for bid, info in builds.items()
            if info.get("timestamp", "") >= cutoff
        }
        if kept:
            purged[pipeline] = kept
    return purged


def acquire_lock() -> bool:
    if LOCK_FILE.exists():
        try:
            lock_data = json.loads(LOCK_FILE.read_text())
            lock_time = datetime.fromisoformat(lock_data["timestamp"])
            if datetime.now(timezone.utc) - lock_time > timedelta(hours=2):
                log.warning("Stale lock detected (>2h), removing")
                LOCK_FILE.unlink()
            else:
                log.info(f"Lock held since {lock_data['timestamp']}, skipping")
                return False
        except Exception:
            LOCK_FILE.unlink()

    lock_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pid": str(subprocess.os.getpid()),
    }
    LOCK_FILE.write_text(json.dumps(lock_data))
    return True


def release_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def get_ado_token() -> str:
    result = subprocess.run(
        ["az", "account", "get-access-token",
         "--resource", ADO_RESOURCE_ID,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get access token: {result.stderr}")
    return result.stdout.strip()


def ado_api_get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_pipeline_id(pipeline_name: str, org: str, project: str, token: str) -> int:
    url = (
        f"{org}/{project}/_apis/build/definitions"
        f"?name={pipeline_name}&api-version=7.0"
    )
    data = ado_api_get(url, token)
    definitions = data.get("value", [])
    if not definitions:
        raise ValueError(f"Pipeline '{pipeline_name}' not found")
    return definitions[0]["id"]


def get_latest_completed_build(pipeline_id: int, org: str, project: str, token: str) -> dict | None:
    url = (
        f"{org}/{project}/_apis/build/builds"
        f"?definitions={pipeline_id}&statusFilter=completed&$top=1"
        f"&queryOrder=finishTimeDescending&api-version=7.0"
    )
    data = ado_api_get(url, token)
    builds = data.get("value", [])
    return builds[0] if builds else None


def get_test_failure_count(build_id: int, org: str, project: str, token: str) -> int:
    url = (
        f"{org}/{project}/_apis/test/runs"
        f"?buildUri=vstfs:///Build/Build/{build_id}&api-version=7.0"
    )
    data = ado_api_get(url, token)
    total_failed = 0
    for run in data.get("value", []):
        stats = run.get("runStatistics", [])
        for stat in stats:
            if stat.get("outcome") == "Failed":
                total_failed += stat.get("count", 0)
    return total_failed


def clone_repo(repo_url: str, branch: str, dest: Path):
    log.info(f"Cloning {repo_url} (branch: {branch}) -> {dest}")
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", branch, repo_url, str(dest)],
        check=True,
        capture_output=True,
        text=True,
    )


def run_claude_analysis(clone_dir: Path, build_id: int, timeout: int) -> dict:
    log.info(f"Running Claude analysis for build {build_id} (timeout: {timeout}s)")
    prompt = f"/analyze-failures {build_id}"
    cmd = [
        "claude", "-p", prompt,
        "--dangerously-skip-permissions",
    ]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(clone_dir),
            timeout=timeout,
            capture_output=True,
            text=True,
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-2000:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": f"Timed out after {timeout}s",
        }


def find_report_url(clone_dir: Path, build_id: int) -> str:
    report_url_file = clone_dir / "pipeline_data" / str(build_id) / "reports" / "report_url.json"
    if report_url_file.exists():
        data = json.load(open(report_url_file))
        return data.get("report_url", data.get("sas_url", ""))
    return ""


def build_notification_payload(clone_dir: Path, build_id: int, pipeline_name: str) -> dict | None:
    data_dir = clone_dir / "pipeline_data" / str(build_id)
    failure_info_file = data_dir / "reports" / "failure_info.json"
    pipeline_info_file = data_dir / "pipeline_info.json"
    report_url_file = data_dir / "reports" / "report_url.json"

    if not failure_info_file.exists():
        log.warning(f"failure_info.json not found: {failure_info_file}")
        return None

    with open(failure_info_file, "r") as f:
        failure_info = json.load(f)

    pipeline_info = {}
    if pipeline_info_file.exists():
        with open(pipeline_info_file, "r") as f:
            pipeline_info = json.load(f)

    report_url = ""
    if report_url_file.exists():
        with open(report_url_file, "r") as f:
            report_data = json.load(f)
            report_url = report_data.get("report_url", report_data.get("sas_url", ""))

    summary = failure_info.get("summary", {})
    cases = failure_info.get("failed_cases", [])
    heal_summary = failure_info.get("heal_summary", [])
    bug_summary = failure_info.get("bug_summary", [])

    healable_count = summary.get("healable_failures", 0)
    non_healable_count = summary.get("non_healable_failures", 0)
    visual_flaky_count = summary.get("visual_flaky_failures", 0)

    channel_suffix = pipeline_name.replace("edge-FSQ-mac-", "").capitalize()
    title = f"FSQ AI Failure Analysis - Mac {channel_suffix}"

    heal_prs = []
    for h in heal_summary:
        pr_url = h.get("pr_url", "")
        if not pr_url:
            continue
        heal_prs.append({
            "pr_title": f"{h.get('heal_group_id', '')}: Fix {h.get('element_description', '')}",
            "pr_url": pr_url,
            "is_new": h.get("status") != "existing",
            "affected_cases": h.get("affected_cases", []),
        })

    bugs = []
    for b in bug_summary:
        bug_url = b.get("ado_bug_url", "")
        if not bug_url:
            continue
        bugs.append({
            "bug_title": f"{b.get('bug_group_id', '')}: {b.get('suggested_title', '')}",
            "bug_url": bug_url,
            "is_new": b.get("status") == "created",
            "affected_cases": b.get("affected_cases", []),
        })

    flaky_groups = []
    flaky_cases_list = []
    for c in cases:
        fa = c.get("failure_analysis", {})
        if fa.get("is_healable") == "visual_flaky":
            flaky_cases_list.append(c["scenario_name"])
    if flaky_cases_list:
        flaky_groups.append({"affected_cases": flaky_cases_list})

    return {
        "title": title,
        "build_id": str(build_id),
        "edge_version": pipeline_info.get("edge_version", ""),
        "fail_count": summary.get("total_failures", 0),
        "healable_count": healable_count,
        "bug_count": non_healable_count,
        "flaky_count": visual_flaky_count,
        "heal_prs": heal_prs,
        "bugs": bugs,
        "flaky_cases": flaky_groups,
        "report_url": report_url,
        "build_url": pipeline_info.get("url", ""),
    }


def notify_power_automate(webhook_url: str, payload: dict):
    if not webhook_url:
        log.info("No Power Automate webhook configured, skipping notification")
        return
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            log.info(f"Power Automate notification sent: HTTP {resp.status}")
    except Exception as e:
        log.error(f"Power Automate notification failed: {e}")


def process_build(build: dict, profile: dict, pipeline_name: str) -> dict:
    build_id = build["id"]
    org = f"https://dev.azure.com/{profile['ado']['organization']}"
    project = profile["ado"]["project"]
    clone_cfg = profile["clone"]
    timeout = profile["claude"]["timeout_seconds"]
    webhook_url = profile.get("power_automate", {}).get("webhook_url", "")

    token = get_ado_token()

    fail_count = get_test_failure_count(build_id, org, project, token)
    log.info(f"Build {build_id} ({pipeline_name}): {fail_count} test failure(s)")

    if fail_count == 0:
        return {"status": "skipped", "reason": "no_failures", "fail_count": 0}

    clone_dir = Path(tempfile.mkdtemp(prefix=f"fsq-{build_id}-"))
    try:
        clone_repo(clone_cfg["repo_url"], clone_cfg["branch"], clone_dir)

        result = run_claude_analysis(clone_dir, build_id, timeout)

        report_url = find_report_url(clone_dir, build_id)

        status = "success" if result["returncode"] == 0 else "failed"

        if status == "success":
            notification_payload = build_notification_payload(
                clone_dir, build_id, pipeline_name
            )
            if notification_payload:
                notify_power_automate(webhook_url, notification_payload)

        ret: dict = {
            "status": status,
            "fail_count": fail_count,
            "report_url": report_url,
            "returncode": result["returncode"],
            "error": result["stderr"] if result["returncode"] != 0 else "",
        }

        if status == "success":
            log.info(f"Cleaning up {clone_dir}")
            shutil.rmtree(clone_dir, ignore_errors=True)
        else:
            log.warning(f"Analysis failed, keeping clone dir for inspection: {clone_dir}")
            ret["clone_dir"] = str(clone_dir)

        return ret
    except Exception:
        log.warning(f"Analysis errored, keeping clone dir for inspection: {clone_dir}")
        raise


def purge_failed_clones(history: dict):
    cutoff = datetime.now(timezone.utc) - timedelta(days=FAILED_CLONE_RETENTION_DAYS)
    for _pipeline, builds in history.items():
        for _bid, info in builds.items():
            clone_dir = info.get("clone_dir")
            if not clone_dir:
                continue
            ts = info.get("timestamp", "")
            if not ts:
                continue
            try:
                build_time = datetime.fromisoformat(ts)
            except (ValueError, TypeError):
                continue
            if build_time < cutoff:
                p = Path(clone_dir)
                if p.exists():
                    log.info(f"Purging failed clone (>{FAILED_CLONE_RETENTION_DAYS}d old): {p}")
                    shutil.rmtree(p, ignore_errors=True)
                info.pop("clone_dir", None)


def poll_once(config: dict):
    history = load_history()
    token = get_ado_token()

    for _, profile in config["profiles"].items():
        org = f"https://dev.azure.com/{profile['ado']['organization']}"
        project = profile["ado"]["project"]

        for pipeline_name in profile["pipelines"]:
            log.info(f"Checking {pipeline_name}...")

            try:
                pipeline_id = get_pipeline_id(pipeline_name, org, project, token)
                build = get_latest_completed_build(pipeline_id, org, project, token)
            except Exception as e:
                log.error(f"Failed to query {pipeline_name}: {e}")
                continue

            if not build:
                log.info(f"  No completed builds found")
                continue

            build_id = str(build["id"])
            pipeline_history = history.get(pipeline_name, {})

            if build_id in pipeline_history:
                log.info(f"  Build {build_id} already processed")
                continue

            log.info(f"  New build: {build_id} ({build.get('buildNumber', '')})")

            result = process_build(build, profile, pipeline_name)

            pipeline_history[build_id] = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "build_number": build.get("buildNumber", ""),
                **result,
            }
            history[pipeline_name] = pipeline_history
            save_history(history)

    retention_days = config.get("history", {}).get("retention_days", 30)
    history = purge_history(history, retention_days)
    purge_failed_clones(history)
    save_history(history)


def run_loop(config: dict):
    interval = config.get("poll_interval_minutes", 10) * 60
    log.info(f"Starting scheduler (poll every {interval // 60} min)")

    while True:
        if not acquire_lock():
            time.sleep(interval)
            continue
        try:
            poll_once(config)
        except Exception:
            log.exception("Error during poll cycle")
        finally:
            release_lock()

        log.info(f"Sleeping {interval // 60} minutes...")
        time.sleep(interval)


def main():
    config = load_config()

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        if not acquire_lock():
            log.error("Another instance is running")
            sys.exit(1)
        try:
            poll_once(config)
        finally:
            release_lock()
    else:
        run_loop(config)


if __name__ == "__main__":
    main()
