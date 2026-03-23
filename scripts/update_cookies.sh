#!/bin/bash
# 快速更新 cookies 脚本

COOKIES_FILE="./data/xianyu_cookies.json"

echo "========================================"
echo "🍪 XianyuBot 快速更新 Cookies"
echo "========================================"
echo ""

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  ./update_cookies.sh '你的cookies字符串'"
    echo ""
    echo "示例:"
    echo "  ./update_cookies.sh '_m_h5_tk=xxx; _m_h5_tk_enc=yyy; unb=zzz'"
    echo ""
    echo "或者交互式输入:"
    echo "  ./update_cookies.sh"
    echo "  然后粘贴 cookies，按 Ctrl+D 结束"
    echo ""
    
    echo "请粘贴 cookies 字符串:"
    COOKIES_STR=$(cat)
else
    COOKIES_STR="$1"
fi

if [ -z "$COOKIES_STR" ]; then
    echo "❌ 错误: 未提供 cookies"
    exit 1
fi

# 创建 data 目录
mkdir -p ./data

# 使用 Python 脚本处理
python3 << EOF
import json
import re
import sys

cookies_str = '''$COOKIES_STR'''

# 解析 cookies
cookies = {}
pairs = re.split(r';\s*', cookies_str)

for pair in pairs:
    pair = pair.strip()
    if not pair or '=' not in pair:
        continue
    key, value = pair.split('=', 1)
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    if key:
        cookies[key] = value

if not cookies:
    print("❌ 未能解析出任何 cookies")
    sys.exit(1)

print(f"✅ 成功解析 {len(cookies)} 个 cookie 字段")

# 检查关键字段
required = ['_m_h5_tk', '_m_h5_tk_enc']
optional = ['unb', 'havana_lgc2_77']

missing_required = [f for f in required if f not in cookies]
missing_optional = [f for f in optional if f not in cookies]

if missing_required:
    print(f"⚠️  缺少必需字段: {missing_required}")
else:
    print("✅ 必需字段检查通过")

if missing_optional:
    print(f"⚠️  缺少可选字段: {missing_optional}")

# 保存
data = {"cookies": cookies}
with open('$COOKIES_FILE', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("")
print("✅ Cookies 更新成功！")
print("📍 保存位置: $COOKIES_FILE")
print("")
print("🚀 现在可以启动机器人了:")
print("   python start_bot.py")
EOF
