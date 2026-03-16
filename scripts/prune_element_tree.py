#!/usr/bin/env python3
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def is_meaningless_group(elem):
    return (
        "Group" in elem.tag
        and not elem.get("label", "")
        and not elem.get("title", "")
        and not elem.get("identifier", "")
        and not elem.get("value", "")
    )


def prune(root):
    def remove_hidden(elem):
        for c in [c for c in list(elem) if c.get("width") == "0" and c.get("height") == "0"]:
            elem.remove(c)
        for c in list(elem):
            remove_hidden(c)

    remove_hidden(root)

    keep = ("label", "title", "identifier", "value", "enabled", "selected", "x", "y", "width", "height")
    for elem in root.iter():
        for k in [k for k in elem.attrib if k not in keep]:
            del elem.attrib[k]
        for k in ("label", "title", "identifier", "value"):
            if elem.get(k, "") == "" and k in elem.attrib:
                del elem.attrib[k]
        if elem.get("enabled") == "true" and "enabled" in elem.attrib:
            del elem.attrib["enabled"]
        if elem.get("selected") == "false" and "selected" in elem.attrib:
            del elem.attrib["selected"]

    changed = True
    while changed:
        changed = False
        for parent in list(root.iter()):
            for i, child in enumerate(list(parent)):
                if is_meaningless_group(child) and len(list(child)) == 1:
                    gc = list(child)[0]
                    parent.remove(child)
                    parent.insert(i, gc)
                    changed = True
                elif is_meaningless_group(child) and len(list(child)) == 0:
                    parent.remove(child)
                    changed = True

    for elem in root.iter():
        elem.tag = elem.tag.replace("XCUIElementType", "")

    return root


def compact_format(elem, depth=0):
    lines = []
    tag = elem.tag
    parts = []
    for attr in ("label", "title", "identifier", "value"):
        v = elem.get(attr, "")
        if v:
            parts.append(attr + '="' + v + '"')
    if elem.get("enabled") == "false":
        parts.append("enabled=false")
    if elem.get("selected") == "true":
        parts.append("selected=true")
    x = elem.get("x", "")
    if x:
        parts.append(
            "@("
            + ",".join([elem.get("x"), elem.get("y"), elem.get("width"), elem.get("height")])
            + ")"
        )
    indent = "  " * depth
    attr_str = " ".join(parts)
    children = list(elem)
    child_lines = []
    for c in children:
        child_lines.extend(compact_format(c, depth + 1))
    if child_lines:
        lines.append(indent + "<" + tag + " " + attr_str + ">")
        lines.extend(child_lines)
        lines.append(indent + "</" + tag + ">")
    else:
        lines.append(indent + "<" + tag + " " + attr_str + "/>")
    return lines


def process_file(input_path, output_path):
    with open(input_path) as f:
        data = json.load(f)

    page_source = data.get("result", {}).get("data", {}).get("page_source", "")
    if not page_source:
        return {"success": False, "error": "No page_source found"}

    orig_size = len(page_source)
    root = ET.fromstring(page_source)
    root = prune(root)
    result = "\n".join(compact_format(root))

    out = {
        "tool_name": data.get("tool_name", ""),
        "parameters": data.get("parameters", {}),
        "error": data.get("result", {}).get("error", ""),
        "page_source_pruned": result,
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    final_size = len(result)
    return {
        "success": True,
        "original_chars": orig_size,
        "pruned_chars": final_size,
        "reduction": f"{(1 - final_size / orig_size) * 100:.1f}%",
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: prune_element_tree.py <error_results_dir>")
        print("  Prunes all error_result_*.json files in the directory.")
        print("  Output: <data_dir>/logs/error_results_pruned/")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    if not input_dir.exists():
        print(f"Directory not found: {input_dir}")
        sys.exit(1)

    output_dir = input_dir.parent / "error_results_pruned"
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("error_result_*.json"))
    if not files:
        print(f"No error_result_*.json files found in {input_dir}")
        sys.exit(1)

    print(f"Processing {len(files)} files...")
    for fp in files:
        out_fp = output_dir / fp.name
        result = process_file(str(fp), str(out_fp))
        if result["success"]:
            print(
                f"  {fp.name[:60]:<60} {result['original_chars']:>8} -> {result['pruned_chars']:>6} ({result['reduction']})"
            )
        else:
            print(f"  {fp.name[:60]:<60} FAILED: {result['error']}")

    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()
