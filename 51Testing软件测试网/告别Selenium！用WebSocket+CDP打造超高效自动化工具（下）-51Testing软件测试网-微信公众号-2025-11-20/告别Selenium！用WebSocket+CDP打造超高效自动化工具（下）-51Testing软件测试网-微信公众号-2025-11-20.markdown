# 告别 Selenium！用 WebSocket + CDP 打造超高效自动化工具（下）

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqbmtIj9wcvRY0tEaUUMUX1Uv61ptf35OfG1KtrK1qIcpDE1qvexR7vzkG8NFdedgA38BhcHbGngA/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=0)**点击蓝字，立即关注**![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqbmtIj9wcvRY0tEaUUMUX1Qyj3vt5n40eiclK2BHGoy1W2za3JCSp7D68303P3nfEicWkicWRry7yZg/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=1)  


在自动化测试和爬虫开发领域，Selenium 是一个广泛使用的工具，但随着技术的发展，Chrome DevTools Protocol（CDP）提供了更高效、更强大的功能。

  


本文将介绍如何结合 WebSocket 和 CDP，打造一个类似 Selenium 的自动化工具，实现对 Chrome 浏览器的精细控制。

  


这种方法不仅性能更高，功能更强大，而且更加轻量级。

  
前面两篇文章为大家介绍了[WebSocket、CDP和Selenium与浏览器通信流程三个概念，以及为什么选择 WebSocket + CDP](https://mp.weixin.qq.com/s?__biz=MjM5NTU0MDg0MA==&mid=2651338106&idx=1&sn=d5b399d5cf6c14c12c4f793811929c1e&scene=21#wechat_redirect)，[如何启动Chrome 并开启远程调试](https://mp.weixin.qq.com/s?__biz=MjM5NTU0MDg0MA==&mid=2651338318&idx=1&sn=1060dac269fdf2c95cd7e72757a8838c&scene=21#wechat_redirect)。  
  
接下来继续为大家介绍如何 **发送 CDP 命令及 **添加其他操作 。****  
  


 **发送 CDP 命令**

  


CDP 连接成功后，我们就可以发送 CDP 命令来操作浏览器。

  


 **步骤一：**

  


首先我们先在 Page 类下创建一个 send_command 方法，用于向 Chrome 的远程调试接口发送命令，并接收响应。

  


这个方法利用了 WebSocket 连接来与 Chrome 通信，发送 JSON 格式的命令，并接收 JSON 格式的响应。

  


代码如下：

  


  *   *   *   *   *   *   *   *   * 

    
```python

class Page(Browser):
    """
    省略其他代码
    """

    def send_command(self, command):
        # 发送 命令
        self.connection.send(json.dumps(command))
        return json.loads(self.connection.recv())
```


 **步骤二：**

  


然后我们添加打开网页的操作。

  


首先在 CDP 协议网站 

https://chromedevtools.github.io/devtools-protocol/ 找到打开网页操作的命令，如下截图所示：

  


![img.png](img.png)

  


然后根据如下格式进行编辑命令：

  


  *   *   *   *   *   *   * 

    
    
```python

command = {
    "id": 1,
    "method": method,
    "params": {
        "key": value
    }
}
```


例如打开网页的操作命令就可写成：

  


  *   *   *   *   *   *   * 

    
    
```python

command = {
    "id": 1,
    "method": "Page.navigate",
    "params": {
        "url": url
    }
}
```


 **步骤三：**

  


下面我们就可以在 Page 类下添加对应的操作方法。

  


例如在 Page 类下封装 navigate_to 方法，用于让 Chrome 浏览器导航到指定的 URL。

  


它通过发送一个 Page.navigate 命令到 Chrome 的远程调试接口来实现这一功能。

  


此方法利用了刚才封装的 send_command 方法来发送命令并处理响应。

  


代码如下：

  


  *   *   *   *   *   *   *   *   *   *   *   *   *   * 

    
    
```python

class Page(Browser):
    """
    省略其他代码
    """

    def navigate_to(self, url):
        command = {
            "id": 1,
            "method": "Page.navigate",
            "params": {
                "url": url
            }
        }
        self.send_command(command)
```


 **步骤四：**

  


接下来进行验证，如下代码：

  


  *   *   *   *   *   * 

    
```python
if __name__ == '__main__':
    browser = Browser()
    browser.start_chrome()
    page = Page()
    page.navigate_to("http://www.cnblogs.com/tynam")
    time.sleep(10)
```


运行上面代码可以看到，启动浏览器后会访问 “http://www.cnblogs.com/tynam” 网页。

  


 **添加其他操作**

  


有了上面添加浏览器操作的经验后，我们便同理添加其他操作。如下：

  


1\. 浏览器打开新的 Tab 页面

  


  *   *   *   *   *   *   *   *   *   *   *   *   *   *   * 

    
    
```python
def new_page(self, new_window: bool = False):
    # 打开新页面
    # new_window：是否在当前浏览器窗口打开
    # 发送命令以创建新标签
    command = {
        "id": 1,
        "method": "Target.createTarget",
        "params": {
            "url": "",
            "newWindow": new_window
        }

    }
    # 接收响应，获取新页面的 targetId
    response = self.send_command(command)
```


2\. 切换 Tab 页面

  


  *   *   *   * 

    
    
```python
def switch_page(self, page_title=None, page_index: int = None):
    # 切换页面
    ws_url = self.get_page_ws_url(page_title, page_index)
    self.connection = self.connect_to_page(ws_url)

```
  


3\. 页面刷新

  


  *   *   *   *   *   *   *   * 

    
    
```python
def page_refresh(self):
    command = {
        "id": 1,
        "method": "Page.reload",
        "params": {}
    }

    self.send_command(command)
```


4\. 获取页面 title

  


  *   *   *   *   *   *   *   *   *   *   *   *   *   * 

    
    
```python

def get_title(self):
    command = {
        "id": 1,
        "method": "Page.getNavigationHistory",
        "params": {}
    }

    response = self.send_command(command)
    if 'result' in response and 'currentIndex' in response['result']:
        result = response['result']
        page_info = result["entries"][result['currentIndex']]
        return page_info['title']
    else:
        raise ValueError("Failed to get page title")
```


5\. 获取页面 url

  


  *   *   *   *   *   *   *   *   *   *   *   *   *   * 

    
    
```python
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
```
  


上面只是基本的页面操作，更多内容可参考 CDP 命令的 Page 操作。

  


由于篇幅问题，在此就不再往下补充了。感兴趣的同学可继续往下探索，例如探索如何获取页面元素并进行点击。

  


  


 **......**

 **  
**

 **本文节选自** **第八十六期《51测试天地》**

 **原创文章** **《 打造基于 WebSocket + CDP 的 Selenium 替代方案》**

 **文章后续还为大家进行了 总结 ** **  
******

 **想继续阅读全文或查看更多《51测试天地》的原创文章**

 **请点击下方** **阅读原文或扫描二维码** **查看**

 **  
**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqN1iaKgIrn28I5M8voGdBhTFxsJXf2ibTxoWveeI8ic9Q8goYWLCuCPW3pCLiadVmkMIC4h0SAZKghSQ/640?wx_fmt=png&from=appmsg&watermark=1&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=31)  
  
声明： 本文为51Testing软件测试网Tynam用户投稿内容，该用户投稿时已经承诺独立承担涉及知识产权的相关法律责任，并且已经向51Testing承诺此文并无抄袭内容。发布本文的用途仅仅为学习交流，不做任何商用，未经授权请勿转载，否则作者和51Testing有权追究责任。如果您发现本公众号中有涉嫌抄袭的内容，欢迎发送邮件至：editor@51testing.com进行举报，并提供相关证据，一经查实，将立刻删除涉嫌侵权内容。

  


  


 **每日有奖互动**

  


  


  


  


  


  


  


  


  


  


 **你认为 CDP + WebSocket 是未来浏览器自动化的趋势吗？**

 **为什么？**

  
  
![图片](https://mmbiz.qpic.cn/sz_mmbiz_gif/BuV4gXrNvFpvmuZxeeT2BuuHo5psDq0ze0mTvhJDHePCLG1wpmnRplhBlJV54ravDg8w6vgsH0J3k9Z4xDLuBg/640?wx_fmt=gif&from=appmsg&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=13)

 **  
**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/BuV4gXrNvFqN1iaKgIrn28I5M8voGdBhT8PEicDZdGNqWkXbDTYNyYDf1xFo0FRQlBkDF3njSJmYHTp0zWrWofXw/640?wx_fmt=jpeg&from=appmsg&watermark=1&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=19)
