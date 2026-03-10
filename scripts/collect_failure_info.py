#!/usr/bin/env python3
"""
Collect failure information from behave test results.

This script parses behave_result.json and collects:
- Failed case details
- Associated screenshots
- Associated element trees
- Error messages and source locations
"""

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
    """Find files matching the case name pattern."""
    if not directory.exists():
        return []
    
    cleaned_name = clean_name_for_matching(case_name)
    pattern = f"*{cleaned_name}*{extension}"
    matches = list(directory.glob(pattern))
    return [str(f) for f in sorted(matches, key=lambda x: x.stat().st_mtime, reverse=True)]


def find_screenshots(case_name: str) -> list[str]:
    """Find screenshots for a given case."""
    return find_matching_files(SCREENSHOTS_DIR, case_name, ".png")


def find_element_trees(case_name: str) -> list[str]:
    """Find element tree JSON files for a given case."""
    return find_matching_files(PAGE_SOURCE_DIR, case_name, ".json")


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
    Analyze the failure type based on error message.
    Returns a dict with failure_type and is_element_change flag.
    """
    if isinstance(error_message, list):
        error_text = "\n".join(error_message)
    else:
        error_text = str(error_message)
    
    error_lower = error_text.lower()
    
    element_change_patterns = [
        "element .* not found",
        "not found or not editable",
        "no such element",
        "unable to locate element",
        "could not find element",
        "element does not exist",
        "stale element reference",
        "element is not attached",
        "invalid element state",
        "element not interactable",
        "element not visible"
    ]
    
    for pattern in element_change_patterns:
        if re.search(pattern, error_lower):
            return {
                "failure_type": "element_change",
                "is_healable": True,
                "pattern_matched": pattern
            }
    
    if "timeout" in error_lower or "timed out" in error_lower:
        return {
            "failure_type": "timeout",
            "is_healable": False,
            "pattern_matched": "timeout"
        }
    
    if "assert" in error_lower and ("expected" in error_lower or "actual" in error_lower):
        return {
            "failure_type": "assertion",
            "is_healable": False,
            "pattern_matched": "assertion"
        }
    
    return {
        "failure_type": "unknown",
        "is_healable": False,
        "pattern_matched": None
    }


def find_behave_result_files() -> list[Path]:
    """Find all behave result JSON files in reports directory."""
    patterns = ["behave_result*.json", "*_behave_result.json"]
    files = []
    for pattern in patterns:
        files.extend(REPORTS_DIR.glob(pattern))
    return sorted(set(files), key=lambda x: x.stat().st_mtime, reverse=True)


def parse_behave_results() -> list[dict]:
    """Parse all behave_result*.json files and extract failed cases."""
    result_files = find_behave_result_files()
    if not result_files:
        raise FileNotFoundError(f"No behave result files found in: {REPORTS_DIR}")
    
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
                
                case_data[dedup_key] = {
                    "scenario_name": scenario_name,
                    "feature_name": feature_name,
                    "feature_file": feature_file,
                    "scenario_location": scenario_location,
                    "tags": element.get("tags", []),
                    "scenario_steps": scenario_text,
                    "failed_step": failed_step,
                    "failure_analysis": failure_analysis,
                    "screenshots": find_screenshots(scenario_name),
                    "element_trees": find_element_trees(scenario_name),
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


def collect_and_save():
    """Main function to collect failure info and save to JSON."""
    print(f"Searching for behave result files in: {REPORTS_DIR}")
    
    try:
        failed_cases = parse_behave_results()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    
    healable_count = sum(1 for c in failed_cases if c["failure_analysis"]["is_healable"])
    
    heal_summary = []
    bug_summary = []
    
    for i, case in enumerate(failed_cases):
        if case["failure_analysis"]["is_healable"]:
            error_msg = case.get("failed_step", {}).get("error_message", [])
            element_desc = error_msg[0][:100] if error_msg else "Element not found"
            heal_summary.append({
                "heal_group_id": f"HEAL-{len(heal_summary)+1:03d}",
                "element_description": element_desc,
                "affected_cases": [case["scenario_name"]],
                "step_file": case.get("failed_step", {}).get("match_location", ""),
                "status": "pending"
            })
        else:
            bug_summary.append({
                "bug_group_id": f"BUG-{len(bug_summary)+1:03d}",
                "suggested_title": f"[Auto] {case['scenario_name']}",
                "affected_cases": [case["scenario_name"]],
                "bug_category": case["failure_analysis"]["failure_type"],
                "confidence": 0,
                "status": "pending"
            })
    
    output = {
        "summary": {
            "total_failures": len(failed_cases),
            "healable_failures": healable_count,
            "non_healable_failures": len(failed_cases) - healable_count,
            "collected_at": datetime.now().isoformat()
        },
        "failed_cases": failed_cases,
        "heal_summary": heal_summary,
        "bug_summary": bug_summary
    }
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Collected {len(failed_cases)} failed cases")
    print(f"  - Healable (element changes): {healable_count}")
    print(f"  - Non-healable: {len(failed_cases) - healable_count}")
    print(f"Output saved to: {OUTPUT_FILE}")
    
    return output


if __name__ == "__main__":
    collect_and_save()
