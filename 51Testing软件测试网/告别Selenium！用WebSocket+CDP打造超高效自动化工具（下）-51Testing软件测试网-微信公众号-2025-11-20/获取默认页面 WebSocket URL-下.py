import atexit
import json
import os
import subprocess
import time
from socket import create_connection
from urllib.parse import urlparse

import requests
import websocket


class Browser:
    # 设置默认值
    _chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    _remote_debugging_port = 9222
    _user_data_dir = r'C:\Program Files\Google\Chrome\Application\chrome_profile'
    _remote_allow_origins = "*"
    _headless = False
    _window_size = ("1280", "768")

    def __init__(self,
                 chrome_path=None,
                 remote_debugging_port=None,
                 user_data_dir=None,
                 remote_allow_origins=None,
                 headless=None,
                 window_size=None):
        self._chrome_path = chrome_path or self._chrome_path
        self._remote_debugging_port = remote_debugging_port or self._remote_debugging_port
        self._user_data_dir = user_data_dir or self._user_data_dir
        self._remote_allow_origins = remote_allow_origins or self._remote_allow_origins
        self._headless = headless or self._headless
        self._window_size = window_size or self._window_size
        self.__process = None

        # 注册清理函数
        atexit.register(self.close_chrome)

    @property
    def chrome_path(self):
        return self._chrome_path

    @chrome_path.setter
    def chrome_path(self, value):
        self._chrome_path = value

    @property
    def remote_debugging_port(self):
        return self._remote_debugging_port

    @remote_debugging_port.setter
    def remote_debugging_port(self, value):
        self._remote_debugging_port = value

    @property
    def user_data_dir(self):
        return self._user_data_dir

    @user_data_dir.setter
    def user_data_dir(self, value):
        self._user_data_dir = value

    @property
    def remote_allow_origins(self):
        return self._remote_allow_origins

    @remote_allow_origins.setter
    def remote_allow_origins(self, value):
        self._remote_allow_origins = value

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, value):
        self._headless = value

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    def window_size(self, value):
        self._window_size = value

    def start_chrome(self):
        # 定义Chrome的完整路径和启动参数
        chrome_args = [
            self.chrome_path,
            f"--remote-debugging-port={self._remote_debugging_port}",
            f"--user-data-dir={self._user_data_dir}",
            f"--remote-allow-origins={self._remote_allow_origins}",
            f"{'--headless=new' if self._headless else ''}",
            f"--window-size={','.join(self._window_size)}",
        ]

        # 启动Chrome浏览器
        self.__process = subprocess.Popen(chrome_args)
        # 等待一段时间，确保Chrome已经启动
        time.sleep(5)

    def close_chrome(self):
        # 关闭Chrome浏览器
        if self.__process:
            self.__process.terminate()
            self.__process.wait()

    def __del__(self):
        self.close_chrome()

    def get_page_ws_url(self, page_title=None, page_index: int = None, page_url=None):
        # 获取chrome的websocket调试url
        resp = requests.get(f"http://127.0.0.1:{self.remote_debugging_port}/json")
        assert resp.status_code == 200, "Failed to get page information from chrome"
        resp_json = resp.json()

        # 过滤出页面类型的target（排除其他类型的target如service worker等）
        pages = [item for item in resp_json if item.get('type') == 'page']

        if page_index is not None:
            if 0 <= page_index < len(pages):
                ws_url = pages[page_index].get('webSocketDebuggerUrl')
            else:
                raise ValueError(f"Page index {page_index} out of range. Total pages: {len(pages)}")
        elif page_title is not None:
            ws_urls = [item['webSocketDebuggerUrl'] for item in pages if item.get('title') == page_title]
            if ws_urls:
                ws_url = ws_urls[0]
            else:
                # 获取所有页面标题用于错误信息
                titles = [item.get('title', 'Untitled') for item in pages]
                raise ValueError(f"No page found with title: '{page_title}'. Available titles: {titles}")
        elif page_url is not None:
            # 通过URL匹配页面
            ws_urls = []
            for item in pages:
                item_url = item.get('url', '')
                # 精确匹配或包含匹配
                if item_url == page_url or page_url in item_url:
                    ws_urls.append(item['webSocketDebuggerUrl'])

            if ws_urls:
                # 优先返回精确匹配的URL
                exact_match = [url for url, page in zip(ws_urls, pages) if page.get('url') == page_url]
                if exact_match:
                    ws_url = exact_match[0]
                else:
                    ws_url = ws_urls[0]  # 返回第一个部分匹配的URL
            else:
                # 获取所有页面URL用于错误信息
                urls = [item.get('url', 'No URL') for item in pages]
                raise ValueError(f"No page found with URL containing: '{page_url}'. Available URLs: {urls}")
        else:
            if pages:
                ws_url = pages[0].get('webSocketDebuggerUrl')
            else:
                raise ValueError("No pages available")
        return ws_url

    def get_all_pages_info(self):
        """获取所有页面的信息"""
        resp = requests.get(f"http://127.0.0.1:{self.remote_debugging_port}/json")
        assert resp.status_code == 200, "Failed to get page information from chrome"
        resp_json = resp.json()

        # 过滤出页面类型的target
        pages = [item for item in resp_json if item.get('type') == 'page']
        return pages


class Page:
    def __init__(self, ws_url=None, browser_instance=None):
        if not browser_instance:
            raise ValueError("browser_instance is required")

        self.browser = browser_instance
        self.ws_url = ws_url or self.browser.get_page_ws_url()
        self.connection = self.connect_to_page(self.ws_url)
        self._current_target_id = None

    def __repr__(self):
        return f"Page(ws_url={self.ws_url!r})"

    def connect_to_page(self, ws_url):
        # 连接到页面
        return websocket.create_connection(ws_url)

    def send_command(self, command):
        # 发送命令
        self.connection.send(json.dumps(command))
        return json.loads(self.connection.recv())

    def navigate_to(self, url):
        command = {
            "id": 1,
            "method": "Page.navigate",
            "params": {
                "url": url
            }
        }
        result = self.send_command(command)
        # 等待页面加载完成
        self.wait_for_page_load()
        return result

    def wait_for_page_load(self, timeout=10):
        """等待页面加载完成"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 检查页面是否已经加载
                command = {
                    "id": 100,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": "document.readyState"
                    }
                }
                result = self.send_command(command)
                if (result.get('result', {}).get('result', {}).get('value') == 'complete'):
                    return True
            except:
                pass
            time.sleep(0.5)
        return False

    def new_page(self, url="about:blank", new_window: bool = False):
        # 打开新页面
        command = {
            "id": 2,
            "method": "Target.createTarget",
            "params": {
                "url": url,
                "newWindow": new_window
            }
        }
        # 接收响应，获取新页面的targetId
        response = self.send_command(command)
        print("createTarget response:", response)
        target_id = response.get('result', {}).get('targetId')
        print("target_id:", target_id)

        if target_id:
            # 等待一段时间让新页面完全创建
            time.sleep(5)

            # 获取新页面的websocket URL
            pages = self.browser.get_all_pages_info()
            print("创建新页面后的pages信息:", pages)
            new_page_info = next((page for page in pages if page.get('id') == target_id), None)
            print("创建的新页面信息new_page_info:", new_page_info)

            if new_page_info:
                new_ws_url = new_page_info.get('webSocketDebuggerUrl')
                # 创建新的Page对象连接到新页面
                new_page = Page(ws_url=new_ws_url, browser_instance=self.browser)
                return new_page

        raise ValueError("Failed to create new page")

    def switch_page(self, page_title=None, page_index: int = None, page_url=None):
        """
        切换页面

        参数:
        page_title: 页面标题（精确匹配）
        page_index: 页面索引
        page_url: 页面URL（支持精确匹配或部分匹配）
        """
        if sum([page_title is not None, page_index is not None, page_url is not None]) != 1:
            raise ValueError("必须且只能指定一个参数：page_title、page_index 或 page_url")

        ws_url = self.browser.get_page_ws_url(
            page_title=page_title,
            page_index=page_index,
            page_url=page_url
        )

        # 关闭当前连接
        if self.connection:
            self.connection.close()

        # 创建新连接
        self.connection = self.connect_to_page(ws_url)
        self.ws_url = ws_url

        # 获取切换后的页面信息用于显示
        current_info = self.get_current_page_info()
        if current_info:
            title = current_info.get('title', 'Unknown Title')
            url = current_info.get('url', 'Unknown URL')
            print(f"Switched to page - Title: '{title}', URL: {url}")
        else:
            print(f"Switched to page: {page_title or page_index or page_url}")

    def switch_page_by_url_contains(self, url_fragment):
        """
        通过URL包含的内容切换页面（便捷方法）

        参数:
        url_fragment: URL中包含的字符串片段
        """
        self.switch_page(page_url=url_fragment)

    def switch_page_by_domain(self, domain):
        """
        通过域名切换页面（便捷方法）

        参数:
        domain: 域名（如 'douyin.com', 'google.com'）
        """
        self.switch_page(page_url=f"https://{domain}")

    def get_current_page_info(self):
        """获取当前页面信息"""
        pages = self.browser.get_all_pages_info()
        current_page = next((page for page in pages if page.get('webSocketDebuggerUrl') == self.ws_url), None)
        return current_page

    def list_all_pages(self):
        """列出所有可用页面"""
        pages = self.browser.get_all_pages_info()
        page_list = []
        for i, page in enumerate(pages):
            page_info = {
                'index': i,
                'title': page.get('title', 'Untitled'),
                'url': page.get('url', 'Unknown'),
                'type': page.get('type', 'Unknown'),
                'ws_url': page.get('webSocketDebuggerUrl', 'Unknown')
            }
            page_list.append(page_info)
        return page_list

    def find_pages_by_url(self, url_fragment):
        """
        查找包含指定URL片段的页面

        参数:
        url_fragment: URL中包含的字符串片段

        返回:
        匹配的页面信息列表
        """
        pages = self.browser.get_all_pages_info()
        matched_pages = []
        for i, page in enumerate(pages):
            page_url = page.get('url', '')
            if url_fragment in page_url:
                page_info = {
                    'index': i,
                    'title': page.get('title', 'Untitled'),
                    'url': page.get('url', 'Unknown'),
                    'type': page.get('type', 'Unknown'),
                    'ws_url': page.get('webSocketDebuggerUrl', 'Unknown')
                }
                matched_pages.append(page_info)
        return matched_pages

    def page_refresh(self):
        # 刷新页面
        command = {
            "id": 3,
            "method": "Page.reload",
            "params": {
                "ignoreCache": True
            }
        }
        self.send_command(command)
        self.wait_for_page_load()

    def get_title(self):
        # 获取页面标题
        command = {
            "id": 4,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.title"
            }
        }
        response = self.send_command(command)
        if 'result' in response and 'result' in response['result']:
            return response['result']['result'].get('value', 'Unknown Title')
        else:
            # 备用方法
            try:
                pages = self.browser.get_all_pages_info()
                current_page = next((page for page in pages if page.get('webSocketDebuggerUrl') == self.ws_url), None)
                if current_page:
                    return current_page.get('title', 'Unknown Title')
            except:
                pass
            return 'Unknown Title'

    def get_url(self):
        command = {
            "id": 5,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "window.location.href"
            }
        }
        response = self.send_command(command)
        if 'result' in response and 'result' in response['result']:
            return response['result']['result'].get('value', 'Unknown URL')
        else:
            # 备用方法
            try:
                pages = self.browser.get_all_pages_info()
                current_page = next((page for page in pages if page.get('webSocketDebuggerUrl') == self.ws_url), None)
                if current_page:
                    return current_page.get('url', 'Unknown URL')
            except:
                pass
            return 'Unknown URL'

    def close_current_page(self):
        """关闭当前页面"""
        current_page = self.get_current_page_info()
        if current_page and 'targetId' in current_page:
            command = {
                "id": 6,
                "method": "Target.closeTarget",
                "params": {
                    "targetId": current_page['targetId']
                }
            }
            response = self.send_command(command)
            self.connection.close()
            return response.get('result', {}).get('success', False)
        return False

    def close(self):
        """关闭页面连接"""
        if self.connection:
            self.connection.close()


# 示例用法
if __name__ == '__main__':
    # 实例化浏览器
    browser = Browser(remote_debugging_port=9223)
    browser.start_chrome()

    # 创建第一个页面实例
    page = Page(browser_instance=browser)
    print(f"Connected to page with WebSocket URL: {page.ws_url}")

    # 导航到第一个页面
    page.navigate_to("https://www.douyin.com")
    print(f"Current page title: {page.get_title()}")
    print(f"Current page URL: {page.get_url()}")

    input("Press Enter to create new page...")

    # 创建新页面
    try:
        new_page = page.new_page(new_window=True)
        print(f"Created new page with WebSocket URL: {new_page.ws_url}")

        # 在新页面中导航
        new_page.navigate_to("https://www.douyu.com")
        print(f"New page title: {new_page.get_title()}")
        print(f"New page URL: {new_page.get_url()}")

        input("Press Enter to list all pages...")

        # 列出所有页面
        pages_info = page.list_all_pages()
        print("All available pages:")
        for page_info in pages_info:
            print(f"  Index: {page_info['index']}, Title: {page_info['title']}, URL: {page_info['url']}")

        input("Press Enter to demonstrate URL switching...")

        # 演示通过URL切换页面
        print("\n=== 演示URL切换功能 ===")

        # 方法1: 通过完整URL切换
        print("1. 通过完整URL切换到抖音页面:")
        new_page.switch_page(page_url="https://www.douyin.com")

        # 方法2: 通过URL片段切换
        print("2. 通过URL片段切换到斗鱼页面:")
        page.switch_page_by_url_contains("douyu.com")

        # 方法3: 通过域名切换
        print("3. 通过域名切换到抖音页面:")
        new_page.switch_page_by_domain("douyin.com")

        # 查找包含特定URL的页面
        print("4. 查找包含'douyin'的页面:")
        douyin_pages = page.find_pages_by_url("douyin")
        for p in douyin_pages:
            print(f"   - Index: {p['index']}, Title: {p['title']}, URL: {p['url']}")

        input("Press Enter to close browser...")

        # 关闭新页面连接
        new_page.close()

    except Exception as e:
        print(f"Error creating new page: {e}")
        # 列出当前所有页面信息用于调试
        try:
            pages_info = page.list_all_pages()
            print("Current pages for debugging:")
            for page_info in pages_info:
                print(f"  Index: {page_info['index']}, Title: {page_info['title']}, URL: {page_info['url']}")
        except Exception as debug_e:
            print(f"Debug error: {debug_e}")

    # 关闭页面连接
    page.close()
    browser.close_chrome()