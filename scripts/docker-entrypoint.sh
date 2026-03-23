#!/bin/bash
# Docker 容器入口脚本

set -e

echo "========================================"
echo "🚀 XianyuBot Docker 启动脚本"
echo "========================================"

# 检查数据目录
if [ ! -d "/app/data" ]; then
    mkdir -p /app/data
fi

# 检查 cookies 文件
cookies_file="/app/data/xianyu_cookies.json"

if [ ! -f "$cookies_file" ]; then
    echo ""
    echo "⚠️  未找到 cookies 文件"
    echo ""
    echo "请通过以下方式之一提供 cookies："
    echo ""
    echo "方式1 - 挂载本地 cookies 文件:"
    echo "  docker run -v /本地路径/xianyu_cookies.json:/app/data/xianyu_cookies.json ..."
    echo ""
    echo "方式2 - 进入容器手动登录:"
    echo "  docker exec -it xianyubot bash"
    echo "  python run.py --login"
    echo ""
    echo "方式3 - 使用环境变量导入 cookies:"
    echo "  设置 XIANYU_COOKIES 环境变量"
    echo ""
    
    # 如果有环境变量，尝试写入
    if [ -n "$XIANYU_COOKIES" ]; then
        echo "📝 检测到 XIANYU_COOKIES 环境变量，正在写入文件..."
        echo "$XIANYU_COOKIES" > "$cookies_file"
        echo "✅ Cookies 已写入"
    else
        echo "❌ 无法启动：缺少 cookies"
        echo "请使用上述方式之一提供 cookies"
        exit 1
    fi
else
    echo "✅ 找到 cookies 文件"
    # 显示 cookies 信息（隐藏敏感内容）
    if command -v python &> /dev/null; then
        python -c "
import json
with open('$cookies_file', 'r') as f:
    cookies = json.load(f)
    print(f'📋 Cookies 包含 {len(cookies)} 个字段')
    for key in cookies.keys():
        print(f'   - {key}')
" 2>/dev/null || echo "📋 Cookies 文件存在"
    fi
fi

echo ""
echo "📊 检查数据库..."
if [ ! -f "/app/data/chat_history.db" ]; then
    echo "📝 数据库不存在，将在首次运行时自动创建"
else
    echo "✅ 数据库已存在"
fi

echo ""
echo "🔧 检查环境变量..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: OPENAI_API_KEY 未设置"
else
    echo "✅ OPENAI_API_KEY 已设置"
fi

if [ -z "$LLM_MODEL" ]; then
    export LLM_MODEL="qwen3-flash"
    echo "📝 使用默认模型: $LLM_MODEL"
else
    echo "✅ 模型: $LLM_MODEL"
fi

echo ""
echo "========================================"
echo "🎉 启动 XianyuBot..."
echo "========================================"
echo ""

# 执行传入的命令，或默认启动机器人
if [ $# -eq 0 ]; then
    exec python start_bot.py
else
    exec "$@"
fi
