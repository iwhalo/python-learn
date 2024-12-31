import urllib.request
import urllib.error

class CustomHttpErrorHandler(urllib.request.HTTPDefaultErrorHandler):

    def http_error_404(self,req,fp,code,msg,hdrs):
        print(f"自定义404处理：{req.full_url}")
        # 可以返回自定义内容或者执行特定操作
        return urllib.error.HTTPError(req.full_url,code,msg,hdrs,fp)

    def http_error_500(self,req,fp,code,msg,hdrs):
        print(f"自定义500处理：{req.full_url}")
        # 可以实现重试逻辑
        try:
            # 尝试重试请求
            return self.parent.open(req)
        except:
            return urllib.error.HTTPError(req.full_url,code,msg,hdrs,fp)

# 创建自定义错误处理器
error_handler=CustomHttpErrorHandler()

# 创建opener
opener=urllib.request.build_opener(error_handler)

# 安装opener
urllib.request.install_opener(opener)

if __name__ == '__main__':
    # 测试404结果
    try:
        response=urllib.request.urlopen('https://httpbin.org/status/404')
    except urllib.error.HTTPError as e:
        print(f"捕获到HTTP错误：{e.code}")
