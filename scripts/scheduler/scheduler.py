#!/usr/bin/env python3
"""
Scheduler for automated test failure analysis.

Polls Azure DevOps pipelines for new completed builds, checks for test failures,
and runs the analyze-failures skill via Claude CLI.
"""

import json
import logging
import os
import select
import subprocess
import shutil
import sys
import tempfile
import threading
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
LOG_DIR = SCRIPT_DIR / "logs"
FAILED_CLONE_RETENTION_DAYS = 7

ADO_RESOURCE_ID = "499b84ac-1321-427f-aa17-267ca6975798"

LOG_DIR.mkdir(exist_ok=True)

log_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# File handler — rotates daily via filename, keeps detail
file_handler = logging.FileHandler(
    LOG_DIR / f"scheduler-{datetime.now().strftime('%Y%m%d')}.log",
    encoding="utf-8",
)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[console_handler, file_handler],
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


def _is_pid_alive(pid: int) -> bool:
    """Check if a process with given PID is still running."""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def acquire_lock() -> bool:
    if LOCK_FILE.exists():
        try:
            lock_data = json.loads(LOCK_FILE.read_text())
            lock_time = datetime.fromisoformat(lock_data["timestamp"])
            lock_pid = int(lock_data.get("pid", 0))

            # Check if the lock-holding process is still alive
            if lock_pid and not _is_pid_alive(lock_pid):
                log.warning(f"Stale lock detected (PID {lock_pid} no longer running), removing")
                LOCK_FILE.unlink()
            elif datetime.now(timezone.utc) - lock_time > timedelta(hours=2):
                log.warning("Stale lock detected (>2h), removing")
                LOCK_FILE.unlink()
            else:
                log.info(f"Lock held since {lock_data['timestamp']} by PID {lock_pid}, skipping")
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
    log.debug("Fetching ADO access token via az CLI")
    result = subprocess.run(
        ["az", "account", "get-access-token",
         "--resource", ADO_RESOURCE_ID,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        log.error(f"az CLI token fetch failed (rc={result.returncode}): {result.stderr}")
        raise RuntimeError(f"Failed to get access token: {result.stderr}")
    token = result.stdout.strip()
    if not token:
        raise RuntimeError("az CLI returned empty access token")
    log.debug(f"Got ADO token ({len(token)} chars)")
    return token


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
        if stats:
            for stat in stats:
                if stat.get("outcome") == "Failed":
                    total_failed += stat.get("count", 0)
        else:
            total_tests = run.get("totalTests", 0)
            passed_tests = run.get("passedTests", 0)
            total_failed += max(0, total_tests - passed_tests)
    return total_failed


def clone_repo(repo_url: str, branch: str, dest: Path):
    log.info(f"Cloning {repo_url} (branch: {branch}) -> {dest}")
    t0 = time.time()
    result = subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", branch, repo_url, str(dest)],
        capture_output=True,
        text=True,
    )
    elapsed = time.time() - t0
    if result.returncode != 0:
        log.error(f"git clone failed (rc={result.returncode}, {elapsed:.1f}s)")
        log.error(f"  stderr: {result.stderr[-1000:]}")
        raise RuntimeError(f"git clone failed (rc={result.returncode}): {result.stderr[-500:]}")
    log.info(f"Clone completed in {elapsed:.1f}s")

    log.info(f"Running uv sync in {dest}")
    t0 = time.time()
    result = subprocess.run(
        ["uv", "sync"],
        cwd=str(dest),
        capture_output=True,
        text=True,
    )
    elapsed = time.time() - t0
    if result.returncode != 0:
        log.error(f"uv sync failed (rc={result.returncode}, {elapsed:.1f}s)")
        log.error(f"  stderr: {result.stderr[-1000:]}")
        raise RuntimeError(f"uv sync failed (rc={result.returncode}): {result.stderr[-500:]}")
    log.info(f"uv sync completed in {elapsed:.1f}s")


def _stream_to_file_and_buffer(stream, log_file, label: str, parse_events: bool = False) -> str:
    """Read a subprocess stream line-by-line, write to log file and collect in buffer.

    If parse_events=True, also write human-readable summaries of stream-json events.
    """
    buf = []
    try:
        for line in iter(stream.readline, ""):
            buf.append(line)
            if parse_events and line.strip():
                try:
                    event = json.loads(line)
                    _write_event_summary(log_file, event)
                except (json.JSONDecodeError, KeyError):
                    log_file.write(line)
                    log_file.flush()
            else:
                log_file.write(line)
                log_file.flush()
    except ValueError:
        pass  # stream closed
    return "".join(buf)


def _write_event_summary(log_file, event: dict):
    """Write a human-readable summary of a Claude stream-json event to the log file."""
    etype = event.get("type", "")
    ts = datetime.now().strftime("%H:%M:%S")

    if etype == "assistant":
        # Assistant message with content blocks
        content = event.get("message", {}).get("content", [])
        for block in content:
            if block.get("type") == "tool_use":
                tool_name = block.get("name", "?")
                tool_input = json.dumps(block.get("input", {}), ensure_ascii=False)
                if len(tool_input) > 300:
                    tool_input = tool_input[:300] + "..."
                log_file.write(f"[{ts}] TOOL_CALL: {tool_name}({tool_input})\n")
            elif block.get("type") == "text":
                text = block.get("text", "")
                if text.strip():
                    preview = text[:500].replace("\n", " ")
                    if len(text) > 500:
                        preview += "..."
                    log_file.write(f"[{ts}] ASSISTANT: {preview}\n")
    elif etype == "result":
        # Tool result
        subtype = event.get("subtype", "")
        if subtype == "tool_result":
            tool_name = event.get("tool_name", "?")
            content = event.get("content", "")
            if isinstance(content, str):
                preview = content[:300].replace("\n", " ")
                if len(content) > 300:
                    preview += "..."
            else:
                preview = str(content)[:300]
            log_file.write(f"[{ts}] TOOL_RESULT ({tool_name}): {preview}\n")
        elif subtype == "success":
            cost = event.get("cost_usd", 0)
            duration = event.get("duration_ms", 0)
            log_file.write(f"[{ts}] COMPLETED: cost=${cost:.4f}, duration={duration/1000:.1f}s\n")
        elif subtype == "error":
            error = event.get("error", "?")
            log_file.write(f"[{ts}] ERROR: {error}\n")
    elif etype == "system":
        msg = event.get("message", "") or event.get("subtype", "")
        if msg:
            log_file.write(f"[{ts}] SYSTEM: {msg}\n")
    else:
        # Unknown event type - log raw for debugging
        raw = json.dumps(event, ensure_ascii=False)
        if len(raw) > 500:
            raw = raw[:500] + "..."
        log_file.write(f"[{ts}] {etype or 'UNKNOWN'}: {raw}\n")

    log_file.flush()


def run_claude_analysis(clone_dir: Path, build_id: int, timeout: int) -> dict:
    log.info(f"Running Claude analysis for build {build_id} (timeout: {timeout}s)")
    prompt = f"/analyze-failures {build_id} --analyze-only"
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json",
        "--verbose",
        "--dangerously-skip-permissions",
    ]
    log.info(f"Running Claude analysis for build {build_id} (timeout: {timeout}s)")
    log.info(f"  Command: {' '.join(cmd)}")
    log.info(f"  Working dir: {clone_dir}")

    # Stream Claude output to a dedicated log file for real-time visibility
    claude_log_path = LOG_DIR / f"claude-{build_id}-{int(time.time())}.log"
    log.info(f"  Claude output log: {claude_log_path}")

    t0 = time.time()
    proc = subprocess.Popen(
        cmd,
        cwd=str(clone_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout_buf = []
    stderr_buf = []

    with open(claude_log_path, "w", encoding="utf-8") as claude_log:
        claude_log.write(f"=== Claude CLI started at {datetime.now(timezone.utc).isoformat()} ===\n")
        claude_log.write(f"=== Command: {' '.join(cmd)} ===\n")
        claude_log.write(f"=== Working dir: {clone_dir} ===\n\n")

        # Stream stdout (stream-json events) and stderr in parallel threads
        stdout_thread = threading.Thread(
            target=lambda: stdout_buf.append(
                _stream_to_file_and_buffer(proc.stdout, claude_log, "stdout", parse_events=True)
            )
        )
        stderr_thread = threading.Thread(
            target=lambda: stderr_buf.append(
                _stream_to_file_and_buffer(proc.stderr, claude_log, "stderr")
            )
        )
        stdout_thread.start()
        stderr_thread.start()

        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            elapsed = time.time() - t0
            log.error(f"Claude timed out after {elapsed:.1f}s, killing process")
            proc.kill()
            proc.wait()
            stdout_thread.join(timeout=5)
            stderr_thread.join(timeout=5)

            full_stdout = stdout_buf[0] if stdout_buf else ""
            full_stderr = stderr_buf[0] if stderr_buf else ""
            claude_log.write(f"\n\n=== TIMED OUT after {elapsed:.1f}s ===\n")

            log.error(f"  Claude log file: {claude_log_path}")
            log.error(f"  stdout (last 2000 chars): {full_stdout[-2000:] or '(empty)'}")
            log.error(f"  stderr (last 2000 chars): {full_stderr[-2000:] or '(empty)'}")
            return {
                "returncode": -1,
                "stdout": full_stdout[-2000:],
                "stderr": f"Timed out after {timeout}s. {full_stderr[-2000:]}".strip(),
                "claude_log": str(claude_log_path),
            }

        stdout_thread.join(timeout=10)
        stderr_thread.join(timeout=10)

    full_stdout = stdout_buf[0] if stdout_buf else ""
    full_stderr = stderr_buf[0] if stderr_buf else ""
    elapsed = time.time() - t0

    log.info(f"Claude exited with code {proc.returncode} after {elapsed:.1f}s")
    log.info(f"  Claude log file: {claude_log_path}")
    if proc.returncode != 0:
        log.error(f"Claude analysis failed (rc={proc.returncode})")
        log.error(f"  stdout (last 2000 chars): {full_stdout[-2000:] or '(empty)'}")
        log.error(f"  stderr (last 2000 chars): {full_stderr[-2000:] or '(empty)'}")
    else:
        log.info(f"  stdout (last 500 chars): {full_stdout[-500:] or '(empty)'}")

    return {
        "returncode": proc.returncode,
        "stdout": full_stdout[-2000:] if full_stdout else "",
        "stderr": full_stderr[-2000:] if full_stderr else "",
        "claude_log": str(claude_log_path),
    }


def upload_report(clone_dir: Path, build_id: int) -> str:
    data_dir = f"pipeline_data/{build_id}"
    log.info(f"Uploading report for build {build_id}")
    t0 = time.time()
    try:
        result = subprocess.run(
            ["uv", "run", "scripts/generate_report.py", "--data-dir", data_dir, "--upload"],
            cwd=str(clone_dir),
            capture_output=True,
            text=True,
            timeout=300,
        )
        elapsed = time.time() - t0
        if result.returncode != 0:
            log.error(f"Report upload failed (rc={result.returncode}, {elapsed:.1f}s)")
            log.error(f"  stdout: {result.stdout[-500:] if result.stdout else '(empty)'}")
            log.error(f"  stderr: {result.stderr[-500:] if result.stderr else '(empty)'}")
        else:
            log.info(f"Report upload completed in {elapsed:.1f}s")
            log.info(f"  stdout: {result.stdout[-500:] if result.stdout else '(empty)'}")
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        log.error(f"Report upload timed out after {elapsed:.1f}s")
    except Exception as e:
        log.exception(f"Report upload raised exception: {e}")
    url = find_report_url(clone_dir, build_id)
    if not url:
        log.warning(f"report_url.json not found or empty after upload")
    return url


def upload_report(clone_dir: Path, build_id: int) -> str:
    data_dir = f"pipeline_data/{build_id}"
    log.info(f"Uploading report for build {build_id}")
    result = subprocess.run(
        ["uv", "run", "scripts/generate_report.py", "--data-dir", data_dir, "--upload"],
        cwd=str(clone_dir),
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        log.error(f"Report upload failed: {result.stderr[-500:]}")
    return find_report_url(clone_dir, build_id)


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
        heal_prs.append({
            "pr_title": f"{h.get('heal_group_id', '')}: Fix {h.get('element_description', '')}",
            "pr_url": h.get("pr_url", ""),
            "is_new": h.get("status") != "existing",
            "affected_cases": h.get("affected_cases", []),
        })

    bugs = []
    for b in bug_summary:
        bugs.append({
            "bug_title": f"{b.get('bug_group_id', '')}: {b.get('suggested_title', '')}",
            "bug_url": b.get("ado_bug_url", ""),
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

    log.info(f"=== Processing build {build_id} for {pipeline_name} ===")
    t0_total = time.time()

    token = get_ado_token()

    fail_count = get_test_failure_count(build_id, org, project, token)
    log.info(f"Build {build_id} ({pipeline_name}): {fail_count} test failure(s)")

    if fail_count == 0:
        return {"status": "skipped", "reason": "no_failures", "fail_count": 0}

    clone_dir = SCRIPT_DIR / f"fsq-{build_id}-{int(time.time())}"
    try:
        clone_repo(clone_cfg["repo_url"], clone_cfg["branch"], clone_dir)

        result = run_claude_analysis(clone_dir, build_id, timeout)

        status = "success" if result["returncode"] == 0 else "failed"

        report_url = ""
        if status == "success":
            report_url = upload_report(clone_dir, build_id)

            notification_payload = build_notification_payload(
                clone_dir, build_id, pipeline_name
            )
            if notification_payload:
                notify_power_automate(webhook_url, notification_payload)

        # Build error message from both stderr and stdout for better diagnostics
        error_msg = ""
        if result["returncode"] != 0:
            parts = []
            if result["stderr"]:
                parts.append(f"stderr: {result['stderr']}")
            if result["stdout"]:
                parts.append(f"stdout: {result['stdout']}")
            error_msg = " | ".join(parts) if parts else "(no output captured)"

        elapsed_total = time.time() - t0_total
        log.info(f"=== Build {build_id} finished: {status} ({elapsed_total:.1f}s total) ===")

        ret: dict = {
            "status": status,
            "fail_count": fail_count,
            "report_url": report_url,
            "returncode": result["returncode"],
            "error": error_msg,
            "clone_dir": str(clone_dir),
            "claude_log": result.get("claude_log", ""),
            "duration_seconds": round(elapsed_total, 1),
        }

        if status != "success":
            log.warning(f"Analysis failed, keeping clone dir for inspection: {clone_dir}")

        return ret
    except Exception as e:
        elapsed_total = time.time() - t0_total
        log.exception(f"Analysis errored after {elapsed_total:.1f}s, keeping clone dir for inspection: {clone_dir}")
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
            build_number = build.get("buildNumber", "")
            build_result = build.get("result", "unknown")
            build_finish = build.get("finishTime", "unknown")
            pipeline_history = history.get(pipeline_name, {})

            if build_id in pipeline_history:
                prev = pipeline_history[build_id]
                if prev.get("status") == "success":
                    log.info(f"  Build {build_id} already succeeded, skipping")
                    continue
                log.info(f"  Build {build_id} previously failed (status={prev.get('status')}), retrying")

            log.info(f"  New build: {build_id} (number={build_number}, result={build_result}, finished={build_finish})")

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
