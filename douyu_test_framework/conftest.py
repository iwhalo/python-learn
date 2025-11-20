"""Pytest配置和固件"""
import pytest
from playwright.sync_api import Browser, Page, BrowserContext
from douyu_test_framework.core.fsm import FSM, PageState
from douyu_test_framework.config import config
import os
from pathlib import Path


def pytest_configure(config):
    """配置Pytest"""
    # 获取项目根目录
    root_dir = Path(__file__).parent
    
    # 创建所有必要的目录
    directories = [
        "screenshots",
        "test-results",  # 确保这个目录存在
        "videos",
        "logs",
        "reports"
    ]

    for dir_name in directories:
        dir_path = root_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"确保目录存在: {dir_path}")


def pytest_sessionstart(session):
    """在测试会话开始前执行"""
    # 再次确保目录存在
    root_dir = Path(__file__).parent
    test_results_dir = root_dir / "test-results"
    test_results_dir.mkdir(parents=True, exist_ok=True)

    # 处理 pytest-html 报告路径
    html_option = getattr(session.config.option, 'htmlpath', None)
    if html_option:
        html_path = Path(html_option)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"确保HTML报告目录存在: {html_path.parent}")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "locale": "zh-CN",
        "timezone_id": "Asia/Shanghai",
        # 添加视频录制
        "record_video_dir": "videos/",
        "record_har_path": "test-results/network.har"
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """配置浏览器启动参数"""
    return {
        **browser_type_launch_args,
        "headless": config.headless,
        "slow_mo": config.slow_mo,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    }


@pytest.fixture(scope="function")
def page(browser: Browser, browser_context_args):
    """为每个测试创建新页面"""
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    page.set_default_timeout(config.timeout)

    # 设置用户代理以避免被检测为自动化
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    yield page

    # 关闭上下文和页面
    try:
        context.close()
    except Exception as e:
        print(f"关闭浏览器上下文时出错: {e}")


@pytest.fixture(scope="function")
def fsm(page: Page):
    """为每个测试创建FSM实例"""
    fsm_instance = FSM(page, PageState.INITIAL)

    # 注册验证器
    from douyu_test_framework.pages.home_page import HomePage
    from douyu_test_framework.pages.category_page import CategoryPage
    from douyu_test_framework.pages.live_room_page import LiveRoomPage
    from douyu_test_framework.pages.login_page import LoginPage
    from douyu_test_framework.pages.register_page import RegisterPage

    fsm_instance.register_validator(
        PageState.HOME,
        lambda p: HomePage(p).is_home_page()
    )
    fsm_instance.register_validator(
        PageState.CATEGORY,
        lambda p: CategoryPage(p).is_category_page()
    )
    fsm_instance.register_validator(
        PageState.LIVE_ROOM,
        lambda p: LiveRoomPage(p).is_live_room_page()
    )
    fsm_instance.register_validator(
        PageState.LOGIN,
        lambda p: LoginPage(p).is_login_page()
    )
    fsm_instance.register_validator(
        PageState.REGISTER,
        lambda p: RegisterPage(p).is_register_page()
    )

    return fsm_instance


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """测试失败时截图"""
    yield

    # 检查测试是否失败
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        # 确保截图目录存在
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        screenshot_path = f"screenshots/{request.node.name}.png"
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"测试失败截图已保存: {screenshot_path}")
        except Exception as e:
            print(f"截图保存失败: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """捕获测试结果的钩子"""
    outcome = yield
    rep = outcome.get_result()

    # 为每个测试阶段存储结果
    setattr(item, f"rep_{rep.when}", rep)

    return rep


# 添加处理 pytest-html 报告目录的钩子
@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    """设置HTML报告标题"""
    report.title = "斗鱼测试框架测试报告"


def pytest_html_results_table_header(cells):
    """自定义HTML报告表头"""
    cells.insert(2, "测试描述")
    cells.insert(1, "持续时间")


def pytest_html_results_table_row(report, cells):
    """自定义HTML报告表格行"""
    cells.insert(2, "功能测试")
    cells.insert(1, f"{report.duration:.2f}s")