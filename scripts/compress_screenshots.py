#!/usr/bin/env python3
"""
Compress screenshots for AI overview analysis.
Outputs compressed copies to screenshots_compressed/ alongside the original screenshots/ directory.
Original files are preserved for high-detail ROI cropping.
"""

import sys
from pathlib import Path
from PIL import Image

MAX_WIDTH = 1920
MAX_HEIGHT = 1440
TARGET_SIZE = 120 * 1024
QUALITY_START = 80
QUALITY_MIN = 20
QUALITY_STEP = 10


def compress_image(image_path: str, output_path: str) -> dict:
    path = Path(image_path)
    if not path.exists():
        return {"success": False, "error": f"File not found: {image_path}"}

    try:
        original_size = path.stat().st_size

        with Image.open(path) as img:
            width, height = img.size

            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            needs_resize = width > MAX_WIDTH or height > MAX_HEIGHT
            if needs_resize:
                ratio = min(MAX_WIDTH / width, MAX_HEIGHT / height)
                new_dims = (int(width * ratio), int(height * ratio))
                img = img.resize(new_dims, Image.LANCZOS)

            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)

            quality = QUALITY_START
            while quality >= QUALITY_MIN:
                img.save(str(out), 'JPEG', quality=quality, optimize=True)
                if out.stat().st_size <= TARGET_SIZE:
                    break
                quality -= QUALITY_STEP

        new_size = Path(output_path).stat().st_size
        reduction = (1 - new_size / original_size) * 100

        return {
            "success": True,
            "original_size": original_size,
            "new_size": new_size,
            "reduction": f"{reduction:.1f}%",
            "quality": quality,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def compress_directory(dir_path: str) -> list[dict]:
    path = Path(dir_path)
    if not path.exists():
        return [{"success": False, "error": f"Directory not found: {dir_path}"}]

    out_dir = path.parent / "screenshots_compressed"
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    skipped = 0
    for img_path in sorted(set(path.glob("*.png")) | set(path.glob("*.PNG"))):
        out_path = out_dir / (img_path.stem + ".jpg")
        if out_path.exists():
            skipped += 1
            continue
        result = compress_image(str(img_path), str(out_path))
        result["file"] = img_path.name
        results.append(result)
        if result["success"]:
            print(f"Compressed: {img_path.name} ({result['reduction']} reduction)")
        else:
            print(f"Failed: {img_path.name} - {result.get('error')}")

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python compress_screenshots.py <directory_path>")
        print("")
        print("Outputs compressed images to <directory_path>/../screenshots_compressed/")
        print("Original files are preserved.")
        sys.exit(1)

    target = sys.argv[1]
    path = Path(target)

    if path.is_dir():
        results = compress_directory(target)
        success = sum(1 for r in results if r["success"])
        out_dir = path.parent / "screenshots_compressed"
        total_png = len(list(set(path.glob("*.png")) | set(path.glob("*.PNG"))))
        skipped = total_png - len(results)
        if skipped > 0:
            print(f"Skipped: {skipped} already compressed")
        print(f"Compressed: {success}/{len(results)} new images")
        print(f"Output: {out_dir}")
    else:
        print(f"Error: {target} is not a valid directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
