"""斗鱼搜索结果页面对象模型"""
from douyu_test_framework.core.base_page import BasePage
from playwright.sync_api import Page
from typing import Optional
from douyu_test_framework.core.fsm import FSM


class SearchResultsPage(BasePage):
    """斗鱼搜索结果页的页面对象"""
    
    # 元素定位器
    SEARCH_RESULTS = ".SearchResult-item, .search-item"
    RESULT_TITLE = ".SearchResult-title, .result-title"
    NO_RESULTS = ".NoResults, .no-result"
    RESULT_TABS = ".SearchTab, .search-tab"
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        super().__init__(page, fsm)
    
    def get_search_results(self, count: int = 10) -> list:
        """获取搜索结果项"""
        try:
            self.wait_for_selector(f"{self.SEARCH_RESULTS}, {self.NO_RESULTS}", timeout=10000)
            
            if self.is_visible(self.NO_RESULTS):
                return []
            
            results = self.page.locator(self.SEARCH_RESULTS)
            actual_count = min(results.count(), count)
            return [results.nth(i) for i in range(actual_count)]
        except:
            return []
    
    def get_results_count(self) -> int:
        """获取结果总数"""
        results = self.get_search_results()
        return len(results)
    
    def select_result(self, index: int = 0):
        """通过索引选择搜索结果"""
        results = self.get_search_results()
        if index < len(results):
            results[index].click()
            self.page.wait_for_load_state("networkidle")
            if self.fsm:
                self.fsm.transition("select_search_result")
        return self
    
    def switch_tab(self, tab_name: str):
        """切换搜索结果标签页"""
        if self.is_visible(self.RESULT_TABS):
            tabs = self.page.locator(self.RESULT_TABS)
            count = tabs.count()
            
            for i in range(count):
                if tab_name.lower() in tabs.nth(i).inner_text().lower():
                    tabs.nth(i).click()
                    self.page.wait_for_timeout(1000)
                    break
        return self
    
    def is_search_results_page(self) -> bool:
        """验证当前页面是否为搜索结果页"""
        return "search" in self.get_url().lower() or self.is_visible(self.SEARCH_RESULTS)
    
    def has_results(self) -> bool:
        """检查是否有搜索结果"""
        return len(self.get_search_results()) > 0
