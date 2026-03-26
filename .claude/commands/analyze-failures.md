# Analyze Failures

Analyze test failures, perform self-healing for element-related issues, and generate HTML report.

## User Configuration

ADO bug creation settings are in `.claude/commands/_ado_bug_config.yaml`. Read this file before creating bugs to get org, project, area_path, tags, fields, templates, etc.

Self-healing PR settings:
- Branch naming: `fix/self-heal-<build_id>-<heal_group_id>` (must be unique per run/build)
- Branch prefix for PR discovery: `fix/self-heal-` (used for PR dedup)
- PR title prefix: `[self-heal]`
- PR body must include `## Affected Cases` section listing case names

## Usage

```
/analyze-failures <build_id> [--skip-download] [--analyze-only]
```

## Parameters

- `build_id`: **Required.** Azure DevOps pipeline run (build) ID. Example: `141562849`
- `--skip-download`: Optional flag to skip artifact download and use existing data in `pipeline_data/<build_id>/`. Useful for re-running analysis on already downloaded data.
- `--analyze-only`: Optional flag to stop after Step 3.0 (bug analysis) and Step 4 (report generation, without upload). Skips PR creation (Step 2.1), ADO bug creation (Step 3.1), report upload, and cleanup (Step 5). Useful for reviewing analysis results before taking action.

## Prerequisites

- Logged in to Azure CLI (`az login`)
- For self-healing: MCP server available

## Important

- **All Python commands MUST use `uv run`** (e.g., `uv run behave`, `uv run scripts/xxx.py`)

## ⚠️ CRITICAL: Initialize Todo List First

**Before any other action, create this COMPLETE todo list to survive /compact:**

**Set `DATA_DIR=pipeline_data/<build_id>` for all subsequent commands.**

```
TodoWrite with ALL these items:
1. [pending] Step 0: Download pipeline artifacts (SKIP if --skip-download)
2. [pending] Step 1: Collect failure info (uv run scripts/collect_failure_info.py --data-dir pipeline_data/<build_id>)
3. [pending] Step 1.1: Compress screenshots (uv run scripts/compress_screenshots.py pipeline_data/<build_id>/screenshots/)
4. [pending] Step 1.1b: Prune element trees (uv run scripts/prune_element_tree.py pipeline_data/<build_id>/logs/error_results/)
5. [pending] Step 1.2: Screenshot + element tree triage (parallel subagents, 3 at a time)
6. [pending] Step 2.0: Healable cases - group by same element (set_heal_group)
7. [pending] Step 2.1: Self-healing - direct code fix with fallback + verify + create PR via script (SKIP if --analyze-only)
8. [pending] Step 3.0: Bug analysis & dedup - main agent reviews all observations, groups bugs
9. [pending] Step 3.1: Create ADO bugs (SKIP if --analyze-only)
10. [pending] Step 4: Generate HTML report (--analyze-only: generate only, no upload; otherwise: generate and upload)
11. [pending] Step 5: Cleanup - return to main branch (SKIP if --analyze-only)
```

**After /compact, ALWAYS check todo list first to see which step to resume.**

## Execution Steps

### 0. Download Pipeline Artifacts

**If `--skip-download` is specified, skip this step entirely and go to Step 1.**

Download test results, screenshots, and logs from the Azure DevOps pipeline run:

```bash
uv run scripts/download_pipeline_artifacts.py <build_id>
```

This script:
- Authenticates via `az` CLI (must be logged in)
- Lists all `MacAutomationTestResults-Agent*` artifacts from the build
- Downloads and extracts each artifact zip via REST API
- Merges all agents' data into `pipeline_data/<build_id>/`:
  - `logs/` — behave result JSON files (renamed per agent), agent logs, error results with element trees
  - `screenshots/` — all screenshots from all agents
  - `logs/error_results/` — error result JSONs containing element trees (XML page_source)
  - `pipeline_info.json` — run metadata and URL
- Skips download if directory already exists (cached)

**Set `DATA_DIR=pipeline_data/<build_id>` for all subsequent steps.**

### 1. Collect Failure Information

Run the collection script with the pipeline data directory:

```bash
uv run scripts/collect_failure_info.py --data-dir pipeline_data/<build_id>
```

This script collects:
- Failed cases from `logs/behave_result*.json` (supports multiple files from parallel pipelines)
- Screenshots from `screenshots/` directory (matched by case name)
- Element trees from `logs/error_results/` directory (matched by screenshot timestamp ±5s)
- Error messages and stack traces
- Source code locations of failed steps
- Deduplicates cases by feature_file + scenario_name (keeps last occurrence)

Output: `pipeline_data/<build_id>/reports/failure_info.json`

**NOTE:** After collection, all cases have `is_healable: null`. The actual determination
happens in Step 1.2 (screenshot + element tree triage) after analyzing screenshots and element trees.

### 1.1 Compress Screenshots

Compress all screenshots to reduce file size before AI analysis:

```bash
uv run scripts/compress_screenshots.py pipeline_data/<build_id>/screenshots/
```

This outputs compressed copies to `screenshots_compressed/` alongside the original `screenshots/` directory.
Original files are preserved for high-detail ROI cropping during triage.
- **Compressed path**: `pipeline_data/<build_id>/screenshots_compressed/<name>.jpg` (for overview analysis)
- **Original path**: `pipeline_data/<build_id>/screenshots/<name>.png` (for ROI crop)

### 1.1b Prune Element Trees

Prune all element tree files to reduce size for AI analysis (85-93% reduction):

```bash
uv run scripts/prune_element_tree.py pipeline_data/<build_id>/logs/error_results/
```

This script applies 4 optimizations:
1. Remove hidden elements (width=0 AND height=0)
2. Strip empty/default attributes (empty label/title/identifier/value, enabled=true, selected=false)
3. Collapse meaningless single-child Groups (no label/title/identifier/value)
4. Shorten tag names (`XCUIElementType` prefix removed) and compact rect format

Output: `pipeline_data/<build_id>/logs/error_results_pruned/` — same filenames, pruned content.

**Pruned file structure:**
```json
{
  "tool_name": "verify_element_exists",
  "parameters": {
    "locator_value": "the locator that failed",
    "locator_strategy": "AppiumBy.ACCESSIBILITY_ID"
  },
  "error": "error message",
  "page_source_pruned": "<compact XML tree>"
}
```

**Subagents in Step 1.2 MUST read from `error_results_pruned/`, NOT `error_results/`.**

### 1.2 Screenshot + Element Tree Triage (Parallel Subagent Analysis)

⚠️ **CRITICAL: This step uses PARALLEL SUBAGENTS to analyze each case's screenshot + element tree, then MAIN AGENT makes final healable/bug judgment** ⚠️

After collection, ALL cases have `is_healable: null`. Each case needs screenshot + element tree analysis to collect evidence.

**Architecture:**
- **Subagents** (Task tool, `general-purpose` type): Each analyzes ONE case — reads screenshot, reads element tree, writes debug log with factual observations. **Subagents do NOT make healable/bug judgment.**
- **Main agent**: After ALL subagents complete, reads all debug logs, then makes healable/bug determination for each case with full cross-case context.
- **Parallelism**: Launch up to **3 subagents concurrently** using multiple Task tool calls in a single message.

**Why both screenshot AND element tree are needed**:
- **Screenshot alone** can show if the UI looks correct, but can't tell you if an element's accessibility ID changed
- **Element tree alone** can show if a specific locator exists, but can't tell you if the page is in the wrong state
- **Together** they give definitive answers:
  - Element visible in screenshot + element exists in tree with different identifier → **Healable**
  - Element visible in screenshot + element NOT in tree at all → **Healable** (locator completely changed)
  - Element absent from screenshot + element absent from tree → **Bug**
  - Wrong page in screenshot + irrelevant tree content → **Bug**

**Step 1: Get all cases pending triage and initialize debug logs**
```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> triage
```

This returns ALL cases with `is_healable: null`, including index, screenshot path, element tree path, error message.

For each pending case, initialize its debug log from template:
```bash
uv run scripts/init_triage_log.py --data-dir pipeline_data/<build_id> --index <index>
```

This creates `pipeline_data/<build_id>/reports/triage_debug/case_<index>.md` with all required sections pre-filled with `PENDING`. It also auto-derives the compressed screenshot path and pruned element tree path.

**Step 2: Launch subagents in batches of 3**

Process all pending cases by launching subagents. In each message, launch up to **3 Task tool calls concurrently**. Wait for all 3 to complete before launching the next batch.

For each case, launch a `general-purpose` subagent with the following prompt (fill in the case-specific values from init_triage_log output):

---

#### Subagent Prompt Template

```
You are analyzing a single test failure case. Collect FACTUAL OBSERVATIONS only — no healable/bug judgment. Do NOT guess content you cannot read.

## Case Info
- Index: <index>
- Scenario: <scenario_name>
- Failed step: <failed_step_name>
- Error: <error_message_first_line>
- Compressed screenshot: <compressed_screenshot_path>
- Element tree: <element_tree_path>
- Update command: uv run scripts/update_triage_log.py --file pipeline_data/<build_id>/reports/triage_debug/case_<index>.md --section <SECTION> --content "<CONTENT>"

You make exactly **2 update calls**: `--section screenshot_all` and `--section element_tree`. For multi-line content use bash $'...\n...' syntax. ALL Bash calls MUST use **timeout: 30000**.

## Task 1: Screenshot Analysis

⚠️ Analyze the screenshot BEFORE looking at the error. Describe what you see with ZERO preconceptions.

1. Read the compressed screenshot file. If read FAILS → update `screenshot_all` with `SCREENSHOT_READ: FAILED (<reason>)` and skip to Task 2.
2. If read SUCCEEDS → compose content following this template exactly, then update `screenshot_all` in ONE call:

```
SCREENSHOT_READ: SUCCESS

### PAGE_LAYOUT
<application name, window mode (normal/fullscreen), overall structure>

### TAB_BAR
<every tab left to right: exact title, active/inactive, visual indicators; or "No tab bar visible">

### TOOLBAR
<every button/icon left to right: exact label or icon shape, enabled/disabled state, address bar content>

### SIDEBAR
<every item with exact label and hierarchy; or "Not visible">

### WEB_CONTENT
<URL in address bar, page title, every heading, every form field with placeholder/value, every button/link text>

### DIALOGS_AND_OVERLAYS
<popup/dialog title, all text, all buttons; or "None">

### OTHER_ELEMENTS
<info bar, download bar, status bar, notifications; or "None">
```

**Detail level required (follow these examples):**

TAB_BAR: "3 tabs left to right: 1) 'New Tab' (inactive, close button visible) 2) 'Google' (active, blue underline) 3) 'Search - Microsoft Bing' (inactive). No tab groups."

TOOLBAR: "Left to right: Back arrow button (disabled), Forward arrow button (disabled), Refresh button (enabled), Address bar containing 'https://www.bing.com' (focused, blue border), Star icon (not filled, enabled), Read-aloud icon, Share icon, Feedback smiley icon, Extensions puzzle icon, Profile avatar (letter 'J'), Three-dot menu button"

WEB_CONTENT: "URL: edge://settings/privacy. Heading: 'Privacy, search, and services'. Section 'Tracking prevention': radio 'Basic' (off), 'Balanced' (selected), 'Strict' (off). Button 'Blocked trackers (0)'. Section 'Clear browsing data': button 'Choose what to clear'. Toggle 'Send Do Not Track requests' (off)."

SIDEBAR: "Vertical tab sidebar. Search box placeholder 'Search tabs'. Pinned: 'Google' with favicon. All tabs: 1) 'New Tab' 2) 'Settings - Microsoft Edge'. Collapse button at bottom."

⚠️ Do NOT use vague terms like "standard toolbar", "some content", "typical layout", "various controls". Every element must be specifically named and enumerated.

## Task 2: Element Tree Analysis

1. Read the pruned element tree file. If path is "N/A" or read FAILS → update `element_tree` with `ELEMENT_TREE_READ: FAILED (no file)` and stop.
2. The file is JSON with `parameters.locator_value`, `parameters.locator_strategy`, and `page_source_pruned` (compact XML, shortened tags like `Button` not `XCUIElementTypeButton`).
3. Search the tree:
   - `ACCESSIBILITY_ID`: match `label`, `title`, or `identifier`
   - `XPATH`: evaluate the XPath against the tree
   - Include **partial matches**
4. Update `element_tree` with ALL fields:
   - `ELEMENT_TREE_READ: SUCCESS`
   - `LOCATOR_SEARCHED: <strategy>=<value>`
   - `TARGET_FOUND_IN_TREE: yes/no`
   - `TREE_MATCH_DETAILS: <matching element attributes if found>`
   - `LOCATOR_DIFFERENCE: <how it differs, or None>`
   - `NEARBY_ELEMENTS: <relevant siblings>`

## Return
"Case <index> (<scenario_name>): Screenshot <SUCCESS/FAILED>, Element tree <SUCCESS/FAILED>."
```

---

**Batching example** (if 7 cases pending: indices 0,1,2,3,4,5,6):

Batch 1: Launch 3 Task tools in ONE message for cases 0, 1, 2
→ Wait for all 3 to complete

Batch 2: Launch 3 Task tools in ONE message for cases 3, 4, 5
→ Wait for all 3 to complete

Batch 3: Launch 1 Task tool for case 6
→ Wait for completion

⚠️ **Handling subagent failures**: If a subagent fails (e.g., context limit exceeded, tool error), do **NOT** retry or attempt to perform the subagent's work in the main agent. Instead:
1. Update the debug log with failure status:
   ```bash
   uv run scripts/update_triage_log.py --file pipeline_data/<build_id>/reports/triage_debug/case_<index>.md --section screenshot_all --content "SCREENSHOT_READ: FAILED (subagent failed)"
   uv run scripts/update_triage_log.py --file pipeline_data/<build_id>/reports/triage_debug/case_<index>.md --section element_tree --content "ELEMENT_TREE_READ: FAILED (subagent failed)"
   ```
2. In Step 4 (update triage), use the fallback error text pattern table to triage this case.
3. Move on to the next batch.

**Step 3: Main agent reads all debug logs and makes judgment**

After ALL subagents have completed, the main agent reads each debug log and applies the judgment logic.

For each case, read the debug log:
```bash
cat "pipeline_data/<build_id>/reports/triage_debug/case_<index>.md"
```

**How to use the evidence**: The subagent's screenshot analysis is a **blind enumeration** — it does not know what element the test was looking for. The main agent must:
1. Read the **error message** to understand what element/locator failed
2. Read the **screenshot enumeration** to see what is actually on the page
3. Read the **element tree analysis** to see if a matching/similar element exists in the tree
4. **Cross-reference** these three sources to make the judgment

⚠️ **IMPORTANT**: Locators (accessibility ID, XPath, name, etc.) are automation identifiers — they are NOT the same as what the user sees on screen. A locator string may contain synthesized state info, internal identifiers, element counts, or descriptive text that never appears visually. Icons and graphical elements have no visible text at all. The main agent must extract the **semantic meaning** from the locator and the test scenario context, then find the corresponding visual element in the screenshot enumeration.

Apply the judgment patterns:

**Pattern 1 — Wrong page/state** (screenshot enumeration shows a completely different page than the test scenario expects):
- → **BUG** (navigation or setup step failed)
- Confidence: HIGH

**Pattern 2 — Element absent from BOTH screenshot and tree** (screenshot enumeration does not contain any element matching the semantic meaning of the locator, AND tree has no match):
- → **BUG** (feature did not execute correctly, element genuinely missing)
- Confidence: HIGH

**Pattern 3 — Unexpected extra element** (DIALOGS_AND_OVERLAYS section lists a blocking popup/dialog):
- → **BUG** (unexpected UI blocked the test)
- Confidence: HIGH

**Pattern 4 — Element present in screenshot + found in tree with different locator** (screenshot enumeration shows the element matching the semantic meaning, AND tree found a partial match with different attribute):
- → **HEALABLE** (element exists, accessibility locator changed)
- Confidence: HIGH

**Pattern 5 — Element present in screenshot + NOT found in tree** (screenshot shows it, tree has no match or tree unavailable):
- → **HEALABLE** (element exists visually, locator likely completely changed)
- Confidence: MEDIUM

**Pattern 6 — Value/state mismatch** (element exists in both, but value/state is wrong):
- → **BUG** (functionality produced wrong result)
- Confidence: HIGH

**Pattern 7 — Visual verification flaky** (`verify_visual_task` tool failure where screenshot contradicts the test result):
- **Detection**: The failed step's `step_implementation` contains `name='verify_visual_task'`, AND our screenshot analysis shows the expected visual state IS actually present (the task_description in the code describes what to verify — check if the screenshot matches it)
- → **VISUAL_FLAKY** (the OpenAI vision API intermittently misjudged the screenshot)
- Confidence: HIGH
- This means: the UI is correct, the test tool produced a false negative. Not a bug, not healable — just flaky visual verification.

⚠️ **Pattern 7 check MUST happen BEFORE other patterns** for `verify_visual_task` cases. If the step calls `verify_visual_task`, first check if our screenshot analysis agrees with the task_description. If it does → Pattern 7. If our analysis ALSO shows the visual state is wrong → Pattern 2 or 6 (real bug).

**Tiebreaker rule**: "Element not found" error refers to an accessibility locator string failing — it does NOT mean the element is visually absent. When screenshot enumeration shows a plausible matching element but tree is ambiguous, prefer HEALABLE.

**Fallback (when subagent reported both reads FAILED)**:
If a case has SCREENSHOT_READ: FAILED AND ELEMENT_TREE_READ: FAILED, fall back to error text patterns:

| Error Pattern | Default Triage | Reason |
|---|---|---|
| `value=, expected <X>` (assertion, value empty) | **bug** | Empty value = functionality failed |
| `value=<Y>, expected <X>` (assertion, value wrong) | **bug** | Wrong value = functionality broken |
| `element .* not found` | **healable** | Default optimistic — element may exist with changed locator |
| `TimeoutException` | **bug** | Cannot determine without screenshot — conservative default |
| `not interactable` / `not clickable` | **healable** | Element exists but interaction method may need update |
| Other / unclear | **bug** | Conservative default |

**Step 4: Update triage for each case**

After making judgment, update the judgment section in the debug log and update triage:

```bash
uv run scripts/update_triage_log.py --file pipeline_data/<build_id>/reports/triage_debug/case_<index>.md --section judgment --content $'PATTERN: <1/2/3/4/5/6/7>\nREASONING: <interpretation combining screenshot + tree evidence>\nCONFIDENCE: <HIGH|MEDIUM|LOW> - <why>\nTRIAGE: <index> <healable|bug|visual_flaky> "<reason>"'
```

For healable:
```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> update_triage <index> true "<reason>"
```

For bug (include observation details):
```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> update_triage <index> false "<reason>" "<observable_state>" "<expected_state>" "<difference>" "<failed_functionality>"
```

For visual_flaky (verify_visual_task intermittent failure):
```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> update_triage <index> visual_flaky "<reason>"
```

**Step 5: Re-check for remaining untriaged cases**

```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> triage
```

If any remain, retry once.

**DO NOT proceed to Step 2 while `pending_triage > 0`.**

### 2.0 Group Healable Cases by Same Element

After triage, group all healable cases by **same element**:

1. **Get healable cases:**
   ```bash
   uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> healable
   ```

2. **Identify same element** based on:
   - Same locator value in error message
   - Same step definition file being modified
   - Same XPath or accessibility ID pattern

3. **Assign heal_group_id** to related cases:
   ```json
   {
     "failure_analysis": {
       "is_healable": true,
       "heal_group_id": "HEAL-001",
       "heal_group_reason": "Same element used in multiple scenarios"
     }
   }
   ```

4. **Create heal summary** in failure_info.json:
   ```bash
   uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> set_heal_group HEAL-001 '0,1' '<element_description>' '<step_file>'
   ```

### 2.1 Self-Healing: Direct Code Fix

**If `--analyze-only` is specified, skip Steps 2.1, 3.1, and 5. Step 4 still runs but without upload.**

**Process by heal_group, NOT by individual case.**

⚠️ **KEY CHANGE**: We already know the exact locator change from the triage debug logs (element tree analysis shows LOCATOR_SEARCHED vs TREE_MATCH_DETAILS). Directly modify the step definition code — no need to re-record.

For each **heal_group**:

##### Step 1: Create Git Branch (one per group)

⚠️ **CRITICAL: Always start from main branch** to avoid carrying changes from a previous heal group:

```bash
git checkout main
git checkout -b fix/self-heal-<build_id>-<heal_group_id>
```

Branch name MUST start with `fix/self-heal-` and include `<build_id>` — this keeps branch names unique across runs while preserving PR dedup discovery by prefix.

##### Step 2: Read Triage Debug Log for Locator Change

Read the debug log of the representative case to get the exact locator difference:
```bash
cat "pipeline_data/<build_id>/reports/triage_debug/case_<index>.md"
```

From the debug log, extract:
- **Old locator**: `LOCATOR_SEARCHED` value (e.g., `AppiumBy.ACCESSIBILITY_ID=Search Engines tab group ("Google" and 2 Other Tabs) - Expanded`)
- **New locator**: `TREE_MATCH_DETAILS` value (e.g., `Button label="Search Engines - Expanded" @(88,1,130,41)`)

##### Step 3: Locate and Modify Step Definition Code

1. Find the step definition file from the heal_group info (or from the case's `source_location`)
2. Find the specific `call_tool_sync` call that uses the old locator
3. Modify the code to **try the new locator first, fall back to the old locator if it fails**

**Code pattern — wrap the single tool call with fallback:**

Before:
```python
result = call_tool_sync(
    context,
    context.session.call_tool(
        name='verify_element_exists',
        arguments={
            'caller': 'behave-automation',
            'locator_value': '<old_locator_value>',
            'locator_strategy': '<locator_strategy>',
            'need_snapshot': 0,
        },
    ),
)
result_json = get_tool_json(result)
assert result_json.get('status') == 'success', (
    f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
)
```

After:
```python
result = call_tool_sync(
    context,
    context.session.call_tool(
        name='verify_element_exists',
        arguments={
            'caller': 'behave-automation',
            'locator_value': '<new_locator_value>',
            'locator_strategy': '<new_locator_strategy>',
            'need_snapshot': 0,
        },
    ),
)
result_json = get_tool_json(result)
if result_json.get('status') != 'success':
    result = call_tool_sync(
        context,
        context.session.call_tool(
            name='verify_element_exists',
            arguments={
                'caller': 'behave-automation',
                'locator_value': '<old_locator_value>',
                'locator_strategy': '<locator_strategy>',
                'need_snapshot': 0,
            },
        ),
    )
    result_json = get_tool_json(result)
assert result_json.get('status') == 'success', (
    f"Expected status to be 'success', got '{result_json.get('status')}', error: '{result_json.get('error')}'"
)
```

**IMPORTANT rules for code modification:**
- The `name` parameter (tool name: `click_element`, `verify_element_exists`, `send_keys`, etc.) must stay the same in both the new and old calls
- Only change `locator_value` and `locator_strategy`
- Keep all other arguments identical (`caller`, `need_snapshot`, `text` for send_keys, etc.)
- The `assert` only appears ONCE at the end, after the fallback
- If the same locator appears in multiple tool calls in the same step, apply the fallback pattern to EACH call

##### Step 4: Verify ALL Cases in Group

Run all cases in the group to verify the fix works:

```bash
uv run behave --name "^(case1|case2|case3)$" <feature_file>
```

##### Step 5: Handle Verification Result

**Classify the failure type** before deciding next action:

**Environment failure indicators** (any of these → environment issue):
- `ConnectionError`, `ConnectionRefusedError`, `socket.error`
- `SessionNotCreatedException`, `WebDriverException` with "session" or "connection"
- `OSError`, `TimeoutError` at session/connection level
- App failed to launch or Appium server not responding
- Error occurs BEFORE the test's actual step executes (in setup/Given steps unrelated to the fix)
- All cases in the group fail with the same infrastructure error

**Real test failure indicators** (any of these → code fix didn't work):
- The SAME element-not-found error as before (original locator AND new locator both fail)
- A DIFFERENT assertion error in the step we modified
- Error occurs IN the step we modified or AFTER it
- Some cases pass, some fail (inconsistent = likely code issue, not env)

**Flow chart:**

```
Verification run
    ├── ALL pass → commit + create PR + git checkout main (see below)
    ├── Environment failure → create PR with [not verified] tag + git checkout main (see below)
    └── Real test failure → retry (max 2 attempts total)
         ├── Attempt 1: Re-read error, adjust code fix, run verification again
         │    ├── ALL pass → commit + create PR + git checkout main
         │    ├── Environment failure → commit + create PR with [not verified] tag + git checkout main
         │    └── Real test failure again → Attempt 2
         └── Attempt 2: Re-read error, adjust code fix, run verification again
              ├── ALL pass → commit + create PR + git checkout main
              ├── Environment failure → commit + create PR with [not verified] tag + git checkout main
              └── Real test failure again → record failure, discard branch, git checkout main
```

**If ALL verifications pass:**
- Commit changes: `git commit -am "fix: self-heal element change for <element_description>"`
- Create PR via script:
  ```bash
  uv run scripts/create_heal_pr.py --data-dir pipeline_data/<build_id> --group-id <heal_group_id>
  ```
  This script automatically:
  1. Fetches all open `fix/self-heal-*` PRs and parses their `## Affected Cases` section
  2. Filters out cases already covered by existing open PRs
  3. If remaining cases > 0: pushes branch + creates PR with `[self-heal]` title prefix
  4. Updates `failure_info.json` with PR URL
- Return to main branch after PR creation:
  ```bash
  git checkout main
  ```

**If environment failure detected:**
- Commit changes: `git commit -am "fix: self-heal element change for <element_description>"`
- Create PR with `[not verified]` tag:
  ```bash
  uv run scripts/create_heal_pr.py --data-dir pipeline_data/<build_id> --group-id <heal_group_id> --not-verified
  ```
  This adds `[not verified]` to the PR title (e.g., `[self-heal][not verified] Fix element change for ...`)
- Return to main branch:
  ```bash
  git checkout main
  ```

**If real test failure after 2 retry attempts:**
- Record failure:
  ```bash
  uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> update_heal <heal_group_id> failed "" "Verification failed after 2 retries"
  ```
- Discard changes and return to main:
  ```bash
  git checkout main
  git branch -D fix/self-heal-<build_id>-<heal_group_id>
  ```

### 3.0 Bug Analysis and Deduplication (Main Agent)

⚠️ **This step is done by MAIN AGENT with full context of all cases** ⚠️

**Step 1: Get ALL observations summary**
```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> observations
```

This outputs for ALL analyzed cases:
- index, scenario name, failed_functionality, difference, error snippet

**Step 2: Analyze patterns and determine bugs**

With the full picture of all failures, the main agent should:

1. **Group by failed_functionality**: Cases with same `failed_functionality` likely share root cause
2. **Compare differences**: Cases with similar `difference` descriptions are likely same bug
3. **Consider test variations**: Same functionality tested in different modes (horizontal/vertical, normal/fullscreen) failing = likely product bug, NOT test infrastructure

**Key insight**: If Case A and Case B both fail on "search tabs" functionality with similar symptoms, they are the SAME BUG even if:
- One is in normal mode, one is in fullscreen
- One is horizontal tabs, one is vertical tabs  
- The error messages are slightly different

**Step 3: Assign bug groups and determine bug vs infrastructure**

For each identified group:
```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> set_bug_group <group_id> <indices> "<reason>" "<title>" <is_bug> <confidence> <category>
```

Example:
```bash
uv run scripts/failure_info_helper.py --data-dir pipeline_data/<build_id> set_bug_group BUG-001 "0,1,2,3" "All cases fail on search tabs functionality" "[Edge] Search tabs not returning results" true 0.85 functional_bug
```

**Decision criteria for is_bug**:
- `true` (product bug): Multiple test variations of same feature all fail similarly
- `true` (product bug): Screenshot shows unexpected UI state that doesn't match product spec  
- `false` (test_infrastructure): Only ONE case fails while similar cases pass
- `false` (test_infrastructure): Screenshot shows correct UI but automation couldn't detect it

⛔ **FORBIDDEN:**
- Do NOT read failure_info.json directly
- Do NOT let individual case triage determine bug status (main agent decides with full cross-case context)

✅ **REQUIRED:**
- Use `observations` to see ALL cases' objective analysis
- Use `set_bug_group` to assign groups WITH bug determination
- Consider cross-case patterns before deciding bug vs infrastructure

### 3.1 Create ADO Bugs (for likely bugs)

**If `--analyze-only` is specified, skip this step. Proceed to Step 4 (report generation without upload).**

Run the bug creation script:

```bash
uv run scripts/create_ado_bugs.py --data-dir pipeline_data/<build_id>
```

This script automatically:
1. Reads config from `.claude/commands/_ado_bug_config.yaml`
2. For each bug group in `bug_summary`:
   - **Dedup check**: Queries `OSG.CustomHTML CONTAINS '<case_name>'` via WIQL — skips if bug already exists
   - **Upload screenshots**: Uploads to ADO attachment API with short filenames, fixes domain for rendering
   - **Build repro HTML**: Shared header (Platform + Build + Recurrence) at top, per-case sections with repro/expected/actual/error/screenshot
   - **Create bug**: Via REST API with all fields (Tags, Severity, Product, CustomHTML, ReproSteps)
3. Updates `failure_info.json` with `ado_bug_url` and `ado_bug_id` for each created bug

**If the script fails:**
- Already-created bugs are preserved (idempotent)
- Re-run safely — dedup check prevents duplicates
- Continue with report generation

### 4. Generate HTML Report

**If `--analyze-only`**: generate report only (no upload):
```bash
uv run scripts/generate_report.py --data-dir pipeline_data/<build_id>
```

**Otherwise**: generate and upload:
```bash
uv run scripts/generate_report.py --data-dir pipeline_data/<build_id> --upload
```

This generates `pipeline_data/<build_id>/reports/failure_analysis.html`. When `--upload` is used, it also uploads both the HTML report and `failure_info.json` to Azure Blob Storage.
The SAS URLs (valid for 7 days) are printed to console and saved to `pipeline_data/<build_id>/reports/report_url.json`.

Blob paths:
- `<pipeline_name>/<build_id>/<date>_<HHMMSS>_failure_analysis.html` (unique per run, never overwrites)
- `<pipeline_name>/<build_id>/<date>_<HHMMSS>_failure_info.json` (uploaded alongside the report)

### 5. Cleanup

Return to main branch:
```bash
git checkout main
```

## Example

```
/analyze-failures 141562849
/analyze-failures 141562849 --analyze-only
/analyze-failures 141562849 --skip-download --analyze-only
```

## Output

- `pipeline_data/<build_id>/` — Downloaded pipeline artifacts
- `pipeline_data/<build_id>/reports/failure_info.json` — Collected failure data with AI analysis (also uploaded)
- `pipeline_data/<build_id>/reports/failure_analysis.html` — Final analysis report
- `pipeline_data/<build_id>/reports/report_url.json` — Uploaded report SAS URL
- PRs created for successfully healed cases (with `[not verified]` tag if env verification failed)

## Notes

1. Element changes affecting the same element are grouped into ONE PR (not separate PRs)
2. Bug analysis groups similar failures into ONE bug entry (not separate bugs)
3. Self-healing is only attempted for element-change failures
4. Screenshots and element trees are matched by case name pattern
