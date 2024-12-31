import urllib.request
import random
import time


class ProxyPool:

    def __init__(self):
        # 代理列表（格式：{'http':'http://ip:port','https':'https://ip:port'}）
        self.proxies = [
            {'http': 'http://123.45.67.89:8080', 'https': 'https://123.45.67.89:8080'},
            {'http': 'http://98.76.54.32:8080', 'https': 'https://98.76.54.32:8080'},
        ]
        self.current_proxy = None  # 当前使用的代理
        self.banned_proxies = set()  # 被禁用的代理集合,使用集合 存储代理的字符串表示，确保唯一性

    def get_proxy(self):
        """获取一个可用代理"""
        # available_proxies = [p for p in self.proxies if p not in self.banned_proxies] # TypeError: unhashable type: 'dict'
        """
        原因是：

            self.banned_proxies 是一个 set()（集合）
            
            集合要求其元素必须是可哈希的（hashable）
            
            字典（dict）是不可哈希的类型，不能直接放入集合中
        """
        available_proxies = [p for p in self.proxies if str(p) not in self.banned_proxies] # TypeError: unhashable type: 'dict'
        if not available_proxies:
            print('所有代理均不可用')
            # 重置禁用列表，重新尝试所有代理
            self.banned_proxies = set()
            available_proxies = self.proxies

        self.current_proxy = random.choice(available_proxies)
        return self.current_proxy

    def ban_current_proxy(self):
        """将当前代理加入禁用列表"""
        if self.current_proxy:
            # self.banned_proxies.add(self.current_proxy) # TypeError: unhashable type: 'dict'
            self.banned_proxies.add(str(self.current_proxy))
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