"""
Token 传值问题演示程序
演示完整的 token 管理流程，包括登录、token使用、刷新和过期处理
"""

import requests
import time
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.api_function import ApiFunction
from config.config import HOST, TOKEN_EXPIRE_TIME, REFRESH_TOKEN_BEFORE_EXPIRE


class TokenDemo:
    def __init__(self):
        self.session = requests.Session()
        self.api = ApiFunction(self.session)
        print("🚀 Token 演示程序初始化完成")
        print(f"API 地址: {HOST}")
        print(f"Token 过期时间: {TOKEN_EXPIRE_TIME} 秒")
        print(f"提前刷新时间: {REFRESH_TOKEN_BEFORE_EXPIRE} 秒")
        print("-" * 60)

    def demo_basic_token_flow(self):
        """演示基本的 token 流程"""
        print("\n" + "=" * 50)
        print("1. 基本 Token 流程演示")
        print("=" * 50)

        # 步骤1: 用户登录获取 token
        print("\n📝 步骤1: 用户登录")
        print("-" * 30)
        token = self.api.api_login("123456789", "13800000011")

        if not token:
            print("❌ 登录失败，终止演示")
            return False

        print(f"✅ 登录成功，获得 Token: {token}")
        print(f"⏰ Token 剩余时间: {self.api.get_token_remaining_time():.0f} 秒")

        # 步骤2: 使用 token 访问受保护的 API
        print("\n📝 步骤2: 访问受保护的 API")
        print("-" * 30)
        response = self.api.api_message()

        if response and response.status_code == 200:
            print("✅ API 访问成功")
            data = response.json()
            print(f"📄 响应数据: {data}")
        else:
            print("❌ API 访问失败")

        # 步骤3: 显示当前 token 状态
        print("\n📝 步骤3: Token 状态检查")
        print("-" * 30)
        current_token = self.api.get_current_token()
        remaining_time = self.api.get_token_remaining_time()
        print(f"🔑 当前 Token: {current_token}")
        print(f"⏰ 剩余时间: {remaining_time:.0f} 秒")

        return True

    def demo_token_refresh_mechanism(self):
        """演示 token 刷新机制"""
        print("\n" + "=" * 50)
        print("2. Token 刷新机制演示")
        print("=" * 50)

        # 先登录获取 token
        print("\n📝 先进行登录")
        print("-" * 30)
        original_token = self.api.api_login("123456789", "13800000011")
        if not original_token:
            return False

        print(f"原始 Token: {original_token}")

        # 模拟 token 即将过期的情况
        print("\n📝 模拟 Token 即将过期")
        print("-" * 30)

        # 为了演示，我们临时修改过期时间
        print("🔄 手动触发 Token 刷新检查...")

        # 检查当前 token 状态
        is_expired = self.api._is_token_expired()
        print(f"Token 是否即将过期: {is_expired}")

        if is_expired:
            print("🔄 检测到 Token 即将过期，自动刷新...")
            refresh_result = self.api._refresh_token()
            if refresh_result:
                new_token = self.api.get_current_token()
                print(f"✅ Token 刷新成功")
                print(f"🆕 新 Token: {new_token}")
            else:
                print("❌ Token 刷新失败")
        else:
            print("ℹ️ Token 尚未过期，无需刷新")
            print(f"⏰ 剩余时间: {self.api.get_token_remaining_time():.0f} 秒")

    def demo_concurrent_requests(self):
        """演示并发请求场景"""
        print("\n" + "=" * 50)
        print("3. 并发请求场景演示")
        print("=" * 50)

        # 先登录
        print("\n📝 用户登录")
        print("-" * 30)
        if not self.api.api_login("123456789", "13800000011"):
            return False

        print("🔄 开始模拟并发请求...")

        # 模拟多个并发请求
        requests_count = 5
        success_count = 0

        for i in range(requests_count):
            print(f"\n📡 请求 #{i + 1}")
            print(f"⏰ Token 剩余时间: {self.api.get_token_remaining_time():.0f} 秒")

            response = self.api.api_message()
            if response and response.status_code == 200:
                success_count += 1
                print(f"✅ 请求 #{i + 1} 成功")
            else:
                status_code = response.status_code if response else "无响应"
                print(f"❌ 请求 #{i + 1} 失败，状态码: {status_code}")

            # 短暂延迟，模拟真实场景
            time.sleep(0.5)

        print(f"\n📊 并发请求结果: {success_count}/{requests_count} 成功")

        return success_count == requests_count

    def demo_token_lifecycle(self):
        """演示完整的 token 生命周期"""
        print("\n" + "=" * 50)
        print("4. Token 完整生命周期演示")
        print("=" * 50)

        # 阶段1: 初始状态
        print("\n📝 阶段1: 初始状态")
        print("-" * 30)
        initial_token = self.api.get_current_token()
        print(f"🔑 初始 Token: {initial_token}")
        print("💡 说明: 用户尚未登录，没有有效 Token")

        # 阶段2: 登录获取 token
        print("\n📝 阶段2: 用户登录")
        print("-" * 30)
        token = self.api.api_login("123456789", "13800000011")
        if token:
            print(f"✅ 登录成功，获得 Token")
            print(f"⏰ Token 有效期: {TOKEN_EXPIRE_TIME} 秒")

        # 阶段3: 使用 token
        print("\n📝 阶段3: 使用 Token 访问 API")
        print("-" * 30)
        for i in range(3):
            print(f"\n🔄 第 {i + 1} 次 API 调用")
            response = self.api.api_message()
            if response and response.status_code == 200:
                print(f"✅ API 调用成功")
                print(f"⏰ Token 剩余时间: {self.api.get_token_remaining_time():.0f} 秒")
            time.sleep(1)

        # 阶段4: 登出清理
        print("\n📝 阶段4: 用户登出")
        print("-" * 30)
        self.api.logout()
        final_token = self.api.get_current_token()
        print(f"🔑 登出后 Token: {final_token}")
        print("✅ Token 已清理，生命周期结束")

    def demo_error_scenarios(self):
        """演示错误场景处理"""
        print("\n" + "=" * 50)
        print("5. 错误场景处理演示")
        print("=" * 50)

        # 场景1: 未登录直接访问 API
        print("\n📝 场景1: 未登录直接访问 API")
        print("-" * 30)
        self.api.logout()  # 确保没有 token
        response = self.api.api_message()
        if not response:
            print("✅ 正确处理: 检测到未登录状态，拒绝访问")
        else:
            print("❌ 处理异常: 未登录状态下不应该能访问 API")

        # 场景2: 使用无效 token
        print("\n📝 场景2: 使用无效 Token")
        print("-" * 30)
        invalid_token = "invalid_token_12345"
        response = self.api.api_message(invalid_token)
        print("💡 说明: 系统会尝试使用无效 token，但最终会失败")

        # 场景3: 网络异常重试
        print("\n📝 场景3: 重试机制演示")
        print("-" * 30)
        print("💡 说明: 当网络异常或服务器返回 5xx 错误时，系统会自动重试")
        print(f"🔄 最大重试次数: {MAX_RETRY_TIMES}")
        print(f"⏰ 重试延迟: {RETRY_DELAY} 秒")

    def run_all_demos(self):
        """运行所有演示"""
        print("🎬 开始 Token 传值问题演示程序")
        print("=" * 60)

        demos = [
            ("基本 Token 流程", self.demo_basic_token_flow),
            ("Token 刷新机制", self.demo_token_refresh_mechanism),
            ("并发请求场景", self.demo_concurrent_requests),
            ("Token 完整生命周期", self.demo_token_lifecycle),
            ("错误场景处理", self.demo_error_scenarios),
        ]

        results = {}

        for demo_name, demo_func in demos:
            try:
                print(f"\n🎯 开始演示: {demo_name}")
                result = demo_func()
                results[demo_name] = result
                print(f"✅ {demo_name} 演示完成")
            except Exception as e:
                print(f"❌ {demo_name} 演示失败: {e}")
                results[demo_name] = False
            finally:
                print("-" * 60)
                time.sleep(1)  # 演示间暂停

        # 显示演示结果总结
        print("\n" + "=" * 60)
        print("📊 演示结果总结")
        print("=" * 60)

        for demo_name, result in results.items():
            status = "✅ 成功" if result else "❌ 失败"
            print(f"{demo_name:20} {status}")

        successful_demos = sum(results.values())
        total_demos = len(results)

        print(f"\n🎉 演示完成: {successful_demos}/{total_demos} 个演示成功")

        if successful_demos == total_demos:
            print("🌟 所有演示均成功完成！")
        else:
            print("💡 部分演示失败，请检查相关问题")

        print("\n🔚 Token 传值问题演示程序结束")

    def cleanup(self):
        """清理资源"""
        self.session.close()
        print("🧹 资源清理完成")


def main():
    """主函数"""
    demo = TokenDemo()

    try:
        demo.run_all_demos()
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断演示")
    except Exception as e:
        print(f"\n\n❌ 演示程序异常: {e}")
    finally:
        demo.cleanup()


if __name__ == "__main__":
    main()