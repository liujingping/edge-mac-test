#!/usr/bin/env python3
"""
Compress screenshots to reduce file size for AI analysis.
"""

import sys
from pathlib import Path
from PIL import Image

MAX_WIDTH = 1440
MAX_HEIGHT = 1080
QUALITY = 80
SIZE_THRESHOLD = 500 * 1024


def compress_image(image_path: str, output_path: str = None) -> dict:
    """Compress a single image."""
    path = Path(image_path)
    if not path.exists():
        return {"success": False, "error": f"File not found: {image_path}"}
    
    if output_path is None:
        output_path = image_path
    
    try:
        original_size = path.stat().st_size
        
        if original_size <= SIZE_THRESHOLD:
            return {
                "success": True,
                "skipped": True,
                "original_size": original_size,
                "reason": "Already small enough"
            }
        
        with Image.open(path) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            width, height = img.size
            if width > MAX_WIDTH or height > MAX_HEIGHT:
                ratio = min(MAX_WIDTH / width, MAX_HEIGHT / height)
                new_size = (int(width * ratio), int(height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            
            img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
        
        new_size = Path(output_path).stat().st_size
        reduction = (1 - new_size / original_size) * 100
        
        return {
            "success": True,
            "original_size": original_size,
            "new_size": new_size,
            "reduction": f"{reduction:.1f}%"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def compress_directory(dir_path: str) -> list[dict]:
    """Compress all images in a directory."""
    path = Path(dir_path)
    if not path.exists():
        return [{"success": False, "error": f"Directory not found: {dir_path}"}]
    
    results = []
    for img_path in path.glob("*.png"):
        result = compress_image(str(img_path))
        result["file"] = img_path.name
        results.append(result)
        if result.get("skipped"):
            print(f"Skipped: {img_path.name} (already small: {result['original_size']} bytes)")
        elif result["success"]:
            print(f"Compressed: {img_path.name} ({result['reduction']} reduction)")
        else:
            print(f"Failed: {img_path.name} - {result.get('error')}")
    
    for img_path in path.glob("*.PNG"):
        result = compress_image(str(img_path))
        result["file"] = img_path.name
        results.append(result)
        if result.get("skipped"):
            print(f"Skipped: {img_path.name} (already small: {result['original_size']} bytes)")
        elif result["success"]:
            print(f"Compressed: {img_path.name} ({result['reduction']} reduction)")
        else:
            print(f"Failed: {img_path.name} - {result.get('error')}")
    
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python compress_screenshots.py <image_path>")
        print("  python compress_screenshots.py <directory_path>")
        print("")
        print("Examples:")
        print("  python compress_screenshots.py screenshots/test.png")
        print("  python compress_screenshots.py screenshots/")
        sys.exit(1)
    
    target = sys.argv[1]
    path = Path(target)
    
    if path.is_file():
        result = compress_image(target)
        if result["success"]:
            print(f"Compressed: {path.name}")
            print(f"  Original: {result['original_size']} bytes")
            print(f"  New: {result['new_size']} bytes")
            print(f"  Reduction: {result['reduction']}")
        else:
            print(f"Failed: {result.get('error')}")
            sys.exit(1)
    elif path.is_dir():
        results = compress_directory(target)
        success = sum(1 for r in results if r["success"])
        print(f"\nTotal: {success}/{len(results)} images compressed")
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
