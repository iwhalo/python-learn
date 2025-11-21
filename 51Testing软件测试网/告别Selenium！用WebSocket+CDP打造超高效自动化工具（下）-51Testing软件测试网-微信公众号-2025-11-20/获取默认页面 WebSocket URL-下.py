import atexit
import json
import os
import subprocess
import time
from socket import create_connection

import requests
from django.db.models.expressions import result


class Browser:
    # 设置默认值
    _chrome_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    _remote_debugging_port=9222
    _user_data_dir=r'C:\Program Files (x86)\Google\Chrome\Application\chrome_profile'
    _remote_allow_origins="*"
    _headless=False
    _window_size=("1280","768")

    def __init__(self,
                 charome_path=None,
                 remote_debugging_port=None,
                 user_data_dir=None,
                 remote_allow_origins=None,
                 headless=None,
                 window_size=None,):
        self._chrome_path=charome_path or self._chrome_path
        self._chrome_debugging_port=remote_debugging_port or self._remote_debugging_port
        self._user_data_dir=user_data_dir or self._user_data_dir
        self._remote_allow_origins=remote_allow_origins or self._remote_allow_origins
        self._headless=headless or self._headless
        self._window_size=window_size or self._window_size
        self.__process=None

        # 注册清理函数
        atexit.register(self.close_chrome)

    @property
    def chrome_path(self):
        return Browser._chrome_path

    @chrome_path.setter
    def cchrome_path(self,value):
        Browser._chrome_path=value

    @property
    def remote_debugging_port(self):
        return Browser._remote_debugging_port

    @remote_debugging_port.setter
    def remote_debugging_port(self,value):
        Browser._remote_debugging_port=value

    @property
    def user_data_dir(self):
        return Browser._user_data_dir

    @user_data_dir.setter
    def user_data_dir(self,value):
        Browser._user_data_dir=value

    @property
    def remote_allow_origins(self):
        return Browser._remote_allow_origins

    @remote_allow_origins.setter
    def remote_allow_origins(self,value):
        Browser._remote_allow_origins=value

    @property
    def headless(self):
        return Browser._headless

    @headless.setter
    def headless(self,value):
        Browser._headless=value

    @property
    def window_size(self):
        return Browser._window_size

    @window_size.setter
    def window_size(self,value):
        Browser._window_size=value

    def start_chrome(self):
        # 定义Chrome的完整路径和启动参数
        chrome_args=[
            self.chrome_path,
            f"--remote-debugging-port={self._remote_debugging_port}",
            f"--user-data-dir={self._user_data_dir}",
            f"--remote-allow-origins={self._remote_allow_origins}",
            f"{'--headless=new' if self._headless else ''}"
            f"--window-size={self._window_size}",

        ]

        # 启动Chrome浏览器
        self.__process=subprocess.Popen(chrome_args)
        # 等待一段时间，确保Chrome已经启动
        time.sleep(5)


    def close_chrome(self):
        # 关闭Chrome浏览器
        if self.__process:
            self.__process.terminate()
            self.__process.wait()

    def __del__(self):
        self.close_chrome()

    def get_page_ws_url(self,page_title=None,page_index:int=None):
        # 获取chrome的websocket调试url

        resp=requests.get(f"http://127.0.0.1:{self.remote_debugging_port}/json")
        assert resp.status_code==200,"Failed to get page information from chrome"
        resp_json=resp.json()
        if page_index is not None:
            ws_url=resp_json[page_index].get('webSocketDebuggerUrl')
        elif page_title is not None:
            ws_urls=[item['webSocketDebuggerUrl'] for item in resp_json if item.get('title')==page_title]
            if ws_urls:
                ws_url=ws_urls[0]
            else:
                raise ValueError(f"No page found with title:{page_title}")
        else:
            ws_url=resp_json[0].get('webSocketDebuggerUrl')
        return ws_url


class Page(Browser):
    def __init__(self,ws_url=None):
        super().__init__()
        self.ws_url=ws_url or self.get_default_page_ws_url()
        self.connection=self.connect_to_page(self.ws_url)

    def __repr__(self):
        return f"Page(ws_url={self.ws_url!r})"

    def connect_to_page(self,ws_url):
        # 连接到页面
        # return create_connection(ws_url)
        import websocket
        return websocket.create_connection(ws_url)

    def get_default_page_ws_url(self):
        # 获取第一个页面 ws  url
        return super().get_page_ws_url()





    def send_command(self,command):
        # 发送命令
        self.connection.send(json.dumps(command))
        return json.loads(self.connection.recv())

    def navigate_to(self,url):
        command={
            "id":1,
            "method":"Page.navigate",
            "params":{
                "url":url
            }
        }
        self.send_command(command)

    def new_page(self,new_window:bool=False):
        # 打开新页面
        # new_window=True 打开新窗口
        command={
            "id":2,
            "method":"Target.createTarget",
            "params":{
                "url":"",
                "newWindow":new_window
            }
        }
        # 接收响应，获取新页面的targetId
        response=self.send_command(command)
        print(response)
        return response

    def switch_page(self,page_title=None,page_index:int=None):
        # 切换页面
        ws_url=self.get_page_ws_url(page_title,page_index)
        self.connection=self.connect_to_page(ws_url)
        self.ws_url=ws_url




    def page_refresh(self):
        # 刷新页面
        command={
            "id":3,
            "method":"Page.reload",
            "params":{
                "ignoreCache":True
            }
        }
        self.send_command(command)

    def get_title(self):
        # 获取页面标题
        command={
            "id":4,
            "method":"Page.getNavigationHistory",
            "params":{}
        }
        response=self.send_command(command)
        if 'result' in response and 'currentIndex' in response['result']:
            result=response['result']
            page_info=result['entries'][result['currentIndex']]
            return page_info['title']
        else:
            raise ValueError("Failed to get page title")

    def get_url(self):
        command = {
            "id": 1,
            "method": "Page.getNavigationHistory",
            "params": {}
        }

        response = self.send_command(command)
        if 'result' in response and 'currentIndex' in response['result']:
            result = response['result']
            page_info = result["entries"][result['currentIndex']]
            return page_info['url']
        else:
            raise ValueError("Failed to get page url")

# 示例用法
if __name__ == '__main__':
    # 实例化时给值
    browser=Browser(remote_debugging_port=9223)
    # 单独赋值
    browser.remote_debugging_port=9224
    browser.start_chrome()
    page=Page()
    print(f"Connected to page with WebSocket URL:{page.ws_url}")
    page.navigate_to("http://wwww.cnblogs.com/tynam")
    input("Press Enter to continue...")

    page.new_page(new_window=True)

    input("Press Enter to continue...")

    page.switch_page()
    input("Press Enter to continue...")

    browser.close_chrome()