import urllib.request
import http.cookiejar




# 创建自定义opener
def create_opener(use_cookies=True,proxy=None,timeout=10,debug=False):
    handlers=[]

    # Cookie处理
    if use_cookies:
        cookie_jar=http.cookiejar.CookieJar()
        handlers.append(urllib.request.HTTPCookieProcessor(cookie_jar))


    # 代理设置
    if proxy:
        handlers.append(urllib.request.ProxyHandler(proxy))

    # 超时设置
    handlers.append(urllib.request.HTTPHandler(debuglevel=1 if debug else 0))
    handlers.append(urllib.request.HTTPSHandler(debuglevel=1 if debug else 0))

    # 创建opener
    opener=urllib.request.build_opener(*handlers)

    # 设置基本请求头
    opener.addheaders=[
        ('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64)'),
        ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9'),
        ('Accept-Language','zh-CN,zh;q=0.9,en;q=0.8')
    ]

    return opener

if __name__ == '__main__':
    # 使用自定义opener
    opener = create_opener(
        use_cookies=True,
        proxy={'http': 'http://127.0.0.1:8080'},
        debug=True
    )

    # 发送请求
    try:
        response = opener.open('https://www.baidu.com/', timeout=5)
        print(response.read().decode('utf-8')[:100])
    except Exception as e:
        print(f"请求失败：{e}")