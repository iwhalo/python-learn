import urllib.request

class CustomMethodHandler(urllib.request.BaseHandler):

    def __init__(self):
        self.allowed_methods=['GET','POST','HEAD','PUT','DELETE','OPTIONS','PATCH']

    def http_request(self,request):
        # 检查请求方法是否在允许列表中
        if request.get_method() not in self.allowed_methods:
            raise urllib.error.HTTPError(
                request.full_url,
                405,
                f"Method Not Allowed:{request.get_method()}",
                {},
                None
            )
        return request
    https_request=http_request

# 创建自定义方法处理器
method_handler=CustomMethodHandler()

# 创建opener
opener=urllib.request.build_opener(method_handler)

# 创建PUT请求
req=urllib.request.Request(
    url='http://httpbin.org/put',
    data=b'{"key":"value"}',
    method='PUT'
)
req.add_header(
    'Content-Type','application/json'
)

# 发送请求
response=opener.open(req)
print(response.read().decode('utf-8'))

# 创建DELETE请求
req=urllib.request.Request(
    url='http://httpbin.org/delete',
    method='DELETE'
)

# 发送请求
response=opener.open(req)
print(response.read().decode('utf-8'))