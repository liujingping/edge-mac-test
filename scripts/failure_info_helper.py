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

# Will be overridden by --data-dir if provided
_failure_info_file = None


def get_failure_info_file() -> Path:
    return _failure_info_file or FAILURE_INFO_FILE


def load_failure_info() -> dict:
    with open(get_failure_info_file(), "r", encoding="utf-8") as f:
        return json.load(f)


def save_failure_info(data: dict):
    with open(get_failure_info_file(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_cases():
    """List all cases with minimal info."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    print(f"Total: {len(cases)} failed cases\n")
    for i, case in enumerate(cases):
        is_healable = case.get("failure_analysis", {}).get("is_healable")
        has_analysis = "ai_analysis" in case
        if is_healable is None:
            status = "needs_triage"
        elif is_healable == "visual_flaky":
            status = "visual_flaky"
        elif is_healable:
            status = "healable"
        elif has_analysis:
            status = "analyzed"
        else:
            status = "pending"
        ft = case.get("failure_analysis", {}).get("failure_type", "?")
        screenshots = case.get("screenshots", [])
        screenshot = Path(screenshots[0]).name if screenshots else "none"
        print(f"{i}: [{status}] [{ft}] {case['scenario_name'][:50]}")
        print(f"   screenshot: {screenshot}")


def get_case(index: int):
    """Get single case info for analysis."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    if index >= len(cases):
        print(f"Error: index {index} out of range (0-{len(cases)-1})")
        return
    case = cases[index]
    fa = case.get("failure_analysis", {})
    print(f"Index: {index}")
    print(f"Scenario: {case['scenario_name']}")
    print(f"Feature: {case['feature_name']}")
    print(f"Failure type: {fa.get('failure_type', 'unknown')}")
    print(f"Healable: {fa.get('is_healable')}")
    print(f"Error: {case.get('failed_step', {}).get('error_message', ['N/A'])[0][:200]}")
    screenshots = case.get("screenshots", [])
    if screenshots:
        print(f"Screenshot: {screenshots[0]}")
    else:
        print("Screenshot: none")


def get_triage():
    """Get all cases pending screenshot-based triage (is_healable is null)."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    pending = []
    for i, case in enumerate(cases):
        if case.get("failure_analysis", {}).get("is_healable") is None:
            pending.append((i, case))
    
    if not pending:
        print("All cases triaged.")
        return
    
    print(f"=== {len(pending)} Cases Pending Triage ===")
    print("")
    for i, case in pending:
        fa = case.get("failure_analysis", {})
        print(f"--- Case {i} ---")
        print(f"Index: {i}")
        print(f"Scenario: {case['scenario_name']}")
        print(f"Feature: {case.get('feature_name', 'N/A')}")
        print(f"Failure type: {fa.get('failure_type', 'unknown')}")
        error = case.get('failed_step', {}).get('error_message', ['N/A'])
        print(f"Error: {(error[0] if error else 'N/A')[:300]}")
        screenshots = case.get("screenshots", [])
        if screenshots:
            print(f"Screenshot: {screenshots[0]}")
        else:
            print("Screenshot: none")
        element_trees = case.get("element_trees", [])
        if element_trees:
            print(f"Element Tree: {element_trees[0]}")
        else:
            print("Element Tree: none")
        scenario_steps = case.get("scenario_steps")
        if scenario_steps:
            print(f"Steps:\n{scenario_steps}")
        step_impl = case.get('failed_step', {}).get('step_implementation')
        if step_impl:
            print(f"Step Implementation:\n{step_impl}")
        print("")


def get_triage_v2():
    """Get all pending triage cases with success screenshot paths for v2 comparison triage.
    
    Outputs everything a subagent needs: index, scenario, failed step, error (first line only),
    fail screenshot (compressed), success screenshot (compressed), and debug log path.
    """
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    data_dir = get_failure_info_file().parent.parent
    debug_dir = data_dir / "reports" / "triage_debug"
    debug_dir.mkdir(parents=True, exist_ok=True)

    pending = []
    for i, case in enumerate(cases):
        if case.get("failure_analysis", {}).get("is_healable") is None:
            pending.append((i, case))

    if not pending:
        print("All cases triaged.")
        return

    print(f"=== {len(pending)} Cases Pending Comparison Triage ===")
    print("")
    for i, case in pending:
        scenario_name = case["scenario_name"]
        failed_step = case.get("failed_step", {})
        failed_step_name = f'{failed_step.get("keyword", "")}{failed_step.get("name", "N/A")}'
        error_lines = failed_step.get("error_message", ["N/A"])
        error_first_line = (error_lines[0] if error_lines else "N/A").split("\n")[0][:300]

        screenshots = case.get("screenshots", [])
        if screenshots:
            fail_original = screenshots[0]
            fail_compressed = fail_original.replace("screenshots/", "screenshots_compressed/").replace(".png", ".jpg")
        else:
            fail_original = "none"
            fail_compressed = "none"

        debug_log = str(debug_dir / f"case_{i}.md")

        print(f"--- Case {i} ---")
        print(f"INDEX: {i}")
        print(f"SCENARIO: {scenario_name}")
        print(f"FAILED_STEP: {failed_step_name}")
        print(f"ERROR: {error_first_line}")
        print(f"FAIL_SCREENSHOT: {fail_compressed}")
        print(f"DEBUG_LOG: {debug_log}")
        print("")


def update_triage(index: int, is_healable, reason: str,
                  observable_state: str = "", expected_state: str = "",
                  difference: str = "", failed_functionality: str = ""):
    """Update triage result for a case after screenshot analysis.
    
    Sets is_healable and stores the triage reason.
    is_healable can be True, False, or "visual_flaky".
    For bug cases, also stores observation fields (observable_state, expected_state,
    difference, failed_functionality) so a separate analysis step is not needed.
    """
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    if index >= len(cases):
        print(f"Error: index {index} out of range")
        return
    
    fa = cases[index].get("failure_analysis", {})
    fa["is_healable"] = is_healable
    fa["triage_reason"] = reason
    cases[index]["failure_analysis"] = fa
    
    if is_healable is False and observable_state:
        cases[index]["ai_analysis"] = {
            "observable_state": observable_state,
            "expected_state": expected_state,
            "difference": difference,
            "failed_functionality": failed_functionality,
            "is_likely_bug": None,
            "bug_confidence": None,
            "bug_category": None
        }
    
    healable_count = sum(1 for c in cases if c.get("failure_analysis", {}).get("is_healable") is True)
    non_healable_count = sum(1 for c in cases if c.get("failure_analysis", {}).get("is_healable") is False)
    visual_flaky_count = sum(1 for c in cases if c.get("failure_analysis", {}).get("is_healable") == "visual_flaky")
    pending_count = sum(1 for c in cases if c.get("failure_analysis", {}).get("is_healable") is None)
    
    data["summary"]["healable_failures"] = healable_count
    data["summary"]["non_healable_failures"] = non_healable_count
    data["summary"]["visual_flaky_failures"] = visual_flaky_count
    data["summary"]["pending_triage"] = pending_count
    
    save_failure_info(data)
    if is_healable == "visual_flaky":
        label = "VISUAL_FLAKY"
    elif is_healable:
        label = "HEALABLE"
    else:
        label = "BUG"
    print(f"Triaged case {index} as {label}: {reason}")
    if is_healable is False and observable_state:
        print(f"  (observation also saved)")


def get_healable():
    """Get all healable cases for grouping analysis."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    healable_cases = []
    for i, case in enumerate(cases):
        if case.get("failure_analysis", {}).get("is_healable") is True:
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
        step_file = case.get('failed_step', {}).get('match_location', 'N/A')
        print(f"    step_file: {step_file}")
        triage_reason = case.get('failure_analysis', {}).get('triage_reason', '')
        if triage_reason:
            print(f"    triage_reason: {triage_reason}")
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
    """Get next pending case that needs AI analysis (non-healable, no ai_analysis yet)."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    for i, case in enumerate(cases):
        is_healable = case.get("failure_analysis", {}).get("is_healable")
        # Skip cases not yet triaged or triaged as healable or visual_flaky
        if is_healable is None or is_healable is True or is_healable == "visual_flaky":
            continue
        has_analysis = "ai_analysis" in case
        if not has_analysis:
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
    """Get ALL pending cases for parallel subagent processing (non-healable, no ai_analysis)."""
    data = load_failure_info()
    cases = data.get("failed_cases", [])
    pending_cases = []
    for i, case in enumerate(cases):
        is_healable = case.get("failure_analysis", {}).get("is_healable")
        if is_healable is None or is_healable is True or is_healable == "visual_flaky":
            continue
        has_analysis = "ai_analysis" in case
        if not has_analysis:
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
        is_healable = case.get("failure_analysis", {}).get("is_healable")
        if is_healable is True:
            print(f"[{i}] {case['scenario_name'][:50]}")
            print(f"    [HEALABLE - skip bug analysis]\n")
            continue
        if is_healable == "visual_flaky":
            print(f"[{i}] {case['scenario_name'][:50]}")
            print(f"    [VISUAL_FLAKY - skip bug analysis]\n")
            continue
        if is_healable is None:
            print(f"[{i}] {case['scenario_name'][:50]}")
            print(f"    [NOT TRIAGED - run triage first]\n")
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
    # Parse --data-dir from anywhere in args
    global _failure_info_file
    args = sys.argv[1:]
    filtered_args = []
    i = 0
    while i < len(args):
        if args[i] == "--data-dir" and i + 1 < len(args):
            data_dir = Path(args[i + 1])
            _failure_info_file = data_dir / "reports" / "failure_info.json"
            i += 2
        else:
            filtered_args.append(args[i])
            i += 1

    if len(filtered_args) < 1:
        print("Usage:")
        print("  python failure_info_helper.py [--data-dir <dir>] list                - List all cases")
        print("  python failure_info_helper.py [--data-dir <dir>] get <index>         - Get case details")
        print("  python failure_info_helper.py [--data-dir <dir>] triage              - Get all cases pending screenshot triage")
        print("  python failure_info_helper.py [--data-dir <dir>] triage_v2            - Get pending cases with success screenshot paths (for v2)")
        print("  python failure_info_helper.py [--data-dir <dir>] update_triage <index> <true|false|visual_flaky> <reason> [observable] [expected] [diff] [functionality]")
        print("  python failure_info_helper.py [--data-dir <dir>] healable            - Get all healable cases for grouping")
        print("  python failure_info_helper.py [--data-dir <dir>] heal_summary        - Get heal_summary (grouped healable cases)")
        print("  python failure_info_helper.py [--data-dir <dir>] pending             - Get next pending case (non-healable, needs analysis)")
        print("  python failure_info_helper.py [--data-dir <dir>] pending_all         - Get ALL pending cases")
        print("  python failure_info_helper.py [--data-dir <dir>] update_observation <index> <observable> <expected> <diff> <functionality>")
        print("  python failure_info_helper.py [--data-dir <dir>] observations        - Get all observations for bug analysis")
        print("  python failure_info_helper.py [--data-dir <dir>] summary             - Get analyzed cases summary")
        print("  python failure_info_helper.py [--data-dir <dir>] set_bug_group <id> <indices> <reason> <title> [is_bug] [confidence] [category]")
        print("  python failure_info_helper.py [--data-dir <dir>] set_heal_group <id> <indices> <element_description> <step_file>")
        print("  python failure_info_helper.py [--data-dir <dir>] update_heal <id> <status> [pr_url] [fix]")
        print("  python failure_info_helper.py [--data-dir <dir>] update_bug_url <bug_group_id> <ado_bug_url>")
        print("")
        print("Examples:")
        print("  python failure_info_helper.py triage")
        print("  python failure_info_helper.py update_triage 0 true 'Install button visible in screenshot but locator changed'")
        print("  python failure_info_helper.py update_triage 1 false 'Translate popup not visible in screenshot - real bug'")
        print("  python failure_info_helper.py update_triage 2 visual_flaky 'verify_visual_task flaky - screenshot shows expected state'")
        print("  python failure_info_helper.py healable")
        print("  python failure_info_helper.py pending")
        print("  python failure_info_helper.py set_bug_group BUG-001 '0,1,2' 'Same failure' '[Edge] Bug' true 0.85 functional_bug")
        print("  python failure_info_helper.py set_heal_group HEAL-001 '0,1' 'Search settings input' 'features/steps/settings.py'")
        sys.exit(1)
    
    cmd = filtered_args[0]
    
    if cmd == "list":
        list_cases()
    elif cmd == "get":
        get_case(int(filtered_args[1]))
    elif cmd == "triage":
        get_triage()
    elif cmd == "triage_v2":
        get_triage_v2()
    elif cmd == "update_triage":
        index = int(filtered_args[1])
        triage_val = filtered_args[2].lower()
        if triage_val == "visual_flaky":
            is_healable = "visual_flaky"
        else:
            is_healable = triage_val == "true"
        reason = filtered_args[3] if len(filtered_args) > 3 else ""
        observable = filtered_args[4] if len(filtered_args) > 4 else ""
        expected = filtered_args[5] if len(filtered_args) > 5 else ""
        diff = filtered_args[6] if len(filtered_args) > 6 else ""
        functionality = filtered_args[7] if len(filtered_args) > 7 else ""
        update_triage(index, is_healable, reason, observable, expected, diff, functionality)
    elif cmd == "healable":
        get_healable()
    elif cmd == "heal_summary":
        get_heal_summary()
    elif cmd == "pending":
        get_pending()
    elif cmd == "pending_all":
        get_pending_all()
    elif cmd == "update_observation":
        index = int(filtered_args[1])
        observable = filtered_args[2]
        expected = filtered_args[3]
        diff = filtered_args[4]
        functionality = filtered_args[5] if len(filtered_args) > 5 else ""
        update_observation(index, observable, expected, diff, functionality)
    elif cmd == "observations":
        get_observations()
    elif cmd == "update":
        index = int(filtered_args[1])
        is_bug = filtered_args[2].lower() == "true"
        confidence = float(filtered_args[3])
        category = filtered_args[4]
        title = filtered_args[5]
        reason = filtered_args[6] if len(filtered_args) > 6 else ""
        update_analysis(index, is_bug, confidence, category, title, reason)
    elif cmd == "summary":
        get_summary_for_dedup()
    elif cmd == "set_bug_group":
        group_id = filtered_args[1]
        indices = [int(x.strip()) for x in filtered_args[2].split(",")]
        reason = filtered_args[3]
        title = filtered_args[4]
        is_bug = filtered_args[5].lower() == "true" if len(filtered_args) > 5 else True
        confidence = float(filtered_args[6]) if len(filtered_args) > 6 else 0.8
        category = filtered_args[7] if len(filtered_args) > 7 else "functional_bug"
        set_bug_groups(group_id, indices, reason, title, is_bug, confidence, category)
    elif cmd == "set_heal_group":
        group_id = filtered_args[1]
        indices = [int(x.strip()) for x in filtered_args[2].split(",")]
        element_description = filtered_args[3]
        step_file = filtered_args[4] if len(filtered_args) > 4 else ""
        set_heal_group(group_id, indices, element_description, step_file)
    elif cmd == "update_heal":
        heal_group_id = filtered_args[1]
        status = filtered_args[2]
        pr_url = filtered_args[3] if len(filtered_args) > 3 else ""
        fix_applied = filtered_args[4] if len(filtered_args) > 4 else ""
        update_heal(heal_group_id, status, pr_url, fix_applied)
    elif cmd == "update_bug_url":
        bug_group_id = filtered_args[1]
        ado_bug_url = filtered_args[2]
        update_bug_url(bug_group_id, ado_bug_url)
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
