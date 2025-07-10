# 🚀 Render部署指南

## 📋 部署前检查清单

### ✅ 必需文件
- [x] `chatbot_web.py` - 主应用文件
- [x] `security_middleware.py` - 安全中间件
- [x] `requirements.txt` - Python依赖
- [x] `templates/index.html` - 前端界面
- [x] `stakeholder_management_rag_sync/` - RAG数据文件
- [x] `README.md` - 项目文档
- [x] `render.yaml` - Render配置
- [x] `deploy.sh` - 部署脚本
- [x] `start.sh` - 启动脚本
- [x] `test_deployment.py` - 测试脚本

### ✅ 环境要求
- [x] OpenAI API密钥
- [x] Git仓库
- [x] Render.com账号

## 🎯 快速部署步骤

### 方法一：使用Git仓库（推荐）

1. **上传到Git仓库**
   ```bash
   cd chatbot-7-10
   git init
   git add .
   git commit -m "Initial commit: Stakeholder Management Chatbot"
   git remote add origin your_repository_url
   git push -u origin main
   ```

2. **在Render创建服务**
   - 登录 [Render.com](https://render.com)
   - 点击 "New +" → "Web Service"
   - 连接你的Git仓库
   - 选择分支（通常是main）

3. **配置服务设置**
   ```
   Name: stakeholder-management-chatbot
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python chatbot_web.py
   ```

4. **设置环境变量**
   - 在"Environment"标签页添加：
   ```
   OPENAI_API_KEY = your_openai_api_key_here
   ```

5. **部署**
   - 点击"Create Web Service"
   - 等待构建完成（约5-10分钟）

### 方法二：直接上传文件

1. **创建Render服务**
   - 在Render创建新的Web Service
   - 选择"Deploy from existing code"

2. **上传文件**
   - 将整个`chatbot-7-10`文件夹内容压缩
   - 上传到Render

3. **配置启动命令**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python chatbot_web.py
   ```

## 🔧 部署后配置

### 1. 验证部署
- 访问Render提供的URL
- 测试基本功能：
  - 页面加载正常
  - Chat功能可用
  - Token Stats显示数据
  - 主题切换正常

### 2. 监控服务
- 在Render控制台查看日志
- 监控服务状态
- 检查错误信息

### 3. 性能优化
- 根据需要调整内存配置
- 监控API调用频率
- 优化响应时间

## 🐛 常见问题解决

### 1. 构建失败
**问题**: 依赖安装失败
**解决**: 
- 检查Python版本（需要3.8+）
- 确认requirements.txt格式正确
- 查看构建日志中的具体错误

### 2. 启动失败
**问题**: 应用无法启动
**解决**:
- 检查环境变量设置
- 确认端口配置正确
- 查看启动日志

### 3. API调用失败
**问题**: OpenAI API错误
**解决**:
- 验证API密钥正确性
- 检查API配额
- 确认网络连接

### 4. 页面加载慢
**问题**: 首次加载缓慢
**解决**:
- 检查RAG数据文件大小
- 优化数据加载逻辑
- 考虑使用CDN

## 📊 部署验证清单

### 功能测试
- [ ] 页面正常加载
- [ ] Chat功能可用
- [ ] Token Stats显示数据
- [ ] 主题切换正常
- [ ] 侧边栏展开/收缩
- [ ] Tab切换正常
- [ ] 历史记录功能
- [ ] 搜索功能

### 性能测试
- [ ] 响应时间 < 3秒
- [ ] 内存使用正常
- [ ] API调用成功
- [ ] 错误处理正常

### 安全测试
- [ ] 输入验证正常
- [ ] 速率限制生效
- [ ] 安全头设置正确
- [ ] 无敏感信息泄露

## 🔄 更新部署

### 代码更新
1. 修改代码
2. 提交到Git仓库
3. Render自动重新部署

### 环境变量更新
1. 在Render控制台修改环境变量
2. 重新部署服务

### 数据更新
1. 更新RAG数据文件
2. 重新上传到Git仓库
3. 触发重新部署

## 📈 监控和维护

### 日志监控
- 定期检查Render日志
- 监控错误率
- 关注性能指标

### 成本监控
- 监控OpenAI API使用量
- 跟踪成本变化
- 优化API调用

### 安全维护
- 定期更新依赖
- 监控安全漏洞
- 更新API密钥

## 🎉 部署成功标志

当看到以下信息时，表示部署成功：

```
✅ 服务状态: Live
✅ 构建状态: Build successful
✅ 健康检查: Healthy
✅ 访问URL: https://your-app-name.onrender.com
```

## 📞 技术支持

如果遇到问题，请检查：
1. Render服务日志
2. 应用启动日志
3. 网络连接状态
4. API密钥有效性

---

**注意**: 部署完成后，请定期监控服务状态和API使用情况，确保系统稳定运行。 