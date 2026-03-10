# Recording Steps (Shared)

This file contains the shared recording steps used by both `record-and-verify` and `analyze-failures` skills.

## Parameters

- `feature_file_path`: Path to the feature file
- `scenario_name`: Name of the scenario
- `mode`: "initial" (use COPILOT_PROMPT) or "heal" (use SELF_HEALING_PROMPT)
- `flag_file`: (Optional) Path to ChromeFeatureState file for Edge launch flags

## Steps

### 1. Extract Scenario Content

Parse the feature file and extract the complete scenario text including all steps:

```bash
uv run scripts/extract_scenario.py <feature_file_path> "<scenario_name>"
```

### 2. Build Recording Prompt

Read `bdd_ai_conf.json` and select prompt based on mode:
- `mode=initial`: Use `COPILOT_PROMPT`
- `mode=heal`: Use `SELF_HEALING_PROMPT`

Replace `${scenario_text}` and `${feature_file_path}` with actual values.

### 3. Execute MCP Recording

Execute the recording flow using MCP tools:

1. **Initialize recording session:**
   ```
   mcp__bdd-auto-mcp__before_gen_code(feature_file=<feature_file_path>, step_file=<step_file_path>)
   ```

2. **Launch application:**
   
   **Without flag file:**
   ```
   mcp__bdd-auto-mcp__app_launch(caller="recording", scenario=<scenario_name>)
   ```
   
   **With flag file (if `flag_file` parameter is provided):**
   First parse the flag file to get launch arguments:
   ```python
   from features.utils.flag_parser import parse_flag_file_to_arguments
   extra_args = parse_flag_file_to_arguments(flag_file)
   ```
   Then launch with arguments:
   ```
   mcp__bdd-auto-mcp__app_launch(caller="recording", scenario=<scenario_name>, arguments=["--no-first-run"] + extra_args)
   ```

3. **Execute each step in the scenario sequentially:**
   - Use `mcp__bdd-auto-mcp__get_page_source_tree` to discover current UI elements
   - Use appropriate action tools based on step type:
     - `mcp__bdd-auto-mcp__click_element` for click actions
     - `mcp__bdd-auto-mcp__send_keys` for text input
     - `mcp__bdd-auto-mcp__verify_element_exists` for verification
     - etc.
   - For element-not-found issues (heal mode), find the new locator from page source

4. **Preview generated code:**
   ```
   mcp__bdd-auto-mcp__preview_code_changes()
   ```

5. **Confirm and apply code changes:**
   ```
   mcp__bdd-auto-mcp__confirm_code_changes()
   ```

6. **Close application:**
   ```
   mcp__bdd-auto-mcp__app_close(caller="recording")
   ```

### 4. Playback Verification

Run the single case to verify recording result.

**Without flag file:**
```bash
uv run behave --name "^<scenario_name>$" <feature_file_path>
```

**With flag file (if `flag_file` parameter is provided):**
```bash
uv run behave -D flag_file=<flag_file> --name "^<scenario_name>$" <feature_file_path>
```

### 5. Return Result

- **Success**: Return list of modified files and verification result
- **Failure**: Return error message and details
