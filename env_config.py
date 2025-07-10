#!/usr/bin/env python3
"""
环境变量配置脚本
支持从.env文件或Render Secret Files读取配置
"""

import os
import sys
from pathlib import Path

def load_env_from_file(file_path):
    """从文件加载环境变量"""
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        return True
    except Exception as e:
        print(f"❌ 读取环境变量文件失败: {e}")
        return False

def load_secrets_from_render():
    """从Render Secret Files加载配置"""
    secrets_dir = Path("/etc/secrets")
    if not secrets_dir.exists():
        return False
    
    try:
        # 查找.env文件
        env_file = secrets_dir / ".env"
        if env_file.exists():
            return load_env_from_file(env_file)
        
        # 查找其他配置文件
        for secret_file in secrets_dir.glob("*"):
            if secret_file.is_file():
                print(f"📁 发现Secret文件: {secret_file.name}")
                # 根据文件名设置环境变量
                if secret_file.name == "openai_api_key":
                    with open(secret_file, 'r') as f:
                        os.environ["OPENAI_API_KEY"] = f.read().strip()
                elif secret_file.name == "secret_key":
                    with open(secret_file, 'r') as f:
                        os.environ["SECRET_KEY"] = f.read().strip()
        
        return True
    except Exception as e:
        print(f"❌ 读取Render Secret Files失败: {e}")
        return False

def setup_environment():
    """设置环境变量"""
    print("🔧 配置环境变量...")
    
    # 优先级1: 检查是否已设置环境变量
    if os.getenv("OPENAI_API_KEY"):
        print("✅ 环境变量已设置")
        return True
    
    # 优先级2: 尝试从Render Secret Files加载
    if load_secrets_from_render():
        print("✅ 从Render Secret Files加载配置成功")
        return True
    
    # 优先级3: 尝试从本地.env文件加载
    env_files = [".env", ".env.local", ".env.production"]
    for env_file in env_files:
        if load_env_from_file(env_file):
            print(f"✅ 从{env_file}加载配置成功")
            return True
    
    # 优先级4: 尝试从应用根目录的.env文件加载
    app_root = Path(__file__).parent
    env_file = app_root / ".env"
    if load_env_from_file(env_file):
        print(f"✅ 从应用根目录的.env文件加载配置成功")
        return True
    
    print("❌ 未找到环境变量配置")
    return False

def create_env_template():
    """创建.env模板文件"""
    template_content = """# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# 应用配置
FLASK_ENV=production
FLASK_DEBUG=false

# 安全配置
SECRET_KEY=your_secret_key_here

# 端口配置
PORT=10000
"""
    
    try:
        with open(".env.template", 'w', encoding='utf-8') as f:
            f.write(template_content)
        print("✅ 创建.env.template文件成功")
        print("📝 请复制此文件为.env并填入您的实际配置")
    except Exception as e:
        print(f"❌ 创建模板文件失败: {e}")

def main():
    """主函数"""
    print("🚀 环境变量配置工具")
    print("=" * 50)
    
    # 设置环境变量
    if setup_environment():
        print("\n✅ 环境变量配置完成")
        
        # 显示当前配置状态
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print(f"🔑 API密钥: {'*' * 10}{api_key[-4:] if len(api_key) > 4 else '****'}")
        else:
            print("❌ API密钥未设置")
        
        secret_key = os.getenv("SECRET_KEY")
        if secret_key:
            print(f"🔐 密钥: {'*' * 10}{secret_key[-4:] if len(secret_key) > 4 else '****'}")
        else:
            print("⚠️  密钥未设置")
    else:
        print("\n❌ 环境变量配置失败")
        print("\n🔧 解决方案:")
        print("1. 在Render控制台添加Secret Files")
        print("2. 创建.env文件并设置OPENAI_API_KEY")
        print("3. 设置环境变量")
        
        # 创建模板文件
        create_env_template()

if __name__ == "__main__":
    main() 