#!/usr/bin/env python3
"""
Create GitHub PRs for self-healing groups.

For each heal_group in failure_info.json:
  1. Check existing open PRs (fix/self-heal-*) for already-covered cases
  2. Filter out covered cases
  3. Push branch + create PR for remaining cases
  4. Update failure_info.json with PR URL
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent

BRANCH_PREFIX = "fix/self-heal-"
PR_TITLE_PREFIX = "[self-heal]"


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def run_cmd(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, check=check)


def get_open_heal_prs() -> list[dict]:
    result = run_cmd([
        "gh", "pr", "list",
        "--state", "open",
        "--search", "head:fix/self-heal-",
        "--json", "number,title,headRefName,url,body",
        "--limit", "100",
    ], check=False)
    if result.returncode != 0:
        print(f"  WARNING: gh pr list failed: {result.stderr.strip()}")
        return []
    prs = json.loads(result.stdout) if result.stdout.strip() else []
    return [p for p in prs if p.get("headRefName", "").startswith(BRANCH_PREFIX)]


def parse_affected_cases_from_body(body: str) -> set[str]:
    cases = set()
    in_section = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Affected Cases") or stripped.startswith("## Affected cases"):
            in_section = True
            continue
        if in_section:
            if stripped.startswith("## "):
                break
            m = re.match(r"^[-*]\s+(.+)$", stripped)
            if m:
                cases.add(m.group(1).strip())
    return cases


def get_covered_cases(open_prs: list[dict]) -> dict[str, str]:
    covered = {}
    for pr in open_prs:
        cases = parse_affected_cases_from_body(pr.get("body", ""))
        for case in cases:
            covered[case] = pr["url"]
    return covered


def current_branch() -> str:
    result = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return result.stdout.strip()


def branch_exists_remote(branch_name: str) -> bool:
    result = run_cmd(["git", "ls-remote", "--heads", "origin", branch_name], check=False)
    return bool(result.stdout.strip())


def push_branch(branch_name: str) -> bool:
    result = run_cmd(["git", "push", "-u", "origin", branch_name], check=False)
    if result.returncode != 0:
        print(f"  ERROR: git push failed: {result.stderr.strip()}")
        return False
    return True


def build_pr_body(heal_group: dict, pipeline_info: dict, remaining_cases: list[str]) -> str:
    element_desc = heal_group.get("element_description", "")
    step_file = heal_group.get("step_file", "")
    fix_applied = heal_group.get("fix_applied", "")
    build_id = pipeline_info.get("build_id", "")
    edge_ver = pipeline_info.get("edge_version", "")

    lines = ["## Summary", ""]
    if fix_applied:
        lines.append(f"- {fix_applied}")
    lines.append(f"- Element: {element_desc}")
    if step_file:
        lines.append(f"- Step file: `{step_file}`")
    lines.append("")

    lines.append("## Affected Cases")
    lines.append("")
    for case in remaining_cases:
        lines.append(f"- {case}")
    lines.append("")

    if build_id:
        lines.append("## Pipeline Reference")
        lines.append("")
        lines.append(f"- Build: {build_id}")
        if edge_ver:
            lines.append(f"- Edge version: {edge_ver}")
        lines.append("")

    lines.append("")
    return "\n".join(lines)


def create_pr(branch_name: str, title: str, body: str) -> Optional[str]:
    result = run_cmd([
        "gh", "pr", "create",
        "--head", branch_name,
        "--title", title,
        "--body", body,
    ], check=False)
    if result.returncode != 0:
        print(f"  ERROR: gh pr create failed: {result.stderr.strip()}")
        return None
    url = result.stdout.strip()
    return url


def process_heal_group(heal_group: dict, pipeline_info: dict,
                       covered_cases: dict,
                       dry_run: bool = False) -> Optional[dict]:
    group_id = heal_group.get("heal_group_id", "")
    affected = heal_group.get("affected_cases", [])
    element_desc = heal_group.get("element_description", "")

    print(f"\n--- Heal Group: {group_id} ---")
    print(f"  Element: {element_desc}")
    print(f"  Cases: {len(affected)}")

    if heal_group.get("pr_url"):
        print(f"  SKIP: Already has PR → {heal_group['pr_url']}")
        return None

    status = heal_group.get("status", "pending")
    if status not in ("pending", "pr_created"):
        if status == "failed":
            print(f"  SKIP: Status is '{status}'")
            return None

    remaining = []
    existing_pr_url = ""
    for case in affected:
        if case in covered_cases:
            print(f"  COVERED: '{case}' → {covered_cases[case]}")
            if not existing_pr_url:
                existing_pr_url = covered_cases[case]
        else:
            remaining.append(case)

    if not remaining:
        print("  SKIP: All cases already covered by open PRs")
        return {"url": existing_pr_url, "remaining_cases": [], "already_covered": True}

    if len(remaining) < len(affected):
        print(f"  PARTIAL: {len(remaining)}/{len(affected)} cases need new PR")

    cur = current_branch()
    expected_prefix = BRANCH_PREFIX
    if not cur.startswith(expected_prefix):
        print(f"  ERROR: Current branch '{cur}' is not a self-heal branch (expected {expected_prefix}*)")
        print("  Agent must create branch and commit code changes before running this script.")
        return None

    branch_name = cur

    if not branch_exists_remote(branch_name):
        print(f"  Pushing branch {branch_name}...")
        if not dry_run:
            if not push_branch(branch_name):
                return None
        else:
            print("  DRY RUN: Would push branch")

    title = f"{PR_TITLE_PREFIX} {element_desc}"
    body = build_pr_body(heal_group, pipeline_info, remaining)

    if dry_run:
        print(f"  DRY RUN: Would create PR")
        print(f"  Title: {title}")
        print(f"  Remaining cases: {remaining}")
        return {"url": "DRY_RUN", "remaining_cases": remaining}

    print(f"  Creating PR...")
    pr_url = create_pr(branch_name, title, body)
    if pr_url:
        print(f"  Created: {pr_url}")
        return {"url": pr_url, "remaining_cases": remaining}

    return None


def main():
    parser = argparse.ArgumentParser(description="Create GitHub PRs for self-healing groups")
    parser.add_argument("--data-dir", required=True,
                        help="Pipeline data directory (e.g., pipeline_data/141562849)")
    parser.add_argument("--group-id", required=True,
                        help="heal_group_id to create PR for")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be created without actually creating")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.is_absolute():
        data_dir = PROJECT_ROOT / data_dir

    failure_info_path = data_dir / "reports" / "failure_info.json"
    pipeline_info_path = data_dir / "pipeline_info.json"

    if not failure_info_path.exists():
        print(f"ERROR: {failure_info_path} not found")
        sys.exit(1)

    failure_info = load_json(failure_info_path)
    pipeline_info = load_json(pipeline_info_path) if pipeline_info_path.exists() else {}

    heal_summary = failure_info.get("heal_summary", [])
    heal_group = next((h for h in heal_summary if h.get("heal_group_id") == args.group_id), None)
    if not heal_group:
        print(f"ERROR: heal_group_id '{args.group_id}' not found in heal_summary")
        sys.exit(1)

    print("Fetching open self-heal PRs...")
    open_prs = get_open_heal_prs()
    print(f"  Found {len(open_prs)} open self-heal PR(s)")
    covered_cases = get_covered_cases(open_prs)
    if covered_cases:
        print(f"  Already covered cases: {len(covered_cases)}")

    result = process_heal_group(heal_group, pipeline_info, covered_cases, args.dry_run)

    if result and not args.dry_run:
        heal_group["status"] = "pr_existing" if result.get("already_covered") else "pr_created"
        heal_group["pr_url"] = result["url"]

        failed_cases = failure_info.get("failed_cases", [])
        for case in failed_cases:
            if case.get("scenario_name") in heal_group["affected_cases"]:
                fa = case.get("failure_analysis", {})
                fa["pr_url"] = result["url"]

        save_json(failure_info_path, failure_info)
        print(f"\nUpdated: {failure_info_path}")

    if not result:
        print("\nNo PR created.")


if __name__ == "__main__":
    main()
