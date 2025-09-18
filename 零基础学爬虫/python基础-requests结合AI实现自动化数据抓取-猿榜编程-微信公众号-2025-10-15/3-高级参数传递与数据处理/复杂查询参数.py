import requests

# 嵌套字典转换为查询参数
params = {
    'search': 'python requests',
    'filters': {
        'language': 'python',
        'license': 'MIT'
    },
    'tags[]': ['http', 'client']  # 数组参数
}
r = requests.get('https://api.example.com/search', params=params)
print(r.url)  # 查看最终构建的 URL