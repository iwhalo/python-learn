"""测试的辅助工具"""
from playwright.sync_api import Page
import time
from typing import Callable


class WaitHelper:
    """等待操作的辅助类"""
    
    @staticmethod
    def wait_until(condition: Callable[[], bool], timeout: int = 30, 
                   interval: float = 0.5) -> bool:
        """等待直到条件满足"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition():
                return True
            time.sleep(interval)
        return False
    
    @staticmethod
    def wait_for_page_load(page: Page, timeout: int = 30):
        """等待页面完全加载"""
        page.wait_for_load_state("networkidle", timeout=timeout * 1000)


class ElementHelper:
    """元素操作的辅助类"""
    
    @staticmethod
    def is_element_present(page: Page, selector: str, timeout: int = 5) -> bool:
        """检查元素是否存在"""
        try:
            page.wait_for_selector(selector, timeout=timeout * 1000)
            return True
        except:
            return False
    
    @staticmethod
    def safe_click(page: Page, selector: str, timeout: int = 10) -> bool:
        """安全地点击元素"""
        try:
            page.wait_for_selector(selector, timeout=timeout * 1000)
            page.click(selector)
            return True
        except:
            return False
    
    @staticmethod
    def get_elements_count(page: Page, selector: str) -> int:
        """获取匹配选择器的元素数量"""
        try:
            return page.locator(selector).count()
        except:
            return 0


class ScreenshotHelper:
    """截图的辅助类"""
    
    @staticmethod
    def take_screenshot(page: Page, name: str, directory: str = "screenshots"):
        """截图并保存"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{directory}/{name}_{timestamp}.png"
        page.screenshot(path=filename)
        return filename
    
    @staticmethod
    def take_full_page_screenshot(page: Page, name: str, 
                                   directory: str = "screenshots"):
        """全页面截图"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{directory}/{name}_full_{timestamp}.png"
        page.screenshot(path=filename, full_page=True)
        return filename
