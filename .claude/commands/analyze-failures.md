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
1. [pending] Step 1: Collect failure info (uv run scripts/collect_failure_info.py)
2. [pending] Step 1.5: Compress screenshots (uv run scripts/compress_screenshots.py screenshots/)
3. [pending] Step 2: AI bug analysis for non-healable failures (read screenshot, analyze, save)
4. [pending] Step 2.2: Run /compact after every 2 screenshot analyses
5. [pending] Step 2.3: Bug deduplication - group similar bugs, assign bug_group_id
6. [pending] Step 3: Categorize failures and create heal_summary for element changes
7. [pending] Step 4: Start Appium (bash scripts/start_appium_auto.sh) before self-healing
8. [pending] Step 4.1: Self-healing for element changes (one PR per heal_group)
9. [pending] Step 5: Create ADO bugs (az boards work-item create for each bug in bug_summary)
10. [pending] Step 6: Generate HTML report (uv run scripts/generate_report.py)
11. [pending] Step 6.1: Open report (open reports/failure_analysis.html)
12. [pending] Step 7: Cleanup - return to main branch
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

### 1.5 Compress Screenshots

Compress all screenshots to reduce file size before AI analysis:

```bash
uv run scripts/compress_screenshots.py screenshots/
```

This reduces image sizes by ~50-70% while preserving enough quality for AI analysis.

### 2. AI Bug Analysis (for non-healable failures)

⚠️ **CRITICAL: Use helper script to avoid reading full JSON** ⚠️

#### 2.1 Process Each Case Sequentially (MANDATORY)

**Use `failure_info_helper.py` to minimize context usage:**

```bash
# Get next pending case (outputs only: index, scenario, error, screenshot path)
uv run scripts/failure_info_helper.py pending
```

**For each pending case:**
1. Run `pending` command to get case info and screenshot path
2. Read the ONE screenshot
3. Analyze and determine if it's a bug
4. Update using helper script:
   ```bash
   uv run scripts/failure_info_helper.py update <index> <is_bug> <confidence> <category> "<title>" "<reason>"
   ```
5. Run `/compact` immediately
6. After compact, run `pending` again for next case

**Example:**
```bash
uv run scripts/failure_info_helper.py update 0 true 0.75 timeout "[Edge] Search tabs timeout" "Test times out waiting for tab"
```

⛔ **FORBIDDEN:**
- Do NOT read failure_info.json directly (use helper script)
- Do NOT read multiple screenshots without /compact between them
- Do NOT skip /compact after reading any screenshot

✅ **REQUIRED:**
- Use `pending` → Read ONE screenshot → `update` → `/compact` → repeat

#### 2.2 Context Management (MANDATORY)

**After analyzing EVERY SINGLE case with screenshot, you MUST run:**

```
/compact
```

This clears context history to prevent overflow. Continue with remaining cases after compact completes.

### 2.3 Bug Deduplication

After analyzing all non-healable failures, review the `ai_analysis` results and identify cases that likely belong to the **same bug**:

1. **Group similar failures** based on:
   - Same error message pattern
   - Same failed step or similar step names
   - Same feature area
   - Similar screenshot observations

2. **Assign bug_group_id** to related cases:
   ```json
   {
     "ai_analysis": {
       "is_likely_bug": true,
       "bug_group_id": "BUG-001",
       "bug_group_reason": "Same 'Search tabs' functionality failure across different tab modes",
       ...
     }
   }
   ```

3. **Create bug summary** in failure_info.json:
   ```json
   {
     "bug_summary": [
       {
         "bug_group_id": "BUG-001",
         "suggested_title": "[Edge] Search tabs not working in tab action menu",
         "affected_cases": ["case1", "case2", "case3"],
         "bug_category": "functional_bug",
         "confidence": 0.85
       }
     ]
   }
   ```

### 3. Categorize Failures

After AI analysis, categorize all failures:

**Element Change** (trigger self-healing):
- Error message contains element not found patterns
- `failure_analysis.is_healable = true`

**Likely Bug** (for ADO reporting):
- AI analysis determined `is_likely_bug = true`
- `bug_confidence >= 0.6`

**Other Failures** (manual investigation needed):
- Timeout errors, unknown errors, low confidence issues

### 3.1 Group Element Changes for PR Deduplication

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

### 4. Self-Healing Process (for element changes)

**Process by heal_group, NOT by individual case:**

For each **heal_group** (not each case):

#### 4.1 Create Git Branch (one per group)

```bash
git checkout -b fix/self-heal-<heal_group_id>-<timestamp>
```

#### 4.2 Execute Self-Healing Recording

Pick **ONE representative case** from the group and follow `.claude/commands/_recording-steps.md` with:
- `feature_file_path`: The representative case's feature file
- `scenario_name`: The representative case's scenario name
- `mode`: "heal"

#### 4.3 Verify ALL Cases in Group

After healing the representative case, run **ALL cases in the group** to verify the fix works for all:

```bash
uv run behave --name "^(case1|case2|case3)$" <feature_file>
```

#### 4.4 Handle Result

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

### 5. Create ADO Bugs (for likely bugs)

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

### 6. Generate HTML Report

Run the report generation script:

```bash
uv run scripts/generate_report.py
```

Output: `reports/failure_analysis.html`

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
