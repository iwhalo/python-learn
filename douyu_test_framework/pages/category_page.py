"""斗鱼分类页页面对象模型"""
from douyu_test_framework.core.base_page import BasePage
from playwright.sync_api import Page
from typing import Optional
from douyu_test_framework.core.fsm import FSM


class CategoryPage(BasePage):
    """斗鱼分类页的页面对象"""
    
    # 元素定位器
    CATEGORY_TITLE = ".Title-header, .CategoryHeader"
    LIVE_ROOM_ITEMS = ".DyListCover-wrap, .ListItem"
    FILTER_OPTIONS = ".CategoryFilter-item, .filter-item"
    LOAD_MORE = ".LoadMore, .load-more-btn"
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        super().__init__(page, fsm)
    
    def get_category_name(self) -> str:
        """获取当前分类名称"""
        try:
            return self.get_text(self.CATEGORY_TITLE)
        except:
            return "Category"
    
    def get_live_rooms(self, count: int = 10) -> list:
        """获取分类中的直播间列表"""
        self.wait_for_selector(self.LIVE_ROOM_ITEMS, timeout=10000)
        rooms = self.page.locator(self.LIVE_ROOM_ITEMS)
        actual_count = min(rooms.count(), count)
        return [rooms.nth(i) for i in range(actual_count)]
    
    def select_live_room(self, index: int = 0):
        """通过索引选择直播间"""
        rooms = self.get_live_rooms()
        if index < len(rooms):
            rooms[index].click()
            self.page.wait_for_load_state("networkidle")
            if self.fsm:
                self.fsm.transition("select_live_room")
        return self
    
    def apply_filter(self, filter_name: str):
        """应用筛选选项"""
        if self.is_visible(self.FILTER_OPTIONS):
            filters = self.page.locator(self.FILTER_OPTIONS)
            count = filters.count()
            
            for i in range(count):
                if filter_name.lower() in filters.nth(i).inner_text().lower():
                    filters.nth(i).click()
                    self.page.wait_for_timeout(1000)
                    break
        return self
    
    def is_category_page(self) -> bool:
        """验证当前页面是否为分类页"""
        return self.is_visible(self.LIVE_ROOM_ITEMS)
    
    def go_back_home(self):
        """返回首页"""
        self.page.go_back()
        if self.fsm:
            self.fsm.transition("go_home")
        return self
