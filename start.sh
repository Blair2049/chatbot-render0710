#!/bin/bash

# Stakeholder Management Chatbot 快速启动脚本

echo "🚀 启动 Stakeholder Management Chatbot..."

# 检查环境变量
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ 错误: 请设置 OPENAI_API_KEY 环境变量"
    echo "示例: export OPENAI_API_KEY='your_api_key_here'"
    exit 1
fi

# 检查Python依赖
echo "📦 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📥 安装依赖..."
    pip install -r requirements.txt
fi

# 启动应用
echo "🌐 启动Web服务器..."
python3 chatbot_web.py 