# UI 自动化测试中“JS 单击”“Action 单击”和“Click 单击”区别

魏波. [51Testing软件测试网](javascript:void(0);)

_2025年11月15日 12:04_ _上海_

在小说阅读器中沉浸阅读

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqbmtIj9wcvRY0tEaUUMUX1Uv61ptf35OfG1KtrK1qIcpDE1qvexR7vzkG8NFdedgA38BhcHbGngA/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=0)

**点击蓝字，立即关注**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFqbmtIj9wcvRY0tEaUUMUX1Qyj3vt5n40eiclK2BHGoy1W2za3JCSp7D68303P3nfEicWkicWRry7yZg/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=1)

  

在 UI 自动化测试中，“JS 单击”、“Action 单击”和“Click 单击”是三种不同的元素交互方式，主要区别体现在触发机制、事件完整性和使用场景上。

  

以下是具体分析：

  

**01**

**Click 单击（常规点击）**

  

**定义：**

  

最基础的点击方式，直接调用测试工具提供的 click() 方法触发元素的点击事件。

  

**触发机制：**

  

由浏览器按照 W3C 标准的事件流模拟用户直接点击元素的行为，触发完整的鼠标事件序列（如 mousedown → mouseup → click）。

  

**特点：**

  

-   是测试工具（如 Selenium、Playwright）的默认点击方式，符合用户真实操作的模拟。
    
      
    
-   浏览器会自动处理事件冒泡、默认行为（如链接跳转、表单提交）等。
    
      
    
-   若元素不可见（如被遮挡、隐藏）或未启用（如 disabled），通常会抛出异常（如 ElementNotInteractableException）。
    

  

**示例（Selenium）：**

  

    WebElement button = driver.findElement(By.id("submitBtn"));

  

**02**

**JS 单击（JavaScript 触发点击）**

  

**定义：**

  

通过执行 JavaScript 脚本直接调用元素的 click() 方法，绕过浏览器的部分事件流模拟。

  

**触发机制：**

  

通过 JavascriptExecutor（Selenium）或类似接口执行 JS 代码 element.click()，相当于在浏览器控制台手动触发点击。

  

**特点：**

  

-   不经过完整的鼠标事件序列：
    
    仅触发 click 事件，可能跳过 mousedown、mouseup 等前置事件（具体取决于前端框架实现）。
    
      
    
-   绕过部分限制：
    
    可用于解决常规点击失效的场景（如元素被透明遮罩覆盖但需触发点击、元素在 iframe 外无法直接操作等）。
    
      
    
-   可能影响事件监听逻辑：
    
    若前端代码对 click 事件的触发方式有特殊判断（如通过 event.isTrusted 区分用户真实点击和 JS 触发），可能导致行为不一致（isTrusted 在 JS 触发时为 false）。
    

  

**示例（Selenium）:**

  

    WebElement button = driver.findElement(By.id("submitBtn"));

  

**03**

**Action 单击（复合操作模拟点击）**

  

**定义：**

  

通过测试工具的“动作链”（如 Selenium 的 ActionChains、Playwright 的 mouse 模块）模拟用户复杂的交互流程，最终触发点击。

  

**触发机制：**

  

按顺序执行多个鼠标操作（如移动到元素上方 moveToElement()、按下鼠标左键 clickAndHold()、释放 release() 等），组合成一次完整的点击。

  

**特点：**

  

-   高度模拟真实用户行为：
    
    触发完整的鼠标事件序列（mouseover → mousemove → mousedown → mouseup → click），甚至支持悬停后点击、双击等复杂操作。
    
      
    
-   灵活性高：
    
    可自定义操作细节（如点击位置偏移、按键组合）。
    
      
    
-   适用于特殊交互场景：
    
    例如需要先悬停再点击的菜单按钮、拖拽后释放的点击等。
    

  

**示例（Selenium）：**

  

    WebElement menu = driver.findElement(By.id("dropdownMenu"));

  

**核心区别总结**

  

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFoTiclu7A2x9tXsb36XqIk0c3F4d0VvEWtTaHibzzKHB6QCuJib7deUA2OJQVTfg1sUwA7UHricGUiajXQ/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

  

**选择建议**

  

-   优先使用Click 单击：覆盖大多数常规场景，符合用户真实行为。
    
      
    
-   仅当常规点击失效时（如元素被覆盖），尝试JS 单击（需验证前端逻辑是否依赖 isTrusted）。
    
      
    
-   对于复杂交互（悬停、偏移点击），使用Action 单击模拟完整操作流程。
    

  

![图片](https://mmbiz.qpic.cn/sz_mmbiz_gif/BuV4gXrNvFpnB28KoJNhH3f2ibg8YFzIxCtibDfxmPmKQaA9qsXw0WicComv7SPE5hIvSV9d2ibDlI8c4ZVaUzV72w/640?wx_fmt=gif&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=27)

**END**