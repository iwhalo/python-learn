"""斗鱼注册页面对象模型"""
from douyu_test_framework.core.base_page import BasePage
from douyu_test_framework.core.fsm import PageState, FSM
from playwright.sync_api import Page
from typing import Optional


class RegisterPage(BasePage):
    """斗鱼注册页面的页面对象"""
    
    # 元素定位器
    REGISTER_MODAL = ".register-modal, .register-container, [class*='register']"
    LOGIN_TAB = "text=登录, .login-tab, [data-type='login']"
    
    # 注册表单字段
    PHONE_INPUT = "input[placeholder*='手机'], input[name='mobile'], input[type='tel']"
    SMS_CODE_INPUT = "input[placeholder*='验证码'], input[name='code'], input[name='sms']"
    USERNAME_INPUT = "input[placeholder*='昵称'], input[placeholder*='用户名'], input[name='username']"
    PASSWORD_INPUT = "input[type='password'], input[name='password']"
    CONFIRM_PASSWORD_INPUT = "input[placeholder*='确认密码'], input[name='confirm_password']"
    EMAIL_INPUT = "input[type='email'], input[name='email']"
    
    # 按钮
    GET_CODE_BUTTON = "button:has-text('获取验证码'), .get-code-btn, button[class*='code']"
    REGISTER_BUTTON = "button:has-text('注册'), .register-btn, button[type='submit']"
    CLOSE_BUTTON = ".close-btn, button[class*='close']"
    
    # 验证和错误提示
    ERROR_MESSAGE = ".error-msg, .error-tip, [class*='error']"
    SUCCESS_MESSAGE = ".success-msg, .success-tip, [class*='success']"
    
    # 错误类型定位器
    PHONE_ERROR = "[data-field='phone'] .error-msg, .phone-error"
    USERNAME_ERROR = "[data-field='username'] .error-msg, .username-error"
    EMAIL_ERROR = "[data-field='email'] .error-msg, .email-error"
    PASSWORD_ERROR = "[data-field='password'] .error-msg, .password-error"
    CODE_ERROR = "[data-field='code'] .error-msg, .code-error"
    
    # 用户协议
    AGREEMENT_CHECKBOX = "input[type='checkbox'], .agreement-checkbox"
    
    def __init__(self, page: Page, fsm: Optional[FSM] = None):
        super().__init__(page, fsm)
        self.url = "https://www.douyu.com"
    
    def open_register_modal(self):
        """打开注册弹窗"""
        register_btn = "text=注册, .register-btn"
        if self.is_visible(register_btn):
            self.click(register_btn)
            self.wait_for_selector(self.REGISTER_MODAL, timeout=5000)
        return self
    
    def switch_to_login(self):
        """切换到登录页面"""
        if self.is_visible(self.LOGIN_TAB):
            self.click(self.LOGIN_TAB)
            if self.fsm:
                self.fsm.transition("switch_to_login")
        return self
    
    def fill_phone(self, phone: str):
        """填写手机号
        
        Args:
            phone: 手机号
        """
        if self.is_visible(self.PHONE_INPUT):
            self.fill(self.PHONE_INPUT, phone)
            self.page.wait_for_timeout(500)
        return self
    
    def request_sms_code(self, phone: str):
        """请求短信验证码
        
        Args:
            phone: 手机号
        """
        self.fill_phone(phone)
        
        if self.is_visible(self.GET_CODE_BUTTON):
            button_text = self.get_text(self.GET_CODE_BUTTON)
            # 检查按钮是否可点击（不是倒计时状态）
            if "秒" not in button_text and "s" not in button_text.lower():
                self.click(self.GET_CODE_BUTTON)
                self.page.wait_for_timeout(1000)
                if self.fsm:
                    self.fsm.transition("verify_phone")
        
        return self
    
    def fill_verification_code(self, code: str):
        """填写验证码
        
        Args:
            code: 验证码
        """
        if self.is_visible(self.SMS_CODE_INPUT):
            self.fill(self.SMS_CODE_INPUT, code)
            self.page.wait_for_timeout(500)
        return self
    
    def fill_username(self, username: str):
        """填写用户名
        
        Args:
            username: 用户昵称
        """
        if self.is_visible(self.USERNAME_INPUT):
            self.fill(self.USERNAME_INPUT, username)
            self.page.wait_for_timeout(500)
        return self
    
    def fill_password(self, password: str):
        """填写密码
        
        Args:
            password: 密码
        """
        if self.is_visible(self.PASSWORD_INPUT):
            self.fill(self.PASSWORD_INPUT, password)
            self.page.wait_for_timeout(500)
        return self
    
    def fill_confirm_password(self, password: str):
        """填写确认密码
        
        Args:
            password: 确认密码
        """
        if self.is_visible(self.CONFIRM_PASSWORD_INPUT):
            self.fill(self.CONFIRM_PASSWORD_INPUT, password)
            self.page.wait_for_timeout(500)
        return self
    
    def fill_email(self, email: str):
        """填写邮箱
        
        Args:
            email: 邮箱地址
        """
        if self.is_visible(self.EMAIL_INPUT):
            self.fill(self.EMAIL_INPUT, email)
            self.page.wait_for_timeout(500)
        return self
    
    def accept_agreement(self):
        """接受用户协议"""
        if self.is_visible(self.AGREEMENT_CHECKBOX):
            checkbox = self.page.locator(self.AGREEMENT_CHECKBOX)
            if not checkbox.is_checked():
                self.click(self.AGREEMENT_CHECKBOX)
        return self
    
    def register(self, phone: str, code: str, username: str, password: str, 
                 email: str = None, confirm_password: str = None):
        """执行注册流程
        
        Args:
            phone: 手机号
            code: 短信验证码
            username: 用户昵称
            password: 密码
            email: 邮箱（可选）
            confirm_password: 确认密码（可选，默认与password相同）
        """
        if confirm_password is None:
            confirm_password = password
        
        # 填写表单
        self.fill_phone(phone)
        self.fill_verification_code(code)
        self.fill_username(username)
        self.fill_password(password)
        
        if self.is_visible(self.CONFIRM_PASSWORD_INPUT):
            self.fill_confirm_password(confirm_password)
        
        if email and self.is_visible(self.EMAIL_INPUT):
            self.fill_email(email)
        
        # 接受协议
        self.accept_agreement()
        
        # 点击注册按钮
        if self.is_visible(self.REGISTER_BUTTON):
            self.click(self.REGISTER_BUTTON)
            self.page.wait_for_timeout(2000)
            
            # 检查注册结果
            if self.is_registration_successful():
                if self.fsm:
                    self.fsm.transition("successful_register")
            elif self.has_error():
                if self.fsm:
                    self.fsm.transition("registration_failed")
        
        return self
    
    def is_register_modal_visible(self) -> bool:
        """检查注册弹窗是否可见"""
        return self.is_visible(self.REGISTER_MODAL)
    
    def is_registration_successful(self) -> bool:
        """检查注册是否成功"""
        # 注册成功可能会跳转到首页或显示成功消息
        return self.is_visible(self.SUCCESS_MESSAGE) or not self.is_register_modal_visible()
    
    def has_error(self) -> bool:
        """检查是否有错误"""
        return self.is_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self) -> str:
        """获取错误消息"""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_phone_error(self) -> str:
        """获取手机号错误提示"""
        if self.is_visible(self.PHONE_ERROR):
            return self.get_text(self.PHONE_ERROR)
        return ""
    
    def get_username_error(self) -> str:
        """获取用户名错误提示"""
        if self.is_visible(self.USERNAME_ERROR):
            return self.get_text(self.USERNAME_ERROR)
        return ""
    
    def get_email_error(self) -> str:
        """获取邮箱错误提示"""
        if self.is_visible(self.EMAIL_ERROR):
            return self.get_text(self.EMAIL_ERROR)
        return ""
    
    def get_password_error(self) -> str:
        """获取密码错误提示"""
        if self.is_visible(self.PASSWORD_ERROR):
            return self.get_text(self.PASSWORD_ERROR)
        return ""
    
    def get_code_error(self) -> str:
        """获取验证码错误提示"""
        if self.is_visible(self.CODE_ERROR):
            return self.get_text(self.CODE_ERROR)
        return ""
    
    def close_register_modal(self):
        """关闭注册弹窗"""
        if self.is_visible(self.CLOSE_BUTTON):
            self.click(self.CLOSE_BUTTON)
        return self
    
    def is_register_page(self) -> bool:
        """验证当前是否在注册页面"""
        return self.is_register_modal_visible() and "douyu.com" in self.get_url()
