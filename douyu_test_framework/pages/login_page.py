"""斗鱼登录页面对象模型"""
from douyu_test_framework.core.base_page import BasePage
from douyu_test_framework.core.fsm import PageState, FSM
from playwright.sync_api import Page
from typing import Optional


class LoginPage(BasePage):
    """斗鱼登录页面的页面对象"""
    
    # 元素定位器
    # 鱼头像登录入口（右上角的鱼头像）
    AVATAR_LOGIN_ENTRY = ".fishIcon, .fish-icon, [class*='fish'], img[src*='fish'], .dy-avatar-icon"
    # 备用登录入口
    LOGIN_ENTRY = ".SignIn, .dy-login, text=登录, button:has-text('登录')"
    
    LOGIN_MODAL = ".login-Slide-module, .login-modal, [class*='login'], .dy-modal"
    PHONE_TAB = "[data-type='phone'], .tab-phone, text=手机登录, button:has-text('手机登录')"
    PASSWORD_TAB = "[data-type='password'], .tab-password, text=密码登录, button:has-text('密码登录')"
    REGISTER_TAB = "text=注册, .register-tab, [data-type='register'], button:has-text('注册')"
    
    # 手机号+验证码登录
    PHONE_INPUT = "input[placeholder*='手机'], input[name='mobile'], input[type='tel']"
    SMS_CODE_INPUT = "input[placeholder*='验证码'], input[name='code'], input[name='sms']"
    GET_CODE_BUTTON = "button:has-text('获取验证码'), .get-code-btn, button[class*='code']"
    
    # 用户名+密码登录
    USERNAME_INPUT = "input[placeholder*='昵称'], input[placeholder*='用户名'], input[name='username']"
    PASSWORD_INPUT = "input[type='password'], input[name='password']"
    
    # 通用按钮
    LOGIN_BUTTON = "button:has-text('登录'), .login-btn, button[type='submit']"
    CLOSE_BUTTON = ".close-btn, button[class*='close']"
    
    # 错误提示
    ERROR_MESSAGE = ".error-msg, .error-tip, [class*='error']"
    
    # 登录成功后的用户信息
    USER_AVATAR = ".user-avatar, .header-avatar"
    USER_NAME = ".user-name, .nickname"
    LOGOUT_BUTTON = "text=退出, .logout, button:has-text('退出登录')"
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        super().__init__(page, fsm)
        self.url = "https://www.douyu.com"
    
    def open_login_modal(self):
        """打开登录弹窗"""
        # 先尝试点击鱼头像入口
        if self.is_visible(self.AVATAR_LOGIN_ENTRY):
            print("找到鱼头像登录入口")
            self.click(self.AVATAR_LOGIN_ENTRY)
            self.page.wait_for_timeout(1500)
        # 如果没有鱼头像，尝试其他登录入口
        elif self.is_visible(self.LOGIN_ENTRY):
            print("找到备用登录入口")
            self.click(self.LOGIN_ENTRY)
            self.page.wait_for_timeout(1500)
        else:
            # 尝试通过更宽松的选择器查找
            print("尝试查找任何可能的登录入口")
            possible_selectors = [
                "img[alt*='鱼']",
                "img[alt*='头像']",
                "[class*='avatar']",
                "[class*='user']",
                ".fish, .Fish",
                "text=/登.*录/"
            ]
            for selector in possible_selectors:
                if self.is_visible(selector):
                    print(f"找到元素: {selector}")
                    self.click(selector)
                    self.page.wait_for_timeout(1500)
                    break
        
        # 等待登录弹窗或相关元素出现
        self.page.wait_for_timeout(1000)
        
        if self.fsm:
            self.fsm.transition("click_login")
        return self
    
    def switch_to_phone_login(self):
        """切换到手机号登录标签"""
        if self.is_visible(self.PHONE_TAB):
            self.click(self.PHONE_TAB)
            self.page.wait_for_timeout(500)
        return self
    
    def switch_to_password_login(self):
        """切换到密码登录标签"""
        if self.is_visible(self.PASSWORD_TAB):
            self.click(self.PASSWORD_TAB)
            self.page.wait_for_timeout(500)
        return self
    
    def switch_to_register(self):
        """切换到注册页面"""
        if self.is_visible(self.REGISTER_TAB):
            self.click(self.REGISTER_TAB)
            if self.fsm:
                self.fsm.transition("switch_to_register")
        return self
    
    def login_with_phone_and_code(self, phone: str, code: str):
        """使用手机号和验证码登录
        
        Args:
            phone: 手机号
            code: 短信验证码
        """
        self.switch_to_phone_login()
        
        if self.is_visible(self.PHONE_INPUT):
            self.fill(self.PHONE_INPUT, phone)
        
        if self.is_visible(self.SMS_CODE_INPUT):
            self.fill(self.SMS_CODE_INPUT, code)
        
        if self.is_visible(self.LOGIN_BUTTON):
            self.click(self.LOGIN_BUTTON)
            self.page.wait_for_timeout(2000)
            
            # 检查是否登录成功
            if self.is_logged_in():
                if self.fsm:
                    self.fsm.transition("successful_login")
            else:
                if self.fsm:
                    self.fsm.transition("login_failed")
        
        return self
    
    def login_with_username_and_password(self, username: str, password: str):
        """使用用户名和密码登录
        
        Args:
            username: 用户昵称
            password: 密码
        """
        self.switch_to_password_login()
        
        if self.is_visible(self.USERNAME_INPUT):
            self.fill(self.USERNAME_INPUT, username)
        
        if self.is_visible(self.PASSWORD_INPUT):
            self.fill(self.PASSWORD_INPUT, password)
        
        if self.is_visible(self.LOGIN_BUTTON):
            self.click(self.LOGIN_BUTTON)
            self.page.wait_for_timeout(2000)
            
            # 检查是否登录成功
            if self.is_logged_in():
                if self.fsm:
                    self.fsm.transition("successful_login")
            else:
                if self.fsm:
                    self.fsm.transition("login_failed")
        
        return self
    
    def request_sms_code(self, phone: str):
        """请求短信验证码
        
        Args:
            phone: 手机号
        """
        if self.is_visible(self.PHONE_INPUT):
            self.fill(self.PHONE_INPUT, phone)
        
        if self.is_visible(self.GET_CODE_BUTTON):
            self.click(self.GET_CODE_BUTTON)
            self.page.wait_for_timeout(1000)
            if self.fsm:
                self.fsm.transition("request_phone_code")
        
        return self
    
    def is_login_modal_visible(self) -> bool:
        """检查登录弹窗是否可见"""
        return self.is_visible(self.LOGIN_MODAL)
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self.is_visible(self.USER_AVATAR) or self.is_visible(self.USER_NAME)
    
    def get_error_message(self) -> str:
        """获取错误消息"""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def logout(self):
        """退出登录"""
        if self.is_logged_in():
            # 点击用户头像打开菜单
            if self.is_visible(self.USER_AVATAR):
                self.click(self.USER_AVATAR)
                self.page.wait_for_timeout(500)
            
            # 点击退出登录
            if self.is_visible(self.LOGOUT_BUTTON):
                self.click(self.LOGOUT_BUTTON)
                self.page.wait_for_timeout(1000)
        
        return self
    
    def close_login_modal(self):
        """关闭登录弹窗"""
        if self.is_visible(self.CLOSE_BUTTON):
            self.click(self.CLOSE_BUTTON)
        return self
    
    def is_login_page(self) -> bool:
        """验证当前是否在登录页面"""
        return self.is_login_modal_visible() and "douyu.com" in self.get_url()
