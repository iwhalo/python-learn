# Token 管理系统项目说明文档

## 📋 项目概述

**Token 管理系统**是一个基于 Python 的完整身份验证和 API 访问控制解决方案。该项目演示了现代 Web 应用中常见的 Token 管理、自动刷新、重试机制等关键功能。

### 🎯 项目目标
- 提供完整的 Token 生命周期管理
- 演示 Token 自动刷新机制
- 实现健壮的 API 请求重试策略
- 展示并发场景下的 Token 管理
- 提供完整的测试和演示用例

---

## 🏗️ 项目结构

```
token-management-system/
├── 📁 api/
│   └── api_function.py          # 核心 Token 管理类
├── 📁 config/
│   └── config.py               # 项目配置文件
├── 📁 tests/
│   └── test01_function.py      # 单元测试文件
├── demo.py                     # 功能演示程序
├── README.md                   # 项目说明文档
└── requirements.txt            # 依赖包列表
```

---

## 📦 核心模块说明

### 1. ApiFunction 类 (`api/api_function.py`)

#### 主要功能
- **用户认证**：模拟登录流程，生成和管理 Token
- **Token 管理**：Token 生成、验证、刷新和过期处理
- **API 请求**：带 Token 的 API 请求发送和响应处理
- **重试机制**：网络异常和 Token 过期的自动重试
- **会话管理**：用户会话的创建和维护

#### 核心方法
| 方法名 | 功能说明 | 参数 | 返回值 |
|--------|----------|------|---------|
| `api_login()` | 用户登录获取 Token | password, mobile | Token 字符串 |
| `api_message()` | 发送 API 请求 | token(可选) | Response 对象 |
| `_refresh_token()` | 刷新 Token | 无 | 布尔值 |
| `_is_token_expired()` | 检查 Token 过期 | 无 | 布尔值 |
| `get_current_token()` | 获取当前 Token | 无 | Token 字符串 |
| `get_token_remaining_time()` | 获取剩余时间 | 无 | 秒数 |
| `logout()` | 用户登出 | 无 | 无 |

### 2. 配置模块 (`config/config.py`)

#### 配置参数
```python
# API 配置
HOST = "https://jsonplaceholder.typicode.com"  # 测试 API 地址

# Token 配置
TOKEN_EXPIRE_TIME = 3600                    # Token 过期时间(秒)
REFRESH_TOKEN_BEFORE_EXPIRE = 300           # 提前刷新时间(秒)
MAX_RETRY_TIMES = 3                         # 最大重试次数
RETRY_DELAY = 1                             # 重试延迟(秒)

# 测试配置
TEST_PASSWORD = "123456789"                 # 测试密码
TEST_MOBILE = "13800000011"                 # 测试手机号
```

### 3. 测试模块 (`tests/test01_function.py`)

#### 测试用例
- `test01_login()`: 登录功能测试
- `test02_message()`: API 请求测试
- `test03_token_expiration_handling()`: Token 过期处理测试
- `test04_concurrent_requests()`: 并发请求测试
- `test05_token_management()`: Token 管理功能测试

### 4. 演示程序 (`demo.py`)

#### 演示场景
1. **基本 Token 流程演示**
2. **Token 刷新机制演示**
3. **并发请求场景演示**
4. **Token 完整生命周期演示**
5. **错误场景处理演示**

---

## 🔧 安装和运行

### 环境要求
- Python 3.7+
- requests 库

### 安装步骤
1. **克隆项目**
   ```bash
   git clone <项目地址>
   cd token-management-system
   ```

2. **安装依赖**
   ```bash
   pip install requests
   ```

3. **运行演示**
   ```bash
   python demo.py
   ```

4. **运行测试**
   ```bash
   # 运行单个测试
   python -m pytest tests/test01_function.py::TestFunction::test01_login -v
   
   # 运行所有测试
   python -m pytest tests/ -v
   ```

---

## 🚀 核心特性

### 1. Token 自动管理
```python
# 自动处理 Token 过期和刷新
api = ApiFunction(session)
token = api.api_login("password", "mobile")  # 获取 Token
response = api.api_message()                 # 自动使用 Token
```

### 2. 智能重试机制
- 网络异常自动重试
- Token 过期自动刷新
- 可配置的重试次数和延迟

### 3. 并发安全
- 支持多个并发请求
- Token 状态一致性保证
- 线程安全的会话管理

### 4. 完整的错误处理
- Token 无效处理
- 网络异常处理
- API 错误响应处理

---

## 📊 使用示例

### 基本使用流程
```python
import requests
from api.api_function import ApiFunction

# 初始化
session = requests.Session()
api = ApiFunction(session)

# 1. 用户登录
token = api.api_login("123456789", "13800000011")
print(f"获取的 Token: {token}")

# 2. 使用 Token 访问 API
response = api.api_message()
if response.status_code == 200:
    print("API 请求成功")
    print(response.json())

# 3. 检查 Token 状态
remaining_time = api.get_token_remaining_time()
print(f"Token 剩余时间: {remaining_time}秒")

# 4. 用户登出
api.logout()
```

### 高级使用场景
```python
# 并发请求处理
for i in range(5):
    response = api.api_message()
    if response:
        print(f"请求 {i+1} 成功")
    
# 自定义 Token 管理
custom_token = "custom_token_123"
api.api_message(custom_token)  # 使用自定义 Token
```

---

## 🛠️ 配置说明

### Token 过期策略
```python
# config.py 中的相关配置
TOKEN_EXPIRE_TIME = 3600                    # 1小时过期
REFRESH_TOKEN_BEFORE_EXPIRE = 300           # 过期前5分钟自动刷新
```

### 重试策略
```python
MAX_RETRY_TIMES = 3     # 最多重试3次
RETRY_DELAY = 1         # 每次重试间隔1秒
```

---

## 🔍 故障排除

### 常见问题

1. **导入错误**
   ```
   ImportError: attempted relative import beyond top-level package
   ```
   **解决方案**: 确保正确设置 Python 路径

2. **Token 获取失败**
   **可能原因**: 
   - 网络连接问题
   - API 服务不可用
   - 认证参数错误

3. **Token 刷新失败**
   **解决方案**: 
   - 检查登录参数是否保存
   - 验证网络连接
   - 查看 API 服务状态

### 调试技巧
```python
# 启用详细日志
api = ApiFunction(session)
# 查看内部状态
print(f"当前 Token: {api.get_current_token()}")
print(f"剩余时间: {api.get_token_remaining_time()}秒")
```

---

## 📈 扩展建议

### 功能扩展
1. **持久化存储**: 将 Token 保存到数据库或文件
2. **多用户支持**: 支持多个用户同时管理
3. **Token 加密**: 增加 Token 加密和安全存储
4. **监控告警**: 添加 Token 使用监控和告警

### 性能优化
1. **连接池**: 使用连接池提高性能
2. **缓存机制**: 添加请求缓存减少 API 调用
3. **异步支持**: 支持异步请求处理

---

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 👥 维护者

- **作者**: [Your Name]
- **邮箱**: [your.email@example.com]
- **项目地址**: [GitHub Repository URL]

---

## 🔄 版本历史

- **v1.0.0** (2024-01-XX)
  - 初始版本发布
  - 核心 Token 管理功能
  - 完整的测试和演示

---

## 📞 技术支持

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至: [your.email@example.com]
- 项目文档: [Documentation URL]

---

**⭐ 如果这个项目对你有帮助，请给我们一个星标！**