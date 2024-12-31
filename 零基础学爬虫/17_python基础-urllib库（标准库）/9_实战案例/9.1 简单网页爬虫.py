import random
import re
import time
import urllib.parse
from collections import deque
from itertools import count


class SimpleSpider:

    def __init__(self, start_url, domain_limit=True):
        self.start_url = start_url
        self.domain_limit = domain_limit
        self.visited_urls = set()
        self.queue = deque([start_url])
        self.domain = urllib.parse.urlparse(start_url).netloc

        # 创建opener
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        ]

    def is_valid_url(self, url):
        """检查URL是否有效且在允许范围内"""
        try:
            parsed = urllib.parse.urlparse(url)
            # 检查URL是否完整
            if not parsed.scheme or not parsed.netloc:
                return False

            # 检查是否限制在同一域名
            if self.domain_limit and parsed.netloc != self.domain:
                return False

            # 检查URL是否已访问
            if url in self.visited_urls:
                return False

            return True
        except:
            return False

    def extract_links(self, html, base_url):
        """从HTML中提取链接"""
        links = []
        # 使用正则表达式提取链接
        pattern = r'<a[^>]+href=[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(pattern, html):
            link = match.group(1)
            # 转换为绝对URL
            absolute_link = urllib.parse.urljoin(base_url, link)
            if self.is_valid_url(absolute_link):
                links.append(absolute_link)

        return links

    def crawl(self, max_pages=10):
        """开始爬取"""
        count = 0
        while self.queue and count < max_pages:
            # 从队列获取URL
            url = self.queue.popleft()
            print(f"爬取：{url}")

            # 标记为已访问
            self.visited_urls.add(url)

            try:
                # 发送请求
                response = self.opener.open(url, timeout=10)
                html = response.read().decode('utf-8')

                # 处理页面内容
                self.process_page(url, html)

                # 提取新链接
                links = self.extract_links(html, url)
                for link in links:
                    if link not in self.visited_urls and link not in self.queue:
                        self.queue.append(link)

                count += 1

                # 添加延迟，避免请求过快
                time.sleep(random.uniform(1, 3))

            except urllib.error.URLError as e:
                print(f"爬取失败：{e.reason}")
            except Exception as e:
                print(f"处理异常：{e}")
        print(f"爬取完成，共访问{count}个页面")

    def process_page(self, url, html):
        """处理页面内容，可在子类中重写"""
        # 提取标题
        title_match = re.search(
            r'<title>([^<]+)</title>', html
        )
        title = title_match.group(1) if title_match else "Not Title"

        print(f"标题：{title}")
        print(f"内容长度：{len(html)}字符")
        print("-" * 50)


# 使用示例
if __name__ == '__main__':
    spider=SimpleSpider('http://www.python.org')
    spider.crawl(max_pages=5)