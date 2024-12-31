import urllib.request
import urllib.parse


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        # 重写了http_error_302方法，使其不自动重定向，而是直接返回响应对象（fp）
        return fp

    # 将其他重定向状态码(301, 303, 307)的处理也指向同一个方法
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


# 创建不进行重定向的opener
opener = urllib.request.build_opener(NoRedirectHandler())

# 发送请求
# 使用自定义opener发送请求到一个会重定向的URL
# 由于我们禁用了自动重定向，可以直接获取重定向信息而不是被自动跳转
# 打印重定向状态码和目标地址
response = opener.open("https://httpbin.org/redirect/1")

# 获取重定向信息
print(f"状态码：{response.code}")
print(f"重定向地址：{response.headers['Location']}")


# 手动跟踪重定向
def follow_redirects(url, max_redirects=10):
    redirect_count = 0
    current_url = url
    while redirect_count < max_redirects:
        print(f"请求：{current_url}")
        response = opener.open(current_url)

        # 检查是否是重定向状态码
        if response.code in (301, 302, 303, 307):
            redirect_count += 1
            # 获取重定向地址并转换为绝对URL
            redirect_url=response.headers['Location']
            # 使用urljoin将相对URL转换为绝对URL
            absolute_url=urllib.parse.urljoin(current_url,redirect_url)
            current_url = absolute_url

            print(f"重定向到：{current_url}")
        else:
            # 不是重定向，返回最终响应
            return response
    raise Exception(f"达到最大重定向次数：{max_redirects}")


if __name__ == '__main__':
    # 测试单个重定向
    response = opener.open("https://httpbin.org/redirect/1")
    print(f"状态码：{response.code}")
    print(f"重定向地址：{response.headers['Location']}")

    # 跟踪重定向链
    final_response = follow_redirects('https://httpbin.org/redirect/3')
    print(f"最终状态码：{final_response.code}")
    print(final_response.read().decode('utf-8')[:100])

"""
在这个代码示例中，URL `https://httpbin.org/redirect/3` 会重定向3次，这是因为 httpbin.org 提供了一个专门用于测试重定向的端点。

httpbin.org 是一个用于测试 HTTP 请求和响应的服务。它的 `/redirect/:n` 端点被设计为：
- 接收一个数字参数 `n`
- 进行 `n` 次重定向
- 最终重定向到 `/get` 端点（返回请求详情）

具体来说：
1. 第一次请求 `https://httpbin.org/redirect/3` 会返回 302 重定向到 `https://httpbin.org/redirect/2`
2. 第二次请求 `https://httpbin.org/redirect/2` 会返回 302 重定向到 `https://httpbin.org/redirect/1`
3. 第三次请求 `https://httpbin.org/redirect/1` 会返回 302 重定向到 `https://httpbin.org/redirect/0`
4. 第四次请求 `https://httpbin.org/redirect/0` 会最终返回 200 状态码和响应内容

所以实际上，当指定参数为 3 时，会发生 3 次重定向，最终在第 4 次请求时到达目的地。

这种设计使得开发者可以方便地测试他们的代码如何处理不同次数的重定向，而不需要自己搭建复杂的重定向服务器。这在测试重定向逻辑、循环检测、最大重定向限制等功能时非常有用。

在代码中，通过手动跟踪这些重定向，我们可以：
1. 观察完整的重定向链
2. 控制重定向过程（例如添加额外的逻辑）
3. 避免自动重定向可能带来的问题（如无限重定向循环）





注意事项
httpbin.org的重定向端点有时会返回相对URL，有时会返回绝对URL，这取决于具体的端点

使用urljoin可以确保无论返回哪种类型的URL，都能正确构建下一个请求的URL

这种处理方式更健壮，能够应对各种重定向场景

修改后的代码应该能够正确处理httpbin.org的重定向链，而不会出现"unknown url type"错误。
"""

# def http_error_302(self, req, fp, code, msg, headers):
#     return urllib.request.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
# def http_error_303(self, req, fp, code, msg, headers):
#     return urllib.request.HTTPRedirectHandler.http_error_303(self, req, fp, code, msg, headers)
# def http_error_307(self, req, fp, code, msg, headers):
#     return urllib.request.HTTPRedirectHandler.http_error_307(self, req, fp, code, msg, headers)
# def http_error_309(self, req, fp, code, msg, headers):
#     return urllib.request.HTTPRedirectHandler.http_error_309(self, req, fp, code, msg, headers)
# def http_error_308(self, req, fp, code, msg, headers):
#     return urllib.request.HTTPRedirectHandler.http_error_308(self, req, fp, code, msg, headers)
