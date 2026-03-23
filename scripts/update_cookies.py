#!/usr/bin/env python3
"""
快速更新 cookies 工具
从浏览器复制的 cookies 字符串直接保存到配置文件
"""

import sys
import os
import json
import re
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

def parse_cookies_string(cookies_str: str) -> dict:
    """解析 cookies 字符串为字典"""
    cookies = {}
    
    # 尝试 JSON 格式
    try:
        data = json.loads(cookies_str)
        if isinstance(data, dict):
            return data
    except:
        pass
    
    # 解析 key=value; 格式
    # 先清理字符串
    cookies_str = cookies_str.strip()
    
    # 按分号分割，但注意 value 中可能包含分号
    pairs = re.split(r';\s*', cookies_str)
    
    for pair in pairs:
        pair = pair.strip()
        if not pair:
            continue
        
        # 找到第一个等号的位置
        if '=' in pair:
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # 清理可能的引号
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            cookies[key] = value
    
    return cookies


def validate_cookies(cookies: dict) -> tuple[bool, list]:
    """验证 cookies 是否有效"""
    required_fields = ['_m_h5_tk', '_m_h5_tk_enc']
    optional_fields = ['unb', 'havana_lgc2_77']
    
    missing_required = [f for f in required_fields if f not in cookies]
    missing_optional = [f for f in optional_fields if f not in cookies]
    
    is_valid = len(missing_required) == 0
    
    return is_valid, missing_required, missing_optional


def save_cookies(cookies: dict, filepath: str = None) -> bool:
    """保存 cookies 到文件"""
    if filepath is None:
        filepath = Path(__file__).parent.parent / 'data' / 'xianyu_cookies.json'
    
    filepath = Path(filepath)
    
    # 确保目录存在
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # 读取现有文件（如果有）
        existing_data = {}
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except:
                pass
        
        # 更新 cookies
        existing_data['cookies'] = cookies
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False


def main():
    print("=" * 60)
    print("🍪 XianyuBot 快速更新 Cookies 工具")
    print("=" * 60)
    print()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 从命令行参数获取
        cookies_str = ' '.join(sys.argv[1:])
    else:
        # 交互式输入
        print("请从浏览器复制 cookies 字符串，然后粘贴到这里：")
        print("（支持格式：key1=value1; key2=value2 或 JSON 格式）")
        print("输入完成后按 Ctrl+D (Linux/Mac) 或 Ctrl+Z + Enter (Windows) 结束")
        print("-" * 60)
        
        try:
            cookies_str = sys.stdin.read()
        except KeyboardInterrupt:
            print("\n\n已取消")
            return
    
    if not cookies_str.strip():
        print("❌ 未输入任何内容")
        return
    
    print("\n🔍 正在解析 cookies...")
    cookies = parse_cookies_string(cookies_str)
    
    if not cookies:
        print("❌ 未能解析出任何 cookies")
        return
    
    print(f"✅ 成功解析 {len(cookies)} 个 cookie 字段")
    print(f"   包含字段: {', '.join(list(cookies.keys())[:5])}{'...' if len(cookies) > 5 else ''}")
    
    # 验证 cookies
    print("\n🔐 验证 cookies...")
    is_valid, missing_required, missing_optional = validate_cookies(cookies)
    
    if missing_required:
        print(f"⚠️  缺少必需字段: {missing_required}")
        print("   这些字段是必需的，否则可能无法正常工作")
    else:
        print("✅ 必需字段检查通过")
    
    if missing_optional:
        print(f"⚠️  缺少可选字段: {missing_optional}")
        print("   建议包含 'unb' 或 'havana_lgc2_77' 以确保稳定性")
    
    # 保存
    print("\n💾 保存 cookies...")
    if save_cookies(cookies):
        print("✅ Cookies 更新成功！")
        print()
        print("📍 保存位置: data/xianyu_cookies.json")
        print()
        print("🚀 现在可以启动机器人了:")
        print("   python start_bot.py")
        print()
        
        if not is_valid:
            print("⚠️  警告: cookies 缺少必需字段，可能无法正常工作")
            print("   建议重新从浏览器获取完整的 cookies")
    else:
        print("❌ 保存失败")


if __name__ == "__main__":
    main()
