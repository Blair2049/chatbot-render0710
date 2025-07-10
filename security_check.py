#!/usr/bin/env python3
"""
安全检查脚本
确保部署包中没有敏感信息泄露
"""

import os
import re
import glob

def check_for_sensitive_data():
    """检查是否有敏感数据泄露"""
    print("🔒 开始安全检查...")
    print("=" * 50)
    
    # 敏感信息模式
    sensitive_patterns = [
        r'sk-proj-[a-zA-Z0-9]{48}',  # OpenAI API密钥
        r'sk-[a-zA-Z0-9]{48}',       # 其他OpenAI密钥格式
        r'pk_[a-zA-Z0-9]{48}',       # Stripe公钥
        r'sk_[a-zA-Z0-9]{48}',       # Stripe私钥
        r'AIza[a-zA-Z0-9]{35}',      # Google API密钥
        r'ghp_[a-zA-Z0-9]{36}',      # GitHub个人访问令牌
        r'gho_[a-zA-Z0-9]{36}',      # GitHub OAuth令牌
    ]
    
    # 硬编码敏感信息模式（排除占位符）
    hardcoded_patterns = [
        r'password\s*=\s*["\'][^"\']{10,}["\']',  # 硬编码密码（至少10个字符）
        r'secret\s*=\s*["\'][^"\']{10,}["\']',    # 硬编码密钥（至少10个字符）
        r'api_key\s*=\s*["\'][^"\']{10,}["\']',   # 硬编码API密钥（至少10个字符）
    ]
    
    # 要检查的文件类型
    file_patterns = [
        '*.py',
        '*.html',
        '*.js',
        '*.json',
        '*.yaml',
        '*.yml',
        '*.md',
        '*.txt',
        '*.sh'
    ]
    
    found_sensitive = False
    
    for pattern in file_patterns:
        for file_path in glob.glob(pattern, recursive=True):
            # 跳过二进制文件和大型数据文件
            if any(skip in file_path for skip in ['__pycache__', '.git', 'node_modules', 'vdb_', 'kv_store_']):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # 检查标准敏感信息模式
                for i, regex in enumerate(sensitive_patterns):
                    matches = re.findall(regex, content, re.IGNORECASE)
                    if matches:
                        print(f"❌ 发现敏感信息: {file_path}")
                        print(f"   模式 {i+1}: {matches[:3]}...")  # 只显示前3个匹配
                        found_sensitive = True
                
                # 检查硬编码敏感信息（排除占位符）
                for i, regex in enumerate(hardcoded_patterns):
                    matches = re.findall(regex, content, re.IGNORECASE)
                    # 过滤掉占位符
                    real_matches = [m for m in matches if not any(placeholder in m.lower() for placeholder in ['your_', 'placeholder', 'example', 'demo'])]
                    if real_matches:
                        print(f"❌ 发现硬编码敏感信息: {file_path}")
                        print(f"   模式 {i+1}: {real_matches[:3]}...")  # 只显示前3个匹配
                        found_sensitive = True
                        
            except Exception as e:
                print(f"⚠️  无法读取文件 {file_path}: {e}")
    
    # 检查环境变量设置
    print("\n🔑 检查环境变量配置...")
    
    # 检查是否有硬编码的API密钥
    api_key_patterns = [
        r'OPENAI_API_KEY\s*=\s*["\'][^"\']+["\']',
        r'os\.environ\["OPENAI_API_KEY"\]\s*=\s*["\'][^"\']+["\']',
    ]
    
    for pattern in api_key_patterns:
        for file_path in glob.glob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"❌ 发现硬编码API密钥: {file_path}")
                    found_sensitive = True
            except Exception as e:
                print(f"⚠️  无法读取文件 {file_path}: {e}")
    
    # 检查示例和文档中的占位符
    print("\n📝 检查文档中的占位符...")
    placeholder_patterns = [
        r'your_api_key_here',
        r'your_openai_api_key_here',
        r'your_repository_url',
    ]
    
    for pattern in placeholder_patterns:
        for file_path in glob.glob('*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"✅ 发现占位符（正常）: {file_path}")
            except Exception as e:
                print(f"⚠️  无法读取文件 {file_path}: {e}")
    
    print("\n" + "=" * 50)
    
    if found_sensitive:
        print("❌ 安全检查失败！发现敏感信息泄露。")
        print("请修复上述问题后再上传到Git仓库。")
        return False
    else:
        print("✅ 安全检查通过！没有发现敏感信息泄露。")
        print("可以安全地上传到Git仓库。")
        return True

def check_gitignore():
    """检查.gitignore文件"""
    print("\n📁 检查.gitignore文件...")
    
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            content = f.read()
            
        important_patterns = [
            '*.pyc',
            '__pycache__',
            '.env',
            '*.log',
            'security.log'
        ]
        
        missing_patterns = []
        for pattern in important_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            print(f"⚠️  建议在.gitignore中添加: {missing_patterns}")
        else:
            print("✅ .gitignore配置良好")
    else:
        print("⚠️  没有找到.gitignore文件，建议创建一个")

if __name__ == "__main__":
    security_passed = check_for_sensitive_data()
    check_gitignore()
    
    if security_passed:
        print("\n🎉 安全检查完成，可以安全部署！")
        exit(0)
    else:
        print("\n🚨 安全检查失败，请修复问题后再部署！")
        exit(1) 