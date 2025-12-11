#!/usr/bin/env python3
"""
比较两个 Edge 特性标志文件的 enable-features 差异
"""

import json
import sys
from pathlib import Path
from typing import Set, Tuple


def load_flag_file(file_path: str) -> dict:
    """加载特性标志 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: 文件 '{file_path}' 不是有效的 JSON 格式: {e}")
        sys.exit(1)


def parse_features(enable_features_str: str) -> Set[str]:
    """
    解析 enable-features 字符串，提取完整特性定义
    
    格式示例: "ImmersiveFullscreen<EdgeImmersiveFullscreen,eefrc<EmptyEdgeFirstRunConfig"
    返回: {"ImmersiveFullscreen<EdgeImmersiveFullscreen", "eefrc<EmptyEdgeFirstRunConfig", ...}
    """
    if not enable_features_str:
        return set()
    
    features = set()
    # 用逗号分割
    items = enable_features_str.split(',')
    
    for item in items:
        item = item.strip()
        if not item:
            continue
        
        # 替换 Unicode 转义的 < 符号为实际的 <
        item = item.replace('\u003C', '<')
        
        if item:
            features.add(item)
    
    return features


def compare_features(file_a: str, file_b: str) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    比较两个文件的 enable-features
    
    返回: (A独有, B独有, 共同拥有)
    """
    data_a = load_flag_file(file_a)
    data_b = load_flag_file(file_b)
    
    features_a = parse_features(data_a.get('enable-features', ''))
    features_b = parse_features(data_b.get('enable-features', ''))
    
    only_in_a = features_a - features_b
    only_in_b = features_b - features_a
    common = features_a & features_b
    
    return only_in_a, only_in_b, common


def print_results(file_a: str, file_b: str, only_in_a: Set[str], only_in_b: Set[str], common: Set[str]):
    """打印比较结果"""
    print("=" * 80)
    print(f"特性标志比较结果")
    print("=" * 80)
    print(f"文件 A: {file_a}")
    print(f"文件 B: {file_b}")
    print("=" * 80)
    
    print(f"\n📊 统计:")
    print(f"  - A 文件共有 {len(only_in_a) + len(common)} 个特性")
    print(f"  - B 文件共有 {len(only_in_b) + len(common)} 个特性")
    print(f"  - 共同特性: {len(common)} 个")
    print(f"  - A 独有特性: {len(only_in_a)} 个")
    print(f"  - B 独有特性: {len(only_in_b)} 个")
    
    if only_in_a:
        print(f"\n✅ A 文件有但 B 文件没有的特性 ({len(only_in_a)} 个):")
        print("-" * 80)
        for feature in sorted(only_in_a):
            print(f"  • {feature}")
    else:
        print(f"\n✅ A 文件有但 B 文件没有的特性: 无")
    
    if only_in_b:
        print(f"\n✅ B 文件有但 A 文件没有的特性 ({len(only_in_b)} 个):")
        print("-" * 80)
        for feature in sorted(only_in_b):
            print(f"  • {feature}")
    else:
        print(f"\n✅ B 文件有但 A 文件没有的特性: 无")
    
    if common:
        print(f"\n🔄 共同特性 ({len(common)} 个):")
        print("-" * 80)
        for feature in sorted(common):
            print(f"  • {feature}")
    
    print("\n" + "=" * 80)


def main():
    """主函数"""
    if len(sys.argv) != 3:
        print("用法: python compare_features.py <文件A路径> <文件B路径>")
        print("\n示例:")
        print("  python compare_features.py test_flag_1.json test_flag_2.json")
        sys.exit(1)
    
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    
    # 检查文件是否存在
    if not Path(file_a).exists():
        print(f"错误: 文件 '{file_a}' 不存在")
        sys.exit(1)
    
    if not Path(file_b).exists():
        print(f"错误: 文件 '{file_b}' 不存在")
        sys.exit(1)
    
    # 比较特性
    only_in_a, only_in_b, common = compare_features(file_a, file_b)
    
    # 打印结果
    print_results(file_a, file_b, only_in_a, only_in_b, common)


if __name__ == "__main__":
    main()
