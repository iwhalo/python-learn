"""斗鱼直播间页面对象模型"""
from douyu_test_framework.core.base_page import BasePage
from playwright.sync_api import Page
from typing import Optional
from douyu_test_framework.core.fsm import FSM


class LiveRoomPage(BasePage):
    """斗鱼直播间的页面对象"""
    
    # 元素定位器
    ROOM_TITLE = ".Title-header h1, .room-title"
    STREAMER_NAME = ".Barrage-nickName, .anchor-name"
    CHAT_INPUT = ".ChatInput, .chat-input"
    FOLLOW_BUTTON = ".FollowButton, .follow-btn"
    SHARE_BUTTON = ".ShareButton, .share-btn"
    VIEWER_COUNT = ".ViewerCount, .viewer-num"
    VIDEO_PLAYER = "video, .player-video"
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        super().__init__(page, fsm)
    
    def get_room_title(self) -> str:
        """获取直播间标题"""
        try:
            self.wait_for_selector(self.ROOM_TITLE, timeout=10000)
            return self.get_text(self.ROOM_TITLE)
        except:
            return ""
    
    def get_streamer_name(self) -> str:
        """获取主播名称"""
        try:
            if self.is_visible(self.STREAMER_NAME):
                return self.get_text(self.STREAMER_NAME)
        except:
            pass
        return ""
    
    def is_video_playing(self) -> bool:
        """检查视频播放器是否存在"""
        return self.is_visible(self.VIDEO_PLAYER)
    
    def get_viewer_count(self) -> str:
        """获取观众数量"""
        try:
            if self.is_visible(self.VIEWER_COUNT):
                return self.get_text(self.VIEWER_COUNT)
        except:
            pass
        return "0"
    
    def click_follow(self):
        """点击关注按钮"""
        if self.is_visible(self.FOLLOW_BUTTON):
            self.click(self.FOLLOW_BUTTON)
        return self
    
    def click_share(self):
        """点击分享按钮"""
        if self.is_visible(self.SHARE_BUTTON):
            self.click(self.SHARE_BUTTON)
        return self
    
    def send_chat_message(self, message: str):
        """发送聊天消息（可能需要登录）"""
        if self.is_visible(self.CHAT_INPUT):
            self.fill(self.CHAT_INPUT, message)
            self.page.keyboard.press("Enter")
        return self
    
    def is_live_room_page(self) -> bool:
        """验证当前页面是否为直播间页面"""
        return self.is_visible(self.VIDEO_PLAYER) or "/topic/" in self.get_url()
    
    def go_back_home(self):
        """返回首页"""
        from douyu_test_framework.pages.home_page import HomePage
        home = HomePage(self.page, self.fsm)
        home.navigate_to_home()
        return home
