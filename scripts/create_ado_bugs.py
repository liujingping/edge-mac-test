#!/usr/bin/env python3
"""
Create ADO bugs from failure_info.json bug_summary.

Reads failure_info.json, pipeline_info.json, and _ado_bug_config.yaml,
then for each bug group:
  1. Dedup check via WIQL (OSG.CustomHTML CONTAINS case_name)
  2. Upload screenshots as ADO attachments
  3. Build repro steps HTML from templates
  4. Create bug via REST API
  5. Update failure_info.json with bug URL
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent.parent
ADO_RESOURCE_ID = "499b84ac-1321-427f-aa17-267ca6975798"


def get_access_token() -> str:
    result = subprocess.run(
        ["az", "account", "get-access-token",
         "--resource", ADO_RESOURCE_ID,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get access token: {result.stderr}")
    return result.stdout.strip()


def load_config() -> dict:
    config_path = PROJECT_ROOT / ".claude" / "commands" / "_ado_bug_config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ado_api_request(url: str, token: str, method: str = "GET",
                    data: bytes | None = None,
                    content_type: str = "application/json") -> dict:
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def dedup_check(case_name: str, config: dict, token: str) -> dict | None:
    org = config["organization"]
    project = config["project"]
    escaped = case_name.replace("'", "''")
    wiql = (
        f"SELECT [System.Id], [System.Title] FROM WorkItems "
        f"WHERE [System.WorkItemType] = 'Bug' "
        f"AND [System.State] <> 'Closed' "
        f"AND [OSG.CustomHTML] CONTAINS '{escaped}'"
    )
    url = f"{org}/{project}/_apis/wit/wiql?api-version=7.0"
    try:
        result = ado_api_request(url, token, method="POST",
                                 data=json.dumps({"query": wiql}).encode())
        items = result.get("workItems", [])
        if items:
            return items[0]
    except Exception as e:
        print(f"  WARNING: Dedup check failed for '{case_name}': {e}")
    return None


def get_work_item(bug_id: int, config: dict, token: str) -> dict | None:
    org = config["organization"]
    project = config["project"]
    fields = "System.Title,Microsoft.VSTS.TCM.ReproSteps,OSG.CustomHTML"
    url = f"{org}/{project}/_apis/wit/workitems/{bug_id}?$fields={fields}&api-version=7.0"
    try:
        return ado_api_request(url, token)
    except Exception as e:
        print(f"  WARNING: Failed to get work item #{bug_id}: {e}")
        return None


def update_bug(bug_id: int, repro_html: str, custom_html: str,
               config: dict, token: str) -> bool:
    org = config["organization"]
    project = config["project"]
    url = f"{org}/{project}/_apis/wit/workitems/{bug_id}?api-version=7.0"
    patch_doc = [
        {"op": "replace", "path": "/fields/OSG.CustomHTML", "value": custom_html},
        {"op": "replace", "path": "/fields/Microsoft.VSTS.TCM.ReproSteps", "value": repro_html},
    ]
    req = urllib.request.Request(
        url,
        data=json.dumps(patch_doc).encode(),
        method="PATCH",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json-patch+json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            json.loads(resp.read())
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR: Update bug #{bug_id} failed ({e.code}): {body[:500]}")
        return False


def upload_screenshot(screenshot_path: Path, config: dict, token: str) -> str | None:
    if not screenshot_path.exists():
        print(f"  WARNING: Screenshot not found: {screenshot_path}")
        return None

    short_name = re.sub(r"[^a-zA-Z0-9_.]", "_", screenshot_path.name)
    if len(short_name) > 80:
        short_name = short_name[:40] + "_" + short_name[-35:]

    org = config["organization"]
    project = config["project"]
    encoded_name = urllib.parse.quote(short_name)
    url = (f"{org}/{project}/_apis/wit/attachments"
           f"?fileName={encoded_name}&api-version=7.0")

    with open(screenshot_path, "rb") as f:
        file_data = f.read()

    try:
        result = ado_api_request(url, token, method="POST",
                                 data=file_data,
                                 content_type="application/octet-stream")
        ado_url = result.get("url", "")
        attachment_domain = config.get("attachment_domain", "microsoft.visualstudio.com")
        ado_url = re.sub(r"dev\.azure\.com/[^/]+", attachment_domain, ado_url)
        return ado_url
    except Exception as e:
        print(f"  WARNING: Screenshot upload failed: {e}")
        return None


def find_case_data(scenario_name: str, failed_cases: list[dict]) -> dict | None:
    for case in failed_cases:
        if case.get("scenario_name") == scenario_name:
            return case
    return None


def extract_repro_steps(case: dict) -> list[str]:
    steps_text = case.get("scenario_steps") or ""
    failed_step_name = case.get("failed_step", {}).get("name", "")
    steps = []
    for line in steps_text.splitlines():
        line = line.strip()
        if not line or line.startswith("@") or line.startswith("Scenario"):
            continue
        raw_step = re.sub(r"^(Given|When|Then|And|But)\s+", "", line)
        if raw_step:
            steps.append(raw_step)
            if failed_step_name and raw_step == failed_step_name:
                break
    return steps


def build_repro_html(bug_group: dict, failed_cases: list[dict],
                     config: dict, pipeline_info: dict,
                     screenshot_urls: dict[str, str]) -> str:
    affected = bug_group["affected_cases"]

    macos_ver = pipeline_info.get("macos_version", "")
    edge_ver = pipeline_info.get("edge_version", "")
    platform_str = config["fields"].get("platform", "macOS")
    if "{macos_version}" in platform_str:
        platform_str = platform_str.replace("{macos_version}", macos_ver)

    header = config.get("repro_shared_header", "")
    header = header.replace("{platform}", platform_str)
    header = header.replace("{edge_version}", edge_ver)

    sections = []
    for i, case_name in enumerate(affected):
        case = find_case_data(case_name, failed_cases)
        if not case:
            continue

        steps = extract_repro_steps(case)
        steps_ol = "<ol>" + "".join(f"<li>{s} </li>" for s in steps) + "</ol>"

        error_lines = case.get("failed_step", {}).get("error_message", [])
        error_msg = error_lines[0] if error_lines else ""
        error_msg = re.sub(r"^Assertion Failed:\s*", "", error_msg)

        ai = case.get("ai_analysis", {})
        expected = ai.get("expected_state", "")
        actual = ai.get("observable_state", "")

        screenshots_html = ""
        for sp in case.get("screenshots", []):
            url = screenshot_urls.get(sp)
            if url:
                screenshots_html += f'<p><img src="{url}" alt=Image> </p>'

        if len(affected) == 1:
            tmpl = config.get("repro_single_case", "")
        else:
            tmpl = config.get("repro_case_section", "")
            tmpl = tmpl.replace("{case_label}", f"Case {i + 1}")

        section = tmpl
        section = section.replace("{scenario_name}", case_name)
        section = section.replace("{repro_steps_ol}", steps_ol)
        section = section.replace("{expected_result}", expected)
        section = section.replace("{actual_result}", actual)
        section = section.replace("{error_message}", error_msg)
        section = section.replace("{screenshots_html}", screenshots_html)
        sections.append(section)

    return header + "<hr>".join(sections)


def build_custom_html(bug_group: dict, config: dict) -> str:
    items = "".join(f"<li>{name}</li>" for name in bug_group["affected_cases"])
    tmpl = config.get("custom_html_template", "<ol>{case_list_items}</ol>")
    return tmpl.replace("{case_list_items}", items)


def create_bug(title: str, repro_html: str, custom_html: str,
               config: dict, token: str) -> dict | None:
    org = config["organization"]
    project = config["project"]
    area_path = config["area_path"]
    tags = "; ".join(config.get("tags", []))
    severity = config["fields"].get("severity", "2")
    product = config["fields"].get("product", "Mac")

    url = f"{org}/{project}/_apis/wit/workitems/$Bug?api-version=7.0"

    patch_doc = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
        {"op": "add", "path": "/fields/System.AreaPath", "value": area_path},
        {"op": "add", "path": "/fields/System.Tags", "value": tags},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Severity", "value": severity},
        {"op": "add", "path": "/fields/OSG.Product", "value": product},
        {"op": "add", "path": "/fields/OSG.CustomHTML", "value": custom_html},
        {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.ReproSteps", "value": repro_html},
    ]

    req = urllib.request.Request(
        url,
        data=json.dumps(patch_doc).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json-patch+json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR: Create bug failed ({e.code}): {body[:500]}")
        return None


def _upload_case_screenshots(case_names: list[str], failed_cases: list[dict],
                             config: dict, token: str,
                             dry_run: bool) -> dict[str, str]:
    screenshot_urls = {}
    for case_name in case_names:
        case = find_case_data(case_name, failed_cases)
        if not case:
            continue
        for sp in case.get("screenshots", []):
            if sp in screenshot_urls:
                continue
            sp_path = PROJECT_ROOT / sp
            if not sp_path.exists():
                compressed = sp.replace("screenshots/", "screenshots_compressed/")
                compressed = re.sub(r"\.png$", ".jpg", compressed)
                sp_path = PROJECT_ROOT / compressed
            print(f"  Uploading: {sp_path.name}")
            if dry_run:
                screenshot_urls[sp] = f"https://DRYRUN/{sp_path.name}"
            else:
                url = upload_screenshot(sp_path, config, token)
                if url:
                    screenshot_urls[sp] = url
    return screenshot_urls


def _append_to_existing_bug(bug_id: int, new_cases: list[str],
                            bug_group: dict, failed_cases: list[dict],
                            config: dict, pipeline_info: dict,
                            token: str, dry_run: bool) -> bool:
    wi = get_work_item(bug_id, config, token)
    if not wi:
        print(f"  WARNING: Cannot read bug #{bug_id}, skipping append")
        return False

    fields = wi.get("fields", {})
    old_repro = fields.get("Microsoft.VSTS.TCM.ReproSteps", "")
    old_custom = fields.get("OSG.CustomHTML", "")

    screenshot_urls = _upload_case_screenshots(new_cases, failed_cases,
                                               config, token, dry_run)

    temp_group = dict(bug_group)
    temp_group["affected_cases"] = new_cases
    new_repro = build_repro_html(temp_group, failed_cases, config,
                                  pipeline_info, screenshot_urls)
    new_repro_body = new_repro
    hr_idx = new_repro.find("<hr>")
    if hr_idx != -1:
        new_repro_body = new_repro[hr_idx:]

    new_items_html = "".join(f"<li>{name}</li>" for name in new_cases)

    merged_repro = old_repro.rstrip() + "\n<hr>" + new_repro_body
    if "</ol>" in old_custom:
        merged_custom = old_custom.replace("</ol>", new_items_html + "</ol>")
    else:
        merged_custom = old_custom + new_items_html

    if dry_run:
        print(f"  DRY RUN: Would append {len(new_cases)} case(s) to bug #{bug_id}")
        return True

    print(f"  Appending {len(new_cases)} case(s) to bug #{bug_id}...")
    return update_bug(bug_id, merged_repro, merged_custom, config, token)


def process_bug_group(bug_group: dict, failed_cases: list[dict],
                      config: dict, pipeline_info: dict,
                      token: str, dry_run: bool = False) -> dict | None:
    group_id = bug_group["bug_group_id"]
    title = bug_group["suggested_title"]
    affected = bug_group["affected_cases"]

    print(f"\n--- Bug Group: {group_id} ---")
    print(f"  Title: {title}")
    print(f"  Cases: {len(affected)}")

    if not bug_group.get("is_likely_bug", False):
        print("  SKIP: Not a likely bug")
        return None

    if bug_group.get("ado_bug_url"):
        print(f"  SKIP: Already created → {bug_group['ado_bug_url']}")
        return None

    covered: dict[str, dict] = {}
    uncovered: list[str] = []
    for case_name in affected:
        existing = dedup_check(case_name, config, token)
        if existing:
            covered[case_name] = existing
        else:
            uncovered.append(case_name)

    if covered:
        ref_bug = next(iter(covered.values()))
        bug_id = ref_bug["id"]
        org = config["organization"]
        project = config["project"]
        bug_url = f"{org}/{project}/_workitems/edit/{bug_id}"
        covered_names = list(covered.keys())
        print(f"  DEDUP: {len(covered_names)} case(s) already in bug #{bug_id}")
        for cn in covered_names:
            print(f"    - {cn}")

        if uncovered:
            print(f"  NEW: {len(uncovered)} case(s) not yet in bug #{bug_id}")
            for cn in uncovered:
                print(f"    + {cn}")
            ok = _append_to_existing_bug(bug_id, uncovered, bug_group,
                                          failed_cases, config, pipeline_info,
                                          token, dry_run)
            if ok:
                print(f"  UPDATED: Bug #{bug_id} now includes all {len(affected)} case(s)")
            else:
                print(f"  WARNING: Failed to append new cases to bug #{bug_id}")

        return {"id": bug_id, "url": bug_url, "dedup": True}

    screenshot_urls = _upload_case_screenshots(affected, failed_cases,
                                               config, token, dry_run)

    repro_html = build_repro_html(bug_group, failed_cases, config,
                                  pipeline_info, screenshot_urls)
    custom_html = build_custom_html(bug_group, config)

    if dry_run:
        print(f"  DRY RUN: Would create bug '{title}'")
        print(f"  Custom HTML: {custom_html[:200]}")
        print(f"  Repro HTML length: {len(repro_html)} chars")
        return {"id": 0, "url": "DRY_RUN", "dedup": False}

    print(f"  Creating bug...")
    result = create_bug(title, repro_html, custom_html, config, token)
    if result:
        bug_id = result["id"]
        org = config["organization"]
        project = config["project"]
        url = f"{org}/{project}/_workitems/edit/{bug_id}"
        print(f"  Created: Bug #{bug_id} → {url}")
        return {"id": bug_id, "url": url, "dedup": False}

    return None


def main():
    parser = argparse.ArgumentParser(description="Create ADO bugs from failure analysis")
    parser.add_argument("--data-dir", required=True,
                        help="Pipeline data directory (e.g., pipeline_data/141562849)")
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
    config = load_config()

    bug_summary = failure_info.get("bug_summary", [])
    failed_cases = failure_info.get("failed_cases", [])

    if not bug_summary:
        print("No bug groups found in failure_info.json")
        sys.exit(0)

    token = get_access_token()

    print(f"Pipeline: {pipeline_info.get('pipeline_name', 'unknown')}")
    print(f"Edge version: {pipeline_info.get('edge_version', 'unknown')}")
    print(f"macOS version: {pipeline_info.get('macos_version', 'unknown')}")
    print(f"Bug groups: {len(bug_summary)}")
    if args.dry_run:
        print("MODE: DRY RUN")

    created = 0
    skipped = 0
    deduped = 0
    failed = 0

    for bug_group in bug_summary:
        result = process_bug_group(bug_group, failed_cases, config,
                                   pipeline_info, token, args.dry_run)
        if result is None:
            skipped += 1
            continue

        is_dedup = result.get("dedup", False)
        if is_dedup:
            deduped += 1
        else:
            created += 1

        if not args.dry_run:
            bug_group["status"] = "existing" if is_dedup else "created"
            bug_group["ado_bug_url"] = result["url"]
            bug_group["ado_bug_id"] = result["id"]

            for case in failed_cases:
                if case.get("scenario_name") in bug_group["affected_cases"]:
                    ai = case.setdefault("ai_analysis", {})
                    ai["ado_bug_url"] = result["url"]
                    ai["ado_bug_id"] = result["id"]

    if not args.dry_run:
        save_json(failure_info_path, failure_info)
        print(f"\nUpdated: {failure_info_path}")

    print(f"\nSummary: {created} created, {deduped} deduped, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
