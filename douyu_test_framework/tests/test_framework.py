"""验证框架设置的简单测试"""
import pytest
from douyu_test_framework.core.fsm import FSM, PageState
from douyu_test_framework.pages.home_page import HomePage


class TestFrameworkSetup:
    """测试框架基本功能"""
    
    def test_fsm_initialization(self, page, fsm):
        """测试FSM可以初始化"""
        assert fsm is not None
        assert fsm.current_state == PageState.INITIAL
    
    def test_fsm_transitions(self):
        """测试FSM状态转换"""
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            fsm = FSM(page, PageState.INITIAL)
            
            # 测试有效转换
            fsm.transition("navigate_home")
            assert fsm.current_state == PageState.HOME
            
            # 测试转换历史
            assert len(fsm.history) == 2
            assert fsm.history[0] == PageState.INITIAL
            assert fsm.history[1] == PageState.HOME
            
            browser.close()
    
    def test_fsm_invalid_transition(self):
        """测试FSM拒绝无效转换"""
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            fsm = FSM(page, PageState.INITIAL)
            
            # 尝试无效转换
            with pytest.raises(ValueError):
                fsm.transition("invalid_action")
            
            browser.close()
    
    def test_page_object_creation(self, page, fsm):
        """测试可以创建页面对象"""
        home_page = HomePage(page, fsm)
        assert home_page is not None
        assert home_page.page == page
        assert home_page.fsm == fsm


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
