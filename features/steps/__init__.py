# features/steps/__init__.py
import os
import pathlib
import importlib.util
import traceback
import sys

# 防止重复导入的标志
_steps_imported = False

def auto_import_steps():
    global _steps_imported
    
    # 如果已经导入过，直接返回
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

            # 检查模块是否已经在 sys.modules 中
            if module_name in sys.modules:
                continue

            print(f"[auto-import] Loading module: {module_name}")
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 将模块添加到 sys.modules 中
            sys.modules[module_name] = module
            imported_count += 1

        except Exception as e:
            print(f"[auto-import] Failed to import {py_file}: {e}")
            traceback.print_exc()
    
    _steps_imported = True

# 只在第一次导入时执行
auto_import_steps()