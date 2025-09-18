import requests

# Form 表单数据
form_data = {'username': 'user1', 'password': 'pass123'}
r = requests.post('https://httpbin.org/post', data=form_data)

# URL 编码的表单数据（手动控制）
from urllib.parse import urlencode
encoded_data = urlencode({'key': 'value with spaces'})
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
r = requests.post('https://httpbin.org/post', data=encoded_data, headers=headers)

# JSON 数据
json_data = {'name': 'John', 'age': 30, 'city': 'New York'}
r = requests.post('https://httpbin.org/post', json=json_data)  # 自动设置 Content-Type
# 或手动编码 JSON
import json
r = requests.post(
    'https://httpbin.org/post',
    data=json.dumps(json_data),
    headers={'Content-Type': 'application/json'}
)

# 复杂表单数据（含文件和字段混合）
files = {
    'file': ('report.pdf', open('report.pdf', 'rb'), 'application/pdf'),
    'file2': ('data.csv', open('data.csv', 'rb'), 'text/csv'),
    'field': (None, 'value'),  # 普通字段
    'field2': (None, json.dumps({'a': 1}), 'application/json')  # JSON 字段
}
r = requests.post('https://httpbin.org/post', files=files)