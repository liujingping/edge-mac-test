#!/usr/bin/env python3
"""
Update a specific section in a triage debug log file.

Replaces content between a section header line and the next header line.
Used by subagents to fill in template sections one at a time.
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

SECTION_HEADERS = {
    "screenshot": "## Screenshot Analysis",
    "screenshot_all": "## Screenshot Analysis",
    "page_layout": "### PAGE_LAYOUT",
    "tab_bar": "### TAB_BAR",
    "toolbar": "### TOOLBAR",
    "sidebar": "### SIDEBAR",
    "web_content": "### WEB_CONTENT",
    "dialogs": "### DIALOGS_AND_OVERLAYS",
    "other": "### OTHER_ELEMENTS",
    "element_tree": "## Element Tree Analysis",
    "judgment": "## Main Agent Judgment",
}

RANGE_END_MARKERS = {
    "screenshot_all": "## Element Tree Analysis",
}


def update_section(file_path: Path, section: str, content: str):
    if section not in SECTION_HEADERS:
        print(f"ERROR: Unknown section '{section}'. Valid: {list(SECTION_HEADERS.keys())}")
        sys.exit(1)

    lines = file_path.read_text().splitlines()
    header = SECTION_HEADERS[section]

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start_idx = i
            break

    if start_idx is None:
        print(f"ERROR: Section '{header}' not found in {file_path}")
        sys.exit(1)

    end_marker = RANGE_END_MARKERS.get(section)
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if end_marker:
            if stripped == end_marker:
                end_idx = i
                break
        else:
            if stripped.startswith("#"):
                end_idx = i
                break

    new_section = [header] + content.rstrip().splitlines() + [""]
    result = lines[:start_idx] + new_section + lines[end_idx:]
    file_path.write_text("\n".join(result) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Update a section in triage debug log")
    parser.add_argument("--file", required=True, help="Path to case_N.md debug log")
    parser.add_argument("--section", required=True,
                        choices=list(SECTION_HEADERS.keys()),
                        help="Section to update")
    parser.add_argument("--content", required=True, help="New content for the section")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.is_absolute():
        file_path = PROJECT_ROOT / file_path

    if not file_path.exists():
        print(f"ERROR: {file_path} not found. Run init_triage_log.py first.")
        sys.exit(1)

    update_section(file_path, args.section, args.content)
    print(f"Updated [{args.section}] in {file_path.name}")


if __name__ == "__main__":
    main()
