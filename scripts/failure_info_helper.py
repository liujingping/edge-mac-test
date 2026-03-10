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


def get_healable():
    """Get all healable cases for grouping analysis."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    healable_cases = []
    for i, case in enumerate(cases):
        healable = case.get("failure_analysis", {}).get("is_healable", False)
        if healable:
            healable_cases.append((i, case))
    
    if not healable_cases:
        print("No healable cases found.")
        return
    
    print(f"=== {len(healable_cases)} Healable Cases ===")
    print("")
    for i, case in healable_cases:
        print(f"[{i}] {case['scenario_name']}")
        print(f"    feature: {case.get('feature_name', 'N/A')}")
        error = case.get('failed_step', {}).get('error_message', ['N/A'])
        print(f"    error: {(error[0] if error else 'N/A')[:150]}")
        step_file = case.get('failed_step', {}).get('step_file', 'N/A')
        print(f"    step_file: {step_file}")
        heal_group = case.get('failure_analysis', {}).get('heal_group_id')
        if heal_group:
            print(f"    heal_group_id: {heal_group}")
        print("")


def get_heal_summary():
    """Get heal_summary for viewing grouped healable cases."""
    data = load_failure_info()
    heal_summary = data.get("heal_summary", [])
    
    if not heal_summary:
        print("No heal groups found.")
        return
    
    print(f"=== {len(heal_summary)} Heal Groups ===")
    print("")
    for heal in heal_summary:
        print(f"[{heal.get('heal_group_id')}] {heal.get('element_description', 'N/A')}")
        print(f"    affected_cases: {len(heal.get('affected_cases', []))} cases")
        print(f"    step_file: {heal.get('step_file', 'N/A')}")
        print(f"    status: {heal.get('status', 'pending')}")
        if heal.get('pr_url'):
            print(f"    pr_url: {heal['pr_url']}")
        print("")


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
            print(f"Feature: {case.get('feature_name', 'N/A')}")
            error = case.get('failed_step', {}).get('error_message', ['N/A'])
            print(f"Error: {error[0][:300] if error else 'N/A'}")
            screenshots = case.get("screenshots", [])
            if screenshots:
                print(f"Screenshot: {screenshots[0]}")
            else:
                print("Screenshot: none")
            scenario_steps = case.get("scenario_steps")
            if scenario_steps:
                print(f"Steps:\n{scenario_steps}")
            step_impl = case.get('failed_step', {}).get('step_implementation')
            if step_impl:
                print(f"Step Implementation:\n{step_impl}")
            return
    print("All cases analyzed or healable.")


def get_pending_all():
    """Get ALL pending cases for parallel subagent processing."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    pending_cases = []
    for i, case in enumerate(cases):
        healable = case.get("failure_analysis", {}).get("is_healable", False)
        has_analysis = "ai_analysis" in case
        if not healable and not has_analysis:
            pending_cases.append((i, case))
    
    if not pending_cases:
        print("All cases analyzed or healable.")
        return
    
    print(f"=== {len(pending_cases)} Pending Cases ===")
    print("")
    for i, case in pending_cases:
        print(f"--- Case {i} ---")
        print(f"Index: {i}")
        print(f"Scenario: {case['scenario_name']}")
        print(f"Feature: {case.get('feature_name', 'N/A')}")
        error = case.get('failed_step', {}).get('error_message', ['N/A'])
        print(f"Error: {error[0][:300] if error else 'N/A'}")
        screenshots = case.get("screenshots", [])
        if screenshots:
            print(f"Screenshot: {screenshots[0]}")
        else:
            print("Screenshot: none")
        scenario_steps = case.get("scenario_steps")
        if scenario_steps:
            print(f"Steps:\n{scenario_steps}")
        step_impl = case.get('failed_step', {}).get('step_implementation')
        if step_impl:
            print(f"Step Implementation:\n{step_impl}")
        print("")


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


def get_summary_for_dedup():
    """Get minimal summary of analyzed cases for bug deduplication."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    print("=== Analyzed Cases Summary (for bug dedup) ===\n")
    for i, case in enumerate(cases):
        ai = case.get("ai_analysis")
        if not ai:
            continue
        if not ai.get("is_likely_bug", False):
            continue
        print(f"[{i}] {case['scenario_name'][:60]}")
        print(f"    title: {ai.get('suggested_bug_title', 'N/A')[:80]}")
        print(f"    category: {ai.get('bug_category', 'N/A')}")
        error = case.get('failed_step', {}).get('error_message', ['N/A'])
        print(f"    error: {(error[0] if error else 'N/A')[:100]}")
        print(f"    feature: {case.get('feature_name', 'N/A')}")
        if ai.get("bug_group_id"):
            print(f"    bug_group_id: {ai['bug_group_id']}")
        print("")


def update_observation(index: int, observable_state: str, expected_state: str, difference: str, failed_functionality: str):
    """Update observation from subagent (no bug judgment)."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    if index >= len(cases):
        print(f"Error: index {index} out of range")
        return
    
    cases[index]["ai_analysis"] = {
        "observable_state": observable_state,
        "expected_state": expected_state,
        "difference": difference,
        "failed_functionality": failed_functionality,
        "is_likely_bug": None,
        "bug_confidence": None,
        "bug_category": None
    }
    
    save_failure_info(data)
    print(f"Updated case {index} with observation")


def get_observations():
    """Get ALL observations for main agent bug analysis."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    print("=== All Case Observations (for bug analysis) ===\n")
    for i, case in enumerate(cases):
        healable = case.get("failure_analysis", {}).get("is_healable", False)
        if healable:
            print(f"[{i}] {case['scenario_name'][:50]}")
            print(f"    [HEALABLE - skip bug analysis]\n")
            continue
        
        ai = case.get("ai_analysis", {})
        print(f"[{i}] {case['scenario_name'][:50]}")
        print(f"    feature: {case.get('feature_name', 'N/A')}")
        print(f"    failed_functionality: {ai.get('failed_functionality', 'N/A')}")
        print(f"    difference: {ai.get('difference', 'N/A')[:150]}")
        error = case.get('failed_step', {}).get('error_message', ['N/A'])
        print(f"    error: {(error[0] if error else 'N/A')[:80]}")
        if ai.get("bug_group_id"):
            print(f"    bug_group_id: {ai['bug_group_id']}")
        print("")


def set_bug_groups(group_id: str, indices: list, reason: str, title: str, is_bug: bool = True, confidence: float = 0.8, category: str = "functional_bug"):
    """Set bug_group_id for multiple cases and create/update bug_summary."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    affected_cases = []
    
    for idx in indices:
        if idx >= len(cases):
            print(f"Warning: index {idx} out of range, skipping")
            continue
        case = cases[idx]
        ai = case.get("ai_analysis", {})
        ai["bug_group_id"] = group_id
        ai["bug_group_reason"] = reason
        ai["is_likely_bug"] = is_bug
        ai["bug_confidence"] = confidence
        ai["bug_category"] = category
        ai["suggested_bug_title"] = title
        case["ai_analysis"] = ai
        affected_cases.append(case["scenario_name"])
    
    bug_summary = data.get("bug_summary", [])
    existing = next((b for b in bug_summary if b.get("bug_group_id") == group_id), None)
    if existing:
        existing["affected_cases"] = affected_cases
        existing["suggested_title"] = title
        existing["bug_group_reason"] = reason
    else:
        bug_summary.append({
            "bug_group_id": group_id,
            "suggested_title": title,
            "affected_cases": affected_cases,
            "bug_category": category,
            "confidence": confidence,
            "is_likely_bug": is_bug,
            "bug_group_reason": reason,
            "status": "pending"
        })
    data["bug_summary"] = bug_summary
    
    save_failure_info(data)
    print(f"Set {group_id} for cases: {indices}")
    print(f"Title: {title}")


def set_heal_group(heal_group_id: str, indices: list, element_description: str, step_file: str):
    """Set heal_group_id for multiple cases and create heal_summary entry."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    affected_cases = []
    
    for idx in indices:
        if idx >= len(cases):
            print(f"Warning: index {idx} out of range, skipping")
            continue
        case = cases[idx]
        fa = case.get("failure_analysis", {})
        fa["is_healable"] = True
        fa["heal_group_id"] = heal_group_id
        fa["heal_group_reason"] = f"Same '{element_description}' element"
        case["failure_analysis"] = fa
        affected_cases.append(case["scenario_name"])
    
    heal_summary = data.get("heal_summary", [])
    existing = next((h for h in heal_summary if h.get("heal_group_id") == heal_group_id), None)
    if existing:
        existing["affected_cases"] = affected_cases
        existing["element_description"] = element_description
        existing["step_file"] = step_file
    else:
        heal_summary.append({
            "heal_group_id": heal_group_id,
            "element_description": element_description,
            "affected_cases": affected_cases,
            "step_file": step_file,
            "status": "pending"
        })
    data["heal_summary"] = heal_summary
    
    save_failure_info(data)
    print(f"Set {heal_group_id} for cases: {indices}")
    print(f"Element: {element_description}")


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


def update_bug_url(bug_group_id: str, ado_bug_url: str):
    """Update bug_summary with ADO bug URL."""
    data = load_failure_info()
    bug_summary = data.get("bug_summary", [])
    
    found = False
    for bug in bug_summary:
        if bug.get("bug_group_id") == bug_group_id:
            bug["ado_bug_url"] = ado_bug_url
            bug["status"] = "created"
            found = True
            break
    
    if not found:
        print(f"Error: bug_group_id '{bug_group_id}' not found")
        return
    
    cases = data.get("failed_cases", [])
    for case in cases:
        ai = case.get("ai_analysis", {})
        if ai.get("bug_group_id") == bug_group_id:
            ai["ado_bug_url"] = ado_bug_url
    
    save_failure_info(data)
    print(f"Updated {bug_group_id}: ado_bug_url={ado_bug_url}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python failure_info_helper.py list                - List all cases")
        print("  python failure_info_helper.py get <index>         - Get case details")
        print("  python failure_info_helper.py healable            - Get all healable cases for grouping")
        print("  python failure_info_helper.py heal_summary        - Get heal_summary (grouped healable cases)")
        print("  python failure_info_helper.py pending             - Get next pending case")
        print("  python failure_info_helper.py pending_all         - Get ALL pending cases")
        print("  python failure_info_helper.py update_observation <index> <observable> <expected> <diff> <functionality>")
        print("  python failure_info_helper.py observations        - Get all observations for bug analysis")
        print("  python failure_info_helper.py summary             - Get analyzed cases summary")
        print("  python failure_info_helper.py set_bug_group <id> <indices> <reason> <title> [is_bug] [confidence] [category]")
        print("  python failure_info_helper.py set_heal_group <id> <indices> <element_description> <step_file>")
        print("  python failure_info_helper.py update_heal <id> <status> [pr_url] [fix]")
        print("  python failure_info_helper.py update_bug_url <bug_group_id> <ado_bug_url>")
        print("")
        print("Examples:")
        print("  python failure_info_helper.py healable")
        print("  python failure_info_helper.py pending")
        print("  python failure_info_helper.py update_observation 0 'Shows empty search' 'Should show results' 'No results' 'search tabs'")
        print("  python failure_info_helper.py observations")
        print("  python failure_info_helper.py set_bug_group BUG-001 '0,1,2' 'Same failure' '[Edge] Bug' true 0.85 functional_bug")
        print("  python failure_info_helper.py set_heal_group HEAL-001 '0,1' 'Search settings input' 'features/steps/settings.py'")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        list_cases()
    elif cmd == "get":
        get_case(int(sys.argv[2]))
    elif cmd == "healable":
        get_healable()
    elif cmd == "heal_summary":
        get_heal_summary()
    elif cmd == "pending":
        get_pending()
    elif cmd == "pending_all":
        get_pending_all()
    elif cmd == "update_observation":
        index = int(sys.argv[2])
        observable = sys.argv[3]
        expected = sys.argv[4]
        diff = sys.argv[5]
        functionality = sys.argv[6] if len(sys.argv) > 6 else ""
        update_observation(index, observable, expected, diff, functionality)
    elif cmd == "observations":
        get_observations()
    elif cmd == "update":
        index = int(sys.argv[2])
        is_bug = sys.argv[3].lower() == "true"
        confidence = float(sys.argv[4])
        category = sys.argv[5]
        title = sys.argv[6]
        reason = sys.argv[7] if len(sys.argv) > 7 else ""
        update_analysis(index, is_bug, confidence, category, title, reason)
    elif cmd == "summary":
        get_summary_for_dedup()
    elif cmd == "set_bug_group":
        group_id = sys.argv[2]
        indices = [int(x.strip()) for x in sys.argv[3].split(",")]
        reason = sys.argv[4]
        title = sys.argv[5]
        is_bug = sys.argv[6].lower() == "true" if len(sys.argv) > 6 else True
        confidence = float(sys.argv[7]) if len(sys.argv) > 7 else 0.8
        category = sys.argv[8] if len(sys.argv) > 8 else "functional_bug"
        set_bug_groups(group_id, indices, reason, title, is_bug, confidence, category)
    elif cmd == "set_heal_group":
        group_id = sys.argv[2]
        indices = [int(x.strip()) for x in sys.argv[3].split(",")]
        element_description = sys.argv[4]
        step_file = sys.argv[5] if len(sys.argv) > 5 else ""
        set_heal_group(group_id, indices, element_description, step_file)
    elif cmd == "update_heal":
        heal_group_id = sys.argv[2]
        status = sys.argv[3]
        pr_url = sys.argv[4] if len(sys.argv) > 4 else ""
        fix_applied = sys.argv[5] if len(sys.argv) > 5 else ""
        update_heal(heal_group_id, status, pr_url, fix_applied)
    elif cmd == "update_bug_url":
        bug_group_id = sys.argv[2]
        ado_bug_url = sys.argv[3]
        update_bug_url(bug_group_id, ado_bug_url)
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
