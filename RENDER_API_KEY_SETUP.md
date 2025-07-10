# Render API密钥设置指南

## 问题诊断

从部署日志中可以看到API密钥错误：
```
Incorrect API key provided: sk-proj-********************************************************************************************************************************************************xXMA
```

这表明API密钥可能被截断或格式不正确。

## 解决步骤

### 1. 获取正确的OpenAI API密钥

1. 登录 [OpenAI Platform](https://platform.openai.com/)
2. 进入 [API Keys](https://platform.openai.com/api-keys) 页面
3. 点击 "Create new secret key"
4. 复制完整的API密钥（应该以 `sk-` 开头，长度约50-100字符）

### 2. 在Render中设置环境变量

1. 登录 [Render控制台](https://dashboard.render.com/)
2. 找到您的服务 `chatbot-render0710`
3. 点击服务名称进入详情页
4. 在左侧菜单中点击 "Environment"
5. 在 "Environment Variables" 部分：
   - 点击 "Add Environment Variable"
   - **Key**: `OPENAI_API_KEY`
   - **Value**: 粘贴您的完整OpenAI API密钥
   - 确保没有多余的空格或换行符
6. 点击 "Save Changes"

### 3. 重新部署服务

1. 在Render控制台中，点击 "Manual Deploy"
2. 选择 "Deploy latest commit"
3. 等待部署完成

### 4. 验证设置

部署完成后，访问您的应用并尝试发送一条消息。如果仍然出现API密钥错误，请检查：

1. **密钥格式**: 确保以 `sk-` 开头
2. **密钥长度**: 正常长度应在50-100字符之间
3. **特殊字符**: 确保没有多余的空格、引号或其他特殊字符
4. **环境变量名称**: 确保变量名是 `OPENAI_API_KEY`（区分大小写）

## 常见问题

### Q: API密钥显示为星号，如何确认是否正确？
A: 在Render控制台中，环境变量值会显示为星号以保护隐私。您可以通过以下方式验证：
1. 临时删除并重新添加环境变量
2. 确保复制粘贴时没有多余字符
3. 使用本地测试脚本验证密钥

### Q: 部署后仍然出现401错误？
A: 可能的原因：
1. 环境变量未正确保存
2. 需要重新部署服务
3. API密钥已过期或被撤销
4. 账户余额不足

### Q: 如何测试API密钥是否有效？
A: 可以使用提供的测试脚本：
```bash
python api_key_debug.py
```

## 本地测试

在本地环境中测试API密钥：

```bash
# 设置环境变量
export OPENAI_API_KEY="your-api-key-here"

# 运行测试脚本
python api_key_debug.py

# 启动本地服务器
python chatbot_web.py
```

## 联系支持

如果问题仍然存在，请：
1. 检查OpenAI账户状态和余额
2. 确认API密钥权限设置
3. 查看Render部署日志获取更多错误信息 