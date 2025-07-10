"""
安全中间件 - 保护您的chatbot
"""
import os
import time
from functools import wraps
from flask import request, jsonify, g
import re

class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.rate_limit = {}  # 简单的速率限制
        self.max_requests = 30  # 每分钟最大请求数（增加阈值）
        self.blocked_ips = set()  # 被封禁的IP
        
    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
    def before_request(self):
        """请求前安全检查"""
        # 获取客户端IP
        client_ip = request.remote_addr
        
        # 检查IP是否被封禁
        if client_ip in self.blocked_ips:
            return jsonify({"error": "Access denied"}), 403
            
        # 速率限制检查
        if not self.check_rate_limit(client_ip):
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        # 记录请求时间
        g.start_time = time.time()
        
    def after_request(self, response):
        """请求后安全处理"""
        # 添加安全头
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # 记录请求时间
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            print(f"Request from {request.remote_addr} took {duration:.2f}s")
            
        return response
        
    def check_rate_limit(self, client_ip):
        """检查速率限制"""
        current_time = time.time()
        if client_ip not in self.rate_limit:
            self.rate_limit[client_ip] = []
            
        # 清理超过1分钟的请求记录
        self.rate_limit[client_ip] = [
            req_time for req_time in self.rate_limit[client_ip] 
            if current_time - req_time < 60
        ]
        
        # 检查是否超过限制
        if len(self.rate_limit[client_ip]) >= self.max_requests:
            return False
            
        # 添加当前请求
        self.rate_limit[client_ip].append(current_time)
        return True

def validate_input(text):
    """验证用户输入"""
    if not text or len(text) > 1000:  # 限制输入长度
        return False
        
    # 检查是否包含恶意代码
    dangerous_patterns = [
        r'<script.*?>',
        r'javascript:',
        r'data:text/html',
        r'vbscript:',
        r'onload=',
        r'onerror='
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
            
    return True

def require_api_key(f):
    """API密钥验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查环境变量中是否有API密钥
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({"error": "API key not configured"}), 500
        return f(*args, **kwargs)
    return decorated_function

def log_security_event(event_type, details):
    """记录安全事件"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {event_type}: {details}\n"
    
    # 写入安全日志文件
    with open('security.log', 'a') as f:
        f.write(log_entry) 