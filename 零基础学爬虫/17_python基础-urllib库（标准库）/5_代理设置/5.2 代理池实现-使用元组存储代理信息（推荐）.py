import urllib.request
import random
import time


class ProxyPool:

    def __init__(self):
        # 使用元组代替字典
        self.proxies = [
            ('http://123.45.67.89:8080', 'https://123.45.67.89:8080'),
            ('http://98.76.54.32:8080', 'https://98.76.54.32:8080'),
        ]
        self.current_proxy = None
        self.banned_proxies = set()

    def get_proxy(self):
        """获取一个可用代理"""
        available_proxies = [p for p in self.proxies if p not in self.banned_proxies]
        if not available_proxies:
            print('所有代理均不可用')
            self.banned_proxies = set()
            available_proxies = self.proxies

        self.current_proxy = random.choice(available_proxies)
        # 转换为字典格式返回
        return {'http': self.current_proxy[0], 'https': self.current_proxy[1]}

    def ban_current_proxy(self):
        """将当前代理加入禁用列表"""
        if self.current_proxy:
            # self.banned_proxies.add(self.current_proxy)
            self.banned_proxies.add(self.current_proxy)
            print(f"代理{self.current_proxy}已被禁用")

    def request(self, url, max_retries=3):
        """使用代理发送请求"""
        for i in range(max_retries):
            proxy = self.get_proxy()
            print(f"使用代理：{proxy}")

            try:
                # 创建代理处理器
                proxy_handler=urllib.request.ProxyHandler(proxy)
                opener=urllib.request.build_opener(proxy_handler)

                # 发送请求
                response=opener.open(url,timeout=10)

                return response.read().decode('utf-8')

            except Exception as e:
                print(f"请求失败：{e}")
                self.ban_current_proxy()

                if i==max_retries-1:
                    print("达到最大重试次数")
                    return None

                # 等待一段时间再重试
                time.sleep(2)


"""
请求处理流程：

创建代理处理器 ProxyHandler(proxy)

构建 opener build_opener(proxy_handler)

发送请求并设置10秒超时

成功则返回解码后的内容

失败则禁用代理并重试
"""
if __name__ == '__main__':
    proxy_pool=ProxyPool()
    result=proxy_pool.request(url="http://www.baidu.com")
    print(result)