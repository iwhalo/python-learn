# Douyu Test Framework

基于 Python + Playwright + Pytest + BDD + FSM 的斗鱼网站自动化测试框架

## 项目特点

- ✅ **Playwright**: 现代化的浏览器自动化工具
- ✅ **Pytest**: 强大的测试框架
- ✅ **BDD (Behavior Driven Development)**: 使用 pytest-bdd 实现行为驱动开发
- ✅ **FSM (Finite State Machine)**: 有限状态机管理页面状态和导航流程
- ✅ **Page Object Model**: 清晰的页面对象模型设计
- ✅ **详细的测试报告**: HTML 报告和日志

## 项目结构

```
douyu_test_framework/
├── config.py                 # 测试配置
├── conftest.py              # Pytest fixtures
├── pytest.ini               # Pytest 配置
├── requirements.txt         # 项目依赖
├── run_tests.py            # 测试运行脚本
├── core/                   # 核心框架代码
│   ├── __init__.py
│   ├── base_page.py       # 基础页面类
│   └── fsm.py            # 有限状态机
├── pages/                 # 页面对象模型
│   ├── __init__.py
│   ├── home_page.py      # 首页
│   ├── category_page.py  # 分类页
│   ├── live_room_page.py # 直播间页
│   └── search_results_page.py # 搜索结果页
├── features/             # BDD 特性文件
│   ├── homepage.feature
│   ├── live_room.feature
│   └── fsm_states.feature
├── step_defs/           # BDD 步骤定义
│   ├── test_homepage_steps.py
│   ├── test_live_room_steps.py
│   └── test_fsm_steps.py
└── utils/              # 工具类
    ├── helpers.py
    ├── logger.py
    └── report.py
```

## 安装依赖

### 方法1: 自动安装
```bash
cd douyu_test_framework
python run_tests.py --install
```

### 方法2: 手动安装
```bash
cd douyu_test_framework
pip install -r requirements.txt
python -m playwright install chromium
```

## 运行测试

### 运行所有测试
```bash
python run_tests.py
```

### 运行特定功能测试
```bash
# 运行首页测试
pytest step_defs/test_homepage_steps.py -v

# 运行直播间测试
pytest step_defs/test_live_room_steps.py -v

# 运行 FSM 状态测试
pytest step_defs/test_fsm_steps.py -v
```

### 使用标记运行测试
```bash
# 运行标记为 smoke 的测试
pytest -m smoke -v

# 运行标记为 fsm 的测试
pytest -m fsm -v
```

### 有界面模式运行
```bash
pytest --headed -v
```

### 并行运行测试
```bash
pytest -n auto -v
```

## FSM 状态机说明

框架使用有限状态机 (FSM) 来管理页面状态和导航流程，确保测试按照有效的状态转换进行。

### 支持的状态

- **INITIAL**: 初始状态
- **HOME**: 首页
- **CATEGORY**: 分类页
- **LIVE_ROOM**: 直播间
- **SEARCH_RESULTS**: 搜索结果页
- **LOGIN**: 登录页
- **ERROR**: 错误状态

### 状态转换

```
INITIAL → HOME → CATEGORY → LIVE_ROOM
         ↓      ↓           ↓
    SEARCH_RESULTS       HOME
         ↓
    LIVE_ROOM
```

## 配置说明

在 `config.py` 中可以修改测试配置:

```python
class TestConfig(BaseModel):
    base_url: str = "https://www.douyu.com"
    browser: str = "chromium"  # chromium, firefox, webkit
    headless: bool = False     # 无头模式
    slow_mo: int = 0          # 慢速执行（毫秒）
    timeout: int = 30000      # 超时时间（毫秒）
    screenshot_on_failure: bool = True  # 失败时截图
```

## BDD 特性示例

```gherkin
Feature: Douyu Homepage Navigation
  
  Scenario: Access Douyu homepage successfully
    Given I am on the Douyu homepage
    Then I should see the Douyu logo
    And the page title should contain "斗鱼"
```

## 测试报告

测试完成后，会生成以下报告和日志：

- `test-results/report.html`: HTML 测试报告
- `logs/test_*.log`: 详细的测试日志
- `screenshots/`: 失败测试的截图

## 扩展框架

### 添加新页面

1. 在 `pages/` 目录创建新的页面对象类
2. 继承 `BasePage` 类
3. 定义页面元素定位器和操作方法

### 添加新测试场景

1. 在 `features/` 目录创建 `.feature` 文件
2. 编写 BDD 场景
3. 在 `step_defs/` 目录实现步骤定义

### 添加新的 FSM 状态

1. 在 `core/fsm.py` 的 `PageState` 枚举中添加新状态
2. 在 `_setup_transitions()` 中定义新的状态转换
3. 注册状态验证器

## 注意事项

1. 确保网络连接正常，能够访问 www.douyu.com
2. 首次运行需要下载 Playwright 浏览器驱动
3. 某些元素定位器可能因网站更新而需要调整
4. 建议在稳定的网络环境下运行测试

## 许可证

MIT License
