import requests

r=requests.get('https://api.github.com/events')

# 响应状态与头信息
# print(r.status_code)  # 状态码
# print(r.reason)       # 状态文本
# print(r.headers)      # 响应头字典
# print(r.headers['Content-Type'])  # 获取特定响应头
# print(r.url)          # 最终响应 URL（可能经过重定向）
# print(r.history)      # 重定向历史
# print(r.elapsed)      # 请求耗时 (timedelta 对象)
# print(r.request)      # 原始请求对象

# 响应内容获取与解析
# print(r.encoding)     # 编码方式
r.encoding = 'utf-8'  # 手动设置编码（覆盖自动检测）
# print(r.text)         # 文本形式的响应内容
# print(r.content)      # 二进制形式的响应内容
# print(r.json())       # 解析 JSON 响应

# 高效的迭代流式响应
for line in r.iter_lines():
    if line:
        print(line.decode('utf-8'))