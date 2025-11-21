import atexit
import os
import subprocess
import time
from socket import create_connection

import requests


class Browser:
    # 设置默认值
    _chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    _remote_debugging_port = 9222
    _user_data_dir = r'C:\Program Files\Google\Chrome\Application\chrome_profile'
    _remote_allow_origins = "*"
    _headless = False
    _window_size = ("1280", "768")

    def __init__(self,
                 chrome_path=None,  # 修正参数名 typo
                 remote_debugging_port=None,
                 user_data_dir=None,
                 remote_allow_origins=None,
                 headless=None,
                 window_size=None):
        # 使用实例属性而不是类属性
        self.chrome_path = chrome_path or self._chrome_path
        self.remote_debugging_port = remote_debugging_port or self._remote_debugging_port
        self.user_data_dir = user_data_dir or self._user_data_dir
        self.remote_allow_origins = remote_allow_origins or self._remote_allow_origins
        self.headless = headless if headless is not None else self._headless
        self.window_size = window_size or self._window_size
        self.__process = None

        # 注册清理函数
        atexit.register(self.close_chrome)

    def start_chrome(self):
        # 定义Chrome的完整路径和启动参数
        chrome_args = [
            self.chrome_path,
            f"--remote-debugging-port={self.remote_debugging_port}",
            f"--user-data-dir={self.user_data_dir}",
            f"--remote-allow-origins={self.remote_allow_origins}",
            f"--window-size={','.join(self.window_size)}",
        ]

        # 添加headless参数
        if self.headless:
            chrome_args.append("--headless=new")

        print(f"启动Chrome命令: {' '.join(chrome_args)}")

        # 启动Chrome浏览器
        try:
            self.__process = subprocess.Popen(chrome_args)
            # 等待Chrome启动并检查端口是否就绪
            self._wait_for_chrome_ready()
            print("Chrome启动成功")
        except Exception as e:
            print(f"启动Chrome失败: {e}")
            raise

    def _wait_for_chrome_ready(self, timeout=30):
        """等待Chrome调试端口就绪"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://127.0.0.1:{self.remote_debugging_port}/json", timeout=5)
                if response.status_code == 200:
                    print("Chrome调试端口已就绪")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)

        raise TimeoutError(f"Chrome在{timeout}秒内未启动完成")

    def close_chrome(self):
        """关闭Chrome浏览器"""
        if self.__process:
            print("正在关闭Chrome...")
            self.__process.terminate()
            try:
                self.__process.wait(timeout=10)
                print("Chrome已关闭")
            except subprocess.TimeoutExpired:
                print("强制终止Chrome进程...")
                self.__process.kill()
            self.__process = None

    def __del__(self):
        self.close_chrome()

    def get_page_ws_url(self, page_title=None, page_index=None):
        """获取chrome的websocket调试url"""
        try:
            resp = requests.get(f"http://127.0.0.1:{self.remote_debugging_port}/json")
            assert resp.status_code == 200, "Failed to get page information from chrome"
            resp_json = resp.json()

            if page_index is not None:
                ws_url = resp_json[page_index].get('webSocketDebuggerUrl')
            elif page_title is not None:
                ws_urls = [item['webSocketDebuggerUrl'] for item in resp_json if item.get('title') == page_title]
                if ws_urls:
                    ws_url = ws_urls[0]
                else:
                    raise ValueError(f"No page found with title: {page_title}")
            else:
                ws_url = resp_json[0].get('webSocketDebuggerUrl')

            return ws_url
        except Exception as e:
            print(f"获取WebSocket URL失败: {e}")
            raise


class Page(Browser):
    def __init__(self, ws_url=None, browser_instance=None):
        # 如果提供了browser实例，使用它的配置
        if browser_instance:
            self.browser = browser_instance
            self.ws_url = ws_url or self.browser.get_page_ws_url()
        else:
            # 否则创建新的Browser实例
            super().__init__()
            self.browser = self
            if not ws_url:
                self.start_chrome()  # 确保Chrome已启动
            self.ws_url = ws_url or self.get_page_ws_url()

        self.connection = self.connect_to_page(self.ws_url)

    def __repr__(self):
        return f"Page(ws_url={self.ws_url!r})"

    def connect_to_page(self, ws_url):
        """连接到页面"""
        try:
            # 注意：这里需要使用WebSocket库，create_connection可能不适用
            # 这里只是示例，实际使用时需要安装websocket库
            print(f"连接到WebSocket: {ws_url}")
            # 实际实现应该使用:
            import websocket
            return websocket.create_connection(ws_url)
            # return create_connection(ws_url.replace("ws://", "http://").replace("/devtools/", "/json/"))
        except Exception as e:
            print(f"连接失败: {e}")
            raise


# 示例用法
if __name__ == '__main__':
    try:
        # 实例化浏览器
        browser = Browser(
            remote_debugging_port=9222,
            user_data_dir=r"C:\Program Files\Google\Chrome\Application\chrome_profile"  # 建议使用其他目录，避免权限问题
        )

        browser.start_chrome()

        # 创建页面连接
        page = Page(browser_instance=browser)
        print(f"Connected to page with WebSocket URL: {page.ws_url}")

        # 保持程序运行
        input("按Enter键退出...")

    except Exception as e:
        print(f"程序执行出错: {e}")
    finally:
        if 'browser' in locals():
            browser.close_chrome()