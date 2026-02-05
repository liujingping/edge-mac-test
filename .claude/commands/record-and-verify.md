# Record and Verify

Record BDD scenario(s) and run playback verification. Can be used for initial code generation or self-healing re-recording.

## Usage

```
/record-and-verify <feature_file_path> [scenario_name] [--heal]
```

## Parameters

- `feature_file_path`: Path to the feature file, e.g., `features/settings/settings.feature`
- `scenario_name`: (Optional) Name of the scenario, e.g., `Search in settings search box`
  - If provided: Record only this scenario
  - If omitted: Record ALL scenarios in the feature file
- `--heal`: Optional flag indicating this is a self-healing recording (uses SELF_HEALING_PROMPT)

## Execution Steps

### Single Scenario Mode

When `scenario_name` is provided:

Follow the steps defined in `.claude/commands/_recording-steps.md` with:
- `feature_file_path`: The provided feature file path
- `scenario_name`: The provided scenario name
- `mode`: "initial" (default) or "heal" (if --heal flag is provided)

### Batch Mode (All Scenarios)

When `scenario_name` is omitted:

#### 1. Extract All Scenarios

Parse the feature file to get list of all scenario names:

```bash
uv run scripts/extract_scenario.py <feature_file_path> --list
```

#### 2. Initialize Results Tracking

Create a results dict to track progress:
```json
{
  "feature_file": "<feature_file_path>",
  "total_scenarios": 0,
  "completed": [],
  "failed": [],
  "started_at": "<timestamp>"
}
```

#### 3. Process Each Scenario Sequentially

⚠️ **Process ONE scenario at a time:**

For each scenario in the list:
1. Follow `.claude/commands/_recording-steps.md` with:
   - `feature_file_path`: The feature file path
   - `scenario_name`: Current scenario name
   - `mode`: "initial" or "heal"

2. Update results based on outcome:
   - **Success**: Add to `completed` list
   - **Failure**: Add to `failed` list with error details:
     ```json
     {
       "scenario_name": "<name>",
       "error": "<error message>",
       "failed_step": "<step that failed>"
     }
     ```

3. **Save results to file after EACH scenario**:
   ```bash
   # Save to reports/record_verify_results.json
   ```

4. Move to next scenario

#### 4. Generate Summary Report

After all scenarios are processed:

```json
{
  "feature_file": "features/settings/settings.feature",
  "total_scenarios": 10,
  "completed": [
    {"scenario_name": "Search in settings", "duration": "45s"},
    {"scenario_name": "Open profile settings", "duration": "32s"}
  ],
  "failed": [
    {
      "scenario_name": "Change language",
      "error": "Element 'Language selector' not found",
      "failed_step": "When I click on language selector"
    }
  ],
  "success_rate": "80%",
  "started_at": "2024-01-15T10:00:00",
  "finished_at": "2024-01-15T10:15:00"
}
```

Save to: `reports/record_verify_results.json`

#### 5. Display Summary

Print summary to console:

```
========================================
Record & Verify Summary
========================================
Feature: features/settings/settings.feature
Total: 10 | Completed: 8 | Failed: 2
Success Rate: 80%

Completed:
  ✓ Search in settings (45s)
  ✓ Open profile settings (32s)
  ...

Failed:
  ✗ Change language
    Error: Element 'Language selector' not found
    Step: When I click on language selector
  ...
========================================
```

## Example

```
# Single scenario
/record-and-verify features/settings/settings.feature "Search in settings search box"

# Single scenario with heal mode
/record-and-verify features/settings/settings.feature "Search in settings search box" --heal

# All scenarios in feature file
/record-and-verify features/settings/settings.feature

# All scenarios with heal mode
/record-and-verify features/settings/settings.feature --heal
```

## Output

- Single mode: Verification result for the scenario
- Batch mode: `reports/record_verify_results.json` with full summary

## Notes

1. Ensure Edge browser is not running or in a clean state before recording
2. Do not manually operate the browser during recording
3. If verification fails, check `reports/behave_result.json` for detailed error information
4. All Python commands use `uv run`
5. In batch mode, failures don't stop the process - all scenarios will be attempted
6. Results are saved after each scenario to prevent data loss
