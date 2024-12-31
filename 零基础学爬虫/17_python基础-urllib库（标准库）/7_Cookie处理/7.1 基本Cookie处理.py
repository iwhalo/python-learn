import urllib.request
import http.cookiejar

# 创建Cookie容器
cookie_jar=http.cookiejar.CookieJar()

# 创建Cookie处理器
cookie_handler=urllib.request.HTTPCookieProcessor(cookie_jar)

# 创建opener
opener=urllib.request.build_opener(cookie_handler)

# 发送请求
response=opener.open('https://httpbin.org/cookies/set?name=value')

# 打印Cookie
print("Cookie内容：")
for cookie in cookie_jar:
    print(f"{cookie.name}：{cookie.value}")


# 发送第二个请求，自动携带Cookie
response=opener.open('https://httpbin.org/cookies')
print("\n响应内容：")
print(response.read().decode('utf-8'))
