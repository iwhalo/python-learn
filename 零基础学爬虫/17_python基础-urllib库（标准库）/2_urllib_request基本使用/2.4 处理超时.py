import urllib.request
import urllib.error
import socket

try:
    # 设置超时时间为3秒
    response=urllib.request.urlopen('http://www.baidu.com',timeout=3)
    html=response.read().decode('utf-8')
    print(html[:300])

except urllib.error.URLError as e:
    # 检查异常原因是否为 socket 超时
    if isinstance(e.reason,socket.timeout):
        print('请求超时')
    else:
        print(f'URLError:{e.reason}')

except socket.timeout:
    print('请求超时')