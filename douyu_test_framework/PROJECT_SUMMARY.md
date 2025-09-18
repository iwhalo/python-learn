# 斗鱼测试框架 - 项目总览

## 🎯 项目简介

这是一个基于 **Python + Playwright + Pytest + BDD + FSM** 的现代化自动化测试框架，专门针对斗鱼网站(www.douyu.com)设计。

### 核心特性

✅ **有限状态机 (FSM)**: 智能管理页面状态和导航流程  
✅ **行为驱动开发 (BDD)**: 使用 Gherkin 语法编写可读性强的测试场景  
✅ **页面对象模型 (POM)**: 清晰的代码结构，易于维护  
✅ **现代化工具链**: Playwright 提供强大的浏览器自动化能力  
✅ **详细报告**: HTML 测试报告、日志、失败截图  

## 📁 项目结构

```
douyu_test_framework/
│
├── 📄 config.py                 # 全局配置文件
├── 📄 conftest.py              # Pytest fixtures 和钩子
├── 📄 pytest.ini               # Pytest 配置
├── 📄 requirements.txt         # Python 依赖
├── 📄 run_tests.py            # 主测试运行脚本
├── 📄 run_tests.bat           # Windows 批处理脚本
├── 📄 example_usage.py        # 使用示例
├── 📄 README.md               # 项目说明文档
├── 📄 QUICKSTART.md           # 快速入门指南
├── 📄 .gitignore              # Git 忽略配置
│
├── 📂 core/                   # 核心框架代码
│   ├── __init__.py
│   ├── base_page.py          # 基础页面类
│   └── fsm.py                # 有限状态机实现
│
├── 📂 pages/                  # 页面对象模型
│   ├── __init__.py
│   ├── home_page.py          # 首页对象
│   ├── category_page.py      # 分类页对象
│   ├── live_room_page.py     # 直播间对象
│   └── search_results_page.py # 搜索结果页对象
│
├── 📂 features/               # BDD 特性文件
│   ├── __init__.py
│   ├── homepage.feature      # 首页测试场景
│   ├── live_room.feature     # 直播间测试场景
│   └── fsm_states.feature    # FSM 状态测试场景
│
├── 📂 step_defs/              # BDD 步骤定义
│   ├── __init__.py
│   ├── test_homepage_steps.py    # 首页步骤实现
│   ├── test_live_room_steps.py   # 直播间步骤实现
│   └── test_fsm_steps.py         # FSM 步骤实现
│
├── 📂 utils/                  # 工具类
│   ├── __init__.py
│   ├── helpers.py            # 辅助函数
│   ├── logger.py             # 日志工具
│   └── report.py             # 报告生成器
│
└── 📂 tests/                  # 单元测试
    ├── __init__.py
    └── test_framework.py     # 框架测试
```

## 🚀 快速开始

### 一键运行（推荐）

```bash
cd D:\PycharmProjects\python-learn\douyu_test_framework
python run_tests.py --install
```

### 分步操作

```bash
# 1. 安装依赖
pip install -r requirements.txt
python -m playwright install chromium

# 2. 运行测试
python run_tests.py

# 或使用 pytest
pytest -v --headed
```

## 🎨 FSM 状态机设计

### 状态定义

```python
class PageState(Enum):
    INITIAL = "initial"          # 初始状态
    HOME = "home"                # 首页
    CATEGORY = "category"        # 分类页
    LIVE_ROOM = "live_room"      # 直播间
    SEARCH_RESULTS = "search_results"  # 搜索结果
    LOGIN = "login"              # 登录页
    ERROR = "error"              # 错误状态
```

### 状态转换流程

```
┌─────────┐
│ INITIAL │
└────┬────┘
     │ navigate_home
     ▼
┌─────────┐
│  HOME   ├──search────────────────┐
└────┬────┘                         │
     │                              ▼
     ├─select_category──→ ┌──────────────────┐
     │                    │ SEARCH_RESULTS   │
     │                    └────────┬─────────┘
     ├─enter_live_room──┐         │
     │                  │         │ select_search_result
     ▼                  ▼         │
┌──────────┐      ┌──────────┐   │
│ CATEGORY │      │LIVE_ROOM │◄──┘
└────┬─────┘      └────┬─────┘
     │                 │
     └─────go_home─────┘
```

## 📚 核心组件说明

### 1. FSM (core/fsm.py)

**功能**：
- 管理页面状态转换
- 验证导航流程的有效性
- 记录状态历史
- 防止非法状态转换

**示例**：
```python
fsm = FSM(page, PageState.INITIAL)
fsm.transition("navigate_home")  # INITIAL → HOME
fsm.transition("search")         # HOME → SEARCH_RESULTS
print(fsm.get_history())        # [INITIAL, HOME, SEARCH_RESULTS]
```

### 2. 页面对象模型

**BasePage (core/base_page.py)**：
- 所有页面对象的基类
- 提供通用操作方法（点击、填写、等待等）

**具体页面对象**：
- `HomePage`: 首页操作（搜索、导航、进入直播间）
- `CategoryPage`: 分类页操作（筛选、选择直播间）
- `LiveRoomPage`: 直播间操作（查看信息、关注、分享）
- `SearchResultsPage`: 搜索结果操作（查看结果、筛选）

### 3. BDD 测试场景

**Feature 文件示例**：
```gherkin
Feature: Douyu Homepage Navigation
  
  Scenario: Access Douyu homepage successfully
    Given I am on the Douyu homepage
    Then I should see the Douyu logo
    And the page title should contain "斗鱼"
```

**步骤定义示例**：
```python
@given('I am on the Douyu homepage')
def navigate_to_homepage(page, fsm):
    home_page = HomePage(page, fsm)
    home_page.navigate_to_home()
```

## 🔧 配置选项

编辑 `config.py`:

```python
class TestConfig(BaseModel):
    base_url: str = "https://www.douyu.com"
    browser: str = "chromium"        # chromium/firefox/webkit
    headless: bool = False           # True=无头模式
    slow_mo: int = 0                 # 延迟执行(ms)
    timeout: int = 30000             # 超时时间(ms)
    screenshot_on_failure: bool = True
    video_on_failure: bool = False
```

## 📊 测试报告

运行测试后自动生成：

1. **HTML 报告**: `test-results/report.html`
   - 详细的测试结果
   - 失败原因
   - 执行时间统计

2. **日志文件**: `logs/test_YYYYMMDD_HHMMSS.log`
   - 详细的执行日志
   - 调试信息

3. **截图**: `screenshots/`
   - 测试失败时自动截图
   - 便于问题定位

## 🎯 测试覆盖场景

### 首页测试
- ✅ 访问首页
- ✅ 验证页面元素
- ✅ 搜索功能
- ✅ 分类导航
- ✅ 进入直播间

### 直播间测试
- ✅ 查看直播间信息
- ✅ 视频播放器验证
- ✅ 观众人数显示
- ✅ 返回首页

### FSM 状态测试
- ✅ 状态转换验证
- ✅ 非法转换拦截
- ✅ 状态历史记录

## 💡 扩展指南

### 添加新页面对象

1. 在 `pages/` 创建新文件
2. 继承 `BasePage`
3. 定义元素定位器
4. 实现页面操作方法

```python
class NewPage(BasePage):
    ELEMENT = ".selector"
    
    def do_something(self):
        self.click(self.ELEMENT)
```

### 添加新测试场景

1. 在 `features/` 创建 `.feature` 文件
2. 编写 Gherkin 场景
3. 在 `step_defs/` 实现步骤定义

### 添加 FSM 状态

1. 在 `PageState` 枚举添加新状态
2. 在 `_setup_transitions()` 定义转换
3. 注册状态验证器

## 🐛 故障排查

### 问题：浏览器未安装
```bash
python -m playwright install chromium
```

### 问题：元素找不到
- 检查网络连接
- 增加超时时间
- 更新选择器

### 问题：测试失败
1. 查看 `screenshots/` 截图
2. 查看 `logs/` 日志文件
3. 运行单个测试定位问题

## 📈 性能优化

### 并行执行
```bash
pip install pytest-xdist
pytest -n auto -v
```

### 无头模式
修改 `config.py`:
```python
headless: bool = True
```

## 🎓 最佳实践

1. ✅ 使用 FSM 确保导航流程正确
2. ✅ 失败时自动截图
3. ✅ 详细的日志记录
4. ✅ 页面对象模型保持代码整洁
5. ✅ BDD 场景提高可读性
6. ✅ 使用 fixtures 共享资源

## 📞 技术栈

- **Python 3.8+**
- **Playwright 1.40+**: 浏览器自动化
- **Pytest 7.4+**: 测试框架
- **Pytest-BDD 6.1+**: BDD 支持
- **Pydantic 2.5+**: 配置管理

## 📝 示例命令

```bash
# 运行所有测试
pytest -v

# 运行特定功能
pytest step_defs/test_homepage_steps.py -v

# 有界面模式
pytest --headed -v

# 生成 HTML 报告
pytest --html=test-results/report.html -v

# 并行执行
pytest -n 4 -v

# 运行标记的测试
pytest -m smoke -v
```

## 🎉 总结

这个框架提供了：
- ✅ 完整的测试自动化解决方案
- ✅ 清晰的代码结构
- ✅ 强大的状态管理（FSM）
- ✅ 可读性强的 BDD 场景
- ✅ 详细的测试报告
- ✅ 易于扩展和维护

立即开始测试：
```bash
cd douyu_test_framework
python run_tests.py --install
```

祝测试愉快！🚀
