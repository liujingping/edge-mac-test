#!/usr/bin/env python3
"""
Extract scenario content from a feature file.

This script parses a Gherkin feature file and extracts the complete text
of a specific scenario including all its steps.
"""

import sys
from pathlib import Path
from typing import Optional


def parse_feature_file(feature_path: str) -> list[dict]:
    """Parse a feature file and extract all scenarios."""
    path = Path(feature_path)
    if not path.exists():
        raise FileNotFoundError(f"Feature file not found: {feature_path}")
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    scenarios = []
    lines = content.split("\n")
    
    current_scenario = None
    in_scenario = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped.startswith("Scenario:") or stripped.startswith("Scenario Outline:"):
            if current_scenario:
                scenarios.append(current_scenario)
            
            scenario_type = "Scenario Outline" if "Outline" in stripped else "Scenario"
            name = stripped.split(":", 1)[1].strip()
            current_scenario = {
                "name": name,
                "type": scenario_type,
                "line_number": i + 1,
                "tags": [],
                "steps": [],
                "raw_text": line
            }
            in_scenario = True
            
            for j in range(i - 1, -1, -1):
                prev_line = lines[j].strip()
                if prev_line.startswith("@"):
                    current_scenario["tags"] = prev_line.split() + current_scenario["tags"]
                elif prev_line:
                    break
        
        elif in_scenario and current_scenario:
            if stripped.startswith(("Given ", "When ", "Then ", "And ", "But ")):
                current_scenario["steps"].append(line)
                current_scenario["raw_text"] += "\n" + line
            elif stripped.startswith("Examples:"):
                current_scenario["raw_text"] += "\n" + line
            elif stripped.startswith("|"):
                current_scenario["raw_text"] += "\n" + line
            elif stripped.startswith("\"\"\"") or (current_scenario.get("in_docstring", False)):
                current_scenario["raw_text"] += "\n" + line
                current_scenario["in_docstring"] = not current_scenario.get("in_docstring", False)
            elif stripped.startswith("Scenario:") or stripped.startswith("Scenario Outline:"):
                pass
            elif stripped.startswith("Feature:") or stripped.startswith("Background:"):
                in_scenario = False
            elif stripped.startswith("@"):
                in_scenario = False
            elif stripped == "":
                next_non_empty = None
                for k in range(i + 1, len(lines)):
                    if lines[k].strip():
                        next_non_empty = lines[k].strip()
                        break
                if next_non_empty and (
                    next_non_empty.startswith("Scenario") or 
                    next_non_empty.startswith("@") or
                    next_non_empty.startswith("Feature")
                ):
                    in_scenario = False
    
    if current_scenario:
        scenarios.append(current_scenario)
    
    for scenario in scenarios:
        scenario.pop("in_docstring", None)
    
    return scenarios


def find_scenario_by_name(feature_path: str, scenario_name: str) -> Optional[dict]:
    """Find a specific scenario by name."""
    scenarios = parse_feature_file(feature_path)
    
    for scenario in scenarios:
        if scenario["name"] == scenario_name:
            return scenario
    
    for scenario in scenarios:
        if scenario_name.lower() in scenario["name"].lower():
            return scenario
    
    return None


def get_scenario_text(feature_path: str, scenario_name: str) -> Optional[str]:
    """Get the complete text of a scenario for use in prompts."""
    scenario = find_scenario_by_name(feature_path, scenario_name)
    if not scenario:
        return None
    
    text_parts = []
    
    if scenario["tags"]:
        text_parts.append(" ".join(scenario["tags"]))
    
    text_parts.append(f"{scenario['type']}: {scenario['name']}")
    
    for step in scenario["steps"]:
        text_parts.append(step)
    
    return "\n".join(text_parts)


def get_step_file_path(feature_path: str) -> str:
    """Determine the corresponding step file path from feature file path."""
    path = Path(feature_path)
    
    parts = list(path.parts)
    try:
        features_idx = parts.index("features")
    except ValueError:
        return ""
    
    relative_parts = parts[features_idx + 1:]
    
    if relative_parts:
        relative_parts[-1] = relative_parts[-1].replace(".feature", ".py")
    
    step_path = Path(parts[0]) if parts[0] == "/" else Path()
    for part in parts[1:features_idx + 1]:
        step_path = step_path / part
    step_path = step_path / "steps"
    for part in relative_parts:
        step_path = step_path / part
    
    return str(step_path)


def list_scenarios(feature_path: str) -> list[str]:
    """List all scenario names in a feature file."""
    scenarios = parse_feature_file(feature_path)
    return [s["name"] for s in scenarios]


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python extract_scenario.py <feature_file_path> <scenario_name>")
        print("  python extract_scenario.py <feature_file_path> --list")
        print("")
        print("Examples:")
        print("  python extract_scenario.py features/settings/settings.feature 'Search in settings'")
        print("  python extract_scenario.py features/settings/settings.feature --list")
        sys.exit(1)
    
    feature_path = sys.argv[1]
    
    if len(sys.argv) == 2 or sys.argv[2] == "--list":
        try:
            scenarios = list_scenarios(feature_path)
            for name in scenarios:
                print(name)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        scenario_name = sys.argv[2]
        try:
            scenario_text = get_scenario_text(feature_path, scenario_name)
            if scenario_text:
                print(scenario_text)
            else:
                print(f"Error: Scenario '{scenario_name}' not found in {feature_path}", file=sys.stderr)
                sys.exit(1)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
