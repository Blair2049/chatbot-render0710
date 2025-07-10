#!/usr/bin/env python3
"""
API密钥调试脚本
用于诊断Render环境中的API密钥问题
"""

import os
import sys

def check_api_key():
    """检查API密钥的状态"""
    print("🔍 API密钥诊断工具")
    print("=" * 50)
    
    # 获取API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY 环境变量未设置")
        print("\n解决方案:")
        print("1. 在Render控制台中设置环境变量")
        print("2. 变量名: OPENAI_API_KEY")
        print("3. 变量值: 您的OpenAI API密钥")
        return False
    
    print(f"✅ 找到API密钥 (长度: {len(api_key)})")
    
    # 检查密钥格式
    if not api_key.startswith("sk-"):
        print("❌ API密钥格式错误")
        print("   正确的格式应以 'sk-' 开头")
        print(f"   当前密钥: {api_key[:10]}...")
        return False
    
    print("✅ API密钥格式正确")
    
    # 检查密钥长度
    if len(api_key) < 20:
        print("❌ API密钥长度不足")
        print(f"   当前长度: {len(api_key)}")
        print("   正常长度应在50-100字符之间")
        return False
    
    print("✅ API密钥长度正常")
    
    # 检查是否包含特殊字符
    if "\\" in api_key or '"' in api_key or "'" in api_key:
        print("⚠️  API密钥包含特殊字符，可能导致解析问题")
        print("   建议重新设置环境变量，避免特殊字符")
    
    # 显示密钥的前几个和后几个字符
    print(f"   密钥预览: {api_key[:10]}...{api_key[-4:]}")
    
    # 检查环境变量设置
    print("\n📋 环境变量信息:")
    print(f"   变量名: OPENAI_API_KEY")
    print(f"   变量值长度: {len(api_key)}")
    print(f"   变量值类型: {type(api_key)}")
    
    # 检查是否有额外的空格或换行符
    stripped_key = api_key.strip()
    if stripped_key != api_key:
        print("⚠️  API密钥包含前导或尾随空格")
        print("   建议重新设置环境变量，去除空格")
    
    return True

def test_openai_connection():
    """测试OpenAI连接"""
    print("\n🧪 测试OpenAI连接...")
    
    try:
        import openai
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ 无法测试：API密钥未设置")
            return False
        
        client = OpenAI(api_key=api_key)
        
        # 尝试一个简单的API调用
        response = client.models.list()
        print("✅ OpenAI连接测试成功")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI连接测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始API密钥诊断...")
    
    # 检查API密钥
    key_valid = check_api_key()
    
    if key_valid:
        # 测试连接
        test_openai_connection()
    
    print("\n" + "=" * 50)
    print("📝 诊断完成")
    
    if not key_valid:
        print("\n🔧 修复建议:")
        print("1. 登录Render控制台")
        print("2. 进入您的服务设置")
        print("3. 在Environment Variables部分添加:")
        print("   - Key: OPENAI_API_KEY")
        print("   - Value: 您的完整OpenAI API密钥")
        print("4. 重新部署服务")
    
    return key_valid

if __name__ == "__main__":
    main() 