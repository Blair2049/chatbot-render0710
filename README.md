# Stakeholder Management Chatbot

一个基于RAG（检索增强生成）的智能问答系统，专门用于利益相关者管理相关问题的回答。

## 🚀 功能特性

### 核心功能
- **智能问答**：基于文档的准确回答
- **多模式查询**：支持naive、local、global、hybrid、mix等多种查询模式
- **自动模式选择**：Best Mode自动选择最佳查询模式
- **实时评分**：对回答质量进行实时评分（完整性、多样性、赋能性）

### 用户界面
- **响应式设计**：支持桌面端和移动端
- **明暗主题切换**：支持深色和浅色主题
- **Tab切换**：Chat和Token Stats两个主要功能模块
- **可折叠侧边栏**：Query History侧边栏支持展开/收缩
- **智能布局**：Token Stats tab时自动收缩侧边栏

### 数据可视化
- **Token使用统计**：实时显示token使用情况
- **成本追踪**：API调用成本统计
- **历史记录**：查询历史记录管理
- **图表展示**：Token使用趋势图表

### 安全特性
- **输入验证**：防止恶意输入
- **速率限制**：防止API滥用
- **安全中间件**：多层安全保护

## 📁 项目结构

```
chatbot-7-10/
├── chatbot_web.py              # 主应用文件
├── security_middleware.py      # 安全中间件
├── requirements.txt            # Python依赖
├── templates/                  # 前端模板
│   └── index.html             # 主页面
├── stakeholder_management_rag_sync/  # RAG数据文件
│   ├── graph_chunk_entity_relation.graphml
│   ├── kv_store_*.json
│   └── vdb_*.json
└── README.md                  # 项目文档
```

## 🛠️ 技术栈

### 后端
- **Flask**：Web框架
- **LightRAG**：RAG检索增强生成框架
- **OpenAI API**：GPT-4o-mini模型
- **tiktoken**：Token计算
- **numpy**：数值计算

### 前端
- **HTML5/CSS3**：页面结构和样式
- **JavaScript**：交互逻辑
- **Chart.js**：数据可视化
- **响应式设计**：移动端适配

## 🚀 部署到Render

### 1. 准备工作

1. 在Render.com注册账号
2. 准备OpenAI API密钥
3. 确保Git仓库已准备好

### 2. 环境变量配置

在Render部署时需要设置以下环境变量：

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 部署步骤

#### 方法一：通过Git仓库部署

1. **上传代码到Git仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your_repository_url
   git push -u origin main
   ```

2. **在Render创建新服务**
   - 登录Render.com
   - 点击"New +" → "Web Service"
   - 连接你的Git仓库
   - 选择分支（通常是main）

3. **配置服务设置**
   - **Name**: `stakeholder-management-chatbot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python chatbot_web.py`
   - **Port**: `8081`

4. **设置环境变量**
   - 在"Environment"标签页添加：
     - `OPENAI_API_KEY`: 你的OpenAI API密钥

#### 方法二：直接上传文件

1. **创建Render服务**
   - 在Render创建新的Web Service
   - 选择"Deploy from existing code"

2. **上传文件**
   - 将整个`chatbot-7-10`文件夹内容上传
   - 确保包含所有必要文件

3. **配置启动命令**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python chatbot_web.py`

### 4. 部署后配置

1. **等待构建完成**
   - Render会自动安装依赖
   - 检查构建日志是否有错误

2. **验证部署**
   - 访问提供的URL
   - 测试基本功能是否正常

3. **监控服务**
   - 在Render控制台监控服务状态
   - 查看日志输出

## 🔧 本地开发

### 环境要求
- Python 3.8+
- OpenAI API密钥

### 安装步骤

1. **克隆项目**
   ```bash
   git clone your_repository_url
   cd chatbot-7-10
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **设置环境变量**
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

4. **运行应用**
   ```bash
   python chatbot_web.py
   ```

5. **访问应用**
   - 打开浏览器访问 `http://localhost:8081`

## 📊 功能使用指南

### Chat功能
1. **选择查询模式**：
   - Best Mode（推荐）：自动选择最佳模式
   - Mix Mode：混合模式
   - Naive Mode：简单模式
   - Local Mode：本地模式
   - Global Mode：全局模式
   - Hybrid Mode：混合模式

2. **提问**：
   - 在输入框中输入问题
   - 按Enter或点击Send按钮
   - 系统会显示回答和评分

### Token Stats功能
1. **查看统计信息**：
   - 总Token使用量
   - 成本统计
   - 请求次数

2. **图表分析**：
   - Token使用趋势图
   - 每日使用统计

### Query History功能
1. **查看历史记录**：
   - 点击侧边栏展开按钮
   - 查看所有查询历史

2. **搜索历史**：
   - 使用搜索框过滤历史记录

3. **查看详情**：
   - 点击历史记录项查看详细信息

## 🔒 安全特性

### 输入验证
- 防止XSS攻击
- 限制输入长度
- 过滤恶意代码

### 速率限制
- 每分钟最多30次请求
- 防止API滥用
- IP封禁机制

### 安全头
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security

## 📈 性能优化

### 缓存机制
- LLM响应缓存
- 实体提取缓存
- 减少重复API调用

### 异步处理
- 异步API调用
- 非阻塞操作
- 提高响应速度

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   - 检查环境变量设置
   - 确认API密钥有效

2. **依赖安装失败**
   - 检查Python版本
   - 更新pip版本
   - 检查网络连接

3. **端口占用**
   - 修改端口号
   - 检查其他服务

4. **内存不足**
   - 增加Render内存配置
   - 优化代码逻辑

### 日志查看
```bash
# 本地运行时的日志
python chatbot_web.py

# Render部署后的日志
# 在Render控制台查看
```

## 📝 更新日志

### v1.0.0 (2025-07-10)
- ✅ 基础RAG问答功能
- ✅ 多模式查询支持
- ✅ 实时评分系统
- ✅ 响应式UI设计
- ✅ Token使用统计
- ✅ 安全中间件
- ✅ 明暗主题切换
- ✅ 智能侧边栏管理

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues
- 邮箱：[your_email@example.com]

---

## 🔑 API密钥设置

### OpenAI API密钥配置

**重要**: 如果遇到API密钥相关错误，请参考详细的 [API密钥设置指南](RENDER_API_KEY_SETUP.md)

#### 获取API密钥
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录您的账户
3. 进入 [API Keys](https://platform.openai.com/api-keys) 页面
4. 点击 "Create new secret key"
5. 复制完整的API密钥（以 `sk-` 开头）

#### 在Render中设置
1. 登录 [Render控制台](https://dashboard.render.com/)
2. 找到您的服务
3. 进入 "Environment" 设置
4. 添加环境变量：
   - **Key**: `OPENAI_API_KEY`
   - **Value**: 您的完整API密钥
5. 保存并重新部署

#### 本地测试
```bash
# 设置环境变量
export OPENAI_API_KEY="your-api-key-here"

# 运行诊断脚本
python api_key_debug.py

# 启动应用
python chatbot_web.py
```

#### 常见问题
- **401错误**: 检查API密钥格式和有效性
- **密钥截断**: 确保复制完整的密钥，无多余字符
- **环境变量未生效**: 重新部署服务

---

**注意**：部署前请确保已正确设置OpenAI API密钥，并了解相关使用限制和成本。 