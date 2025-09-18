import requests

# 使用上下文管理器自动关闭会话
with requests.Session() as s:
    s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
    r = s.get('https://httpbin.org/cookies')
    print(r.json())  # 自动携带之前设置的 Cookie
# 会话自动关闭，释放连接池资源

"""
{'cookies': {'sessioncookie': '123456789'}}
"""