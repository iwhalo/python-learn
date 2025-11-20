"""斗鱼首页页面对象模型"""
from douyu_test_framework.core.base_page import BasePage
from douyu_test_framework.core.fsm import PageState
from playwright.sync_api import Page
from typing import Optional
from douyu_test_framework.core.fsm import FSM


class HomePage(BasePage):
    """斗鱼首页的页面对象"""
    
    # 元素定位器
    LOGO = ".Title-header-logo, .header-logo, img[alt*='斗鱼'], [class*='logo']"
    SEARCH_INPUT = "input[placeholder*='搜索'], input[type='text'][class*='search']"
    SEARCH_BUTTON = ".SearchBtn, button[class*='search']"
    CATEGORY_NAV = ".NavMenu-item, .nav-menu-item, [class*='nav'] a"
    # 鱼头像登录/用户入口
    AVATAR_ICON = ".fishIcon, .fish-icon, [class*='fish'], .dy-avatar-icon, img[src*='fish']"
    LOGIN_BUTTON = ".SignIn, .dy-login, text=登录"
    HOT_LIVE_ROOMS = ".DyListCover-wrap, .recommend-item, [class*='live-item']"
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        super().__init__(page, fsm)
        self.url = "https://www.douyu.com"
    
    def navigate_to_home(self):
        """导航到首页"""
        print(f"正在导航到: {self.url}")
        self.navigate(self.url)
        # 等待页面加载完成，斗鱼会自动在URL后面添加dyshid参数
        # 输入网址https://www.douyu.com/后浏览器会自动在网址后面增加/?dyshid=0-ba439b3aea51951c74a2f47c00071701
        self.page.wait_for_load_state("networkidle")
        # 额外等待以确保页面完全渲染
        self.page.wait_for_timeout(2000)
        current_url = self.page.url
        print(f"当前URL: {current_url}")
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
        # 斗鱼会在URL后面添加dyshid参数，所以只检查基本域名
        current_url = self.get_url()
        is_douyu = "douyu.com" in current_url
        # 检查是否是首页（不是其他子页面）
        is_homepage = current_url.rstrip('/').split('?')[0].endswith('douyu.com')
        return self.is_visible(self.LOGO) and is_douyu and is_homepage
    
    def get_page_title(self) -> str:
        """获取首页标题"""
        return self.get_title()
