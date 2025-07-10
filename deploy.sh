#!/bin/bash

# Stakeholder Management Chatbot 部署脚本
# 用于快速部署到Render或其他平台

echo "🚀 开始部署 Stakeholder Management Chatbot..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "📋 Python版本: $python_version"

# 检查必要文件
echo "📁 检查项目文件..."
required_files=("chatbot_web.py" "security_middleware.py" "requirements.txt" "templates/index.html")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
        exit 1
    fi
done

# 检查RAG数据文件
echo "📊 检查RAG数据文件..."
rag_dir="stakeholder_management_rag_sync"
if [ -d "$rag_dir" ]; then
    echo "✅ RAG数据目录存在"
    file_count=$(find "$rag_dir" -name "*.json" -o -name "*.graphml" | wc -l)
    echo "📈 找到 $file_count 个数据文件"
else
    echo "❌ RAG数据目录缺失"
    exit 1
fi

# 检查环境变量
echo "🔑 检查环境变量..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: OPENAI_API_KEY 环境变量未设置"
    echo "请在部署时设置此环境变量"
else
    echo "✅ OPENAI_API_KEY 已设置"
fi

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 测试应用
echo "🧪 测试应用..."
python3 -c "
import sys
sys.path.append('.')
try:
    from chatbot_web import app
    print('✅ 应用导入成功')
except Exception as e:
    print(f'❌ 应用导入失败: {e}')
    sys.exit(1)
"

echo "✅ 部署准备完成！"
echo ""
echo "📋 部署步骤："
echo "1. 将整个 chatbot-7-10 文件夹上传到Git仓库"
echo "2. 在Render.com创建新的Web Service"
echo "3. 连接你的Git仓库"
echo "4. 设置环境变量 OPENAI_API_KEY"
echo "5. 部署配置："
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python chatbot_web.py"
echo "   - Port: 8081 (或让Render自动设置)"
echo ""
echo "🌐 部署完成后，访问提供的URL即可使用！" 