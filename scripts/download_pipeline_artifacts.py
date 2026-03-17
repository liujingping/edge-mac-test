#!/usr/bin/env python3
"""
Download test artifacts from an Azure DevOps pipeline run.

Three-phase selective download:
  Phase 1: Download zips, extract only behave_results.json per agent
  Phase 2: Parse results to find failed cases
  Phase 3: Extract only failed case screenshots + error_result JSONs (with element trees)
"""

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
PIPELINE_DATA_DIR = PROJECT_ROOT / "pipeline_data"

ADO_ORG = "https://dev.azure.com/microsoft"
ADO_PROJECT = "Edge"
ADO_RESOURCE_ID = "499b84ac-1321-427f-aa17-267ca6975798"


def get_access_token() -> str:
    """Get Azure DevOps access token via az CLI."""
    result = subprocess.run(
        ["az", "account", "get-access-token",
         "--resource", ADO_RESOURCE_ID,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to get access token. Run 'az login' first.\n{result.stderr}"
        )
    return result.stdout.strip()


def get_pipeline_run_info(build_id: str, token: str) -> dict:
    """Get pipeline run metadata."""
    import urllib.request

    url = (
        f"{ADO_ORG}/{ADO_PROJECT}/_apis/build/builds/{build_id}"
        f"?api-version=7.0"
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_build_environment_info(build_id: str, run_info: dict, token: str) -> dict:
    """Extract Edge version from triggerInfo and macOS version from job logs."""
    import urllib.request

    info = {}

    trigger_info = run_info.get("triggerInfo", {})
    info["edge_version"] = trigger_info.get("version", "")

    try:
        timeline_url = (
            f"{ADO_ORG}/{ADO_PROJECT}/_apis/build/builds/{build_id}/timeline"
            f"?api-version=7.0"
        )
        req = urllib.request.Request(timeline_url, headers={
            "Authorization": f"Bearer {token}",
        })
        with urllib.request.urlopen(req) as resp:
            timeline = json.loads(resp.read())

        log_id = None
        for record in timeline.get("records", []):
            if (record.get("type") == "Job"
                    and "Mac Tests" in record.get("name", "")
                    and record.get("log")):
                log_id = record["log"]["id"]
                break

        if log_id:
            project_id = run_info.get("project", {}).get("id", ADO_PROJECT)
            log_url = (
                f"{ADO_ORG}/{project_id}/_apis/build/builds/{build_id}"
                f"/logs/{log_id}"
            )
            req = urllib.request.Request(log_url, headers={
                "Authorization": f"Bearer {token}",
            })
            with urllib.request.urlopen(req) as resp:
                log_lines = resp.read().decode("utf-8", errors="replace").splitlines()[:40]

            in_os_section = False
            in_runner_section = False
            os_lines = []
            for line in log_lines:
                text = re.sub(r"^\d{4}-.*?Z\s*", "", line).strip()
                if "##[group]Operating System" in text:
                    in_os_section = True
                    continue
                if "##[group]Runner Image" in text:
                    in_os_section = False
                    in_runner_section = True
                    continue
                if "##[endgroup]" in text:
                    in_os_section = False
                    in_runner_section = False
                    continue
                if in_os_section:
                    os_lines.append(text)
                if in_runner_section and text.startswith("Image:"):
                    info["runner_image"] = text.split(":", 1)[1].strip()

            if len(os_lines) >= 2:
                info["macos_version"] = os_lines[1]
    except Exception:
        pass

    return info


def list_artifacts(build_id: str, token: str) -> list[dict]:
    """List all artifacts for a pipeline run."""
    import urllib.request

    url = (
        f"{ADO_ORG}/{ADO_PROJECT}/_apis/build/builds/{build_id}/artifacts"
        f"?api-version=7.0"
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data.get("value", [])


def download_artifact_zip(build_id: str, artifact_name: str, token: str, dest_path: Path):
    """Download a single artifact as a zip file."""
    import urllib.request
    import urllib.parse

    encoded_name = urllib.parse.quote(artifact_name)
    url = (
        f"{ADO_ORG}/{ADO_PROJECT}/_apis/build/builds/{build_id}/artifacts"
        f"?artifactName={encoded_name}&api-version=7.0&%24format=zip"
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
    })
    with urllib.request.urlopen(req) as resp:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)


def clean_name_for_matching(name: str) -> str:
    """Clean scenario name for file matching (same logic as collect_failure_info)."""
    if not name:
        return ""
    cleaned = re.sub(r"[^\w\s\-]", "_", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.replace(" ", "_")
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = cleaned.strip("_")
    return cleaned


def extract_behave_results(zip_path: Path, artifact_name: str, output_dir: Path, agent_index: int) -> Path:
    """Phase 1: Extract only behave_results.json (not pretty) from artifact zip."""
    target = f"{artifact_name}/reports/json/behave_results.json"
    logs_dir = output_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    dest = logs_dir / f"behave_results_agent{agent_index}.json"

    with zipfile.ZipFile(zip_path, "r") as zf:
        if target in zf.namelist():
            with zf.open(target) as src, open(dest, "wb") as dst:
                dst.write(src.read())
            return dest

    raise FileNotFoundError(f"behave_results.json not found in {zip_path.name}")


def parse_failed_case_names(reports_dir: Path) -> set[str]:
    """Parse all behave_results_agent*.json to find failed scenario names."""
    failed_names = set()
    passed_keys = set()

    for result_file in sorted(reports_dir.glob("behave_results_agent*.json")):
        with open(result_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            continue

        for feature in data:
            for element in feature.get("elements", []):
                if element.get("type") != "scenario":
                    continue
                name = element.get("name", "")
                location = element.get("location", "")
                feature_file = location.split(":")[0] if ":" in location else ""
                dedup_key = f"{feature_file}::{name}"
                status = element.get("status", "unknown")

                if status == "passed":
                    passed_keys.add(dedup_key)
                elif status == "failed":
                    failed_names.add((dedup_key, name))

    # Exclude cases that eventually passed on retry
    return {name for key, name in failed_names if key not in passed_keys}


def extract_error_results_by_uuids(zip_path: Path, artifact_name: str, output_dir: Path, needed_uuids: set[str]) -> int:
    """Extract only error_result files matching the specified UUIDs."""
    if not needed_uuids:
        return 0

    error_results_dir = output_dir / "logs" / "error_results"
    error_results_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"{artifact_name}/logs/"
    extracted = 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            if not member.startswith(prefix) or not member.endswith(".json"):
                continue
            file_name = member[len(prefix):]
            if not file_name.startswith("error_result_"):
                continue
            if not any(uuid in file_name for uuid in needed_uuids):
                continue
            dest = error_results_dir / file_name
            if dest.exists():
                continue
            with zf.open(member) as src, open(dest, "wb") as dst:
                dst.write(src.read())
            extracted += 1

    return extracted


def extract_agent_logs(zip_path: Path, artifact_name: str, output_dir: Path) -> int:
    """Extract mac_automation_tests_agent_*.log files from artifact zip."""
    logs_dir = output_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"{artifact_name}/logs/"
    extracted = 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            if not member.startswith(prefix):
                continue
            file_name = member[len(prefix):]
            if not file_name.startswith("mac_automation_tests_agent_"):
                continue
            dest = logs_dir / file_name
            if dest.exists():
                continue
            with zf.open(member) as src, open(dest, "wb") as dst:
                dst.write(src.read())
            extracted += 1

    return extracted


def _parse_agent_logs_for_screenshots(logs_dir: Path) -> dict[str, list[str]]:
    """Parse agent log files to build screenshot_filename -> [error_result_uuid] mapping.

    Tracks error UUIDs during each scenario run and maps them to the
    screenshot saved after that run finishes. This ensures UUIDs are
    correctly associated with specific retry attempts.
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


def extract_screenshots_for_cases(zip_path: Path, artifact_name: str, output_dir: Path,
                                  failed_patterns: set[str]) -> tuple[int, list[str]]:
    """Extract only the LATEST screenshot per failed case.

    For each case, keeps only the screenshot with the latest timestamp
    (from the final retry attempt) plus its associated ChromeFeatureState file.

    Returns (extracted_count, list_of_extracted_png_filenames).
    """
    screenshots_dir = output_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"{artifact_name}/screenshots/"
    pattern_re = re.compile(
        r"^(?:" + "|".join(re.escape(p) for p in failed_patterns) + r")_\d{8}_"
    )

    # First pass: collect all matching members grouped by case pattern
    case_png_members: dict[str, list[str]] = {}
    all_matching_members: set[str] = set()

    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            if not member.startswith(prefix) or member.endswith("/"):
                continue
            file_name = member[len(prefix):]
            if not pattern_re.match(file_name):
                continue
            all_matching_members.add(member)

            if file_name.endswith(".png"):
                for pat in failed_patterns:
                    if file_name.startswith(pat + "_"):
                        case_png_members.setdefault(pat, []).append(member)
                        break

    # For each case, select only the latest .png and its associated files
    to_extract: list[str] = []
    latest_png_filenames: list[str] = []
    for pat, png_members in case_png_members.items():
        png_members.sort()  # Sorted by name (timestamp) - latest is last
        latest_png = png_members[-1]
        to_extract.append(latest_png)
        latest_png_filenames.append(latest_png[len(prefix):])

        # Include associated ChromeFeatureState (same base name)
        latest_base = latest_png[:-4]  # strip .png
        for member in all_matching_members:
            if member != latest_png and member.startswith(latest_base):
                to_extract.append(member)

    # Extract selected files
    extracted = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in to_extract:
            file_name = member[len(prefix):]
            dest = screenshots_dir / file_name
            if dest.exists():
                continue
            with zf.open(member) as src, open(dest, "wb") as dst:
                dst.write(src.read())
            extracted += 1

    return extracted, latest_png_filenames


def download_pipeline_artifacts(build_id: str) -> Path:
    """Main function: download all artifacts for a pipeline run."""
    output_dir = PIPELINE_DATA_DIR / str(build_id)
    if output_dir.exists():
        print(f"Directory already exists: {output_dir}")
        print("Using cached data. Delete the directory to re-download.")
        return output_dir

    print(f"Downloading artifacts for build {build_id}...")
    token = get_access_token()

    # Get run info
    run_info = get_pipeline_run_info(build_id, token)
    print(f"  Pipeline: {run_info.get('definition', {}).get('name', 'unknown')}")
    print(f"  Build: {run_info.get('buildNumber', 'unknown')}")
    print(f"  Status: {run_info.get('status', 'unknown')} / {run_info.get('result', 'unknown')}")

    # List artifacts
    artifacts = list_artifacts(build_id, token)
    test_artifacts = [
        a for a in artifacts
        if a["name"].startswith("MacAutomationTestResults-")
    ]

    if not test_artifacts:
        print("No MacAutomationTestResults artifacts found!")
        print(f"Available artifacts: {[a['name'] for a in artifacts]}")
        sys.exit(1)

    print(f"  Found {len(test_artifacts)} test artifact(s):")
    for a in test_artifacts:
        size_mb = int(a["resource"]["properties"].get("artifactsize", 0)) / 1024 / 1024
        print(f"    - {a['name']} ({size_mb:.1f} MB)")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Save run metadata
    meta = {
        "build_id": build_id,
        "build_number": run_info.get("buildNumber"),
        "pipeline_name": run_info.get("definition", {}).get("name"),
        "status": run_info.get("status"),
        "result": run_info.get("result"),
        "url": f"{ADO_ORG}/{ADO_PROJECT}/_build/results?buildId={build_id}&view=results",
        "artifacts": [a["name"] for a in test_artifacts],
    }

    env_info = get_build_environment_info(build_id, run_info, token)
    if env_info.get("edge_version"):
        meta["edge_version"] = env_info["edge_version"]
        print(f"  Edge version: {env_info['edge_version']}")
    if env_info.get("macos_version"):
        meta["macos_version"] = env_info["macos_version"]
        print(f"  macOS version: {env_info['macos_version']}")
    if env_info.get("runner_image"):
        meta["runner_image"] = env_info["runner_image"]
        print(f"  Runner image: {env_info['runner_image']}")

    with open(output_dir / "pipeline_info.json", "w") as f:
        json.dump(meta, f, indent=2)

    # Phase 1: Download zips and extract only behave_results.json
    print(f"\n--- Phase 1: Download & extract behave results ---")
    zip_paths = []
    for i, artifact in enumerate(test_artifacts):
        name = artifact["name"]
        zip_path = output_dir / f"{name}.zip"

        print(f"  Downloading {name}...")
        download_artifact_zip(build_id, name, token, zip_path)
        print(f"    Downloaded: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")

        result_path = extract_behave_results(zip_path, name, output_dir, i)
        print(f"    Extracted: {result_path.name}")
        zip_paths.append((zip_path, name))

    # Phase 2: Parse results to find failed cases
    print(f"\n--- Phase 2: Identify failed cases ---")
    logs_dir = output_dir / "logs"
    failed_names = parse_failed_case_names(logs_dir)

    if not failed_names:
        print("  No failed cases found! Cleaning up zips.")
        for zip_path, _ in zip_paths:
            zip_path.unlink()
        print(f"\n{'='*50}")
        print(f"Download complete: {output_dir}")
        print(f"  All tests passed - no screenshots needed.")
        return output_dir

    # Build filename patterns from failed case names
    failed_patterns = {clean_name_for_matching(name) for name in failed_names}
    print(f"  Found {len(failed_names)} failed case(s):")
    for name in sorted(failed_names):
        print(f"    - {name}")

    # Phase 3: Extract artifacts for failed cases
    print(f"\n--- Phase 3: Extract artifacts for failed cases ---")

    # 3a: Extract agent logs first (needed to map screenshots to error results)
    for zip_path, name in zip_paths:
        extract_agent_logs(zip_path, name, output_dir)

    # 3b: Parse agent logs -> screenshot_filename -> [uuid] mapping
    screenshot_uuid_mapping = _parse_agent_logs_for_screenshots(output_dir / "logs")

    # 3c: Extract only latest screenshots per case
    total_screenshots = 0
    all_latest_screenshots: list[str] = []
    for zip_path, name in zip_paths:
        count, filenames = extract_screenshots_for_cases(zip_path, name, output_dir, failed_patterns)
        total_screenshots += count
        all_latest_screenshots.extend(filenames)
        if count:
            print(f"  {name}: {count} screenshot(s) (latest only)")

    # 3d: Collect UUIDs for the latest screenshots, extract matching error results
    needed_uuids: set[str] = set()
    for ss_name in all_latest_screenshots:
        needed_uuids.update(screenshot_uuid_mapping.get(ss_name, []))

    total_error_results = 0
    for zip_path, name in zip_paths:
        er_count = extract_error_results_by_uuids(zip_path, name, output_dir, needed_uuids)
        total_error_results += er_count
        if er_count:
            print(f"  {name}: {er_count} error result(s)")

    # Clean up zip files
    for zip_path, _ in zip_paths:
        zip_path.unlink()

    # Summary
    report_count = len(list(logs_dir.glob("behave_results*.json")))
    screenshots_dir = output_dir / "screenshots"
    screenshot_count = len(list(screenshots_dir.glob("*"))) if screenshots_dir.exists() else 0

    error_results_dir = output_dir / "logs" / "error_results"
    error_result_count = len(list(error_results_dir.glob("*.json"))) if error_results_dir.exists() else 0

    print(f"\n{'='*50}")
    print(f"Download complete: {output_dir}")
    print(f"  Reports: {report_count} behave result file(s)")
    print(f"  Screenshots: {screenshot_count} file(s) (failed cases only)")
    print(f"  Error results: {error_result_count} file(s) (with element trees)")
    print(f"  Pipeline URL: {meta['url']}")

    return output_dir


def main():
    if len(sys.argv) < 2:
        print("Usage: python download_pipeline_artifacts.py <build_id>")
        print("")
        print("Example:")
        print("  python download_pipeline_artifacts.py 141562849")
        sys.exit(1)

    build_id = sys.argv[1]
    if not build_id.isdigit():
        print(f"Error: build_id must be a number, got '{build_id}'")
        sys.exit(1)

    download_pipeline_artifacts(build_id)


if __name__ == "__main__":
    main()
