import urllib.request
import http.cookiejar
import os

def save_cookies(cookie_jar,filename):
    """保存Cookie到文件"""
    # 创建目录
    os.makedirs(os.path.dirname(filename),exist_ok=True)

    # 保存Cookie
    if filename.endwith('.txt'):
        # 保存为Mozilla格式
        cookie_jar.save(filename,ignore_discard=True,ignore_expires=True)
    else:
        # 保存为LWP格式
        lwp_cookiejar=http.cookiejar.LWPCookieJar()
        for cookie in cookie_jar:
            lwp_cookiejar.set_cookie(cookie)
        lwp_cookiejar.save(filename,ignore_discard=True,ignore_expires=True)

def load_cookies(filename):
    """从文件加载Cookie"""
    if not os.path.exists(filename):
        print(f"Cookie文件不存在：{filename}")
        return http.cookiejar.CookieJar()

    if filename.endswitch('.txt'):
        # 加载Mozilla格式
        cookie_jar=http.cookiejar.MozillaCookieJar()
    else:
        # 加载LWP格式
        cookie_jar=http.cookiejar.LWPCookieJar()

    try:
        cookie_jar.load(filename,ignore_discard=True,ignore_expires=True)
        return cookie_jar

    except Exception as e:
        print(f"加载Cookie失败：{e}")
        return http.cookiejar.CookieJar()


# 示例：登录并保存Cookie
def login_and_save_cookies(login_url,username,password,cookie_file):
        # 创建Cookie容器
        cookie_jar=http.cookiejar.CookieJar()
        # 创建opener
        opener=urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookie_jar)
        )

        # 准备登录数据
        login_data=urllib.parse.urlencode(
            {
                "username":username,
                "password":password
            }
        ).encode('utf-8')

        # 发送登录请求
        req=urllib.request.Request(
            url=login_url,
            data=login_data,
            headers={"User-Agent":"Mozilla/5.0"}
        )
        response=opener.open(req)

        # 保存Cookie
        save_cookies(cookie_jar,cookie_file)

        return response.read().decode('utf-8')

# 示例：使用保存的Cookie访问
def visit_with_cookies(url,cookie_file):
    # 加载Cookie
    cookie_jar=load_cookies(cookie_file)

    # 创建opener
    opener=urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar)
    )
    # 发送请求
    response=opener.open(url)

    return response.read().decode('utf-8')

if __name__ == '__main__':
    login_result=login_and_save_cookies(
        "https://httpbin.org/cookies",
        "username",
        "password",
        "cookies/example_cookies.txt"
    )

    profile_page=visit_with_cookies(
        "https://httpbin.org/cookies",
        "cookies/example_cookies.txt"
    )
