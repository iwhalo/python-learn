import traceback
import urllib.request
import urllib.error
import socket

def safe_request(url,timeout=10):
    try:
        response=urllib.request.urlopen(url=url,timeout=timeout)
        return response.read().decode('utf-8')

    except urllib.error.HTTPError as e:
        # HTTP错误（如404、500等）
        print(f"HTTP错误：{e.code} {e.reason}")
        print(f"错误信息：{e.read().decode('utf-8')}")

        return None
    except urllib.error.URLError as e:
        # URL错误（如连接失败、DNS解析失败等）
        print(f"URL错误：{e.reason}")
        if isinstance(e.reason,socket.timeout):
            print("连接超时")
        elif isinstance(e.reason,socket.gaierror):
            print("DNS解析失败")

        return None
    except socket.timeout:
        # 超时错误
        print("请求超时")
        return None
    except Exception as e:
        # 其他错误
        print(f"未知错误：{e}")
        return None

if __name__ == '__main__':
    # 测试不同类型的错误
    print('\n测试正常请求：')
    print(safe_request("http://www.baidu.com")[:100])

    print('\n测试HTTP错误：')
    print(safe_request('https://httpbin.org/status/404'))

    print('\n测试超时错误：')
    print(safe_request('https://httpbin.org/delay/15',timeout=5))

    print('\n测试DNS错误')
    print(safe_request('https://this-domain-does-not-exist.com'))