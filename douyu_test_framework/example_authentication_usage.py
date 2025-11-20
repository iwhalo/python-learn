"""
斗鱼登录注册功能使用示例

此文件展示了如何使用登录和注册页面对象进行测试。
注意：这是一个示例文件，不是实际的测试文件。
"""
from playwright.sync_api import sync_playwright
from douyu_test_framework.pages.home_page import HomePage
from douyu_test_framework.pages.login_page import LoginPage
from douyu_test_framework.pages.register_page import RegisterPage
from douyu_test_framework.core.fsm import FSM, PageState


def example_login_with_phone():
    """示例：使用手机号和验证码登录"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        fsm = FSM(page, PageState.INITIAL)
        
        # 导航到首页
        home_page = HomePage(page, fsm)
        home_page.navigate_to_home()
        
        # 打开登录弹窗
        login_page = LoginPage(page, fsm)
        login_page.open_login_modal()
        
        # 使用手机号和验证码登录
        login_page.login_with_phone_and_code("13800138000", "123456")
        
        # 检查登录状态
        if login_page.is_logged_in():
            print("登录成功！")
        else:
            error = login_page.get_error_message()
            print(f"登录失败: {error}")
        
        browser.close()


def example_login_with_password():
    """示例：使用用户名和密码登录"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        fsm = FSM(page, PageState.INITIAL)
        
        # 导航到首页
        home_page = HomePage(page, fsm)
        home_page.navigate_to_home()
        
        # 打开登录弹窗并使用用户名密码登录
        login_page = LoginPage(page, fsm)
        login_page.open_login_modal()
        login_page.login_with_username_and_password("testuser", "password123")
        
        # 检查登录状态
        if login_page.is_logged_in():
            print("登录成功！")
        else:
            error = login_page.get_error_message()
            print(f"登录失败: {error}")
        
        browser.close()


def example_user_registration():
    """示例：用户注册流程"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        fsm = FSM(page, PageState.INITIAL)
        
        # 导航到首页
        home_page = HomePage(page, fsm)
        home_page.navigate_to_home()
        
        # 打开登录弹窗并切换到注册
        login_page = LoginPage(page, fsm)
        login_page.open_login_modal()
        login_page.switch_to_register()
        
        # 执行注册
        register_page = RegisterPage(page, fsm)
        register_page.register(
            phone="13900139000",
            code="123456",
            username="newuser123",
            password="Pass@1234",
            email="newuser@example.com"
        )
        
        # 检查注册结果
        if register_page.is_registration_successful():
            print("注册成功！")
        else:
            error = register_page.get_error_message()
            print(f"注册失败: {error}")
        
        browser.close()


def example_registration_with_validation():
    """示例：注册时的各种验证场景"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        fsm = FSM(page, PageState.INITIAL)
        
        home_page = HomePage(page, fsm)
        home_page.navigate_to_home()
        
        login_page = LoginPage(page, fsm)
        login_page.open_login_modal()
        login_page.switch_to_register()
        
        register_page = RegisterPage(page, fsm)
        
        # 场景1：手机号格式错误
        register_page.fill_phone("123")
        register_page.request_sms_code("123")
        phone_error = register_page.get_phone_error()
        if phone_error:
            print(f"手机号格式错误: {phone_error}")
        
        # 场景2：邮箱格式错误
        register_page.fill_email("invalid-email")
        page.keyboard.press("Tab")  # 触发验证
        page.wait_for_timeout(500)
        email_error = register_page.get_email_error()
        if email_error:
            print(f"邮箱格式错误: {email_error}")
        
        # 场景3：密码不匹配
        register_page.fill_password("Pass@1234")
        register_page.fill_confirm_password("DifferentPass")
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
        password_error = register_page.get_password_error()
        if password_error:
            print(f"密码不匹配: {password_error}")
        
        browser.close()


def example_logout():
    """示例：退出登录"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        fsm = FSM(page, PageState.INITIAL)
        
        home_page = HomePage(page, fsm)
        home_page.navigate_to_home()
        
        # 假设已登录，执行退出操作
        login_page = LoginPage(page, fsm)
        if login_page.is_logged_in():
            login_page.logout()
            print("已退出登录")
        else:
            print("用户未登录")
        
        browser.close()


def example_fsm_state_transitions():
    """示例：FSM状态转换"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        fsm = FSM(page, PageState.INITIAL)
        
        print(f"初始状态: {fsm.get_current_state()}")
        
        # HOME -> LOGIN
        home_page = HomePage(page, fsm)
        home_page.navigate_to_home()
        print(f"当前状态: {fsm.get_current_state()}")
        
        # LOGIN -> REGISTER
        login_page = LoginPage(page, fsm)
        login_page.open_login_modal()
        print(f"当前状态: {fsm.get_current_state()}")
        
        login_page.switch_to_register()
        print(f"当前状态: {fsm.get_current_state()}")
        
        # 查看状态历史
        print(f"状态历史: {[s.value for s in fsm.get_history()]}")
        
        browser.close()


if __name__ == "__main__":
    print("=" * 60)
    print("斗鱼登录注册功能使用示例")
    print("=" * 60)
    print("\n注意：这些示例需要实际的测试账号和验证码。")
    print("在实际测试中，您需要：")
    print("1. 使用有效的测试账号")
    print("2. 处理验证码（可能需要手动输入或使用测试环境）")
    print("3. 根据实际页面结构调整元素定位器")
    print("\n可用的示例函数：")
    print("- example_login_with_phone(): 手机号+验证码登录")
    print("- example_login_with_password(): 用户名+密码登录")
    print("- example_user_registration(): 用户注册")
    print("- example_registration_with_validation(): 注册验证场景")
    print("- example_logout(): 退出登录")
    print("- example_fsm_state_transitions(): FSM状态转换演示")
    print("\n取消注释下面的函数调用来运行示例：")
    print("=" * 60)
    
    # 取消注释下面的行来运行示例
    # example_fsm_state_transitions()
    # example_login_with_phone()
    # example_login_with_password()
    # example_user_registration()
    # example_registration_with_validation()
    # example_logout()
