# Analyze Failures

Analyze test failures, perform self-healing for element-related issues, and generate HTML report.

## User Configuration

```yaml
# Azure DevOps Settings (for bug creation)
ado:
  organization: https://dev.azure.com/microsoft
  project: Edge
  area_path: Edge\Edge China\Mac
  default_tags: FSQ_Auto
```

## Usage

```
/analyze-failures [--report-only]
```

## Parameters

- `--report-only`: Optional flag to skip self-healing and only generate analysis report

## Prerequisites

- Test execution completed with `reports/behave_result.json` generated
- For self-healing: MCP server available

## Important

- **All Python commands MUST use `uv run`** (e.g., `uv run behave`, `uv run scripts/xxx.py`)

## ⚠️ CRITICAL: Initialize Todo List First

**Before any other action, create this COMPLETE todo list to survive /compact:**

```
TodoWrite with ALL these items:
1. [pending] Step 1: Collect failure info and categorize (healable vs non-healable)
2. [pending] Step 2: Self-healing for element changes (one PR per heal_group)
3. [pending] Step 3: Compress screenshots (uv run scripts/compress_screenshots.py screenshots/)
4. [pending] Step 3.1: Screenshot analysis - subagents describe what they see (no bug judgment)
5. [pending] Step 3.2: Bug analysis & dedup - main agent reviews all observations, groups bugs
6. [pending] Step 4: Create ADO bugs (az boards work-item create for each bug in bug_summary)
7. [pending] Step 5: Generate HTML report (uv run scripts/generate_report.py)
8. [pending] Step 5.1: Open report (open reports/failure_analysis.html)
9. [pending] Step 6: Cleanup - return to main branch
```

**After /compact, ALWAYS check todo list first to see which step to resume.**

## Execution Steps

### 1. Collect Failure Information

Run the collection script to gather all failure data:

```bash
uv run scripts/collect_failure_info.py
```

This script collects:
- Failed cases from `reports/behave_result*.json` (supports multiple files from parallel pipelines)
- Screenshots from `screenshots/` directory (matched by case name)
- Element trees from `logs/page_source/` directory (matched by case name)
- Error messages and stack traces
- Source code locations of failed steps
- Deduplicates cases by feature_file + scenario_name (keeps last occurrence)

Output: `reports/failure_info.json`

### 1.1 Categorize Failures

After collecting failure info, categorize all failures:

**Element Change** (trigger self-healing):
- Error message contains element not found patterns
- `failure_analysis.is_healable = true`

**Non-Healable** (for bug analysis later):
- Other failures that need screenshot analysis

### 1.2 Group Element Changes for PR Deduplication

Before self-healing, analyze all element_change failures and group them by **same element**:

1. **Identify same element** based on:
   - Same locator value in error message (e.g., "Element 'Search settings' not found")
   - Same step definition file being modified
   - Same XPath or accessibility ID pattern

2. **Assign heal_group_id** to related cases:
   ```json
   {
     "failure_analysis": {
       "is_healable": true,
       "heal_group_id": "HEAL-001",
       "heal_group_reason": "Same 'Search settings' element used in multiple scenarios"
     }
   }
   ```

3. **Create heal summary** in failure_info.json:
   ```json
   {
     "heal_summary": [
       {
         "heal_group_id": "HEAL-001",
         "element_description": "Search settings input field",
         "affected_cases": ["case1", "case2"],
         "step_file": "features/steps/settings/settings.py"
       }
     ]
   }
   ```

### 2. Self-Healing Process (for element changes)

**Process by heal_group, NOT by individual case:**

For each **heal_group** (not each case):

#### 2.1 Create Git Branch (one per group)

```bash
git checkout -b fix/self-heal-<heal_group_id>-<timestamp>
```

#### 2.2 Find Matching Flag File (if exists)

Before recording, check if a matching ChromeFeatureState file exists in `reports/` directory:

```bash
ls reports/*<scenario_name_pattern>*ChromeFeatureState 2>/dev/null | head -1
```

Where `<scenario_name_pattern>` is the scenario name with spaces replaced by underscores (e.g., "Add a website to favorites" → "Add_a_website_to_favorites").

If found, this `flag_file` should be passed to the recording steps to ensure Edge launches with the same flags.

#### 2.3 Execute Self-Healing Recording

Pick **ONE representative case** from the group and follow `.claude/commands/_recording-steps.md` with:
- `feature_file_path`: The representative case's feature file
- `scenario_name`: The representative case's scenario name
- `mode`: "heal"
- `flag_file`: (Optional) Path to matching ChromeFeatureState file from step 2.2

#### 2.4 Verify ALL Cases in Group

After healing the representative case, run **ALL cases in the group** to verify the fix works for all.

**Without flag file:**
```bash
uv run behave --name "^(case1|case2|case3)$" <feature_file>
```

**With flag file (if found in step 2.2):**
```bash
uv run behave -D flag_file=<flag_file> --name "^(case1|case2|case3)$" <feature_file>
```

#### 2.5 Handle Result

**If ALL verifications pass:**
- Commit changes: `git commit -am "fix: self-heal element change for <element_description>"`
- Create ONE PR for the entire group
- **IMPORTANT: Update failure_info.json with PR URL:**
  ```bash
  uv run scripts/failure_info_helper.py update_heal <heal_group_id> healed "<pr_url>" "<fix_description>"
  ```
  Example:
  ```bash
  uv run scripts/failure_info_helper.py update_heal HEAL-001 healed "https://github.com/org/repo/pull/123" "Updated XPath locator"
  ```

**If any verification fails:**
- Record failure in report:
  ```bash
  uv run scripts/failure_info_helper.py update_heal <heal_group_id> failed "" "Verification failed"
  ```
- Discard changes: `git checkout main`

### 3. Compress Screenshots

Compress all screenshots to reduce file size before AI analysis:

```bash
uv run scripts/compress_screenshots.py screenshots/
```

This reduces image sizes by ~50-70% while preserving enough quality for AI analysis.

### 3.1 AI Screenshot Analysis (for non-healable failures)

⚠️ **CRITICAL: Use Task subagent to avoid context bloat from screenshots** ⚠️

**Important**: Subagents only do **objective screenshot analysis** - they describe what they see, NOT whether it's a bug. Bug determination happens later in Step 3.2.

#### Process Each Case Using Task Subagent (MANDATORY)

**Step 1: Get pending case info**
```bash
uv run scripts/failure_info_helper.py pending
```

This returns: index, scenario_name, error_message, screenshot_path

**Step 2: Launch Task subagent for EACH case**

For each pending case, use the Task tool with this EXACT format:

```
Task(
  subagent_type: "general-purpose",
  description: "Analyze failure case <index>",
  prompt: """
You are a test failure observer. Read the screenshot and describe what you see objectively.
DO NOT edit any code files - this is READ-ONLY analysis.

## Case Information
- Index: <index>
- Scenario: <scenario_name>
- Feature: <feature_name>
- Error Message: <error_message>
- Screenshot Path: <screenshot_path>

## Test Steps (from feature file)
<scenario_steps>

## Failed Step Implementation Code
The test failed at this verification step. Here is the actual Python code:
<step_implementation>

## Your Task
1. Read the screenshot at the path above using the Read tool
2. **Analyze the failed step code** to understand:
   - What exact element/condition is being verified (look for XPath, element names, expected values)
   - What the verification logic checks (e.g., "contains", "equals", "exists")
   - What would cause the timeout or assertion to fail
3. **Objectively describe** what the screenshot shows:
   - What page/URL is displayed in the browser?
   - What is visible in the tab bar (tab names, tab count)?
   - For Split Screen tests: describe BOTH left and right panes separately
   - What UI elements are visible (dialogs, search boxes, input fields)?
   - What text/content is shown in key areas?
4. **Compare against the verification code**:
   - Based on the step implementation, what specific element was the test looking for?
   - Is that element visible in the screenshot? If so, what is its state/value?
   - If the test expected text to "contain" something, what is the actual text shown?
5. Provide:
   - observable_state: Factual description focusing on the UI area the test was checking (2-3 sentences)
   - expected_state: What the failed step's code was specifically trying to verify
   - difference: The precise gap between what the code expected and what the screenshot shows
   - failed_functionality: Which functionality/feature failed (e.g., "search tabs", "split screen navigation")

**DO NOT determine if this is a bug or test issue** - that decision is made later with full context.

## Response Format
Return ONLY this line (no other text):
RESULT: <index> "<observable_state>" "<expected_state>" "<difference>" "<failed_functionality>"

Example:
RESULT: 0 "Screenshot shows the settings page with 'Privacy' section expanded. The search box contains 'tracking' but the results list below shows 'No results found' message." "Step code verifies element with XPath containing 'tracking-prevention' should exist after search." "Test expected search results to show tracking prevention settings, but UI shows no matching results." "settings search"
"""
)
```

**Step 3: Update failure_info.json with subagent result**

After subagent returns, parse the RESULT line and run:
```bash
uv run scripts/failure_info_helper.py update_observation <index> "<observable_state>" "<expected_state>" "<difference>" "<failed_functionality>"
```

**Step 4: Repeat for next pending case**

Run `pending` again to get next case, launch another Task subagent.

#### Parallel Processing (Recommended)

For faster analysis, get ALL pending cases at once and launch multiple Task subagents:

```bash
# Get all pending cases with full info for subagents
uv run scripts/failure_info_helper.py pending_all
```

Then launch multiple Task subagents in ONE message (3-5 at a time):
```
Task(...case 0...)
Task(...case 1...)
Task(...case 2...)
```

After all subagents return, update each case with its result.

⛔ **FORBIDDEN:**
- Do NOT read screenshots directly in main conversation (use Task subagent)
- Do NOT read failure_info.json directly (use helper script)
- Do NOT let subagent determine if something is a bug (that's done in Step 3.2)

✅ **REQUIRED:**
- Use Task subagent for screenshot analysis (keeps images out of main context)
- Use `pending` or `list` to get case info
- Use `update_observation` to save observation results

### 3.2 Bug Analysis and Deduplication (Main Agent)

⚠️ **This step is done by MAIN AGENT with full context of all cases** ⚠️

**Step 1: Get ALL observations summary**
```bash
uv run scripts/failure_info_helper.py observations
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
uv run scripts/failure_info_helper.py set_bug_group <group_id> <indices> "<reason>" "<title>" <is_bug> <confidence> <category>
```

Example:
```bash
uv run scripts/failure_info_helper.py set_bug_group BUG-001 "0,1,2,3" "All cases fail on search tabs functionality" "[Edge] Search tabs not returning results" true 0.85 functional_bug
```

**Decision criteria for is_bug**:
- `true` (product bug): Multiple test variations of same feature all fail similarly
- `true` (product bug): Screenshot shows unexpected UI state that doesn't match product spec  
- `false` (test_infrastructure): Only ONE case fails while similar cases pass
- `false` (test_infrastructure): Screenshot shows correct UI but automation couldn't detect it

⛔ **FORBIDDEN:**
- Do NOT read failure_info.json directly
- Do NOT let individual subagent analysis determine bug status (main agent decides with full context)

✅ **REQUIRED:**
- Use `observations` to see ALL cases' objective analysis
- Use `set_bug_group` to assign groups WITH bug determination
- Consider cross-case patterns before deciding bug vs infrastructure

### 4. Create ADO Bugs (for likely bugs)

For each unique bug in `bug_summary`, create a work item using settings from **User Configuration** above:

```bash
az boards work-item create \
  --org <ado.organization> \
  --project <ado.project> \
  --type Bug \
  --title "<suggested_title>" \
  --area "<ado.area_path>" \
  --fields "System.Tags=<ado.default_tags>" "Microsoft.VSTS.TCM.ReproSteps=<repro_steps>"
```

Where `<repro_steps>` includes:
- Affected test cases
- Error message
- Screenshot analysis summary

**After creating each bug:**
1. Capture the bug URL from the command output
2. Update `failure_info.json` with the bug URL:
   ```json
   {
     "bug_summary": [
       {
         "bug_group_id": "BUG-001",
         "ado_bug_url": "https://dev.azure.com/org/project/_workitems/edit/12345",
         ...
       }
     ]
   }
   ```
3. Also update each affected case's `ai_analysis` with the bug URL

**If `az` command fails:**
- Skip bug creation
- Log warning in report
- Continue with report generation

### 5. Generate HTML Report

Run the report generation script:

```bash
uv run scripts/generate_report.py
```

Output: `reports/failure_analysis.html`

### 5.1 Open Report

Open the report in default browser:

```bash
open reports/failure_analysis.html
```

Report includes:
- Summary statistics (total failures, healed, likely bugs, other)
- List of all failed cases with:
  - Scenario name and feature file
  - Error message
  - Failure category (element_change, likely_bug, other)
  - AI analysis details (for likely bugs):
    - Bug confidence score
    - Bug category
    - Analysis reason
    - Suggested bug title and description
  - Self-healing status (attempted/succeeded/failed/skipped)
  - PR link (if created)
  - Screenshots (embedded or linked)

### 6. Cleanup

Return to main branch:
```bash
git checkout main
```

## Example

```
/analyze-failures
/analyze-failures --report-only
```

## Output

- `reports/failure_info.json`: Collected failure data with AI analysis
- `reports/failure_analysis.html`: Final analysis report
- PRs created for successfully healed cases

## Notes

1. Element changes affecting the same element are grouped into ONE PR (not separate PRs)
2. Bug analysis groups similar failures into ONE bug entry (not separate bugs)
3. Self-healing is only attempted for element-change failures
4. AI bug analysis is performed for non-element-change failures
5. Bug and heal group results can be used for ADO integration
6. Screenshots and element trees are matched by case name pattern
