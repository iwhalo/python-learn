# Jmeter 性能测试利器（入门指南）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFoosqKEsEnMos3oEWQdB4eudCT6o9RxVglib79ekuFbKpUIKiaTl1PlmHl1v04uAiaCPIUh2wd7tdocA/640?wx_fmt=png&from=appmsg)**点击蓝字，立即关注**![](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFoosqKEsEnMos3oEWQdB4euXvQVeA6mNJt00o1LvdEgg84ibz8Ha63XHuHuODibowKczEy1ISO5hFIA/640?wx_fmt=png&from=appmsg)

  


 **摘要** ：本文简单介绍Jmeter性能测试工具的使用，包括组件的使用和常见的业务场景的接口测试，后端接口使用的springboot做服务端。

  


  
  
 **安装**  
  


  


我下载的是：https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.zip

下载地址：https://jmeter.apache.org/download_jmeter.cgi

  


  
  
 **打开界面使用**  
  


  


先解压，然后切换到bin目录双击jmeter.bat

![img.png](img.png)

  


 **设置中文语言**

  


![img_1.png](img_1.png)

永久设置方案，配置jmeter.properties，在39行左右。

  *   *   * 

    
    
```python
#Preferred GUI language. Comment out to use the JVM default locale's language.
#language=en
language=zh_CN

```

  


 **创建一个测试计划**

  


创建一个计划并保存

![img_2.png](img_2.png)

  


 **第一个测试案例**

  


 **创建一个线程组**

线程组就理解为用户，多少个用户同时访问，线程组下面设置的变量，只要没有设置为全局的，都是当前线程共享的，不会跨线程。

![img_3.png](img_3.png)

  


 **添加取样器HTTP请求**

就是配置你调用的接口，如果有请求头一类的的，你再添加【配置元件/HTTP请求头管理器】

![img_4.png](img_4.png)

  


 **添加JSON提取器**

因为我们要获取数据给下一个接口，提取了下面的data属性。

  *   *   *   *   * 

    
    
```python
{
    "code": 200,
    "data": 1755763130398,
    "message": "success"
}

```

  


![img_5.png](img_5.png)

  


 **配置下一个HTTP请求**

可以使用上面提取的参数

![img_6.png](img_6.png)
  


 **添加监听器**

  *  **查看结果树** 添加到取样器下面的；

  *  **汇总报告** 可以添加到取样器下也可以添加到线程组下面查询总体情况；


![img_7.png](img_7.png)
  

![img_8.png](img_8.png)
  
  
 **常用处理器使用说明**  
  


  


 **BeanShell**

它功能非常强大，通过脚本转换出来新的值，传递给全局或者当前线程。

  


 **vars** ：当前线程变量；

 **通过 vars对象的方法访问：**

  *  **vars.get("key")** ：获取字符串值（若键不存在返回 null）。

  *  **vars.put("key", "value")** ：设置字符串值。

  *  **vars.getObject("key")** ：获取任意类型的对象（需手动转换）。




 **props：全局共享**

  *  **props.get("key")** ：获取字符串值（若键不存在返回 null）。

  *  **props.setProperty("key", "value")** ：设置字符串值（等价于 props.put("key", "value")）。

  *  **JMeter 函数** ：${__P(key)}（等价于 props.get("key")）、${__property(key, defaultValue)}（若键不存在返回默认值）。




  


![img_9.png](img_9.png)
  


 **现场变量转换为全局变量**

  * 

    
    
```js
props.setProperty("total_requests", vars.get("goodsId"));

```

  


 **编写 MD5 加密逻辑，将原始密码替换为加密后的值**

  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   * 

    
    
```js
mport java.security.MessageDigest;

// 原始密码（可从变量获取，如 ${raw_pwd}）
String rawPwd = vars.get("raw_pwd");

// MD5 加密方法
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] digest = md.digest(rawPwd.getBytes());
StringBuilder sb = new StringBuilder();
for (byte b : digest) {
    sb.append(String.format("%02x", b & 0xFF));
}
String encryptedPwd = sb.toString();

// 替换请求参数中的密码（假设请求体中有 password 字段）
// 方法 1：修改变量（后续请求体用 ${encrypted_pwd} 调用）
vars.put("encrypted_pwd", encryptedPwd);
// 方法 2：直接修改请求体（需结合请求体的变量名，如请求体为 JSON）
// prev.setBodyData("{"username":"test","password":"" + encryptedPwd + ""}");

```
