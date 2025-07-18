#!/usr/bin/env python3
"""
Cross-platform BDD Project Formatter
Python (Ruff) + Feature files (reformat-gherkin)
"""

import subprocess
import sys
import os
from pathlib import Path


def run_format_command(cmd, description):
    """Run formatting command"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False


def main():
    """Main function"""
    project_root = Path(__file__).parent
    
    print("=" * 60)
    print("🎨 Cross-platform BDD Project Formatter")
    print("🐍 Ruff (Python) + 🥒 reformat-gherkin (Feature)")
    print("=" * 60)
    
    # Change to project directory
    import os
    os.chdir(project_root)
    
    # Count files
    python_files = list(Path(".").rglob("features/**/*.py"))
    feature_files = list(Path(".").rglob("features/**/*.feature"))
    
    print(f"📊 Found {len(python_files)} Python files, {len(feature_files)} Feature files")
    print()
    
    # Format Python files
    success1 = run_format_command(
        "uv run ruff format features/",
        "Formatting Python files"
    )
    
    print()
    
    # Format Feature files
    success2 = run_format_command(
        "uv run reformat-gherkin features/",
        "Formatting Feature files"
    )
    
    print("\n" + "=" * 60)
    
    if success1 and success2:
        print("🎉 All files formatted successfully!")
    else:
        print("⚠️  Some files failed to format, please check error messages")


if __name__ == '__main__':
    main()
