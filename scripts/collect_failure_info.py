#!/usr/bin/env python3
"""
Collect failure information from behave test results.

This script parses behave_result.json and collects:
- Failed case details
- Associated screenshots
- Associated element trees
- Error messages and source locations
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent))
from extract_scenario import get_scenario_text


PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
PAGE_SOURCE_DIR = PROJECT_ROOT / "logs" / "page_source"
ERROR_RESULTS_DIR = PROJECT_ROOT / "logs" / "error_results"
OUTPUT_FILE = REPORTS_DIR / "failure_info.json"


def clean_name_for_matching(name: str) -> str:
    """Clean scenario name for file matching."""
    if not name:
        return ""
    cleaned = re.sub(r"[^\w\s\-]", "_", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.replace(" ", "_")
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = cleaned.strip("_")
    return cleaned


def find_matching_files(directory: Path, case_name: str, extension: str) -> list[str]:
    """Find files matching the case name pattern.
    
    Uses exact prefix match: {cleaned_name}_YYYYMMDD to avoid
    containment issues (e.g., 'foo_bar' matching 'foo_bar_baz').
    """
    if not directory.exists():
        return []
    
    cleaned_name = clean_name_for_matching(case_name)
    # Match name followed by _YYYYMMDD (8 digits) to avoid containment
    pattern = f"{cleaned_name}_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]*{extension}"
    matches = list(directory.glob(pattern))
    return [str(f) for f in sorted(matches, key=lambda x: x.stat().st_mtime, reverse=True)]


def find_screenshots(case_name: str, screenshots_dir: Path = None) -> list[str]:
    """Find the latest screenshot for a given case (skip older retry attempts)."""
    results = find_matching_files(screenshots_dir or SCREENSHOTS_DIR, case_name, ".png")
    return results[:1]


def _timestamps_close(ts1: str, ts2: str, max_diff_seconds: int = 2) -> bool:
    """Check if two timestamps (YYYYMMDD_HHMMSS) are within max_diff_seconds."""
    from datetime import datetime as _dt
    try:
        dt1 = _dt.strptime(ts1, "%Y%m%d_%H%M%S")
        dt2 = _dt.strptime(ts2, "%Y%m%d_%H%M%S")
        return abs((dt1 - dt2).total_seconds()) <= max_diff_seconds
    except ValueError:
        return False


def _parse_agent_logs(logs_dir: Path) -> dict[str, list[str]]:
    """Parse agent log files to build screenshot_filename -> [error_result_uuid] mapping.

    Tracks error UUIDs during each scenario run and maps them to the
    screenshot saved after that run finishes. This ensures UUIDs are
    correctly associated with specific retry attempts (only the last
    attempt's screenshot and its error results are linked).

    Log format:
      'Starting Scenario (N/M): <name>'     -> reset UUID collection
      'Tool Call - Error Result - ID: <uuid> ...'  -> collect UUID
      'Screenshot saved: .../filename.png'  -> map filename to collected UUIDs
    """
    mapping: dict[str, list[str]] = {}
    if not logs_dir.exists():
        return mapping

    for log_file in sorted(logs_dir.glob("mac_automation_tests_agent_*.log")):
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        current_uuids: list[str] = []
        for line in content.split("\n"):
            if re.search(r"Starting Scenario \(\d+/\d+\):", line):
                current_uuids = []
                continue

            m = re.search(r"Error Result.*ID: ([0-9a-f-]+)", line)
            if m:
                current_uuids.append(m.group(1))
                continue

            m = re.search(r"Screenshot saved: .+/([^/]+\.png)$", line)
            if m and current_uuids:
                mapping[m.group(1)] = list(current_uuids)

    return mapping


def find_element_trees(case_name: str, page_source_dir: Path = None,
                       screenshot_files: list[str] = None,
                       error_results_dir: Path = None,
                       uuid_mapping: dict[str, list[str]] = None) -> list[str]:
    """Find element tree files for a given case.

    Strategy 1 (legacy): Match JSON files by scenario name prefix in page_source_dir.
    Strategy 2 (primary): Match error_result files by UUID from agent log.
    Strategy 3 (fallback): Match error_result files by screenshot timestamp ±5s.
    """
    # Strategy 1: legacy page_source directory
    results = find_matching_files(page_source_dir or PAGE_SOURCE_DIR, case_name, ".json")
    if results:
        return results

    er_dir = error_results_dir or ERROR_RESULTS_DIR
    if not er_dir.exists():
        return []

    # Strategy 2: UUID from agent log via screenshot filename (most reliable)
    if uuid_mapping and screenshot_files:
        matched = []
        for ss_path in screenshot_files:
            ss_name = Path(ss_path).name
            if ss_name in uuid_mapping:
                for uuid in uuid_mapping[ss_name]:
                    for er_file in er_dir.glob(f"error_result_*{uuid}*.json"):
                        matched.append(str(er_file))
        if matched:
            return sorted(matched, key=lambda x: Path(x).stat().st_mtime, reverse=True)

    # Strategy 3: timestamp fallback
    if not screenshot_files:
        return []

    ss_timestamps = set()
    for ss in screenshot_files:
        m = re.search(r'_(\d{8}_\d{6})\.png$', ss)
        if m:
            ss_timestamps.add(m.group(1))
    if not ss_timestamps:
        return []

    matched = []
    for er_file in er_dir.glob("error_result_*.json"):
        m = re.search(r'_(\d{8}_\d{6})\.json$', er_file.name)
        if not m:
            continue
        er_ts = m.group(1)
        for ss_ts in ss_timestamps:
            if _timestamps_close(ss_ts, er_ts, max_diff_seconds=5):
                matched.append(str(er_file))
                break

    return sorted(matched, key=lambda x: Path(x).stat().st_mtime, reverse=True)


def extract_step_implementation(match_location: str, context_lines: int = 30) -> Optional[str]:
    """
    Extract the step implementation code from the match_location.
    
    Args:
        match_location: Step file path and line number (e.g., "features/steps/foo.py:123")
        context_lines: Number of lines to read after the match line
    
    Returns:
        The step implementation code or None if not found
    """
    if not match_location or ":" not in match_location:
        return None
    
    try:
        file_path, line_str = match_location.rsplit(":", 1)
        line_num = int(line_str)
        
        full_path = PROJECT_ROOT / file_path
        if not full_path.exists():
            return None
        
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        start_line = max(0, line_num - 1)
        end_line = min(len(lines), line_num + context_lines)
        
        code_lines = []
        in_function = False
        indent_level = None
        
        for i in range(start_line, end_line):
            line = lines[i]
            
            if i == start_line:
                in_function = True
                indent_level = len(line) - len(line.lstrip())
                code_lines.append(line.rstrip())
                continue
            
            if in_function:
                current_indent = len(line) - len(line.lstrip())
                if line.strip() and current_indent <= indent_level and not line.strip().startswith(('@', '#')):
                    break
                code_lines.append(line.rstrip())
        
        return "\n".join(code_lines)
    except Exception:
        return None


def extract_failed_step_info(scenario: dict) -> Optional[dict]:
    """Extract information about the failed step."""
    steps = scenario.get("steps", [])
    for step in steps:
        result = step.get("result", {})
        if result.get("status") == "failed":
            match_location = step.get("match", {}).get("location", "")
            step_implementation = extract_step_implementation(match_location)
            return {
                "keyword": step.get("keyword", ""),
                "name": step.get("name", ""),
                "location": step.get("location", ""),
                "match_location": match_location,
                "error_message": result.get("error_message", []),
                "duration": result.get("duration", 0),
                "step_implementation": step_implementation
            }
    return None


def analyze_failure_type(error_message: Union[list, str]) -> dict:
    """
    Classify the error type from the error message.
    
    NOTE: is_healable is always null here. The actual healable/bug determination
    happens later after screenshot analysis (see failure_info_helper.py triage command).
    """
    if isinstance(error_message, list):
        error_text = "\n".join(error_message)
    else:
        error_text = str(error_message)
    
    error_lower = error_text.lower()
    
    element_not_found_patterns = [
        "element .* not found",
        "not found or not editable",
        "no such element",
        "unable to locate element",
        "could not find element",
        "element does not exist",
    ]
    
    element_state_patterns = [
        "stale element reference",
        "element is not attached",
        "invalid element state",
        "element not interactable",
        "element not visible",
        "not found or not clickable",
    ]
    
    for pattern in element_not_found_patterns:
        if re.search(pattern, error_lower):
            return {
                "failure_type": "element_not_found",
                "is_healable": None,
                "pattern_matched": pattern
            }
    
    for pattern in element_state_patterns:
        if re.search(pattern, error_lower):
            return {
                "failure_type": "element_state",
                "is_healable": None,
                "pattern_matched": pattern
            }
    
    if "timeout" in error_lower or "timed out" in error_lower:
        return {
            "failure_type": "timeout",
            "is_healable": None,
            "pattern_matched": "timeout"
        }
    
    if "assert" in error_lower and ("expected" in error_lower or "actual" in error_lower):
        return {
            "failure_type": "assertion",
            "is_healable": None,
            "pattern_matched": "assertion"
        }
    
    return {
        "failure_type": "unknown",
        "is_healable": None,
        "pattern_matched": None
    }


def find_behave_result_files(reports_dir: Path = None) -> list[Path]:
    """Find all behave result JSON files in reports directory."""
    reports_dir = reports_dir or REPORTS_DIR
    patterns = ["behave_result*.json", "*_behave_result.json"]
    files = []
    for pattern in patterns:
        files.extend(reports_dir.glob(pattern))
    return sorted(set(files), key=lambda x: x.stat().st_mtime, reverse=True)


def parse_behave_results(reports_dir: Path = None, screenshots_dir: Path = None,
                        page_source_dir: Path = None, error_results_dir: Path = None,
                        logs_dir: Path = None) -> list[dict]:
    """Parse all behave_result*.json files and extract failed cases."""
    reports_dir = reports_dir or REPORTS_DIR
    result_files = find_behave_result_files(reports_dir)
    if not result_files:
        raise FileNotFoundError(f"No behave result files found in: {reports_dir}")

    # Build scenario -> UUID mapping from agent logs
    _logs_dir = logs_dir or (PROJECT_ROOT / "logs")
    uuid_mapping = _parse_agent_logs(_logs_dir)
    if not result_files:
        raise FileNotFoundError(f"No behave result files found in: {reports_dir}")
    
    print(f"Found {len(result_files)} behave result file(s):")
    for f in result_files:
        print(f"  - {f.name}")
    
    all_results = []
    for result_file in result_files:
        with open(result_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                all_results.extend(data)
    
    case_status: dict[str, str] = {}
    case_data: dict[str, dict] = {}
    
    for feature in all_results:
        feature_name = feature.get("name", "Unknown Feature")
        
        for element in feature.get("elements", []):
            if element.get("type") != "scenario":
                continue
            
            scenario_name = element.get("name", "Unknown Scenario")
            scenario_location = element.get("location", "")
            feature_file = scenario_location.split(":")[0] if ":" in scenario_location else ""
            dedup_key = f"{feature_file}::{scenario_name}"
            
            current_status = element.get("status", "unknown")
            
            if current_status == "passed":
                case_status[dedup_key] = "passed"
            elif current_status == "failed" and case_status.get(dedup_key) != "passed":
                case_status[dedup_key] = "failed"
                
                failed_step = extract_failed_step_info(element)
                error_message = failed_step.get("error_message", []) if failed_step else []
                failure_analysis = analyze_failure_type(error_message)
                
                scenario_text = None
                if feature_file:
                    try:
                        scenario_text = get_scenario_text(str(PROJECT_ROOT / feature_file), scenario_name)
                    except Exception:
                        pass
                
                    screenshots = find_screenshots(scenario_name, screenshots_dir)
                case_data[dedup_key] = {
                    "scenario_name": scenario_name,
                    "feature_name": feature_name,
                    "feature_file": feature_file,
                    "scenario_location": scenario_location,
                    "tags": element.get("tags", []),
                    "scenario_steps": scenario_text,
                    "failed_step": failed_step,
                    "failure_analysis": failure_analysis,
                    "screenshots": screenshots,
                    "element_trees": find_element_trees(
                        scenario_name, page_source_dir,
                        screenshot_files=screenshots,
                        error_results_dir=error_results_dir,
                        uuid_mapping=uuid_mapping,
                    ),
                    "collected_at": datetime.now().isoformat()
                }
    
    failed_cases = [
        case_data[key] for key in case_data
        if case_status.get(key) == "failed"
    ]
    
    retry_success_count = len(case_data) - len(failed_cases)
    if retry_success_count > 0:
        print(f"  - {retry_success_count} case(s) failed but passed on retry (excluded)")
    
    return failed_cases


def collect_and_save(data_dir: str = None):
    """Main function to collect failure info and save to JSON."""
    if data_dir:
        data_path = Path(data_dir)
        reports_dir = data_path / "reports"
        screenshots_dir = data_path / "screenshots"
        page_source_dir = data_path / "logs" / "page_source"
        error_results_dir = data_path / "logs" / "error_results"
        logs_dir = data_path / "logs"
        output_file = data_path / "reports" / "failure_info.json"
    else:
        reports_dir = REPORTS_DIR
        screenshots_dir = SCREENSHOTS_DIR
        page_source_dir = PAGE_SOURCE_DIR
        error_results_dir = ERROR_RESULTS_DIR
        logs_dir = PROJECT_ROOT / "logs"
        output_file = OUTPUT_FILE

    print(f"Searching for behave result files in: {reports_dir}")
    
    try:
        failed_cases = parse_behave_results(reports_dir, screenshots_dir, page_source_dir, error_results_dir, logs_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    
    # Count by error type (is_healable is null until screenshot triage)
    type_counts = {}
    for c in failed_cases:
        ft = c["failure_analysis"]["failure_type"]
        type_counts[ft] = type_counts.get(ft, 0) + 1
    
    output = {
        "summary": {
            "total_failures": len(failed_cases),
            "healable_failures": 0,
            "non_healable_failures": 0,
            "pending_triage": len(failed_cases),
            "collected_at": datetime.now().isoformat()
        },
        "failed_cases": failed_cases,
        "heal_summary": [],
        "bug_summary": []
    }
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Collected {len(failed_cases)} failed cases")
    for ft, count in sorted(type_counts.items()):
        print(f"  - {ft}: {count}")
    print(f"  (all pending screenshot triage)")
    print(f"Output saved to: {output_file}")
    print(f"Output saved to: {output_file}")
    
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect failure info from behave results")
    parser.add_argument("--data-dir", help="Pipeline data directory (e.g., pipeline_data/141562849)")
    args = parser.parse_args()
    collect_and_save(data_dir=args.data_dir)
