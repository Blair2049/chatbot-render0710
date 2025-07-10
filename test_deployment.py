#!/usr/bin/env python3
"""
部署测试脚本
用于验证所有必要文件是否存在且可正常工作
"""

import os
import sys
import json
from pathlib import Path

def test_file_exists(file_path, description):
    """测试文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False

def test_import_module(module_name, description):
    """测试模块是否可以导入"""
    try:
        __import__(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {description}: {module_name} - 导入失败: {e}")
        return False

def test_json_file(file_path, description):
    """测试JSON文件是否有效"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ {description}: {file_path}")
        return True
    except Exception as e:
        print(f"❌ {description}: {file_path} - JSON格式错误: {e}")
        return False

def main():
    print("🧪 开始部署测试...")
    print("=" * 50)
    
    # 测试必要文件
    required_files = [
        ("chatbot_web.py", "主应用文件"),
        ("security_middleware.py", "安全中间件"),
        ("requirements.txt", "Python依赖文件"),
        ("templates/index.html", "前端模板"),
        ("README.md", "项目文档"),
        ("render.yaml", "Render部署配置"),
        ("deploy.sh", "部署脚本"),
        ("start.sh", "启动脚本")
    ]
    
    file_tests = []
    for file_path, description in required_files:
        file_tests.append(test_file_exists(file_path, description))
    
    # 测试RAG数据文件
    rag_files = [
        ("stakeholder_management_rag_sync/graph_chunk_entity_relation.graphml", "图数据文件"),
        ("stakeholder_management_rag_sync/kv_store_doc_status.json", "文档状态缓存"),
        ("stakeholder_management_rag_sync/kv_store_full_docs.json", "完整文档缓存"),
        ("stakeholder_management_rag_sync/kv_store_text_chunks.json", "文本块缓存"),
        ("stakeholder_management_rag_sync/vdb_chunks.json", "向量数据库-块"),
        ("stakeholder_management_rag_sync/vdb_entities.json", "向量数据库-实体"),
        ("stakeholder_management_rag_sync/vdb_relationships.json", "向量数据库-关系")
    ]
    
    rag_tests = []
    for file_path, description in rag_files:
        rag_tests.append(test_file_exists(file_path, description))
    
    # 测试JSON文件格式
    json_files = [
        ("stakeholder_management_rag_sync/kv_store_doc_status.json", "文档状态JSON"),
        ("stakeholder_management_rag_sync/kv_store_full_docs.json", "完整文档JSON"),
        ("stakeholder_management_rag_sync/kv_store_text_chunks.json", "文本块JSON"),
        ("stakeholder_management_rag_sync/vdb_chunks.json", "向量数据库JSON")
    ]
    
    json_tests = []
    for file_path, description in json_files:
        json_tests.append(test_json_file(file_path, description))
    
    # 测试Python模块导入
    print("\n📦 测试Python模块导入...")
    module_tests = []
    
    # 测试基础模块
    basic_modules = [
        ("flask", "Flask框架"),
        ("numpy", "NumPy"),
        ("tiktoken", "Token编码器")
    ]
    
    for module_name, description in basic_modules:
        module_tests.append(test_import_module(module_name, description))
    
    # 测试应用模块
    try:
        sys.path.append('.')
        from chatbot_web import app
        print("✅ 主应用模块: chatbot_web")
        module_tests.append(True)
    except Exception as e:
        print(f"❌ 主应用模块: chatbot_web - 导入失败: {e}")
        module_tests.append(False)
    
    try:
        from security_middleware import SecurityMiddleware
        print("✅ 安全中间件: security_middleware")
        module_tests.append(True)
    except Exception as e:
        print(f"❌ 安全中间件: security_middleware - 导入失败: {e}")
        module_tests.append(False)
    
    # 统计结果
    print("\n" + "=" * 50)
    print("📊 测试结果统计:")
    
    total_tests = len(file_tests) + len(rag_tests) + len(json_tests) + len(module_tests)
    passed_tests = sum(file_tests) + sum(rag_tests) + sum(json_tests) + sum(module_tests)
    
    print(f"📁 文件存在测试: {sum(file_tests)}/{len(file_tests)} 通过")
    print(f"📊 RAG数据测试: {sum(rag_tests)}/{len(rag_tests)} 通过")
    print(f"📄 JSON格式测试: {sum(json_tests)}/{len(json_tests)} 通过")
    print(f"🐍 模块导入测试: {sum(module_tests)}/{len(module_tests)} 通过")
    print(f"📈 总体通过率: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 所有测试通过！部署包准备就绪。")
        print("📋 下一步:")
        print("1. 上传到Git仓库")
        print("2. 在Render.com创建Web Service")
        print("3. 设置OPENAI_API_KEY环境变量")
        print("4. 部署并测试")
        return True
    else:
        print("\n⚠️  部分测试失败，请检查上述错误并修复。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 