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
        self.banned_indices = set()  # 被禁用的代理集合,使用集合 存储被禁用的索引 ，确保唯一性

    def get_proxy(self):
        """获取一个可用代理"""
        available_indices = [
            i for i in range(len(self.proxies))
            if i not in self.banned_indices
        ]
        if not available_indices:
            print('所有代理均不可用')
            # 重置禁用列表，重新尝试所有代理
            self.banned_indices = set()
            available_indices = list(range(len(self.proxies)))

        self.current_index = random.choice(available_indices)
        return self.proxies[self.current_index]

    def ban_current_proxy(self):
        """将当前代理加入禁用列表"""
        if self.current_index is not None:
            self.banned_indices.add(self.current_index)
            print(f"代理{self.proxies[self.current_index]}已被禁用")

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


"""
当前方案是最简单和最高效的，因为它：

避免了字典不可哈希的问题

使用索引管理，性能更好

代码更简洁易懂
"""