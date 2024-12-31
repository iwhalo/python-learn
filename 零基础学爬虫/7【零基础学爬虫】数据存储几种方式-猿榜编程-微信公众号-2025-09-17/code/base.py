# base.py
import requests


class Sqide:
    """基础的爬虫类"""

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch(self, url, **kwargs):
        """发送请求"""
        response = self.session.get(url, headers=self.headers, **kwargs)
        response.encoding = 'utf-8'
        return response