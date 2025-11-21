import random
import time

from config import HOST,TOKEN

class ApiFunction:
    def __init__(self,session):
        self.session=session
        # 登录
        self.__url_login=HOST+"访问方向"
        # 消息通知
        self.__url_message=HOST+"访问方向"

    # 登录
    def api_login(self,password,mobile):
        data={
            "password":password,
            "mobile":mobile
        }
        result=self.session.post(url=self.__url_login,data=data)
        # 检查响应
        if result.status_code==200:
            data=result.json()
            if 'data' in data:
                token=data['data']['token']
                print("登录成功，获取到的TOKEN为：",token)
                return token
            else:
                print("api未找到 token 值")
        else:
            print("api请求登录失败，状态码：",result.status_code)
        return None

    # 获取消息通知
    def api_message(self,token):
        if token is None:
            print("未找到有效的token，请先执行登录方法")
            return

        headers={
            "Authorization":"Bearer "+token,
            "Content-Type":"application/json",
            "Accept":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Connection":"keep-alive",
            "Cache-Control":"max-age=0",
            "TE":"Trailers",
            "X-Request-ID":f"{random.randint(1000000, 9999999)}-{int(time.time())}",
            "X-Access-Token":token


        }

        result=self.session.get(url=self.__url_message,headers=headers)
        return result