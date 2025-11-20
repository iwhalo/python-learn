"""
测试验证脚本 - 验证登录注册功能修复

运行此脚本来快速验证框架修复：
python douyu_test_framework/verify_auth_fix.py
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def verify_imports():
    """验证所有模块可以正确导入"""
    print("=" * 60)
    print("1. 验证模块导入...")
    print("=" * 60)
    
    try:
        from douyu_test_framework.core.fsm import FSM, PageState
        print("✓ FSM模块导入成功")
        
        # 检查新增的状态
        assert hasattr(PageState, 'LOGIN'), "缺少LOGIN状态"
        assert hasattr(PageState, 'REGISTER'), "缺少REGISTER状态"
        assert hasattr(PageState, 'PHONE_VERIFY'), "缺少PHONE_VERIFY状态"
        print("✓ FSM新增状态验证通过")
        
        from douyu_test_framework.pages.home_page import HomePage
        print("✓ HomePage模块导入成功")
        
        from douyu_test_framework.pages.login_page import LoginPage
        print("✓ LoginPage模块导入成功")
        
        from douyu_test_framework.pages.register_page import RegisterPage
        print("✓ RegisterPage模块导入成功")
        
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False


def verify_page_objects():
    """验证页面对象的关键属性"""
    print("\n" + "=" * 60)
    print("2. 验证页面对象...")
    print("=" * 60)
    
    try:
        from douyu_test_framework.pages.login_page import LoginPage
        from douyu_test_framework.pages.register_page import RegisterPage
        from douyu_test_framework.pages.home_page import HomePage
        
        # 验证LoginPage的关键定位器
        assert hasattr(LoginPage, 'AVATAR_LOGIN_ENTRY'), "LoginPage缺少AVATAR_LOGIN_ENTRY"
        assert hasattr(LoginPage, 'LOGIN_MODAL'), "LoginPage缺少LOGIN_MODAL"
        print("✓ LoginPage定位器验证通过")
        
        # 验证RegisterPage的关键定位器
        assert hasattr(RegisterPage, 'REGISTER_MODAL'), "RegisterPage缺少REGISTER_MODAL"
        assert hasattr(RegisterPage, 'PHONE_INPUT'), "RegisterPage缺少PHONE_INPUT"
        print("✓ RegisterPage定位器验证通过")
        
        # 验证HomePage的更新
        assert hasattr(HomePage, 'AVATAR_ICON'), "HomePage缺少AVATAR_ICON"
        print("✓ HomePage定位器验证通过")
        
        return True
    except Exception as e:
        print(f"✗ 页面对象验证失败: {e}")
        return False


def verify_step_definitions():
    """验证步骤定义文件存在"""
    print("\n" + "=" * 60)
    print("3. 验证步骤定义文件...")
    print("=" * 60)
    
    step_file = project_root / "step_defs" / "test_authentication_steps.py"
    if step_file.exists():
        print(f"✓ 步骤定义文件存在: {step_file}")
        
        # 读取文件检查关键步骤
        content = step_file.read_text(encoding='utf-8')
        
        # 不应该有重复的 'I am on the Douyu homepage' 定义
        if '@given(\'I am on the Douyu homepage\')' in content:
            print("✗ 警告: test_authentication_steps.py中不应该有重复的'I am on the Douyu homepage'定义")
            print("  该步骤应该只在test_homepage_steps.py中定义")
            return False
        else:
            print("✓ 没有重复的步骤定义")
        
        # 检查是否有其他必要的步骤
        required_steps = [
            '@when(\'I click on the login button\')',
            '@when(\'I switch to register tab\')',
            '@given(\'I am logged in\')'
        ]
        
        for step in required_steps:
            if step in content:
                print(f"✓ 找到步骤: {step}")
            else:
                print(f"✗ 缺少步骤: {step}")
                return False
        
        return True
    else:
        print(f"✗ 步骤定义文件不存在: {step_file}")
        return False


def verify_feature_file():
    """验证特性文件"""
    print("\n" + "=" * 60)
    print("4. 验证特性文件...")
    print("=" * 60)
    
    feature_file = project_root / "features" / "authentication.feature"
    if feature_file.exists():
        print(f"✓ 特性文件存在: {feature_file}")
        
        content = feature_file.read_text(encoding='utf-8')
        
        # 检查是否有语言声明（不应该有）
        if content.startswith('# language:') or content.startswith('#language:'):
            print("✗ 警告: 特性文件不应该有语言声明")
            return False
        
        # 检查是否以Feature开头
        if content.strip().startswith('Feature:'):
            print("✓ 特性文件格式正确")
        else:
            print("✗ 特性文件格式不正确")
            return False
        
        return True
    else:
        print(f"✗ 特性文件不存在: {feature_file}")
        return False


def main():
    """主验证流程"""
    print("\n" + "=" * 60)
    print("斗鱼测试框架 - 登录注册功能修复验证")
    print("=" * 60)
    
    results = []
    
    # 执行所有验证
    results.append(("模块导入", verify_imports()))
    results.append(("页面对象", verify_page_objects()))
    results.append(("步骤定义", verify_step_definitions()))
    results.append(("特性文件", verify_feature_file()))
    
    # 输出结果
    print("\n" + "=" * 60)
    print("验证结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:12s}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ 所有验证通过！框架修复成功。")
        print("\n下一步:")
        print("1. 清除pytest缓存: rm -rf .pytest_cache douyu_test_framework/.pytest_cache")
        print("2. 运行测试: python run_tests.py")
        print("3. 或运行特定测试: pytest -v step_defs/test_authentication_steps.py -k login")
        return 0
    else:
        print("\n✗ 部分验证失败，请检查上述错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
