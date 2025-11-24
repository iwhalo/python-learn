from pydoc import pager

# Playwright 中route 方法模拟测试数据(Mocking)详解（上）

蛋仔聊测试 [51Testing软件测试网](javascript:void(0);)

_2025年11月14日 15:30_ _上海_

在小说阅读器中沉浸阅读

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFoTiclu7A2x9tXsb36XqIk0cybTgib2tad5FlJjdLmnslBK64n1asMaDVQ87qLONDkMXp5ibiaChXzL0Q/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

**点击蓝字，立即关注**

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/BuV4gXrNvFoTiclu7A2x9tXsb36XqIk0cQN029E1KpqvKV9Jb0wNNHxJLN2KPAtvLe3rF7k66Is7iadIHI7xibAng/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

  

Mocking 是 route 方法最重要的应用之一，用于在测试中模拟后端 API 响应，实现测试与真实后端服务的解耦。

  

**01**

  

**基础 Mocking 模式**

  

  

基本响应模拟

```python
from playwright.sync_api import sync_playwright
def test_basic_mock():
    with sync_playwright() as p:
        browser=p.chromium.lanch()
        page=browser.new_page()
        # 模拟用户列表 API
        def mock_users(route):
            route.fullfill(
                status=200,
                content_type="application/json",
                body='{"users":[{"id":1,"name":"张三"},{"id":2,"name":"李四"}]}'
            )
        page.route("**/api/users",mock_users)
        page.goto("http://localhost:3000")
        # 此时页面调用/api/users 将返回模拟数据
        browser.close()
```
  

**02**

  

**动态 Mocking 数据**

  

  

基于请求参数的动态响应

```python
def dynamic_mock_based_on_request(route):
    request=route.request()
    # 根据查询参数返回不同数据
    if "user_id=1" in request.url:
        route.fullfill(
            status=200,
            body='{"id":1,"name":"管理员","role":"admin"}'
            
        )
    elif "user_id=2" in request.url:
        route.fullfill(
            status=200,
            body='{"id":2,"name":"普通用户","role":"user"}'
        )
    else:
        route.fullfill(
            status=404,
            body={"error":"用户不存在"}
        )

page.route("**/api/user**",dynamic_mock_based_on_request)
```

  

基于请求体的动态响应

```python
def mock_based_on_post_data(route):
    request=route.request()
    if request.method=="POST":
        post_data=request.post_data
        if "login" in request.url:
            # 解析登录数据
            if "admin" in post_data:
                route.fullfill(
                    status=200,
                    body='{"token:"admin-token","user":{"role":"admin"}}'
                )
            else:
                route.fullfill(
                    status=200,
                    body='{"tokne":"user-token","user":{"role":"user"}}'
                )
        else:
            route.continue_()
    else:
        route.continue_()

page.route("**/api/**",mock_based_on_post_data)
```

  

**03**

  

**复杂业务场景 Mocking**

  

  

完整的 CRUD 操作模拟

```python
import json


class UserServiceMock:
    def __init__(self):
        self.users = [
            {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
            {"id": 2, "name": "李四", "email": "lisi@example.com"}
        ]

        self.next_id = 3

    def handle_user_routes(self, route):
        request = route.request()
        if request.method == "GET":
            self.handle_get(route)
        elif request.method == "POST":
            self.handle_post(route)
        elif request.method == "PUT":
            self.handle_put(route)
        elif request.method == "DELETE":
            self.handle_delete(route)

    def handle_get(self, route):
        if route.request.url.endwith("/api/users"):
            # 获取用户列表
            route.fullfill(
                status=200,
                body=json.dumps({"users": self.users})
            )
        else:
            # 获取单个用户
            user_id = int(route.request.url.split("/"))
            user = next((u for u in self.users if u["id"] == user_id), None)
            if user:
                route.fullfill(
                    status=200,
                    body=json.dumps(user)
                )
            else:
                route.fullfill(
                    status=404,
                    body='{"error":"用户不存在"}'
                )

    def handle_post(self,route):
        # 创建用户
        post_data=json.loads(route.request.post_data)
        new_user={
            "id":self.next_id,
            "name":post_data["name"],
            "email":post_data["email"]
        }

        self.users.append(new_user)
        self.next_id+=1
        route.fullfill(
            status=201,
            body=json.dumps(new_user)
        )


    def handle_put(self,route):
        # 更新用户
        user_id=int(route.request.url.split("/")[-1])
        user_data=json.loads(route.request.post_data)
        
        for user in self.users:
            if user['id']==user_id:
                user.update(user_data)
                route.fullfill(
                    status=200,
                    body=json.dumps(user)
                )
                return 

        route.fullfill(
            status=404,
            body='{"error":"用户不存在"}'
        )


    def handle_delete(self,route):
        # 删除用户
        user_id=int(route.request.url.split("/")[-1])
        self.users=[u for u in self.users if u["id"]==user_id]
        route.fullfill(
            status=204
        )

# 使用模拟服务
user_mock=UserServiceMock()
page.route("**/api/users**",user_mock.handle_user_routes)
```

  

未完待续，下篇我们将带领大家继续学习**错误场景模拟**、**高级 Mocking 技巧**、**测试用例中的最佳实践**以及**调试和验证**等内容~