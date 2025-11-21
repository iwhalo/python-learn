# demo_usage.py
import requests
import sys
import os

# 添加项目根目录到 Python 路径，避免相对导入问题
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.api_function import ApiFunction


def main():
    """演示使用 ApiFunction 类"""
    print("=== Token 管理演示程序 ===\n")

    # 创建 session 和 ApiFunction 实例
    session = requests.Session()
    api_func = ApiFunction(session)

    # 1. 登录获取 token
    print("1. 用户登录")
    print("-" * 30)
    token = api_func.api_login("password123", "13800138000")
    if token:
        print(f"当前 token: {token}")
        print(f"Token 剩余时间: {api_func.get_token_remaining_time():.0f} 秒\n")

    # 2. 使用 token 访问 API
    print("2. 访问消息通知 API")
    print("-" * 30)
    response = api_func.api_message()
    if response and response.status_code == 200:
        print(f"API 响应数据: {response.json()}\n")

    # 3. 显示 token 信息
    print("3. Token 信息")
    print("-" * 30)
    print(f"当前 token: {api_func.get_current_token()}")
    print(f"Token 剩余时间: {api_func.get_token_remaining_time():.0f} 秒\n")

    # 4. 登出
    print("4. 用户登出")
    print("-" * 30)
    api_func.logout()
    print(f"登出后 token: {api_func.get_current_token()}")


if __name__ == "__main__":
    main()