import requests

# 指定接受的响应格式
headers = {'Accept': 'application/json'}
r = requests.get('https://api.example.com/users', headers=headers)

# 指定接受的编码方式
headers = {'Accept-Encoding': 'gzip, deflate, br'}
r = requests.get('https://example.com', headers=headers)

# 指定接受的语言
headers = {'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
r = requests.get('https://example.com', headers=headers)