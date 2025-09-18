# 斗鱼测试框架快速入门指南

## 🚀 快速开始

### 1. 安装依赖和运行测试（一键完成）

```bash
# 进入项目目录
cd D:\PycharmProjects\python-learn\douyu_test_framework

# 安装依赖并运行测试
python run_tests.py --install
```

**或者在 Windows 上双击运行：**
```
run_tests.bat
```

### 2. 手动安装（可选）

如果想分步安装：

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
python -m playwright install chromium
```

### 3. 运行测试

```bash
# 运行所有测试
python run_tests.py

# 或者使用 pytest
pytest -v

# 有界面模式运行（可以看到浏览器操作）
pytest --headed -v

# 运行特定测试
pytest step_defs/test_homepage_steps.py -v
pytest step_defs/test_fsm_steps.py -v
```

## 📋 项目架构说明

### 核心组件

1. **FSM (有限状态机)** - `core/fsm.py`
   - 管理页面状态转换
   - 确保导航流程的有效性
   - 追踪状态历史

2. **Page Object Model** - `pages/`
   - `home_page.py`: 首页操作
   - `category_page.py`: 分类页操作
   - `live_room_page.py`: 直播间操作
   - `search_results_page.py`: 搜索结果操作

3. **BDD 特性文件** - `features/`
   - 使用 Gherkin 语法编写测试场景
   - 可读性强，业务人员也能理解

4. **步骤定义** - `step_defs/`
   - 实现 BDD 特性文件中的步骤
   - 连接业务场景和代码实现

## 🎯 示例代码

### 示例 1: 基本使用

```python
from playwright.sync_api import sync_playwright
from douyu_test_framework.core.fsm import FSM, PageState
from douyu_test_framework.pages.home_page import HomePage

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # 初始化 FSM
    fsm = FSM(page, PageState.INITIAL)
    
    # 导航到首页
    home_page = HomePage(page, fsm)
    home_page.navigate_to_home()
    
    # 搜索
    home_page.search("英雄联盟")
    
    # 查看 FSM 状态
    print(f"当前状态: {fsm.get_current_state()}")
    print(f"状态历史: {fsm.get_history()}")
    
    browser.close()
```

### 示例 2: 运行示例脚本

```bash
# 运行示例代码
python example_usage.py
```

## 📊 测试报告

测试完成后，查看以下位置的报告：

- **HTML 报告**: `test-results/report.html` （用浏览器打开）
- **日志文件**: `logs/test_*.log`
- **截图**: `screenshots/` （失败的测试会自动截图）

## 🔧 配置修改

编辑 `config.py` 来修改测试配置：

```python
class TestConfig(BaseModel):
    base_url: str = "https://www.douyu.com"
    browser: str = "chromium"        # 浏览器类型
    headless: bool = False           # True=无头模式，False=有界面
    slow_mo: int = 0                 # 慢速执行（毫秒）
    timeout: int = 30000             # 超时时间
    screenshot_on_failure: bool = True  # 失败时截图
```

## 🎨 FSM 状态转换图

```
INITIAL
   ↓ navigate_home
  HOME ←――――――――――――――→ (go_home)
   ├→ search → SEARCH_RESULTS
   ├→ select_category → CATEGORY → select_live_room → LIVE_ROOM
   └→ enter_live_room → LIVE_ROOM
```

## 📝 编写新测试

### 1. 添加 BDD 特性文件

在 `features/` 目录创建 `.feature` 文件：

```gherkin
Feature: 新功能测试
  Scenario: 测试场景
    Given 前置条件
    When 执行操作
    Then 验证结果
```

### 2. 实现步骤定义

在 `step_defs/` 目录创建步骤定义文件：

```python
from pytest_bdd import scenarios, given, when, then

scenarios('../features/your_feature.feature')

@given('前置条件')
def setup():
    pass

@when('执行操作')
def action():
    pass

@then('验证结果')
def verify():
    pass
```

## 🐛 常见问题

### 1. Playwright 浏览器未安装
```bash
python -m playwright install chromium
```

### 2. 元素找不到
- 检查网络连接
- 增加等待时间
- 更新元素定位器

### 3. 测试失败
- 查看 `screenshots/` 目录的截图
- 查看 `logs/` 目录的日志
- 查看 `test-results/report.html` 报告

## 📚 更多信息

- Playwright 文档: https://playwright.dev/python/
- Pytest 文档: https://docs.pytest.org/
- Pytest-BDD 文档: https://pytest-bdd.readthedocs.io/

## 🎉 开始测试！

```bash
cd D:\PycharmProjects\python-learn\douyu_test_framework
python run_tests.py --install
```

祝测试顺利！ 🚀
