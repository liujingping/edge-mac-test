#!/usr/bin/env python3
"""
Helper script for failure_info.json operations.
Reduces context usage by only outputting necessary information.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FAILURE_INFO_FILE = PROJECT_ROOT / "reports" / "failure_info.json"


def load_failure_info() -> dict:
    with open(FAILURE_INFO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_failure_info(data: dict):
    with open(FAILURE_INFO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_cases():
    """List all cases with minimal info."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    print(f"Total: {len(cases)} failed cases\n")
    for i, case in enumerate(cases):
        healable = case.get("failure_analysis", {}).get("is_healable", False)
        has_analysis = "ai_analysis" in case
        status = "healable" if healable else ("analyzed" if has_analysis else "pending")
        screenshots = case.get("screenshots", [])
        screenshot = Path(screenshots[0]).name if screenshots else "none"
        print(f"{i}: [{status}] {case['scenario_name'][:50]}")
        print(f"   screenshot: {screenshot}")


def get_case(index: int):
    """Get single case info for analysis."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    if index >= len(cases):
        print(f"Error: index {index} out of range (0-{len(cases)-1})")
        return
    case = cases[index]
    print(f"Index: {index}")
    print(f"Scenario: {case['scenario_name']}")
    print(f"Feature: {case['feature_name']}")
    print(f"Healable: {case.get('failure_analysis', {}).get('is_healable', False)}")
    print(f"Error: {case.get('failed_step', {}).get('error_message', ['N/A'])[0][:200]}")
    screenshots = case.get("screenshots", [])
    if screenshots:
        print(f"Screenshot: {screenshots[0]}")
    else:
        print("Screenshot: none")


def get_pending():
    """Get next pending case that needs AI analysis."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    for i, case in enumerate(cases):
        healable = case.get("failure_analysis", {}).get("is_healable", False)
        has_analysis = "ai_analysis" in case
        if not healable and not has_analysis:
            print(f"Index: {i}")
            print(f"Scenario: {case['scenario_name']}")
            error = case.get('failed_step', {}).get('error_message', ['N/A'])
            print(f"Error: {error[0][:200] if error else 'N/A'}")
            screenshots = case.get("screenshots", [])
            if screenshots:
                print(f"Screenshot: {screenshots[0]}")
            return
    print("All cases analyzed or healable.")


def update_analysis(index: int, is_bug: bool, confidence: float, category: str, title: str, reason: str):
    """Update AI analysis for a case."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    if index >= len(cases):
        print(f"Error: index {index} out of range")
        return
    
    cases[index]["ai_analysis"] = {
        "is_likely_bug": is_bug,
        "bug_confidence": confidence,
        "bug_category": category,
        "suggested_bug_title": title,
        "analysis_reason": reason
    }
    
    bug_summary = data.get("bug_summary", [])
    for bug in bug_summary:
        if cases[index]["scenario_name"] in bug.get("affected_cases", []):
            bug["suggested_title"] = title
            bug["bug_category"] = category
            bug["confidence"] = confidence
            break
    
    save_failure_info(data)
    print(f"Updated case {index} with AI analysis")


def update_heal(heal_group_id: str, status: str, pr_url: str = "", fix_applied: str = ""):
    """Update heal_summary with status and PR URL."""
    data = load_failure_info()
    heal_summary = data.get("heal_summary", [])
    
    found = False
    for heal in heal_summary:
        if heal.get("heal_group_id") == heal_group_id:
            heal["status"] = status
            if pr_url:
                heal["pr_url"] = pr_url
            if fix_applied:
                heal["fix_applied"] = fix_applied
            found = True
            break
    
    if not found:
        print(f"Error: heal_group_id '{heal_group_id}' not found")
        return
    
    save_failure_info(data)
    print(f"Updated {heal_group_id}: status={status}, pr_url={pr_url}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python failure_info_helper.py list              - List all cases")
        print("  python failure_info_helper.py get <index>       - Get case details")
        print("  python failure_info_helper.py pending           - Get next pending case")
        print("  python failure_info_helper.py update <index> <is_bug> <confidence> <category> <title> <reason>")
        print("  python failure_info_helper.py update_heal <heal_group_id> <status> [pr_url] [fix_applied]")
        print("")
        print("Examples:")
        print("  python failure_info_helper.py pending")
        print("  python failure_info_helper.py update 0 true 0.8 timeout '[Edge] Search tabs timeout' 'Test infrastructure issue'")
        print("  python failure_info_helper.py update_heal HEAL-001 healed 'https://github.com/org/repo/pull/123' 'Updated XPath'")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        list_cases()
    elif cmd == "get":
        get_case(int(sys.argv[2]))
    elif cmd == "pending":
        get_pending()
    elif cmd == "update":
        index = int(sys.argv[2])
        is_bug = sys.argv[3].lower() == "true"
        confidence = float(sys.argv[4])
        category = sys.argv[5]
        title = sys.argv[6]
        reason = sys.argv[7] if len(sys.argv) > 7 else ""
        update_analysis(index, is_bug, confidence, category, title, reason)
    elif cmd == "update_heal":
        heal_group_id = sys.argv[2]
        status = sys.argv[3]
        pr_url = sys.argv[4] if len(sys.argv) > 4 else ""
        fix_applied = sys.argv[5] if len(sys.argv) > 5 else ""
        update_heal(heal_group_id, status, pr_url, fix_applied)
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
