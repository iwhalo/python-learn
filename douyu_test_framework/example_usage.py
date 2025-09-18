"""
斗鱼测试框架 - 快速入门示例

本示例演示框架的基本用法。
"""
from playwright.sync_api import sync_playwright
from douyu_test_framework.core.fsm import FSM, PageState
from douyu_test_framework.pages.home_page import HomePage
from douyu_test_framework.pages.live_room_page import LiveRoomPage
from douyu_test_framework.utils.logger import logger


def example_basic_navigation():
    """示例：在斗鱼网站上进行基本导航"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        # 初始化FSM
        fsm = FSM(page, PageState.INITIAL)
        
        # 导航到首页
        logger.info("Navigating to Douyu homepage")
        home_page = HomePage(page, fsm)
        home_page.navigate_to_home()
        
        # 验证首页
        assert home_page.is_home_page(), "Should be on homepage"
        logger.info(f"Page title: {home_page.get_page_title()}")
        
        # 检查FSM状态
        assert fsm.get_current_state() == PageState.HOME
        logger.info(f"FSM State: {fsm.get_current_state().value}")
        
        # 搜索内容
        logger.info("Searching for '英雄联盟'")
        home_page.search("英雄联盟")
        page.wait_for_timeout(2000)
        
        # 返回首页
        page.go_back()
        page.wait_for_timeout(1000)
        
        # 进入直播间
        logger.info("Entering first live room")
        try:
            home_page.enter_first_live_room()
            page.wait_for_timeout(3000)
            
            live_room = LiveRoomPage(page, fsm)
            logger.info(f"Room title: {live_room.get_room_title()}")
            logger.info(f"Viewer count: {live_room.get_viewer_count()}")
        except Exception as e:
            logger.error(f"Failed to enter live room: {e}")
        
        # 检查FSM历史
        logger.info(f"FSM History: {[s.value for s in fsm.get_history()]}")
        
        browser.close()
        logger.info("Test completed successfully")


def example_fsm_state_transitions():
    """示例：FSM状态转换"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 初始化FSM
        fsm = FSM(page, PageState.INITIAL)
        
        logger.info("Testing FSM state transitions")
        
        # 转换: INITIAL → HOME
        logger.info("Transition: INITIAL → HOME")
        fsm.transition("navigate_home")
        assert fsm.get_current_state() == PageState.HOME
        
        # 转换: HOME → SEARCH_RESULTS
        logger.info("Transition: HOME → SEARCH_RESULTS")
        fsm.transition("search")
        assert fsm.get_current_state() == PageState.SEARCH_RESULTS
        
        # 转换: SEARCH_RESULTS → HOME
        logger.info("Transition: SEARCH_RESULTS → HOME")
        fsm.transition("go_home")
        assert fsm.get_current_state() == PageState.HOME
        
        # 测试无效转换
        logger.info("Testing invalid transition")
        try:
            # 这应该失败: HOME → ERROR 需要特定动作
            fsm.current_state = PageState.LIVE_ROOM
            fsm.transition("click_login")  # 从LIVE_ROOM无效
            logger.error("Should have raised ValueError")
        except ValueError as e:
            logger.info(f"Correctly caught invalid transition: {e}")
        
        # 打印历史
        logger.info(f"State history: {[s.value for s in fsm.get_history()]}")
        
        browser.close()
        logger.info("FSM test completed")


if __name__ == "__main__":
    print("Douyu Test Framework - Examples\n")
    print("=" * 60)
    
    print("\n[1] Running basic navigation example...")
    print("-" * 60)
    example_basic_navigation()
    
    print("\n[2] Running FSM state transitions example...")
    print("-" * 60)
    example_fsm_state_transitions()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
