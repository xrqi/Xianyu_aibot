@echo off
chcp 65001 >nul
echo ========================================
echo 🍪 XianyuBot 快速更新 Cookies
echo ========================================
echo.

if "%~1"=="" (
    echo 使用方法:
    echo   update_cookies.bat "你的cookies字符串"
    echo.
    echo 示例:
    echo   update_cookies.bat "_m_h5_tk=xxx; _m_h5_tk_enc=yyy; unb=zzz"
    echo.
    echo 或者运行 Python 脚本进行交互式输入:
    echo   python scripts\update_cookies.py
    echo.
    pause
    exit /b 1
)

set COOKIES_STR=%~1

:: 创建 data 目录
if not exist "data" mkdir data

:: 使用 Python 处理
python -c "
import json
import re
import sys

cookies_str = r'''%COOKIES_STR%'''

# 解析 cookies
cookies = {}
pairs = re.split(r';\s*', cookies_str)

for pair in pairs:
    pair = pair.strip()
    if not pair or '=' not in pair:
        continue
    key, value = pair.split('=', 1)
    key = key.strip()
    value = value.strip().strip('\"').strip(\"'\")
    if key:
        cookies[key] = value

if not cookies:
    print('❌ 未能解析出任何 cookies')
    sys.exit(1)

print(f'✅ 成功解析 {len(cookies)} 个 cookie 字段')

# 检查关键字段
required = ['_m_h5_tk', '_m_h5_tk_enc']
optional = ['unb', 'havana_lgc2_77']

missing_required = [f for f in required if f not in cookies]
missing_optional = [f for f in optional if f not in cookies]

if missing_required:
    print(f'⚠️  缺少必需字段: {missing_required}')
else:
    print('✅ 必需字段检查通过')

if missing_optional:
    print(f'⚠️  缺少可选字段: {missing_optional}')

# 保存
data = {'cookies': cookies}
with open('data/xianyu_cookies.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('')
print('✅ Cookies 更新成功！')
print('📍 保存位置: data/xianyu_cookies.json')
print('')
print('🚀 现在可以启动机器人了:')
print('   python start_bot.py')
"

if errorlevel 1 (
    echo ❌ 更新失败
    pause
    exit /b 1
)

echo.
pause
