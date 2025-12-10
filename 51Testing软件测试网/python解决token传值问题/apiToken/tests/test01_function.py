import requests

import sys
import os

# 添加项目根目录到 Python 路径，避免相对导入问题
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 现在可以直接导入配置和 ApiFunction

from api.api_function import ApiFunction


class TestFunction:

    def setup_method(self, method):
        """测试初始化 - pytest会在每个测试方法前自动调用"""
        print("***********************初始化操作开始***********************")
        self.session = requests.session()
        self.api = ApiFunction(self.session)
        self.test_token = None  # 用于存储测试token
        print("***********************初始化操作结束***********************")

    def teardown_method(self, method):
        """测试清理 - pytest会在每个测试方法后自动调用"""
        print("***********************测试清理操作开始***********************")
        self.session.close()
        print("***********************测试清理操作结束***********************")

    def test01_login(self, password="123456789", mobile="13800000011"):
        """测试登录并获取token"""
        print(f"\n==== 测试登录功能 ====")
        print(f"手机号：{mobile}")
        print(f"密码：{password}")

        # 调用api_login方法获取token值
        token = self.api.api_login(password, mobile)

        # 检查token是否获取成功
        if token is not None:
            print("✅ test成功获取到token值：", token)
            print(f"✅ token剩余时间：{self.api.get_token_remaining_time():.0f}秒")
            self.test_token = token  # 保存token供其他测试使用
            return True
        else:
            print("❌ test获取token失败")
            return False

    def test02_message(self):
        """测试获取消息通知"""
        print(f"\n==== 测试消息通知功能 ====")

        # 使用实例中的token，而不是导入的TOKEN
        current_token = self.api.get_current_token()
        if current_token is None:
            print("❌ test未找到有效的token，请先执行登录方法")
            return False

        print(f"使用token：{current_token}")
        result = self.api.api_message(current_token)

        if result and result.status_code == 200:
            print(f"✅ test消息通知请求成功，状态码为：{result.status_code}")
            print(f"✅ 响应内容：{result.json()}")
            print(f"✅ token剩余时间：{self.api.get_token_remaining_time():.0f}秒")
            return True
        else:
            status_code = result.status_code if result else "无响应"
            print(f"❌ test消息通知请求失败，状态码：{status_code}")
            return False

    def test03_token_expiration_handling(self):
        """测试token过期处理机制"""
        print(f"\n==== 测试token过期处理机制 ====")

        # 先登录获取token
        if not self.test01_login():
            return False

        print(f"\n--- 测试token剩余时间查询 ---")
        remaining_time = self.api.get_token_remaining_time()
        print(f"当前token剩余时间：{remaining_time:.0f}秒")

        print("\n--- 测试正常消息获取 ---")
        result1 = self.api.api_message()
        if result1 and result1.status_code == 200:
            print(f"✅ 正常消息获取成功")
        else:
            print(f"❌ 正常消息获取失败")
            return False

        print(f"\n--- 测试token刷新机制 ---")
        # 模拟token即将过期的情况
        print("模拟token刷新过程...")
        original_token = self.api.get_current_token()
        print("original_token",original_token)

        # 手动触发刷新（这里只是演示，实际刷新由内部逻辑处理）
        print("当前token状态检查...")
        if self.api._is_token_expired():
            print("检测到token需要刷新")
            if self.api._refresh_token():
                new_token = self.api.get_current_token()
                if new_token != original_token:
                    print(f"✅ token刷新成功，新的token：{new_token}")
                else:
                    print(f"ℹ️ token刷新完成（测试环境下token可能相同）")
            else:
                print(f"❌ token刷新失败")
        else:
            print(f"ℹ️ token尚未过期，无需刷新")

        print("\n--- 测试重试机制 ---")
        # 测试带重试的请求
        result2 = self.api.api_message()
        if result2 and result2.status_code == 200:
            print("✅ 重试机制测试通过")
            return True
        else:
            print("❌ 重试机制测试失败")
            return False

    def test04_concurrent_requests(self):
        """测试并发请求场景下的token管理"""
        print(f"\n==== 测试并发请求场景 ====")

        # 先登录

        if not self.test01_login():
            return False

        print(f"模拟连续多次请求...")
        success_count = 0

        for i in range(5):
            print(f"\n第 {i + 1} 次请求")
            result = self.api.api_message()
            if result and result.status_code == 200:
                success_count += 1
                print(f"✅ 第 {i + 1} 次请求成功")
                # 显示当前token状态
                remaining_time = self.api.get_token_remaining_time()
                print(f"   token剩余时间：{remaining_time:.0f}秒")
            else:
                status_code = result.status_code if result else "无响应"
                print(f"❌ 第 {i + 1} 次请求失败，状态码：{status_code}")

        print(f"\n并发测试结果：{success_count}/5 次请求成功")
        return success_count >= 3  # 允许部分失败，因为测试API可能有限制

    def test05_token_management(self):
        """测试token管理功能"""
        print(f"\n==== 测试token管理功能 ====")

        # 测试1: 初始状态
        print("\n1. 初始状态检查")
        initial_token = self.api.get_current_token()
        initial_remaining = self.api.get_token_remaining_time()
        print(f"初始token: {initial_token}")
        print(f"初始剩余时间: {initial_remaining:.0f}秒")

        # 测试2: 登录后状态
        print("\n2. 登录后状态检查")
        if self.test01_login():
            after_login_token = self.api.get_current_token()
            after_login_remaining = self.api.get_token_remaining_time()
            print(f"登录后token: {after_login_token}")
            print(f"登录后剩余时间: {after_login_remaining:.0f}秒")

            # 测试3: 登出功能
            print("\n3. 登出功能测试")
            self.api.logout()
            after_logout_token = self.api.get_current_token()
            print(f"登出后token: {after_logout_token}")

            if after_logout_token is None:
                print("✅ 登出功能测试通过")
                return True
            else:
                print("❌ 登出功能测试失败")
                return False
        else:
            print("❌ 登录失败，跳过后续测试")
            return False

    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始执行测试套件...")

        # 手动调用setup（因为直接运行不是通过pytest）
        self.setup_method(None)

        test_results = {}

        try:
            # 执行基础功能测试
            print("\n" + "=" * 60)
            test_results['login'] = self.test01_login()

            # 如果登录成功，执行其他测试
            if test_results['login']:
                print("\n" + "=" * 60)
                test_results['message'] = self.test02_message()

                print("\n" + "=" * 60)
                test_results['token_expiration'] = self.test03_token_expiration_handling()

                print("\n" + "=" * 60)
                test_results['concurrent'] = self.test04_concurrent_requests()

                print("\n" + "=" * 60)
                test_results['token_management'] = self.test05_token_management()

            else:
                print("❌ 跳过后续测试，因为登录失败")

            # 输出测试总结
            print("\n" + "=" * 60)
            print("📊 测试总结:")
            print("=" * 60)
            for test_name, result in test_results.items():
                status = "✅ 通过" if result else "❌ 失败"
                print(f"{test_name:20} {status}")

            total_passed = sum(test_results.values())
            total_tests = len(test_results)
            print(f"\n总成绩: {total_passed}/{total_tests} 通过")

            if total_passed == total_tests:
                print("🎉 所有测试通过！")
            else:
                print("💡 部分测试失败，请检查相关问题")

        except Exception as e:
            print(f"❌ 测试执行过程中发生异常: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.teardown_method(None)
            print(f"\n测试套件执行完毕，会话已关闭")


if __name__ == '__main__':
    # 创建测试实例并运行
    test_runner = TestFunction()
    test_runner.run_all_tests()