"""基础页面对象模型"""
from playwright.sync_api import Page, expect
from typing import Optional
from douyu_test_framework.core.fsm import FSM, PageState


class BasePage:
    """所有页面对象的基类"""
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        self.page = page
        self.fsm = fsm
        self.timeout = 30000
    
    def navigate(self, url: str):
        """导航到指定URL"""
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
    
    def wait_for_selector(self, selector: str, timeout: Optional[int] = None):
        """等待元素可见"""
        self.page.wait_for_selector(selector, timeout=timeout or self.timeout)
    
    def click(self, selector: str):
        """点击元素"""
        self.page.click(selector)
    
    def fill(self, selector: str, text: str):
        """填充输入框"""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        return self.page.locator(selector).inner_text()
    
    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        try:
            return self.page.locator(selector).is_visible(timeout=5000)
        except:
            return False
    
    def screenshot(self, name: str):
        """截图"""
        self.page.screenshot(path=f"screenshots/{name}.png")
    
    def get_title(self) -> str:
        """获取页面标题"""
        return self.page.title()
    
    def get_url(self) -> str:
        """获取当前URL"""
        return self.page.url
