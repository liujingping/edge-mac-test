#!/usr/bin/env python3
"""
Generate HTML failure analysis report.

This script reads failure_info.json and generates a comprehensive HTML report
showing all failed cases, their analysis, and self-healing results.
"""

import argparse
import json
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional


GITHUB_REPO_BASE = "https://github.com/edge-microsoft/FSQ_AI_Testcases_Mac/blob/main"


PROJECT_ROOT = Path(__file__).parent.parent


def encode_image_base64(image_path: str) -> Optional[str]:
    compressed = str(image_path).replace("screenshots/", "screenshots_compressed/")
    compressed = compressed.rsplit(".", 1)[0] + ".jpg"
    p = Path(compressed)
    if not p.is_absolute():
        p = PROJECT_ROOT / compressed
    if not p.exists():
        p = Path(image_path)
        if not p.is_absolute():
            p = PROJECT_ROOT / image_path
    if not p.exists():
        return None
    ext = p.suffix.lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    try:
        with open(p, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None


def load_debug_log(data_dir: Path, index: int) -> str:
    log_path = data_dir / "reports" / "triage_debug" / f"case_{index}.md"
    if not log_path.exists():
        return ""
    return log_path.read_text()


def _extract_section(log_text: str, header: str) -> str:
    idx = log_text.find(header)
    if idx == -1:
        return ""
    end = len(log_text)
    next_h2 = log_text.find("\n## ", idx + len(header))
    if next_h2 != -1:
        end = next_h2
    return log_text[idx:end].strip()


def extract_judgment(log_text: str) -> dict:
    section = _extract_section(log_text, "## Main Agent Judgment")
    if not section:
        return {}
    result = {}
    for line in section.splitlines():
        line = line.strip()
        for key in ["PATTERN", "REASONING", "CONFIDENCE", "TRIAGE"]:
            if line.startswith(f"{key}:"):
                result[key.lower()] = line[len(key) + 1:].strip()
    return result


def extract_evidence(log_text: str) -> str:
    if not log_text:
        return ""
    parts = []
    for header in ["## Screenshot Analysis", "## Element Tree Analysis"]:
        content = _extract_section(log_text, header)
        if content:
            parts.append(content)
    return "\n\n".join(parts)


def md_to_html(text: str) -> str:
    lines = text.split("\n")
    html_lines = []
    for line in lines:
        if line.startswith("### "):
            html_lines.append(f'<h5 class="md-h3">{line[4:]}</h5>')
        elif line.startswith("## "):
            html_lines.append(f'<h4 class="md-h2">{line[3:]}</h4>')
        else:
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_lines.append(f"<p>{escaped}</p>" if escaped.strip() else "")
    return "\n".join(html_lines)


def make_github_link(location: str) -> str:
    if not location or location == "N/A":
        return location or "N/A"
    parts = location.split(":")
    file_path = parts[0]
    line = parts[1] if len(parts) > 1 else ""
    anchor = f"#L{line}" if line else ""
    return f'<a href="{GITHUB_REPO_BASE}/{file_path}{anchor}" target="_blank" class="code-link">{location}</a>'



def generate_html(failure_info: dict, data_dir: Optional[Path] = None,
                   pipeline_info: Optional[dict] = None) -> str:
    summary = failure_info.get("summary", {})
    failed_cases = failure_info.get("failed_cases", [])
    bug_summary_data = failure_info.get("bug_summary", {})
    bug_summary = bug_summary_data.get("bugs", []) if isinstance(bug_summary_data, dict) else bug_summary_data
    heal_summary_data = failure_info.get("heal_summary", {})
    heal_summary = heal_summary_data.get("cases", []) if isinstance(heal_summary_data, dict) else heal_summary_data

    element_change_count = 0
    likely_bug_count = 0
    other_count = 0

    for case in failed_cases:
        failure_analysis = case.get("failure_analysis", {})
        ai_analysis = case.get("ai_analysis", {})
        if failure_analysis.get("is_healable") is True:
            element_change_count += 1
        elif ai_analysis.get("is_likely_bug"):
            likely_bug_count += 1
        else:
            other_count += 1

    actual_bugs = [b for b in bug_summary if b.get("status") == "created" or b.get("ado_bug_url")] if bug_summary else []
    unique_bugs = len(actual_bugs) if actual_bugs else likely_bug_count
    unique_heals = len(heal_summary) if heal_summary else element_change_count

    pi = pipeline_info or {}
    pipeline_name = pi.get("pipeline_name", "")
    build_id = pi.get("build_id", "")
    edge_version = pi.get("edge_version", "")
    pipeline_url = pi.get("url", "")

    header_info_html = ""
    if pipeline_name or build_id:
        parts = []
        if pipeline_name:
            parts.append(f"<span>Pipeline: <strong>{pipeline_name}</strong></span>")
        if build_id:
            if pipeline_url:
                parts.append(f'<span>Build: <a href="{pipeline_url}" target="_blank" style="color: #ddd; text-decoration: underline;">{build_id}</a></span>')
            else:
                parts.append(f"<span>Build: <strong>{build_id}</strong></span>")
        if edge_version:
            parts.append(f"<span>Edge: <strong>{edge_version}</strong></span>")
        header_info_html = '<div class="pipeline-info">' + " &nbsp;|&nbsp; ".join(parts) + "</div>"

    pr_table_html = ""
    if heal_summary:
        pr_rows = ""
        for i, group in enumerate(heal_summary, 1):
            affected_cases = group.get("affected_cases", [])
            if not affected_cases and group.get("scenario_name"):
                affected_cases = [group.get("scenario_name")]
            affected = ", ".join(affected_cases)
            element_desc = group.get("element_description", group.get("element_not_found", "N/A"))
            pr_url = group.get("pr_url", "")
            heal_action = group.get("heal_action", {})
            if not pr_url and heal_action:
                pr_url = heal_action.get("pr_url", "")
            if not pr_url:
                pr_url = group.get("branch_url", "")
            status = group.get("status", "pending")
            pr_link = f'<a href="{pr_url}" target="_blank">PR Link</a>' if pr_url else "N/A"
            origin_label = '<span class="origin-new">New</span>' if status == "pr_created" else '<span class="origin-existing">Existing</span>' if status == "pr_existing" or (pr_url and status != "pr_created") else ''
            pr_rows += f'''
            <tr>
                <td>{group.get("heal_group_id", f"HEAL-{i:03d}")}</td>
                <td>{element_desc}</td>
                <td class="affected-cases">{affected}</td>
                <td>{pr_link} {origin_label}</td>
            </tr>
            '''
        pr_table_html = f'''
        <div class="summary-table">
            <h3>Self-Healing Summary</h3>
            <table>
                <thead>
                    <tr>
                        <th>Group ID</th>
                        <th>Element</th>
                        <th>Affected Cases</th>
                        <th>PR</th>
                    </tr>
                </thead>
                <tbody>
                    {pr_rows}
                </tbody>
            </table>
        </div>
        '''

    bug_table_html = ""
    if actual_bugs:
        bug_rows = ""
        for i, bug in enumerate(actual_bugs, 1):
            affected_cases = bug.get("affected_cases", bug.get("case_names", []))
            affected = ", ".join(affected_cases) if isinstance(affected_cases, list) else str(affected_cases)
            bug_title = bug.get("suggested_title", bug.get("title", "N/A"))
            ado_url = bug.get("ado_bug_url", "")
            ado_link = f'<a href="{ado_url}" target="_blank">Bug Link</a>' if ado_url else "N/A"
            bug_status = bug.get("status", "")
            origin_label = '<span class="origin-new">New</span>' if bug_status == "created" else '<span class="origin-existing">Existing</span>' if bug_status == "existing" else ''
            bug_rows += f'''
            <tr>
                <td>{bug.get("bug_group_id", f"BUG-{i:03d}")}</td>
                <td>{bug_title}</td>
                <td class="affected-cases">{affected}</td>
                <td>{ado_link} {origin_label}</td>
            </tr>
            '''
        bug_table_html = f'''
        <div class="summary-table">
            <h3>Bug Summary</h3>
            <table>
                <thead>
                    <tr>
                        <th>Bug ID</th>
                        <th>Title</th>
                        <th>Affected Cases</th>
                        <th>ADO Bug</th>
                    </tr>
                </thead>
                <tbody>
                    {bug_rows}
                </tbody>
            </table>
        </div>
        '''

    cases_html = ""
    for i, case in enumerate(failed_cases):
        error_message = case.get("failed_step", {}).get("error_message", [])
        if isinstance(error_message, list):
            error_text = "<br>".join(error_message[:5])
            if len(error_message) > 5:
                error_text += f"<br>... ({len(error_message) - 5} more lines)"
        else:
            error_text = str(error_message)

        screenshots_html = ""
        for screenshot in case.get("screenshots", [])[:3]:
            img_src = encode_image_base64(screenshot)
            if img_src:
                screenshots_html += f'''
                <div class="screenshot">
                    <img src="{img_src}" alt="Screenshot" onclick="openModal(this.src)">
                    <p class="screenshot-name">{Path(screenshot).name}</p>
                </div>
                '''
        if not screenshots_html:
            screenshots_html = '<p class="no-data">No screenshots available</p>'

        failed_step = case.get("failed_step", {})
        failure_analysis = case.get("failure_analysis", {})
        ai_analysis = case.get("ai_analysis", {})

        artifact_links = []
        pr_url = ""
        heal_action = case.get("healing_result", {})
        if heal_action:
            pr_url = heal_action.get("pr_url", "")
        if not pr_url:
            fa = case.get("failure_analysis", {})
            pr_url = fa.get("pr_url", "")
        if not pr_url:
            fa = case.get("failure_analysis", {})
            if fa.get("heal_group_id") and heal_summary:
                for g in heal_summary:
                    if g.get("heal_group_id") == fa["heal_group_id"]:
                        pr_url = g.get("pr_url", "")
                        break
        ado_url = ai_analysis.get("ado_bug_url", "")
        if pr_url:
            artifact_links.append(f'<a href="{pr_url}" target="_blank" class="artifact-btn pr-btn"><svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z"/></svg> Pull Request</a>')
        if ado_url:
            artifact_links.append(f'<a href="{ado_url}" target="_blank" class="artifact-btn ado-btn"><svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm9-3a1 1 0 11-2 0 1 1 0 012 0zM6.75 7.75a.75.75 0 000 1.5h.75v2.25a.75.75 0 001.5 0v-3a.75.75 0 00-.75-.75h-1.5z"/></svg> ADO Bug</a>')
        artifacts_html = " ".join(artifact_links) if artifact_links else ""

        analysis_html = ""
        debug_log_text = load_debug_log(data_dir, i) if data_dir else ""
        judgment = extract_judgment(debug_log_text)
        evidence_text = extract_evidence(debug_log_text)

        judgment_html = ""
        if judgment:
            pattern_val = judgment.get("pattern", "")
            reasoning_val = judgment.get("reasoning", "")
            confidence_val = judgment.get("confidence", "")
            triage_val = judgment.get("triage", "")
            conf_class = "conf-high" if "HIGH" in confidence_val.upper() else "conf-medium" if "MEDIUM" in confidence_val.upper() else "conf-low"
            judgment_html = f'''
            <div class="judgment-card">
                <div class="judgment-row"><span class="judgment-label">Pattern</span><span class="judgment-value">#{pattern_val}</span></div>
                <div class="judgment-row"><span class="judgment-label">Reasoning</span><span class="judgment-value">{reasoning_val}</span></div>
                <div class="judgment-row"><span class="judgment-label">Confidence</span><span class="judgment-value {conf_class}">{confidence_val}</span></div>
                <div class="judgment-row"><span class="judgment-label">Triage</span><span class="judgment-value">{triage_val}</span></div>
            </div>
            '''
        elif failure_analysis.get("triage_reason"):
            judgment_html = f'''
            <div class="judgment-card">
                <div class="judgment-row"><span class="judgment-label">Triage</span><span class="judgment-value">{failure_analysis.get("triage_reason", "")}</span></div>
            </div>
            '''

        evidence_html = ""
        if evidence_text:
            evidence_rendered = md_to_html(evidence_text)
            evidence_html = f'''
            <details class="evidence-details">
                <summary>Screenshot & Element Tree Evidence</summary>
                <div class="evidence-content">{evidence_rendered}</div>
            </details>
            '''

        if judgment_html or evidence_html:
            analysis_html = f'''
            <div class="ai-analysis-section">
                <h4>AI Analysis</h4>
                {judgment_html}
                {evidence_html}
            </div>
            '''

        healable_value = failure_analysis.get("is_healable")
        if healable_value is True:
            healable_display = '<span class="healable-yes">Healable</span>'
        elif healable_value is False:
            healable_display = '<span class="healable-no">Bug</span>'
        else:
            healable_display = '<span class="healable-pending">Pending</span>'

        scenario_loc = case.get("scenario_location", "")
        scenario_link = make_github_link(scenario_loc)
        step_match_loc = failed_step.get("match_location", "N/A")
        step_match_link = make_github_link(step_match_loc)

        cases_html += f'''
        <div class="case-card">
            <div class="case-header">
                <span class="case-number">#{i}</span>
                <h3 class="case-name">{case["scenario_name"]}</h3>
                {healable_display}
                {artifacts_html}
            </div>

            <div class="case-details">
                <div class="detail-row">
                    <span class="label">Location:</span>
                    <span class="value">{scenario_link}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Failed Step:</span>
                    <span class="value">{failed_step.get("keyword", "")} {failed_step.get("name", "N/A")} <span class="step-loc">({step_match_link})</span></span>
                </div>
                {f'<div class="detail-row"><span class="label">Triage Reason:</span><span class="value">{failure_analysis.get("triage_reason", "")}</span></div>' if failure_analysis.get("triage_reason") else ''}
            </div>

            <div class="error-section">
                <h4>Error Message</h4>
                <pre class="error-message">{error_text}</pre>
            </div>

            {analysis_html}

            <div class="screenshots-section">
                <h4>Screenshots</h4>
                <div class="screenshots-container">
                    {screenshots_html}
                </div>
            </div>
        </div>
        '''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Failure Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}

        .header .timestamp {{
            opacity: 0.8;
            font-size: 13px;
        }}

        .pipeline-info {{
            margin-top: 12px;
            font-size: 14px;
            opacity: 0.95;
        }}

        .pipeline-info a {{
            color: #ddd;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .summary-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .summary-card .label {{
            color: #666;
            font-size: 14px;
        }}

        .summary-card.total .number {{ color: #333; }}
        .summary-card.element-change .number {{ color: #fd7e14; }}
        .summary-card.bugs .number {{ color: #d63384; }}
        .summary-card.other .number {{ color: #6c757d; }}

        .summary-table {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            padding: 20px;
        }}

        .summary-table h3 {{
            margin-bottom: 15px;
            color: #333;
            font-size: 18px;
        }}

        .summary-table table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .summary-table th, .summary-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}

        .summary-table td:last-child {{
            min-width: 180px;
            white-space: nowrap;
        }}

        .summary-table th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}

        .summary-table tr:hover {{
            background: #f8f9fa;
        }}

        .summary-table a {{
            color: #667eea;
            text-decoration: none;
        }}

        .summary-table a:hover {{
            text-decoration: underline;
        }}

        .summary-table .affected-cases {{
            font-size: 12px;
            color: #666;
            max-width: 400px;
        }}

        .summary-table .status-healed {{ color: #28a745; font-weight: 600; }}
        .summary-table .status-failed {{ color: #dc3545; font-weight: 600; }}

        .case-card {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            overflow: hidden;
        }}

        .case-header {{
            display: flex;
            align-items: center;
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #eee;
            gap: 10px;
        }}

        .case-number {{
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            flex-shrink: 0;
        }}

        .case-name {{
            flex: 1;
            font-size: 18px;
        }}

        .healable-yes {{
            background: #fd7e14;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            flex-shrink: 0;
        }}

        .healable-no {{
            background: #dc3545;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            flex-shrink: 0;
        }}

        .healable-pending {{
            background: #6c757d;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            flex-shrink: 0;
        }}

        .artifact-btn {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            flex-shrink: 0;
            transition: all 0.15s ease;
            border: 1px solid transparent;
        }}

        .pr-btn {{
            background: #dafbe1;
            color: #1a7f37;
            border-color: #a6e3b0;
        }}

        .pr-btn:hover {{
            background: #1a7f37;
            color: white;
        }}

        .ado-btn {{
            background: #deeaf6;
            color: #0366d6;
            border-color: #a8cef1;
        }}

        .ado-btn:hover {{
            background: #0366d6;
            color: white;
        }}

        .origin-new {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 1px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 6px;
        }}

        .origin-existing {{
            display: inline-block;
            background: #6c757d;
            color: white;
            padding: 1px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 6px;
        }}

        .case-details {{
            padding: 20px;
        }}

        .detail-row {{
            display: flex;
            margin-bottom: 10px;
        }}

        .detail-row .label {{
            width: 150px;
            font-weight: 600;
            color: #666;
            flex-shrink: 0;
        }}

        .detail-row .value {{
            flex: 1;
        }}

        .code-link {{
            color: #667eea;
            text-decoration: none;
        }}

        .code-link:hover {{
            text-decoration: underline;
        }}

        .step-loc {{
            color: #888;
        }}

        .error-section, .screenshots-section, .ai-analysis-section {{
            padding: 15px 20px;
            border-top: 1px solid #eee;
        }}

        .error-section h4, .screenshots-section h4, .ai-analysis-section h4 {{
            margin-bottom: 10px;
            color: #333;
        }}

        .ai-analysis-section {{
            background: #f8f9fa;
        }}

        .ai-analysis-section h4 {{
            color: #555;
        }}

        .judgment-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 12px;
        }}

        .judgment-row {{
            display: flex;
            padding: 6px 0;
            border-bottom: 1px solid #f0f0f0;
        }}

        .judgment-row:last-child {{
            border-bottom: none;
        }}

        .judgment-label {{
            width: 100px;
            font-weight: 600;
            color: #555;
            flex-shrink: 0;
            font-size: 13px;
        }}

        .judgment-value {{
            flex: 1;
            font-size: 13px;
        }}

        .conf-high {{ color: #28a745; font-weight: 600; }}
        .conf-medium {{ color: #fd7e14; font-weight: 600; }}
        .conf-low {{ color: #dc3545; font-weight: 600; }}

        .evidence-details {{
            margin-top: 8px;
        }}

        .evidence-details summary {{
            cursor: pointer;
            font-size: 13px;
            color: #667eea;
            font-weight: 600;
            padding: 4px 0;
        }}

        .evidence-details summary:hover {{
            text-decoration: underline;
        }}

        .evidence-content {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 15px;
            max-height: 400px;
            overflow-y: auto;
            margin-top: 8px;
            font-size: 13px;
            line-height: 1.5;
        }}

        .evidence-content .md-h2 {{
            font-size: 15px;
            color: #333;
            margin: 16px 0 8px 0;
            padding-bottom: 4px;
            border-bottom: 1px solid #eee;
        }}

        .evidence-content .md-h3 {{
            font-size: 13px;
            color: #555;
            margin: 12px 0 4px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .evidence-content p {{
            margin: 2px 0;
            color: #444;
        }}

        .error-message {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 13px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-all;
        }}

        .screenshots-container {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}

        .screenshot {{
            text-align: center;
        }}

        .screenshot img {{
            max-width: 400px;
            max-height: 250px;
            border-radius: 5px;
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .screenshot img:hover {{
            transform: scale(1.05);
        }}

        .screenshot-name {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}

        .no-data {{
            color: #999;
            font-style: italic;
        }}

        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}

        .modal img {{
            max-width: 90%;
            max-height: 90%;
        }}

        .modal.active {{
            display: flex;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Failure Analysis Report</h1>
            <p class="timestamp">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            {header_info_html}
        </div>

        <div class="summary">
            <div class="summary-card total">
                <div class="number">{summary.get("total_failures", len(failed_cases))}</div>
                <div class="label">Total Failures</div>
            </div>
            <div class="summary-card element-change">
                <div class="number">{element_change_count}</div>
                <div class="label">Element Changes</div>
            </div>
            <div class="summary-card bugs">
                <div class="number">{unique_bugs}</div>
                <div class="label">Likely Bugs</div>
            </div>
            <div class="summary-card other">
                <div class="number">{other_count}</div>
                <div class="label">Other</div>
            </div>
        </div>

        {pr_table_html}
        {bug_table_html}

        <div class="cases">
            {cases_html}
        </div>
    </div>

    <div class="modal" id="imageModal" onclick="closeModal()">
        <img id="modalImage" src="" alt="Full size screenshot">
    </div>

    <script>
        function openModal(src) {{
            document.getElementById("modalImage").src = src;
            document.getElementById("imageModal").classList.add("active");
        }}

        function closeModal() {{
            document.getElementById("imageModal").classList.remove("active");
        }}

        document.addEventListener("keydown", function(e) {{
            if (e.key === "Escape") closeModal();
        }});
    </script>
</body>
</html>
'''
    return html


def generate_report(data_dir: Optional[Path] = None, upload: bool = False):
    if data_dir:
        failure_info_file = data_dir / "reports" / "failure_info.json"
        pipeline_info_file = data_dir / "pipeline_info.json"
        output_file = data_dir / "reports" / "failure_analysis.html"
    else:
        failure_info_file = PROJECT_ROOT / "reports" / "failure_info.json"
        pipeline_info_file = PROJECT_ROOT / "pipeline_info.json"
        output_file = PROJECT_ROOT / "reports" / "failure_analysis.html"

    print(f"Loading failure info from: {failure_info_file}")

    if not failure_info_file.exists():
        print(f"Error: {failure_info_file} not found")
        return None

    with open(failure_info_file, "r", encoding="utf-8") as f:
        failure_info = json.load(f)

    pipeline_info = None
    if pipeline_info_file.exists():
        with open(pipeline_info_file, "r", encoding="utf-8") as f:
            pipeline_info = json.load(f)

    html_content = generate_html(failure_info, data_dir, pipeline_info)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Report generated: {output_file}")

    if upload:
        try:
            from upload_report import upload_report as do_upload
            pi = pipeline_info or {}
            build_id = pi.get("build_id", "")
            if not build_id and data_dir:
                build_id = data_dir.name
            pipeline_name = pi.get("pipeline_name", "")
            sas_url = do_upload(
                file_path=str(output_file),
                build_id=build_id,
                pipeline_name=pipeline_name,
            )
            return sas_url
        except Exception as e:
            print(f"Warning: upload failed: {e}")

    return str(output_file)


def main():
    parser = argparse.ArgumentParser(description="Generate HTML failure analysis report")
    parser.add_argument("--data-dir",
                        help="Pipeline data directory (e.g., pipeline_data/141562849)")
    parser.add_argument("--upload", action="store_true",
                        help="Upload report to Azure Blob Storage and print SAS URL")
    args = parser.parse_args()

    data_dir = None
    if args.data_dir:
        data_dir = Path(args.data_dir)
        if not data_dir.is_absolute():
            data_dir = PROJECT_ROOT / data_dir

    generate_report(data_dir=data_dir, upload=args.upload)


if __name__ == "__main__":
    main()
