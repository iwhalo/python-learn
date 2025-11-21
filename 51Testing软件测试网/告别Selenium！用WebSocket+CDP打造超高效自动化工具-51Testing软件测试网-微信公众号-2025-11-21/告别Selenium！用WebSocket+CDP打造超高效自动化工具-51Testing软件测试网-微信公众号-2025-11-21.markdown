# 告别 Selenium！用 WebSocket + CDP 打造超高效自动化工具

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqbmtIj9wcvRY0tEaUUMUX1Uv61ptf35OfG1KtrK1qIcpDE1qvexR7vzkG8NFdedgA38BhcHbGngA/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=0)**点击蓝字，立即关注**![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqbmtIj9wcvRY0tEaUUMUX1Qyj3vt5n40eiclK2BHGoy1W2za3JCSp7D68303P3nfEicWkicWRry7yZg/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=1)  


在自动化测试和爬虫开发领域，Selenium 是一个广泛使用的工具，但随着技术的发展，Chrome DevTools Protocol（CDP）提供了更高效、更强大的功能。

  


本文将介绍如何结合 WebSocket 和 CDP，打造一个类似 Selenium 的自动化工具，实现对 Chrome 浏览器的精细控制。

  


这种方法不仅性能更高，功能更强大，而且更加轻量级。

  
上篇文章为大家介绍了[WebSocket、CDP和Selenium与浏览器通信流程三个概念，以及为什么选择 WebSocket + CDP](https://mp.weixin.qq.com/s?__biz=MjM5NTU0MDg0MA==&mid=2651338106&idx=1&sn=d5b399d5cf6c14c12c4f793811929c1e&scene=21#wechat_redirect)。接下来将为大家介绍如何 ** **启动Chrome 并开启远程调试。****

  


 **启动 Chrome 并开启远程调试**

  


 **01**

 **准备工作**

  


在开始之前，你需要确保已经安装了以下工具和库：

  


  * Chrome 浏览器：

确保你的 Chrome 浏览器版本支持 CDP。

  


  * Python：

用于编写自动化脚本。版本最好在 Python3.6 以上。

  


  * websocket-client：

用于与 Chrome 的 WebSocket 调试端口通信。

  


websocket-client 是 Python 的一个第三方库，需要提前安装。

  


安装命令：pip install websocket-client

  


  * requests：

一个非常流行的 Python HTTP 库，用于发送 HTTP 请求，支持多种 HTTP 方法（如 GET、POST、PUT、DELETE 等），并提供了丰富的功能等。




  


 **02**

 **启动 Chrome 并开启远程调试**

  


不同操作系统，启动 Chrome 并开启远程调试的命令稍微有所区别，下面对主流的 Windows、Linux 和 MacOS 系统进行介绍。

  


在 Windows 系统中，可以通过以下命令启动 Chrome 并开启远程调试：

  


    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

  


在 Linux 系统中，可以通过以下命令启动 Chrome 并开启远程调试：

  


    google-chrome 
    
    \--remote-debugging-port=9222

  


在 MacOS 系统中，可以通过以下命令启动 Chrome 并开启远程调试：

  


    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

  


在启动时，我们还可以添加一些参数来指定调试端口、用户数据目录、代理服务器等。以下是一些常用的参数及其说明：

  


![img.png](img.png)

  


例如我们启动一个调试端口为 9222、用户数据目录为 /users/ydj/chrome_profile、初始窗口大小为 1280x768 、限制访问范围为所有人都可以访问的 Chrome。

  


命令就可以写成：

  


    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir=/users/ydj/chrome_profile --window-size=1280,768 --remote-allow-origins=*

![img_2.png](img_2.png)  

```bash
C:\Program Files (x86)\Google\Chrome\Application>chrome.exe --remote-debugging-port=9222 --window-size=1280,768 --remote-allow-origins=* --user-data-dir="C:\Program Files (x86)\Google\Chrome\Application\chrome_profile"
```

Windows命令行执行上面命令后不会等待接收消息

![img_10.png](img_10.png)

```shell
为什么没有消息反馈？
Chrome以无界面模式启动 - 命令执行后Chrome会在后台启动

Windows命令行特性 - 不会像Linux那样显示进程ID等信息

程序正常运行中 - 没有错误就意味着命令已成功执行

如何验证Chrome是否正常运行？
方法1：检查任务管理器
按 Ctrl + Shift + Esc 打开任务管理器

在"进程"标签中查找 chrome.exe

应该能看到Chrome进程正在运行

方法2：通过浏览器访问调试端口
打开另一个浏览器（如Edge或另一个Chrome实例）

访问：http://localhost:9222/json/version

如果看到JSON格式的版本信息，说明调试模式已启动

方法3：查看JSON端点列表
访问：http://localhost:9222/json/list
这会显示所有可调试的标签页信息
```

此时，打开另一个浏览器，输入：http://localhost:9222/json/version

可以看到JSON格式的版本信息，说明调试模式已启动

![img_11.png](img_11.png) 


http://localhost:9222/json

![img_12.png](img_12.png)

Chrome DevTools Protocol 开启协议监视器（参考：https://developer.chrome.google.cn/docs/devtools/protocol-monitor?hl=zh-cn&name=Halo&img_url=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaEIsJ87NpVEfzDxS6iaIBrmicOYSWK9lcco8nWw9WXzwXD2KBfic78CgiaO6bAkJZibicnMkjgYqXzdDiba1B7ib4GIJu346QhkzcbKeKuWRvGfWFKibDBQ%2F132&key=6d2e5200a17a72da0fdd88c0f2bbd2e9e1e2ab5831043597e18f42b6b7beb149&redirected=true）

![img_3.png](img_3.png)

依次选择 Settingssettings > Experiments，然后勾选 Protocol Monitor 复选框。

![img_4.png](img_4.png)


输入命令
按以下任一键打开命令菜单：

    macOS：Command+Shift+P
    Windows、Linux、ChromeOS：Ctrl+Shift+P


![img_5.png](img_5.png)

命令参数
 Show Protocol monitor

![img_6.png](img_6.png)

![img_7.png](img_7.png)

```bash
记录 CDP 请求和响应
当您打开协议监视器时，它会自动开始录制当前网页中的 CDP 消息。即使您刷新页面或关闭 DevTools，协议监视器也会继续录制。

如需停止或开始录制，请点击面板顶部操作栏左侧的录制按钮。

点击相应的标头标签页，即可在请求或响应数据之间切换。

右键点击“方法”列中的值可显示基于上下文的选项。

清除和下载 CDP 消息
如需清除所有已记录的 CDP 消息，请点击操作栏中的清除分块按钮。

如需将录制的邮件下载为 JSON 文件，请点击“下载”图标 下载。

发送原始 CDP 命令
通过协议监视器发送 CDP 命令主要有两种方式：

如果命令不需要任何参数，请在 Protocol Monitor（协议监视器）底部的输入字段中输入该命令，然后按 Enter 键，例如 Page.captureScreenshot。

如果命令需要参数，请以 JSON 格式提供这些参数，例如 {"cmd":"Page.captureScreenshot","args":{"format": "jpeg"}}。

输入字段右侧的下拉菜单用于指定目标。
————————————————

```


在命令行窗口执行上面命令后，会按照参数设置的启动浏览器，如下图所示：

  


![img_1.png](img_1.png)

  


在命令行工具中可以看到 

    DevTools listening on ws:
    
    //127.0.0.1:9222/devtools/browser/817dfbee-8e34-47c6-8f0d-c8d614961a45信息。

  


表示Chrome 已经成功启动，并且 DevTools（开发者工具）正在监听 

    WebSocket 地址 ws:
    
    //127.0.0.1:9222/devtools/browser/817dfbee-8e34-47c6-8f0d-c8d614961a45。

  


这意味着我们可以通过这个地址连接到 Chrome 的远程调试接口。

  


 **03**

 **获取 WebSocket 调试 URL**

  


启动 Chrome 并开启远程调试后，输入地址http://127.0.0.1:9222/json将得到一个 JSON 格式的列表，包含所有正在运行的 Chrome 实例及其调试信息。

  


我们可以从中找到目标实例，并通过其 WebSocket URL 连接到 DevTools。

  


如下图标记处，就是新打开 Page 页面的 WebSocket URL：

  


![img_8.png](img_8.png)

  


 **04**

 **代码封装**

  


前面几步介绍了手动操作，从打开启动 Chrome 并开启远程调试到获取 WebSocket 调试 URL。

  


接下来我们需要将上面内容使用 Python 进行封装。

  


本次代码封装我们做到两个功能，第一需要一个命令来启动 Chrome 浏览器，并通过远程调试功能连接到特定页面。第二需要支持无头模式、自定义窗口大小、用户数据目录等参数。

  


在类结构上，我们需要设计一个 Browser 类和 Page类，Browser 类负责启动和管理 Chrome 浏览器；Page 类继承自 Browser 类，负责连接到特定页面并进行 WebSocket 通信。

  


下面对这两个类中方法或变量进行说明：

  


 **1\. Browser 类：**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/BuV4gXrNvFqWFItV2tTVS3kgabogNSeqPaQiaRiaOib3oX0FJXXJaSAjmdu5bwYhICxDT0aQjceVuZgFyxXOmbVKw/640?wx_fmt=gif&from=appmsg)

  


  


  * 默认值：

定义一些默认值，如 Chrome 的路径、远程调试端口等。

  


  * 初始化方法：

允许用户在实例化时覆盖默认值。

  


  * 设置方法：

提供动态设置参数的功能。

  


  * 启动 Chrome：

构造启动参数并使用 subprocess.Popen 启动 Chrome。

  


  * 关闭 Chrome：

确保在程序退出时关闭 Chrome。

  


  * 获取页面 WebSocket URL：

发送 HTTP 请求到远程调试端口，解析返回的 JSON 数据，找到对应的 WebSocket URL。




  


 **2\. Page 类：**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/BuV4gXrNvFqWFItV2tTVS3kgabogNSeqPaQiaRiaOib3oX0FJXXJaSAjmdu5bwYhICxDT0aQjceVuZgFyxXOmbVKw/640?wx_fmt=gif&from=appmsg)

  


  


  * 初始化方法：

调用父类的初始化方法，设置 WebSocket URL，默认为第一个页面的 WebSocket URL。

  


  * 连接到页面：

使用 websocket.create_connection 方法连接到指定的 WebSocket URL。

  


  * 获取默认页面 WebSocket URL：

获取第一个页面的 WebSocket URL。




  


根据上面逻辑实现的代码如下：

  


  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   * 

    
    
```python
import atexit
import subprocess
import time
import requests
from websocket import create_connection

class Browser:
    # 设置默认值
    _chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    _remote_debugging_port = 9222
    _user_data_dir = "/users/ydj/chrome_profile"
    _remote_allow_origins = "*"
    _headless = False
    _window_size = ("1280", "768")

    def __init__(self,
                 chrome_path=None,
                 remote_debugging_port=None,
                 user_data_dir=None,
                 remote_allow_origins=None,
                 headless=None,
                 window_size=None,
                 ):
        self.chrome_path = chrome_path or self._chrome_path
        self.remote_debugging_port = remote_debugging_port or self._remote_debugging_port
        self.user_data_dir = user_data_dir or self._user_data_dir
        self.remote_allow_origins = remote_allow_origins or self._remote_allow_origins
        self.headless = headless or self._headless
        self.window_size = window_size or self._window_size
        self.__process = None
        # 注册清理函数
        atexit.register(self.close_chrome)

    @property
    def chrome_path(self):
        return Browser._chrome_path

    @chrome_path.setter
    def chrome_path(self, value):
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
            f"{'--headless=new' if self._headless else ''}",
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
        # 获取 Chrome 的 WebSocket 调试 URL
        resp = requests.get(f'http://127.0.0.1:{self.remote_debugging_port}/json')
        assert resp.status_code == 200, "Failed to get page information from Chrome"
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

class Page(Browser):
    def __init__(self, ws_url=None):
        super().__init__()
        self.ws_url = ws_url or self.get_default_page_ws_url()
        self.connection = self.connect_to_page(self.ws_url)

    def __repr__(self):
        return f"Page(ws_url={self.ws_url!r})"

    def connect_to_page(self, ws_url):
        # 连接页面
        return create_connection(ws_url)

    def get_default_page_ws_url(self):
        # 获取第一个页面 ws url
        return super().get_page_ws_url()

# 示例用法
if __name__ == '__main__':
    # 实例化时给值
    browser = Browser(remote_debugging_port=9223)
    # 单独赋值
    browser.remote_debugging_port = 9224
    browser.start_chrome()
    page = Page()
    print(f"Connected to page with WebSocket URL: {page.ws_url}")
```
  


上面代码中：

  


 **1\. Browser 类**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/BuV4gXrNvFqWFItV2tTVS3kgabogNSeqPaQiaRiaOib3oX0FJXXJaSAjmdu5bwYhICxDT0aQjceVuZgFyxXOmbVKw/640?wx_fmt=gif&from=appmsg)

  


Browser 类用于启动和管理一个 Chrome 浏览器实例，支持远程调试功能。以下是其主要功能和方法：

  


  * 初始化方法 (__init__)：

  




    * 设置 Chrome 的路径、远程调试端口、用户数据目录、允许的远程来源、是否无头模式以及窗口大小。

    * 注册 close_chrome 方法，确保在程序退出时关闭 Chrome 浏览器。




  


  * 属性装饰器：

  




    * @property 和 @<property>.setter 装饰器用于管理类变量的访问和修改。




  


  * 启动 Chrome (start_chrome)：

  




    * 构造 Chrome 的启动参数列表。

    * 使用 subprocess.Popen 启动 Chrome 浏览器。

    * 等待 5 秒，确保 Chrome 已经启动。




  


  * 关闭 Chrome (close_chrome)：

  




    * 如果浏览器进程存在，则终止并等待其退出。




  


  * 获取页面 WebSocket URL 

(get_page_ws_url)：

  




    * 发送 HTTP 请求到 Chrome 的远程调试端口，获取页面信息。

    * 根据提供的 page_title 或 page_index，找到对应的 WebSocket URL。

    * 如果没有找到匹配的页面，抛出 ValueError。




  


 **2\. Page 类**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/BuV4gXrNvFqWFItV2tTVS3kgabogNSeqPaQiaRiaOib3oX0FJXXJaSAjmdu5bwYhICxDT0aQjceVuZgFyxXOmbVKw/640?wx_fmt=gif&from=appmsg)

  


Page 类继承自 Browser 类，用于连接到一个特定的 Chrome 页面，并通过 WebSocket 进行通信。以下是其主要功能和方法：

  


  * 初始化方法 (__init__)：




  


    * 调用父类的初始化方法。

    * 设置 WebSocket URL，默认为第一个页面的 WebSocket URL。

    * 连接到页面。




  


  * 连接到页面 (connect_to_page)：




  


    * 使用 websocket.create_connection 方法连接到指定的 WebSocket URL。




  


  * 获取默认页面 WebSocket URL 

(get_default_page_ws_url)：




  


    * 调用父类的 get_page_ws_url 方法，获取第一个页面的 WebSocket URL。




  


运行上面代码，首先实例化 Browser 类，并设置远程调试端口为 9223，然后修改为 9224，接着启动 Chrome 浏览器；

  


最后创建 Page 实例，连接到第一个页面，并打印 WebSocket URL。

  


代码运行成功后，控制台会成功输出第一个页面的 WebSocket URL。

  


如下图：

  


![img_9.png](img_9.png)


  


 **......**

 **  
**

 **本文节选自** **第八十六期《51测试天地》**

 **原创文章** **《 打造基于 WebSocket + CDP 的 Selenium 替代方案》**

 **文章后续将继续为大家介绍**

 ** **“如何发** **送** CDP 命令及添加其他操作” ** **  
******

 **想继续阅读全文或查看更多《51测试天地》的原创文章**

 **请点击下方** **阅读原文或扫描二维码** **查看**

 **  
**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqWFItV2tTVS3kgabogNSeqMiaeYvsOXdGKZElmibPzoPROjwskxWud3fvxHPuzhRTHq3WO7yqom7ibA/640?wx_fmt=png&from=appmsg&watermark=1&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=31)  
  
声明： 本文为51Testing软件测试网Tynam用户投稿内容，该用户投稿时已经承诺独立承担涉及知识产权的相关法律责任，并且已经向51Testing承诺此文并无抄袭内容。发布本文的用途仅仅为学习交流，不做任何商用，未经授权请勿转载，否则作者和51Testing有权追究责任。如果您发现本公众号中有涉嫌抄袭的内容，欢迎发送邮件至：editor@51testing.com进行举报，并提供相关证据，一经查实，将立刻删除涉嫌侵权内容。

  


  


 **每日有奖互动**

  


  


  


  


  


  


  


  


  


  


 **你在项目中用过其他自动化测试方案吗？**

 **和本文的方案相比，体验如何？**

  
  
![图片](https://mmbiz.qpic.cn/sz_mmbiz_gif/BuV4gXrNvFpvmuZxeeT2BuuHo5psDq0ze0mTvhJDHePCLG1wpmnRplhBlJV54ravDg8w6vgsH0J3k9Z4xDLuBg/640?wx_fmt=gif&from=appmsg&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=13)

 **  
**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/BuV4gXrNvFqWFItV2tTVS3kgabogNSeqgJo9rRiagE1a7wPgdIjmibIrEEOLpTps5jRKYzxEJfhYz9QUOtKpoEMw/640?wx_fmt=jpeg&from=appmsg&watermark=1&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=19)
