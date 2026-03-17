#!/usr/bin/env python3
"""
Initialize triage debug log from template for a single case.

Creates a structured debug log file with all required sections as placeholders.
Subagent fills each section incrementally via scripts/update_triage_log.py.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

TEMPLATE = """# Case {index}: {scenario_name}

## Case Info
- **Index:** {index}
- **Scenario:** {scenario_name}
- **Failed Step:** {failed_step}
- **Error:** {error_message}
- **Screenshot:** {screenshot_path}
- **Element Tree:** {element_tree_path}

## Screenshot Analysis
SCREENSHOT_READ: PENDING

### PAGE_LAYOUT
PENDING

### TAB_BAR
PENDING

### TOOLBAR
PENDING

### SIDEBAR
PENDING

### WEB_CONTENT
PENDING

### DIALOGS_AND_OVERLAYS
PENDING

### OTHER_ELEMENTS
PENDING

## Element Tree Analysis
ELEMENT_TREE_READ: PENDING
LOCATOR_SEARCHED: PENDING
TARGET_FOUND_IN_TREE: PENDING
TREE_MATCH_DETAILS: PENDING
LOCATOR_DIFFERENCE: PENDING
NEARBY_ELEMENTS: PENDING

## Main Agent Judgment
PATTERN: PENDING
REASONING: PENDING
CONFIDENCE: PENDING
TRIAGE: PENDING
"""


def main():
    parser = argparse.ArgumentParser(description="Initialize triage debug log from template")
    parser.add_argument("--data-dir", required=True, help="Pipeline data directory")
    parser.add_argument("--index", required=True, type=int, help="Case index in failure_info.json")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.is_absolute():
        data_dir = PROJECT_ROOT / data_dir

    failure_info_path = data_dir / "reports" / "failure_info.json"
    if not failure_info_path.exists():
        print(f"ERROR: {failure_info_path} not found")
        sys.exit(1)

    with open(failure_info_path) as f:
        failure_info = json.load(f)

    cases = failure_info.get("failed_cases", [])
    if args.index >= len(cases):
        print(f"ERROR: index {args.index} out of range (total {len(cases)} cases)")
        sys.exit(1)

    case = cases[args.index]
    failed_step = case.get("failed_step", {})
    error_lines = failed_step.get("error_message", [])
    error_first = error_lines[0] if error_lines else "N/A"

    screenshots = case.get("screenshots", [])
    screenshot_path = screenshots[0] if screenshots else "N/A"
    compressed = screenshot_path.replace("screenshots/", "screenshots_compressed/").replace(".png", ".jpg") if screenshot_path != "N/A" else "N/A"

    element_trees = case.get("element_trees", [])
    tree_path = element_trees[0] if element_trees else "N/A"
    pruned_path = tree_path.replace("error_results/", "error_results_pruned/") if tree_path != "N/A" else "N/A"

    content = TEMPLATE.format(
        index=args.index,
        scenario_name=case.get("scenario_name", "N/A"),
        failed_step=f"{failed_step.get('keyword', '')} {failed_step.get('name', 'N/A')}".strip(),
        error_message=error_first,
        screenshot_path=compressed,
        element_tree_path=pruned_path,
    )

    debug_dir = data_dir / "reports" / "triage_debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    output_path = debug_dir / f"case_{args.index}.md"
    output_path.write_text(content)
    print(f"Created: {output_path}")
    print(f"Screenshot: {compressed}")
    print(f"Element tree: {pruned_path}")


if __name__ == "__main__":
    main()
