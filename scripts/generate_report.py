#!/usr/bin/env python3
"""
Generate HTML failure analysis report.

This script reads failure_info.json and generates a comprehensive HTML report
showing all failed cases, their analysis, and self-healing results.
"""

import json
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional


PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
FAILURE_INFO_FILE = REPORTS_DIR / "failure_info.json"
OUTPUT_FILE = REPORTS_DIR / "failure_analysis.html"
TEMPLATE_FILE = Path(__file__).parent / "templates" / "report_template.html"


def load_failure_info() -> dict:
    """Load failure info from JSON file."""
    if not FAILURE_INFO_FILE.exists():
        raise FileNotFoundError(f"Failure info file not found: {FAILURE_INFO_FILE}")
    
    with open(FAILURE_INFO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def encode_image_base64(image_path: str) -> Optional[str]:
    """Encode image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None


def get_status_class(status: str) -> str:
    """Get CSS class for status."""
    status_classes = {
        "healed": "status-healed",
        "healing_failed": "status-failed",
        "skipped": "status-skipped",
        "pending": "status-pending"
    }
    return status_classes.get(status, "status-pending")


def get_status_text(status: str) -> str:
    """Get display text for status."""
    status_texts = {
        "healed": "Healed",
        "healing_failed": "Healing Failed",
        "skipped": "Skipped (Not Healable)",
        "pending": "Pending"
    }
    return status_texts.get(status, "Unknown")


def generate_html(failure_info: dict, healing_results: Optional[dict] = None) -> str:
    """Generate HTML report content."""
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
        
        if failure_analysis.get("is_healable"):
            element_change_count += 1
        elif ai_analysis.get("is_likely_bug"):
            likely_bug_count += 1
        else:
            other_count += 1
    
    actual_bugs = [b for b in bug_summary if b.get("status") == "created" or b.get("ado_bug_url")] if bug_summary else []
    unique_bugs = len(actual_bugs) if actual_bugs else likely_bug_count
    unique_heals = len(heal_summary) if heal_summary else element_change_count
    
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
            status_class = "healed" if status == "healed" else "failed" if status == "failed" else "pending"
            pr_link = f'<a href="{pr_url}" target="_blank">PR Link</a>' if pr_url else "N/A"
            pr_rows += f'''
            <tr>
                <td>{group.get("heal_group_id", f"HEAL-{i:03d}")}</td>
                <td>{element_desc}</td>
                <td class="affected-cases">{affected}</td>
                <td class="status-{status_class}">{status.title()}</td>
                <td>{pr_link}</td>
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
                        <th>Status</th>
                        <th>PR URL</th>
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
            confidence = bug.get("confidence", 0)
            bug_title = bug.get("suggested_title", bug.get("title", "N/A"))
            ado_url = bug.get("ado_bug_url", "")
            ado_link = f'<a href="{ado_url}" target="_blank">Bug Link</a>' if ado_url else "N/A"
            bug_rows += f'''
            <tr>
                <td>{bug.get("bug_group_id", f"BUG-{i:03d}")}</td>
                <td>{bug_title}</td>
                <td>{bug.get("bug_category", bug.get("category", "unknown")).replace("_", " ").title()}</td>
                <td class="confidence-{"high" if confidence >= 0.7 else "medium" if confidence >= 0.4 else "low"}">{confidence:.0%}</td>
                <td class="affected-cases">{affected}</td>
                <td>{ado_link}</td>
            </tr>
            '''
        bug_table_html = f'''
        <div class="summary-table">
            <h3>Bug Summary (Deduplicated)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Bug ID</th>
                        <th>Title</th>
                        <th>Category</th>
                        <th>Confidence</th>
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
    for i, case in enumerate(failed_cases, 1):
        healing_result = case.get("healing_result", {"status": "pending"})
        status = healing_result.get("status", "pending")
        pr_url = healing_result.get("pr_url", "")
        
        error_message = case.get("failed_step", {}).get("error_message", [])
        if isinstance(error_message, list):
            error_text = "<br>".join(error_message[:5])
            if len(error_message) > 5:
                error_text += f"<br>... ({len(error_message) - 5} more lines)"
        else:
            error_text = str(error_message)
        
        screenshots_html = ""
        for screenshot in case.get("screenshots", [])[:3]:
            img_data = encode_image_base64(screenshot)
            if img_data:
                screenshots_html += f'''
                <div class="screenshot">
                    <img src="data:image/png;base64,{img_data}" alt="Screenshot" onclick="openModal(this.src)">
                    <p class="screenshot-name">{Path(screenshot).name}</p>
                </div>
                '''
        
        if not screenshots_html:
            screenshots_html = '<p class="no-data">No screenshots available</p>'
        
        element_trees_html = ""
        for tree_file in case.get("element_trees", [])[:2]:
            tree_name = Path(tree_file).name
            element_trees_html += f'<li><a href="file://{tree_file}" target="_blank">{tree_name}</a></li>'
        
        if not element_trees_html:
            element_trees_html = '<li class="no-data">No element trees available</li>'
        
        pr_html = ""
        if pr_url:
            pr_html = f'<a href="{pr_url}" target="_blank" class="pr-link">{pr_url}</a>'
        
        failed_step = case.get("failed_step", {})
        failure_analysis = case.get("failure_analysis", {})
        ai_analysis = case.get("ai_analysis", {})
        
        ai_analysis_html = ""
        if ai_analysis:
            bug_confidence = ai_analysis.get("bug_confidence", 0)
            confidence_class = "high" if bug_confidence >= 0.7 else "medium" if bug_confidence >= 0.4 else "low"
            ai_analysis_html = f'''
            <div class="ai-analysis-section">
                <h4>AI Bug Analysis</h4>
                <div class="ai-analysis-content">
                    <div class="detail-row">
                        <span class="label">Likely Bug:</span>
                        <span class="value {"bug-yes" if ai_analysis.get("is_likely_bug") else "bug-no"}">{"Yes" if ai_analysis.get("is_likely_bug") else "No"}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Confidence:</span>
                        <span class="value confidence-{confidence_class}">{bug_confidence:.0%}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Category:</span>
                        <span class="value">{ai_analysis.get("bug_category", "N/A").replace("_", " ").title()}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Analysis:</span>
                        <span class="value">{ai_analysis.get("analysis_reason", "N/A")}</span>
                    </div>
                    {f'<div class="detail-row"><span class="label">Suggested Title:</span><span class="value suggested-title">{ai_analysis.get("suggested_bug_title", "")}</span></div>' if ai_analysis.get("suggested_bug_title") else ''}
                    {f'<div class="detail-row"><span class="label">Suggested Description:</span><pre class="suggested-desc">{ai_analysis.get("suggested_bug_description", "")}</pre></div>' if ai_analysis.get("suggested_bug_description") else ''}
                </div>
            </div>
            '''
        
        cases_html += f'''
        <div class="case-card">
            <div class="case-header">
                <span class="case-number">#{i}</span>
                <h3 class="case-name">{case["scenario_name"]}</h3>
                <span class="status-badge {get_status_class(status)}">{get_status_text(status)}</span>
            </div>
            
            <div class="case-details">
                <div class="detail-row">
                    <span class="label">Feature:</span>
                    <span class="value">{case["feature_name"]}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Location:</span>
                    <span class="value">{case["scenario_location"]}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Failed Step:</span>
                    <span class="value">{failed_step.get("keyword", "")} {failed_step.get("name", "N/A")}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Step Location:</span>
                    <span class="value">{failed_step.get("match_location", "N/A")}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Failure Type:</span>
                    <span class="value failure-type-{failure_analysis.get("failure_type", "unknown")}">{failure_analysis.get("failure_type", "unknown").replace("_", " ").title()}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Healable:</span>
                    <span class="value">{"Yes" if failure_analysis.get("is_healable") else "No"}</span>
                </div>
                {f'<div class="detail-row"><span class="label">PR:</span><span class="value">{pr_html}</span></div>' if pr_url else ''}
            </div>
            
            <div class="error-section">
                <h4>Error Message</h4>
                <pre class="error-message">{error_text}</pre>
            </div>
            
            {ai_analysis_html}
            
            <div class="screenshots-section">
                <h4>Screenshots</h4>
                <div class="screenshots-container">
                    {screenshots_html}
                </div>
            </div>
            
            <div class="element-trees-section">
                <h4>Element Trees</h4>
                <ul class="element-trees-list">
                    {element_trees_html}
                </ul>
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
            margin-bottom: 10px;
        }}
        
        .header .timestamp {{
            opacity: 0.9;
            font-size: 14px;
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
            max-width: 300px;
        }}
        
        .summary-table .status-healed {{ color: #28a745; font-weight: 600; }}
        .summary-table .status-failed {{ color: #dc3545; font-weight: 600; }}
        .summary-table .status-pending {{ color: #fd7e14; }}
        
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
        }}
        
        .case-number {{
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            margin-right: 15px;
        }}
        
        .case-name {{
            flex: 1;
            font-size: 18px;
        }}
        
        .status-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .status-healed {{ background: #d4edda; color: #155724; }}
        .status-failed {{ background: #f8d7da; color: #721c24; }}
        .status-skipped {{ background: #e2e3e5; color: #383d41; }}
        .status-pending {{ background: #fff3cd; color: #856404; }}
        
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
        }}
        
        .detail-row .value {{
            flex: 1;
        }}
        
        .failure-type-element_change {{ color: #fd7e14; font-weight: 600; }}
        .failure-type-timeout {{ color: #6c757d; }}
        .failure-type-assertion {{ color: #dc3545; }}
        .failure-type-likely_bug {{ color: #dc3545; font-weight: 600; }}
        
        .error-section, .screenshots-section, .element-trees-section, .ai-analysis-section {{
            padding: 15px 20px;
            border-top: 1px solid #eee;
        }}
        
        .error-section h4, .screenshots-section h4, .element-trees-section h4, .ai-analysis-section h4 {{
            margin-bottom: 10px;
            color: #333;
        }}
        
        .ai-analysis-section {{
            background: #fff8f0;
        }}
        
        .ai-analysis-section h4 {{
            color: #d63384;
        }}
        
        .bug-yes {{ color: #dc3545; font-weight: 600; }}
        .bug-no {{ color: #28a745; }}
        
        .confidence-high {{ color: #dc3545; font-weight: 600; }}
        .confidence-medium {{ color: #fd7e14; }}
        .confidence-low {{ color: #6c757d; }}
        
        .suggested-title {{
            background: #e7f1ff;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: 600;
        }}
        
        .suggested-desc {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-size: 12px;
            white-space: pre-wrap;
            margin-top: 5px;
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
            max-width: 300px;
            max-height: 200px;
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
        
        .element-trees-list {{
            list-style: none;
        }}
        
        .element-trees-list li {{
            padding: 5px 0;
        }}
        
        .element-trees-list a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .element-trees-list a:hover {{
            text-decoration: underline;
        }}
        
        .no-data {{
            color: #999;
            font-style: italic;
        }}
        
        .pr-link {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .pr-link:hover {{
            text-decoration: underline;
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
            <p class="timestamp">Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
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


def generate_report(healing_results: Optional[dict] = None):
    """Main function to generate HTML report."""
    print(f"Loading failure info from: {FAILURE_INFO_FILE}")
    
    try:
        failure_info = load_failure_info()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run collect_failure_info.py first.")
        return None
    
    html_content = generate_html(failure_info, healing_results)
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Report generated: {OUTPUT_FILE}")
    return str(OUTPUT_FILE)


if __name__ == "__main__":
    generate_report()
