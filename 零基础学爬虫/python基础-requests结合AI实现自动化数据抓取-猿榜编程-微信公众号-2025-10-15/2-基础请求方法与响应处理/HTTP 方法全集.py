import requests

response=requests.get('https://httpbin.org/get')
# print(response)
"""
<Response [200]>
"""
# print(response.text)
"""
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.32.3", 
    "X-Amzn-Trace-Id": "Root=1-68ef61fc-589f8dad3ff71ae246c88750"
  }, 
  "origin": "116.211.230.4", 
  "url": "https://httpbin.org/get"
}
"""

response=requests.post(url='https://httpbin.org/get', data={'key':'value'})
print(response)
"""
<Response [405]>
"""
print(response.text)
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
"""


response = requests.put('https://httpbin.org/put', data={'key': 'value'})
response = requests.delete('https://httpbin.org/delete')
response = requests.head('https://httpbin.org/get')  # 只返回响应头
response = requests.options('https://httpbin.org/get')  # 查询服务器支持的方法
response = requests.patch('https://httpbin.org/patch', data={'key': 'value'})