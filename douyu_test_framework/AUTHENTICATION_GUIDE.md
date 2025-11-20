# 斗鱼登录注册功能测试指南

## 概述

本测试框架已增强，支持斗鱼平台的登录和注册功能测试，包括多种登录方式、注册流程和异常场景处理。

## 新增功能

### 1. URL参数处理

**问题**：斗鱼网站会自动在URL后添加`dyshid`参数
- 输入：`https://www.douyu.com/`
- 实际：`https://www.douyu.com/?dyshid=0-ba439b3aea51951c74a2f47c00071701`

**解决方案**：
- 更新了`HomePage.is_home_page()`方法，能够正确识别带参数的首页URL
- 在导航方法中增加了`wait_for_load_state("networkidle")`等待页面稳定

### 2. FSM状态扩展

![img.png](img.png)

新增以下页面状态：
- `LOGIN` - 登录页面状态
- `REGISTER` - 注册页面状态
- `PHONE_VERIFY` - 手机验证状态

新增状态转换：
```
HOME -> LOGIN (click_login)
LOGIN -> REGISTER (switch_to_register)
LOGIN -> HOME (successful_login)
REGISTER -> LOGIN (switch_to_login)
REGISTER -> HOME (successful_register)
```

### 3. 页面对象

#### LoginPage (登录页面)

**主要功能**：
- `open_login_modal()` - 打开登录弹窗
- `switch_to_phone_login()` - 切换到手机号登录
- `switch_to_password_login()` - 切换到密码登录
- `login_with_phone_and_code(phone, code)` - 手机号+验证码登录
- `login_with_username_and_password(username, password)` - 用户名+密码登录
- `request_sms_code(phone)` - 请求短信验证码
- `logout()` - 退出登录
- `is_logged_in()` - 检查登录状态
- `get_error_message()` - 获取错误信息

#### RegisterPage (注册页面)

**主要功能**：
- `register(phone, code, username, password, email, confirm_password)` - 完整注册流程
- `fill_phone(phone)` - 填写手机号
- `request_sms_code(phone)` - 请求验证码
- `fill_verification_code(code)` - 填写验证码
- `fill_username(username)` - 填写用户名
- `fill_password(password)` - 填写密码
- `fill_email(email)` - 填写邮箱
- `accept_agreement()` - 接受用户协议
- `get_phone_error()` - 获取手机号错误提示
- `get_email_error()` - 获取邮箱错误提示
- `get_username_error()` - 获取用户名错误提示
- `get_password_error()` - 获取密码错误提示

## 测试场景

### 登录场景

#### 1. 手机号+验证码登录
```gherkin
Scenario: Login with phone number and verification code - Success
  When I click on the login button
  And I switch to phone login tab
  And I enter phone number "13800138000"
  And I request SMS verification code
  And I enter verification code "123456"
  And I click login button
  Then I should see login success or error message
```

#### 2. 用户名+密码登录
```gherkin
Scenario: Login with username and password - Success
  When I click on the login button
  And I switch to password login tab
  And I enter username "testuser"
  And I enter password "password123"
  And I click login button
  Then I should see login success or error message
```

#### 3. 登录异常场景
- 手机号格式错误
- 用户名或密码为空
- 验证码错误

### 注册场景

#### 1. 正常注册流程
```gherkin
Scenario: Register new user - Success
  When I click on the login button
  And I switch to register tab
  And I enter registration phone number "13900139000"
  And I request registration SMS code
  And I enter registration code "123456"
  And I enter registration username "newuser123"
  And I enter registration password "Pass@1234"
  And I accept user agreement
  And I click register button
  Then I should see registration success or error message
```

#### 2. 注册异常场景
- **用户名已存在**：提示用户名已被使用
- **手机号格式错误**：格式验证失败
- **邮箱格式错误**：邮箱格式不正确
- **密码不匹配**：两次密码输入不一致

### 退出登录
```gherkin
Scenario: Logout successfully
  Given I am logged in
  When I click on user avatar
  And I click logout button
  Then I should be logged out
```

## 使用示例

### Python API方式

```python
from douyu_test_framework.pages.home_page import HomePage
from douyu_test_framework.pages.login_page import LoginPage
from douyu_test_framework.pages.register_page import RegisterPage
from douyu_test_framework.core.fsm import FSM, PageState

# 创建FSM实例
fsm = FSM(page, PageState.INITIAL)

# 导航到首页
home_page = HomePage(page, fsm)
home_page.navigate_to_home()

# 手机号登录
login_page = LoginPage(page, fsm)
login_page.open_login_modal()
login_page.login_with_phone_and_code("13800138000", "123456")

# 用户注册
register_page = RegisterPage(page, fsm)
register_page.register(
    phone="13900139000",
    code="123456",
    username="newuser",
    password="Pass@1234"
)
```

### BDD测试方式

运行认证测试：
```bash
# 运行所有认证测试
pytest -v -m authentication

# 运行烟雾测试
pytest -v -m smoke

# 运行特定场景
pytest -v -k "login_with_phone"
```

## 多分支流程建模

框架支持复杂的多分支业务流程：

### 注册流程分支

```
开始注册
├── 填写手机号
│   ├── 格式正确 → 请求验证码
│   └── 格式错误 → 显示错误提示
├── 填写验证码
│   ├── 验证码正确 → 继续
│   └── 验证码错误 → 显示错误提示
├── 填写用户名
│   ├── 用户名可用 → 继续
│   └── 用户名已存在 → 显示错误提示
├── 填写邮箱（可选）
│   ├── 格式正确 → 继续
│   └── 格式错误 → 显示错误提示
├── 填写密码
│   ├── 两次密码一致 → 提交注册
│   └── 密码不一致 → 显示错误提示
└── 注册结果
    ├── 成功 → 跳转首页
    └── 失败 → 显示错误信息
```

### 登录流程分支

```
开始登录
├── 手机号登录
│   ├── 手机号格式正确
│   │   ├── 验证码正确 → 登录成功
│   │   └── 验证码错误 → 显示错误
│   └── 手机号格式错误 → 显示错误
└── 用户名密码登录
    ├── 凭据正确 → 登录成功
    ├── 凭据错误 → 显示错误
    └── 凭据为空 → 显示错误
```

## 运行测试

```bash
# 安装依赖（首次运行）
python run_tests.py --install

# 运行所有测试
python run_tests.py

# 运行认证相关测试
pytest -v step_defs/test_authentication_steps.py

# 运行简单测试
pytest -v tests/test_authentication.py

# 查看HTML报告
# 测试完成后打开: test-results/report.html
```

## 注意事项

1. **元素定位器**：实际页面结构可能变化，需要根据实际情况调整定位器
2. **验证码**：真实测试需要处理验证码（手动输入或测试环境Mock）
3. **测试数据**：使用测试账号，避免污染生产数据
4. **异步加载**：页面可能有动画和异步加载，已添加适当的等待
5. **错误处理**：所有页面方法都包含错误检查和宽松验证

## 文件结构

```
douyu_test_framework/
├── core/
│   ├── fsm.py (更新：新增登录注册状态)
│   └── base_page.py
├── pages/
│   ├── home_page.py (更新：URL参数处理)
│   ├── login_page.py (新增)
│   └── register_page.py (新增)
├── features/
│   └── authentication.feature (新增)
├── step_defs/
│   └── test_authentication_steps.py (新增)
├── tests/
│   └── test_authentication.py (新增)
├── conftest.py (更新：注册新状态验证器)
└── example_authentication_usage.py (新增：使用示例)
```

## 扩展建议

1. **验证码处理**：集成验证码识别服务或使用测试专用接口
2. **测试数据管理**：使用配置文件管理测试账号
3. **Cookie管理**：保存登录状态以加速测试
4. **错误重试**：对网络问题和临时错误添加重试机制
5. **性能监控**：记录登录注册的响应时间
6. **安全测试**：添加SQL注入、XSS等安全测试场景

## 示例代码

查看`example_authentication_usage.py`获取更多使用示例。
