#!/bin/bash
# XianyuBot Docker 启动脚本（带 cookies 处理）

set -e

COOKIES_FILE="./data/xianyu_cookies.json"
ENV_FILE="./.env"

echo "========================================"
echo "🚀 XianyuBot Docker 启动向导"
echo "========================================"

# 检查 .env 文件
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ 错误: .env 文件不存在"
    echo "请复制 .env.example 并配置:"
    echo "  cp .env.example .env"
    exit 1
fi

# 检查 cookies 文件
check_cookies() {
    if [ ! -f "$COOKIES_FILE" ]; then
        return 1
    fi
    
    # 检查文件是否为空
    if [ ! -s "$COOKIES_FILE" ]; then
        return 1
    fi
    
    return 0
}

# 方式1: 已有 cookies
if check_cookies; then
    echo "✅ 检测到 cookies 文件"
    echo "📋 文件大小: $(ls -lh $COOKIES_FILE | awk '{print $5}')"
    
    # 显示 cookies 内容摘要
    if command -v python &> /dev/null; then
        python -c "
import json
try:
    with open('$COOKIES_FILE', 'r') as f:
        cookies = json.load(f)
        print(f'📋 Cookies 包含 {len(cookies)} 个字段:')
        for key in list(cookies.keys())[:5]:
            value = cookies[key]
            preview = str(value)[:30] + '...' if len(str(value)) > 30 else str(value)
            print(f'   - {key}: {preview}')
        if len(cookies) > 5:
            print(f'   ... 还有 {len(cookies) - 5} 个字段')
except Exception as e:
    print(f'⚠️  读取 cookies 失败: {e}')
"
    fi
    
    echo ""
    read -p "是否使用此 cookies 启动? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "请更新 cookies 文件后重试"
        exit 1
    fi
else
    echo "⚠️  未找到 cookies 文件"
    echo ""
    echo "请选择导入方式:"
    echo "1) 从浏览器复制 cookies 字符串"
    echo "2) 从文件导入"
    echo "3) 进入容器手动登录（需要图形界面）"
    echo "4) 退出"
    echo ""
    read -p "选择 (1-4): " choice
    
    case $choice in
        1)
            echo ""
            echo "请粘贴 cookies 字符串（JSON格式），按 Ctrl+D 结束:"
            cat > "$COOKIES_FILE"
            echo "✅ Cookies 已保存"
            ;;
        2)
            read -p "请输入 cookies 文件路径: " cookies_path
            if [ -f "$cookies_path" ]; then
                cp "$cookies_path" "$COOKIES_FILE"
                echo "✅ Cookies 已复制"
            else
                echo "❌ 文件不存在"
                exit 1
            fi
            ;;
        3)
            echo "将启动容器并进入交互式登录模式..."
            echo "注意: 此方式需要服务器有图形界面或 X11 转发"
            docker-compose run --rm xianyubot python run.py --login
            exit 0
            ;;
        4)
            echo "已退出"
            exit 0
            ;;
        *)
            echo "无效选择"
            exit 1
            ;;
    esac
fi

# 检查 cookies 有效性
echo ""
echo "🔍 检查 cookies 有效性..."
if command -v python &> /dev/null; then
    python -c "
import json
import sys

try:
    with open('$COOKIES_FILE', 'r') as f:
        cookies = json.load(f)
    
    # 检查关键字段
    required_fields = ['_m_h5_tk', '_m_h5_tk_enc']
    optional_fields = ['unb', 'havana_lgc2_77']
    
    missing_required = [f for f in required_fields if f not in cookies]
    missing_optional = [f for f in optional_fields if f not in cookies]
    
    if missing_required:
        print(f'⚠️  缺少关键字段: {missing_required}')
        print('   这些字段是必需的，否则可能无法正常工作')
        sys.exit(1)
    else:
        print('✅ 关键字段检查通过')
    
    if missing_optional:
        print(f'⚠️  缺少可选字段: {missing_optional}')
        print('   这些字段有助于提高稳定性')
    
    print('✅ Cookies 格式有效')
    
except json.JSONDecodeError as e:
    print(f'❌ JSON 格式错误: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ 检查失败: {e}')
    sys.exit(1)
" || {
    echo "⚠️  无法验证 cookies，将继续启动..."
}
fi

# 启动 Docker
echo ""
echo "🚀 启动 Docker 容器..."
docker-compose up -d

echo ""
echo "========================================"
echo "✅ XianyuBot 已启动"
echo "========================================"
echo ""
echo "📊 查看状态:"
echo "  docker-compose ps"
echo ""
echo "📜 查看日志:"
echo "  docker-compose logs -f"
echo ""
echo "🌐 Web 反馈后台:"
echo "  http://localhost:5000"
echo ""
echo "🔧 进入容器:"
echo "  docker-compose exec xianyubot bash"
echo ""
echo "⏹️  停止服务:"
echo "  docker-compose down"
echo ""
