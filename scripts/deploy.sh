#!/bin/bash
# XianyuBot Docker 部署脚本

set -e

echo "========================================"
echo "🚀 XianyuBot Docker 部署脚本"
echo "========================================"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，从 .env.example 复制"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ 已创建 .env 文件，请编辑并填入你的配置"
        echo "   必须配置: OPENAI_API_KEY"
        exit 1
    else
        echo "❌ .env.example 也不存在"
        exit 1
    fi
fi

# 检查 API Key
if grep -q "your_api_key_here" .env; then
    echo "❌ 请先在 .env 文件中设置 OPENAI_API_KEY"
    exit 1
fi

echo ""
echo "📦 构建 Docker 镜像..."
docker-compose build

echo ""
echo "🚀 启动服务..."
docker-compose up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "========================================"
    echo "✅ XianyuBot 部署成功！"
    echo "========================================"
    echo ""
    echo "📊 服务状态:"
    docker-compose ps
    echo ""
    echo "🌐 访问地址:"
    echo "   Web反馈后台: http://localhost:5000"
    echo ""
    echo "📋 常用命令:"
    echo "   查看日志: docker-compose logs -f"
    echo "   停止服务: docker-compose down"
    echo "   重启服务: docker-compose restart"
    echo "   进入容器: docker-compose exec xianyubot bash"
    echo ""
else
    echo "❌ 服务启动失败，请检查日志:"
    docker-compose logs
    exit 1
fi
