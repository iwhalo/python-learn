import atexit
import json
import subprocess
import time

import websocket
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
                 charome_path=None,
                 remote_debugging_port=None,
                 user_data_dir=None,
                 remote_allow_origins=None,
                 headless=None,
                 window_size=None, ):
        self._chrome_path = charome_path or self._chrome_path
        self._chrome_debugging_port = remote_debugging_port or self._remote_debugging_port
        self._user_data_dir = user_data_dir or self._user_data_dir
        self._remote_allow_origins = remote_allow_origins or self._remote_allow_origins
        self._headless = headless or self._headless
        self._window_size = window_size or self._window_size
        self.__process = None

        # 注册清理函数
        atexit.register(self.close_chrome)

    @property
    def chrome_path(self):
        return Browser._chrome_path

    @chrome_path.setter
    def cchrome_path(self, value):
        Browser._chrome_path = value

    @property
    def remote_debugging_port(self):
        return Browser._remote_debugging_port

    @remote_debugging_port.setter
    def remote_debugging_port(self, value):
        Browser._remote_debugging_port = value

    @property
    def user_data_dir(self):
        return Browser._user_data_dir

    @user_data_dir.setter
    def user_data_dir(self, value):
        Browser._user_data_dir = value

    @property
    def remote_allow_origins(self):
        return Browser._remote_allow_origins

    @remote_allow_origins.setter
    def remote_allow_origins(self, value):
        Browser._remote_allow_origins = value

    @property
    def headless(self):
        return Browser._headless

    @headless.setter
    def headless(self, value):
        Browser._headless = value

    @property
    def window_size(self):
        return Browser._window_size

    @window_size.setter
    def window_size(self, value):
        Browser._window_size = value

    def start_chrome(self):
        # 定义Chrome的完整路径和启动参数
        chrome_args = [
            self.chrome_path,
            f"--remote-debugging-port={self._remote_debugging_port}",
            f"--user-data-dir={self._user_data_dir}",
            f"--remote-allow-origins={self._remote_allow_origins}",
            f"{'--headless=new' if self._headless else ''}"
            f"--window-size={self._window_size}",

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

    def get_page_ws_url(self, page_title=None, page_index: int = None):
        # 获取chrome的websocket调试url

        resp = requests.get(f"http://127.0.0.1:{self.remote_debugging_port}/json")
        assert resp.status_code == 200, "Failed to get page information from chrome"
        resp_json = resp.json()
        print(f"获取页面信息成功: {resp_json}")
        """
        [{'description': '', 'devtoolsFrontendUrl': 'https://chrome-devtools-frontend.appspot.com/serve_rev/@c128b60bcfa95fd7050b7241c5289967d4ee077c/inspector.html?ws=127.0.0.1:9222/devtools/page/7A5D600126FFEB99D373468A05B15025', 'id': '7A5D600126FFEB99D373468A05B15025', 'title': '新标签页', 'type': 'page', 'url': 'chrome://newtab/', 'webSocketDebuggerUrl': 'ws://127.0.0.1:9222/devtools/page/7A5D600126FFEB99D373468A05B15025'}]
        """
        if page_index is not None:
            ws_url = resp_json[page_index].get('webSocketDebuggerUrl')
        elif page_title is not None:
            ws_urls = [item['webSocketDebuggerUrl'] for item in resp_json if item.get('title') == page_title]
            if ws_urls:
                ws_url = ws_urls[0]
            else:
                raise ValueError(f"No page found with title:{page_title}")
        else:
            ws_url = resp_json[0].get('webSocketDebuggerUrl')
        return ws_url
    # ... 之前的代码保持不变 ...

    def get_all_targets(self):
        """获取所有目标（标签页）"""
        try:
            resp = requests.get(f"http://127.0.0.1:{self.remote_debugging_port}/json")
            if resp.status_code == 200:
                return resp.json()
            return []
        except Exception as e:
            print(f"获取目标列表失败: {e}")
            return []

    def switch_to_tab_by_index(self, index):
        """通过索引切换标签页"""
        targets = self.get_all_targets()
        if 0 <= index < len(targets):
            print(f"切换到标签页 {index}:{targets[index]['webSocketDebuggerUrl']}")
            return targets[index]['webSocketDebuggerUrl']
        else:
            raise ValueError(f"标签页索引 {index} 超出范围")

    def switch_to_tab_by_title(self, title):
        """通过标题切换标签页"""
        targets = self.get_all_targets()
        matching_targets = [target for target in targets if title.lower() in target.get('title', '').lower()]
        if matching_targets:
            return matching_targets[0]['webSocketDebuggerUrl']
        else:
            raise ValueError(f"未找到包含标题 '{title}' 的标签页")

    def switch_to_tab_by_url(self, url):
        """通过URL切换标签页"""
        targets = self.get_all_targets()
        matching_targets = [target for target in targets if url.lower() in target.get('url', '').lower()]
        if matching_targets:
            return matching_targets[0]['webSocketDebuggerUrl']
        else:
            raise ValueError(f"未找到包含URL '{url}' 的标签页")

    def create_new_tab(self, url="about:blank"):
        """创建新标签页"""
        try:
            resp = requests.put(f"http://127.0.0.1:{self.remote_debugging_port}/json/new?{url}")
            if resp.status_code == 200:
                new_tab = resp.json()
                return new_tab['webSocketDebuggerUrl']
            else:
                raise Exception(f"创建新标签页失败: {resp.status_code}")
        except Exception as e:
            print(f"创建新标签页失败: {e}")
            raise

    def close_tab(self, ws_url):
        """关闭指定标签页"""
        try:
            # 通过Target.closeTarget方法关闭
            targets = self.get_all_targets()
            target_id = None
            for target in targets:
                if target.get('webSocketDebuggerUrl') == ws_url:
                    target_id = target.get('id')
                    break

            if target_id:
                close_url = f"http://127.0.0.1:{self.remote_debugging_port}/json/close/{target_id}"
                resp = requests.get(close_url)
                if resp.status_code == 200:
                    print(f"已关闭标签页: {target_id}")
                else:
                    print(f"关闭标签页失败: {resp.status_code}")
        except Exception as e:
            print(f"关闭标签页失败: {e}")


class Page:
    def __init__(self, ws_url=None, browser_instance=None):
        if browser_instance is None:
            raise ValueError("必须提供browser_instance参数")

        self.browser = browser_instance
        self.ws_url = ws_url or self.browser.get_page_ws_url()
        self.connection = None
        self.target_id = None
        self.session_id = None

        # 连接到页面
        self.connect()

    def connect(self):
        """连接到页面"""
        try:
            import websocket
            self.connection = websocket.create_connection(self.ws_url)

            # 获取target信息
            targets = self.browser.get_all_targets()
            print("targets:", targets)
            """
            [{'description': '', 'devtoolsFrontendUrl': 'https://chrome-devtools-frontend.appspot.com/serve_rev/@c128b60bcfa95fd7050b7241c5289967d4ee077c/inspector.html?ws=127.0.0.1:9222/devtools/page/3FE8516B3CB381390621E30AA044561F', 'id': '3FE8516B3CB381390621E30AA044561F', 'title': '新标签页', 'type': 'page', 'url': 'chrome://newtab/', 'webSocketDebuggerUrl': 'ws://127.0.0.1:9222/devtools/page/3FE8516B3CB381390621E30AA044561F'}]
            """
            for target in targets:
                if target.get('webSocketDebuggerUrl') == self.ws_url:
                    self.target_id = target.get('id')
                    break

            print(f"已连接到标签页: {self.target_id}")
            return True

        except ImportError:
            print("请安装websocket-client库: pip install websocket-client")
            return False
        except Exception as e:
            print(f"WebSocket连接失败: {e}")
            return False

    def switch_tab(self, **kwargs):
        """切换标签页的通用方法"""
        try:
            # 关闭当前连接
            if self.connection:
                self.connection.close()
                self.connection = None

            # 根据参数获取新的WebSocket URL
            if 'index' in kwargs:
                new_ws_url = self.browser.switch_to_tab_by_index(kwargs['index'])
            elif 'title' in kwargs:
                new_ws_url = self.browser.switch_to_tab_by_title(kwargs['title'])
            elif 'url' in kwargs:
                new_ws_url = self.browser.switch_to_tab_by_url(kwargs['url'])
            elif 'ws_url' in kwargs:
                new_ws_url = kwargs['ws_url']
            else:
                raise ValueError("请提供 index、title、url 或 ws_url 参数")

            # 更新WebSocket URL并重新连接
            self.ws_url = new_ws_url
            return self.connect()

        except Exception as e:
            print(f"切换标签页失败: {e}")
            return False

    def create_new_tab(self, url="about:blank"):
        """创建并切换到新标签页"""
        try:
            # 关闭当前连接
            if self.connection:
                self.connection.close()
                self.connection = None

            # 创建新标签页
            new_ws_url = self.browser.create_new_tab(url)
            self.ws_url = new_ws_url
            return self.connect()

        except Exception as e:
            print(f"创建新标签页失败: {e}")
            return False

    def close_current_tab(self):
        """关闭当前标签页并切换到第一个标签页"""
        try:
            current_ws_url = self.ws_url

            # 关闭当前连接
            if self.connection:
                self.connection.close()
                self.connection = None

            # 关闭标签页
            self.browser.close_tab(current_ws_url)

            # 切换到第一个标签页
            new_ws_url = self.browser.switch_to_tab_by_index(0)
            self.ws_url = new_ws_url
            return self.connect()

        except Exception as e:
            print(f"关闭当前标签页失败: {e}")
            return False

    def list_tabs(self):
        """列出所有标签页"""
        targets = self.browser.get_all_targets()
        print(f"\n当前共有 {len(targets)} 个标签页:")
        for i, target in enumerate(targets):
            current_indicator = "✓" if target.get('webSocketDebuggerUrl') == self.ws_url else " "
            print(f"  [{current_indicator}] {i}: {target.get('title', 'No Title')}")
            print(f"      URL: {target.get('url', 'No URL')}")
            print(f"      Type: {target.get('type', 'Unknown')}")
        return targets

    def send_command(self, method, params=None):
        """发送CDP命令"""
        if self.connection is None:
            if not self.connect():
                return None

        message = {
            "id": 1,
            "method": method,
            "params": params or {}
        }

        try:
            self.connection.send(json.dumps(message))
            response = self.connection.recv()
            return json.loads(response)
        except Exception as e:
            print(f"发送命令失败: {e}")
            return None

    def navigate(self, url):
        """导航到指定URL"""
        return self.send_command("Page.navigate", {"url": url})

    def get_title(self):
        """获取页面标题"""
        result = self.send_command("Runtime.evaluate", {
            "expression": "document.title"
        })
        if result and 'result' in result and 'result' in result['result']:
            return result['result']['result'].get('value', '')
        return ""

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            self.connection = None


# 示例用法
if __name__ == '__main__':
    browser = None
    try:
        # 实例化浏览器
        browser = Browser(
            remote_debugging_port=9222,
            user_data_dir=r"C:\Program Files\Google\Chrome\Application\chrome_profile"
        )

        browser.start_chrome()

        # 创建页面连接
        page = Page(browser_instance=browser)
        print(f"当前页面WebSocket URL: {page.ws_url}")

        # 列出所有标签页
        page.list_tabs()

        # 创建新标签页并导航到百度
        print("\n1. 创建新标签页...")
        if page.create_new_tab("https://www.baidu.com"):
            print("新标签页创建成功")
            page.list_tabs()

        # 切换到第一个标签页
        print("\n2. 切换到第一个标签页...")
        if page.switch_tab(index=0):
            print("切换成功")
            page.list_tabs()

        # 通过标题切换（如果知道标题的话）
        # page.switch_tab(title="百度")

        # 通过URL切换
        # page.switch_tab(url="baidu")

        # 保持程序运行
        input("\n按Enter键退出...")

    except Exception as e:
        print(f"程序执行出错: {e}")
    finally:
        if browser:
            browser.close_chrome()