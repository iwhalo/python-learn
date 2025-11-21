import sys
import os

import requests
import requests.exceptions
import time
import uuid


# 添加项目根目录到 Python 路径，避免相对导入问题
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import HOST,TOKEN_EXPIRE_TIME,REFRESH_TOKEN_BEFORE_EXPIRE,MAX_RETRY_TIMES,RETRY_DELAY



class ApiFunction:
    def __init__(self, session):
        self.session = session
        # 登录-使用公开测试api端点
        self.__url_login = HOST + "/posts"  # 模拟登录接口
        self.__url_message = HOST + "/posts/1"  # 模拟消息通知接口

        # Token管理相关属性
        self._token = None
        self._token_expire_time = None
        self._last_login_params = None

    def api_login(self, password, mobile):
        """模拟登录并获取token"""
        # 保存登录参数用于token刷新
        self._last_login_params = {
            "password": password,
            "mobile": mobile
        }

        # 由于使用公开测试api，这里模拟登录过程
        data = {
            "password": password,
            "mobile": mobile,
            "timestamp": int(time.time())
        }

        try:
            # 模拟登录请求
            result = self.session.post(url=self.__url_login, json=data)
            if result.status_code == 201:  # 创建成功
                # 从模拟响应中生成token（因为测试API不会返回真实token）
                response_data = result.json()
                # 生成模拟token
                self._token = f"mock_token_{mobile}_{uuid.uuid4().hex[:8]}"

                if self._token:
                    # 设置token过期时间
                    self._token_expire_time = time.time() + TOKEN_EXPIRE_TIME
                    print(f"✅ 登录成功，获取到的TOKEN为：{self._token}")
                    print(f"✅ Token过期时间：{time.ctime(self._token_expire_time)}")
                    return self._token
                else:
                    print("❌ API未找到 token 值")
            else:
                print(f"❌ API请求登录失败，状态码：{result.status_code}")
        except Exception as e:
            print(f"❌ 登录请求异常：{str(e)}")

        return None

    def _is_token_expired(self):
        """检查token是否过期"""
        if self._token is None or self._token_expire_time is None:
            return True

        # print("self._token_expire_time",self._token_expire_time)

        # 检查是否接近过期时间
        time_remaining = self._token_expire_time - time.time()
        # print("time_remaining",time_remaining)
        # print("REFRESH_TOKEN_BEFORE_EXPIRE",REFRESH_TOKEN_BEFORE_EXPIRE)
        return time_remaining <= REFRESH_TOKEN_BEFORE_EXPIRE

    def _refresh_token(self):
        """刷新token"""
        if self._last_login_params is None:
            print("❌ 无法刷新token：缺少登录参数")
            return False

        print("🔄 检测到token即将过期，正在刷新token...")
        try:
            new_token = self.api_login(
                self._last_login_params["password"],
                self._last_login_params["mobile"]
            )
            if new_token:
                print("✅ 刷新token成功，新的token为：", new_token)
                return True
            else:
                print("❌ 刷新token失败")
                return False
        except Exception as e:
            print(f"❌ 刷新token时发生错误：{str(e)}")
            return False

    def _make_request_with_retry(self, method, url, **kwargs):
        """带重试的请求方法"""
        for attempt in range(MAX_RETRY_TIMES):
            try:
                # 检查并刷新token
                # print(self._is_token_expired())
                if self._is_token_expired():
                    if not self._refresh_token():
                        print("❌ 无法刷新token，请重新登录")
                        return None

                # 更新请求头中的token
                if "headers" not in kwargs:
                    kwargs["headers"] = {}
                kwargs["headers"]["Authorization"] = "Bearer " + self._token
                print(kwargs["headers"]["Authorization"]) # Bearer mock_token_13800000011_afe22abd

                print(f"🔄 第 {attempt + 1} 次请求: {method} {url}")

                # 执行请求
                if method.upper() == "GET":
                    result = self.session.get(url, **kwargs)
                elif method.upper() == "POST":
                    result = self.session.post(url, **kwargs)
                else:
                    result = self.session.request(method, url, **kwargs)

                print(f"result1:{result.json()}")
                print(f"📡 响应状态码：{result.status_code}")

                # 检查响应状态
                if result.status_code == 401:  # Token过期
                    print("⚠️ 收到401响应，尝试刷新token后重试...")
                    if self._refresh_token():
                        continue  # 重试
                    else:
                        return result
                else:
                    return result

            except requests.exceptions.RequestException as e:
                print(f"❌ 请求异常（尝试 {attempt + 1}/{MAX_RETRY_TIMES}）：{e}")
                if attempt < MAX_RETRY_TIMES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    print("❌ 达到最大重试次数，请求失败")
                    return None

        return None

    def api_message(self, token=None):
        """获取消息通知（支持token自动管理）"""
        if token is not None:
            print("token",token)
            self._token = token
            self._token_expire_time = time.time() + TOKEN_EXPIRE_TIME

        print("self.token",self._token)
        if self._token is None:
            print("❌ 未找到有效token，请先执行登录方法")
            return None

        # 使用带重试的请求方法
        print("使用带重试的请求方法")
        result = self._make_request_with_retry("GET", self.__url_message)
        print(f"result2:{result.json()}")

        if result is None:
            print("❌ API消息通知请求失败：网络错误或重试耗尽")
            return None

        if result.status_code == 200:
            print("✅ API消息通知请求成功")
            return result
        else:
            print(f"❌ API消息通知请求失败，状态码为：{result.status_code}")
            return result

    def get_current_token(self):
        """获取当前token"""
        return self._token

    def get_token_remaining_time(self):
        """获取token剩余时间（秒）"""
        if self._token is None or self._token_expire_time is None:
            return 0
        remaining = self._token_expire_time - time.time()
        return max(0, remaining)

    def logout(self):
        """登出，清除token"""
        self._token = None
        self._token_expire_time = None
        self._last_login_params = None
        print("✅ 已登出，token已清除")