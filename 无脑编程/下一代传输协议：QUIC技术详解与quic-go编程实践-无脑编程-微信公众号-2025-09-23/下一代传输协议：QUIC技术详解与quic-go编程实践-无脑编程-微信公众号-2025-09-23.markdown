# 下一代传输协议：QUIC技术详解与quic-go编程实践

# 什么是quic协议？

QUIC（快速UDP互联网连接协议）是Google推出的创新性网络传输协议，旨在突破TCP协议的性能限制。该协议利用UDP实现高效、安全且低延迟的网络传输，现已被IETF确立为标准协议，并作为HTTP/3的基础传输层协议。

QUIC协议设计原理：

1）采用 UDP 替代 TCP：通过绕过操作系统内核的 TCP 协议栈，有效规避队头阻塞问题，同时实现自主可控的可靠传输机制。

2）零往返时连接（0-RTT）：通过首次连接缓存密钥信息，后续连接可跳过握手环节（类似TCP中TLS 1.3的0-RTT机制），显著降低30%-50%的延迟。

## QUIC协议优势

特性| 说明  
---|---  
‌ **多路复用无阻塞** ‌|数据流独立传输，单条数据流丢包不会影响其他流（避免了TCP的固有缺陷）。  
‌ **原生加密** ‌| 默认启用 TLS 1.3，实现报文头部及载荷的全链路强制加密。  
‌ **智能拥塞控制** ‌| 动态调整数据包发送速率（如采用 BBR 算法），以适配不同网络环。  
‌ **连接迁移** ‌| 设备在Wi-Fi和5G网络间切换时，能保持稳定连接，无需重新建立握手协议。  
  
## QUIC协议与TCP+TLS协议对比

对比项| TCP + TLS| QUIC  
---|---|---  
‌ **握手延迟** ‌| 1-RTT (TLS 1.2+)| ‌0-RTT‌ (非首次连接)  
‌ **队头阻塞** ‌| 存在（单流阻塞）| ‌无‌（多流独立）  
‌ **加密范围** ‌| 仅加密载荷| ‌头部+载荷全加密‌  
‌ **协议升级** ‌| 需操作系统支持| ‌用户态实现‌，快速迭代  
‌ **抗丢包能力** ‌| 依赖重传| ‌前向纠错（FEC）‌ 选项  
  
# quic-go介绍

quic-go 是一个基于 Go 语言的 QUIC 协议实现库，全面兼容以下核心标准：

1）RFC 9000（QUIC 基础协议）2）RFC 9001（TLS 集成）3）RFC 9002（拥塞控制）

该库采用 UDP 传输实现低延迟通信，并深度整合了 HTTP/3（RFC 9114）及其关键技术：

1）QPACK 头部压缩（RFC 9204）2）HTTP 数据报（RFC 9297）

quic-go 在核心规范之外还提供以下增强功能：

1）不可靠数据报扩展（RFC 9221）：支持非可靠传输模式，适用于实时音视频等场景。2）路径 MTU 发现（RFC 8899）：动态探测网络最大传输单元，优化数据分片。3）QUIC 版本 2（RFC 9369）：兼容新版协议特性。4）qlog 事件日志：遵循 IETF 草案标准记录连接事件，便于调试分析。5）WebTransport 支持：通过 webtransport-go 子库实现基于 HTTP/3 的实时双向通信（草案 ietf-webtrans-http3）。

# quic-go实战

##  **实现HTTP3服务端**

首先创建QUIC配置对象，接着初始化TLS配置（将InsecureSkipVerify设置为true，系统将跳过证书验证环节）。然后构建HTTP/3服务对象，最后调用其ListenAndServeTLS方法启动服务监听，该方法需指定证书文件路径。代码示例如下：

```go

func main() {

    quicConfig := &quic.Config{}

    tlsConfig := &tls.Config{
        InsecureSkipVerify: true,
    }

    fmt.Println("监听地址：127.0.0.1，端口号：8181")

    server := &http3.Server{
        Addr:       "127.0.0.1:8181",
        Port:       8181,
        TLSConfig:  tlsConfig,
        QUICConfig: quicConfig,
        Handler:    http3Handler(),
    }

    err := server.ListenAndServeTLS("D://ca/server.crt", "D://ca/server.key")
    if err != nil {
        logrus.Errorf("ListenAndServeTLS failed , error: %v", err)
        return
    }
}
```

定义HTTP3服务的URL路由处理器http3Handler，并配置NotFoundHandler和MethodNotAllowedHandler分别处理无效URL和不支持的方法请求。 代码示例如下：

```go

func http3Handler() http.Handler {

    router := mux.NewRouter()

    // 获取用户信息
    router.HandleFunc("/user/info", getUserInfo).Methods(http.MethodGet)

    // 删除用户信息
    router.HandleFunc("/user/info/{name}", delUserInfo).Methods(http.MethodDelete)

    // 添加用户信息
    router.HandleFunc("/user/info", addUserInfo).Methods(http.MethodPost)

    // 未找到匹配到URL处理
    router.NotFoundHandler = http.HandlerFunc(notFoundHandler)

    // 未找到匹配到方法处理
    router.MethodNotAllowedHandler = http.HandlerFunc(notMethodHandler)

    return router
}
```

如上代码所示，实现了用户信息查询、删除及新增三个接口功能。具体代码示例如下：

```go
// 获取用户信息
func getUserInfo(resp http.ResponseWriter, req *http.Request) {

    fmt.Printf("获取用户信息接口调用，URL: %s, 客户端地址: %s\n", req.URL.Path, req.RemoteAddr)

    sendResponseWithBody(resp, "", "获取用户信息")
}
// 添加用户信息
func addUserInfo(resp http.ResponseWriter, req *http.Request) {

    fmt.Printf("添加用户信息接口调用，URL: %s, 客户端地址: %s\n", req.URL.Path, req.RemoteAddr)

    body, err := io.ReadAll(req.Body)
    if err != nil {
        fmt.Printf("读取消息体失败，%v", err)
        sendResponse(resp, http.StatusBadRequest, err.Error())
        return
    }

    fmt.Printf("添加用户信息：%s\n", string(body))

    sendResponse(resp, http.StatusOK, "")
}

// 删除用户信息
func delUserInfo(resp http.ResponseWriter, req *http.Request) {

    fmt.Printf("删除用户信息接口调用，URL: %s, 客户端地址: %s\n", req.URL.Path, req.RemoteAddr)

    vars := mux.Vars(req)

    fmt.Printf("删除[%s]用户信息\n", vars["name"])

    sendResponse(resp, http.StatusOK, "")
}
```

提供两种消息发送方式：支持附带消息体的完整发送和不带消息体的简化发送。 ，具体代码示例如下：

```go

// 响应信息
func sendResponse(resp http.ResponseWriter, statusCode int, statusDesc string) {

    resp.WriteHeader(statusCode)

    if statusDesc == "" {
        _, _ = io.WriteString(resp, statusDesc)
    } else {
        _, _ = io.WriteString(resp, http.StatusText(statusCode))
    }
}

// 发送响应消息，携带消息体
func sendResponseWithBody(resp http.ResponseWriter, contentType, body string) {

    if contentType != "" {
        resp.Header().Set("Content-Type", contentType)
    }

    resp.Header().Set("Content-Length", strconv.Itoa(len(body)))

    _, err := io.WriteString(resp, body)
    if err != nil {
        sendResponse(resp, http.StatusInternalServerError, err.Error())
    }
}
```
当HTTP3服务端遇到无法识别的URL或HTTP请求方法时，会自动触发NotFoundHandler和MethodNotAllowedHandler方法，NotFoundHandler和MethodNotAllowedHandler具体实现代码如下：

```go

// 未找到匹配到URL处理
func notFoundHandler(resp http.ResponseWriter, req *http.Request) {

    fmt.Printf("unkown url: %s, method:%s, relay 404\n", req.URL, req.Method)

    sendResponse(resp, http.StatusNotFound, "URL not found")
}

// 未找到匹配到方法处理
func notMethodHandler(resp http.ResponseWriter, req *http.Request) {

    fmt.Printf("unkown method:%s, url: %s, relay 405\n", req.Method, req.URL)

    sendResponse(resp, http.StatusMethodNotAllowed, "Method Not Allowed")
}
```


## 实现HTTP3客户端

首先创建QUIC配置对象，并初始化x509证书池。接着设置TLS配置，启用InsecureSkipVerify选项以跳过证书验证。完成这些基础配置后，创建RoundTripper并构建最终的HTTP/3客户端对象。代码示例如下：

```djangourlpath

func main() {

    quicConfig := &quic.Config{}

    pool, err := x509.SystemCertPool()
    if err != nil {
        return
    }

    tlsConfig := &tls.Config{
        RootCAs:            pool,
        InsecureSkipVerify: true,
    }

    roundTripper := &http3.RoundTripper{
        TLSClientConfig: tlsConfig,
        QuicConfig:      quicConfig,
    }

    hclient := &http.Client{
        Transport: roundTripper,
    }

    getUserInfo(hclient)

    addUserInfo(hclient, "李四")

    deleteUserInfo(hclient, "张三")
}
```

如需使用证书，客户端需通过调用pool接口进行证书添加，上述示例演示的是无证书验证场景。代码示例如下：

```djangourlpath

caCertRaw, err := os.ReadFile("D://ca/ca.crt")
if err != nil {
    return
}

if ok := pool.AppendCertsFromPEM(caCertRaw); !ok {
    return
}
```

HTTP3实现用户信息的获取、新增与删除接口调用 ，代码示例如下：

```djangourlpath

// 获取用户信息
func getUserInfo(client *http.Client) {

    fmt.Println("获取用户信息:")

    request, err := http.NewRequest("GET", "https://127.0.0.1:8181/user/info", nil)
    if err != nil {
        return
    }

    resp, err := client.Do(request)
    if err != nil {
        return
    }

    body := &bytes.Buffer{}

    _, err = io.Copy(body, resp.Body)

    fmt.Printf("获取用户信息，响应码：%d， 消息体：%s\n", resp.StatusCode, body)
}

// 添加用户信息
func addUserInfo(client *http.Client, name string) {

    fmt.Printf("添加用户信息:%s", name)

    request, err := http.NewRequest("POST", "https://127.0.0.1:8181/user/info", strings.NewReader(name))
    if err != nil {
        return
    }

    resp, err := client.Do(request)
    if err != nil {
        return
    }

    body := &bytes.Buffer{}

    _, err = io.Copy(body, resp.Body)

    fmt.Printf("添加用户信息，响应码：%d\n", resp.StatusCode)
}

// 删除用户信息
func deleteUserInfo(client *http.Client, name string) {

    fmt.Printf("删除用户:%s", name)

    request, err := http.NewRequest("DELETE",
        fmt.Sprintf("https://127.0.0.1:8181/user/info/%s", name), nil)
    if err != nil {
        return
    }

    resp, err := client.Do(request)
    if err != nil {
        return
    }

    body := &bytes.Buffer{}

    _, err = io.Copy(body, resp.Body)

    fmt.Printf("删除用户信息，响应码：%d\n", resp.StatusCode)
}
```

代码运行

HTTP3服务端启动结果如下图所示：

![img_1.png](img_1.png)

客户端运行结果如下图所示：

![img_2.png](img_2.png)

服务端接收到客户端请求后输出如下图所示：

![img_3.png](img_3.png)

经抓包分析，服务器与客户端之间的通信协议采用QUIC协议，如下图所示：

![img_4.png](img_4.png)

  

