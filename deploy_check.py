#!/usr/bin/env python3
"""
部署检查脚本 - 用于诊断Render环境问题
"""

import os
import sys
import platform

def check_environment():
    """检查环境变量和配置"""
    print("🔍 环境检查开始...")
    print("=" * 50)
    
    # 检查Python版本
    print(f"Python版本: {platform.python_version()}")
    print(f"Python路径: {sys.executable}")
    
    # 检查环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY已设置")
        print(f"   密钥长度: {len(api_key)}")
        print(f"   密钥前缀: {api_key[:10]}...")
        
        # 验证密钥格式
        if api_key.startswith("sk-"):
            print("   ✅ 密钥格式正确")
        else:
            print("   ❌ 密钥格式错误，应以'sk-'开头")
            
        if len(api_key) >= 20:
            print("   ✅ 密钥长度正常")
        else:
            print("   ❌ 密钥长度不足")
    else:
        print("❌ OPENAI_API_KEY未设置")
    
    # 检查其他环境变量
    port = os.getenv("PORT", "8081")
    print(f"端口设置: {port}")
    
    # 检查工作目录
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查文件存在性
    required_files = [
        "chatbot_web.py",
        "requirements.txt",
        "render.yaml",
        "lightrag/__init__.py",
        "lightrag/llm.py",
        "templates/index.html"
    ]
    
    print("\n📁 文件检查:")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - 文件不存在")
    
    print("\n" + "=" * 50)

def test_imports():
    """测试模块导入"""
    print("📦 模块导入测试...")
    print("=" * 50)
    
    try:
        import flask
        print("✅ Flask导入成功")
    except ImportError as e:
        print(f"❌ Flask导入失败: {e}")
    
    try:
        import numpy
        print("✅ NumPy导入成功")
    except ImportError as e:
        print(f"❌ NumPy导入失败: {e}")
    
    try:
        import tiktoken
        print("✅ Tiktoken导入成功")
    except ImportError as e:
        print(f"❌ Tiktoken导入失败: {e}")
    
    try:
        import openai
        print("✅ OpenAI导入成功")
    except ImportError as e:
        print(f"❌ OpenAI导入失败: {e}")
    
    # 测试本地lightrag模块
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from lightrag import LightRAG
        print("✅ LightRAG导入成功")
    except ImportError as e:
        print(f"❌ LightRAG导入失败: {e}")
    
    try:
        from lightrag.llm import openai_complete_if_cache
        print("✅ openai_complete_if_cache导入成功")
    except ImportError as e:
        print(f"❌ openai_complete_if_cache导入失败: {e}")
    
    print("\n" + "=" * 50)

def test_api_connection():
    """测试API连接"""
    print("🌐 API连接测试...")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 无法测试API连接：API密钥未设置")
        return
    
    try:
        import openai
        client = openai.AsyncOpenAI(api_key=api_key)
        print("✅ OpenAI客户端创建成功")
        
        # 测试简单请求
        print("正在测试API连接...")
        # 这里可以添加实际的API测试
        
    except Exception as e:
        print(f"❌ API连接测试失败: {e}")
    
    print("\n" + "=" * 50)

def main():
    """主函数"""
    print("🚀 Render部署环境检查")
    print("=" * 50)
    
    check_environment()
    test_imports()
    test_api_connection()
    
    print("✅ 检查完成！")
    print("\n📋 如果发现问题，请检查：")
    print("1. Render环境变量设置")
    print("2. API密钥是否正确")
    print("3. 依赖是否正确安装")
    print("4. 文件路径是否正确")

if __name__ == "__main__":
    main() 