"""斗鱼首页页面对象模型"""
from douyu_test_framework.core.base_page import BasePage
from douyu_test_framework.core.fsm import PageState
from playwright.sync_api import Page
from typing import Optional
from douyu_test_framework.core.fsm import FSM


class HomePage(BasePage):
    """斗鱼首页的页面对象"""
    
    # 元素定位器
    LOGO = ".Title-header-logo"
    SEARCH_INPUT = "input[placeholder*='搜索']"
    SEARCH_BUTTON = ".SearchBtn"
    CATEGORY_NAV = ".NavMenu-item"
    LOGIN_BUTTON = ".SignIn, .dy-login"
    HOT_LIVE_ROOMS = ".DyListCover-wrap, .recommend-item"
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        super().__init__(page, fsm)
        self.url = "https://www.douyu.com"
    
    def navigate_to_home(self):
        """导航到首页"""
        self.navigate(self.url)
        if self.fsm:
            self.fsm.transition("navigate_home")
        return self
    
    def search(self, keyword: str):
        """搜索内容"""
        # 等待搜索输入框可用
        self.wait_for_selector(self.SEARCH_INPUT, timeout=10000)
        self.fill(self.SEARCH_INPUT, keyword)
        self.page.keyboard.press("Enter")
        
        if self.fsm:
            self.fsm.transition("search")
        return self
    
    def select_category(self, category_name: str):
        """从导航栏选择分类"""
        categories = self.page.locator(self.CATEGORY_NAV)
        count = categories.count()
        
        for i in range(count):
            if category_name.lower() in categories.nth(i).inner_text().lower():
                categories.nth(i).click()
                if self.fsm:
                    self.fsm.transition("select_category")
                return self
        
        raise ValueError(f"Category '{category_name}' not found")
    
    def click_login(self):
        """点击登录按钮"""
        if self.is_visible(self.LOGIN_BUTTON):
            self.click(self.LOGIN_BUTTON)
            if self.fsm:
                self.fsm.transition("click_login")
        return self
    
    def get_hot_live_rooms(self) -> list:
        """获取热门直播间列表"""
        self.wait_for_selector(self.HOT_LIVE_ROOMS, timeout=10000)
        rooms = self.page.locator(self.HOT_LIVE_ROOMS)
        return [rooms.nth(i) for i in range(min(rooms.count(), 10))]
    
    def enter_first_live_room(self):
        """进入第一个直播间"""
        rooms = self.get_hot_live_rooms()
        if rooms:
            rooms[0].click()
            self.page.wait_for_load_state("networkidle")
            if self.fsm:
                self.fsm.transition("enter_live_room")
        return self
    
    def is_home_page(self) -> bool:
        """验证当前页面是否为首页"""
        return self.is_visible(self.LOGO) and "douyu.com" in self.get_url()
    
    def get_page_title(self) -> str:
        """获取首页标题"""
        return self.get_title()
