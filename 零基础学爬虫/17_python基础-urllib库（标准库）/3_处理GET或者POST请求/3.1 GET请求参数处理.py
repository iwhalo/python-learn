import urllib.request
import urllib.parse

# 基础url
base_url='http://www.baidu.com'

# 请求参数
params={
    'name':'张三',
    'age':25,
    'city':'beijing'
}

# 构建完整url
query_string=urllib.parse.urlencode(params)
full_url=f'{base_url}?{query_string}'

print(f'完整URL：{full_url}')

# 发送GET请求
response=urllib.request.urlopen(full_url)
result=response.read().decode('utf-8')
print(result)

