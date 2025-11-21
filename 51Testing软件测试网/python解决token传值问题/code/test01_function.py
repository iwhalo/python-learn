import requests
import config

from api_function import ApiFunction

class TestFunction:

    def setup(self):
        self.session=requests.session()
        self.api=ApiFunction(self.session)

    def teardown(self):
        self.session.close()

    # 登录
    def test01_login(self,password='123456789',mobile='13800138000'):
        # 调用api_login方法获取到token值
        config.TOKEN=self.api.api_login(password, mobile)
        # 检查token是否为空
        if config.TOKEN:
            print("test成功获取到 token 值：", config.TOKEN)
        else:
            print("test获取 token 失败")

    def test02_message(self):
        if config.TOKEN:
            result=self.api.api_message(config.TOKEN)
            if result.status_code==200:
                print("test消息通知请求成功，状态码为：",result.status_code)
            else:
                print("test消息通知请求失败，状态码为：",result.status_code)
        else:
            print("test未找到有效的token，请先执行登录方法")
