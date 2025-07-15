# features/steps/__init__.py
import os
import pathlib
import importlib.util
import traceback
import sys

# Flag to prevent duplicate imports
_steps_imported = False

def auto_import_steps():
    global _steps_imported
    
    # If already imported, return directly
    if _steps_imported:
        return
    
    print("[auto-import] Starting auto-import of step modules...")
    steps_dir = pathlib.Path(__file__).parent
    base_dir = steps_dir.parent 

    imported_count = 0
    current_file = pathlib.Path(__file__)
    
    for py_file in steps_dir.rglob("*.py"):
        if py_file.name == "__init__.py" or py_file.samefile(current_file):
            continue

        try:
            rel_path = py_file.relative_to(base_dir)
            module_name = ".".join(rel_path.with_suffix("").parts)

            # Check if module is already in sys.modules
            if module_name in sys.modules:
                continue

            print(f"[auto-import] Loading module: {module_name}")
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Add module to sys.modules
            sys.modules[module_name] = module
            imported_count += 1

        except Exception as e:
            print(f"[auto-import] Failed to import {py_file}: {e}")
            traceback.print_exc()
    
    _steps_imported = True

# Execute only on first import
auto_import_steps()