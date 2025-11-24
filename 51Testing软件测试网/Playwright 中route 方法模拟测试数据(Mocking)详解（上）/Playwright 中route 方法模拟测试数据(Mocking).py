
from playwright.sync_api import sync_playwright

"""01 基础 Mocking 模式"""

# 基本响应模拟
def test_basic_mock():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # 模拟用户列表 API
        def mock_users(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"users": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]}'
            )
        page.route("**/api/users", mock_users)
        page.goto("http://localhost:3000")
        # 此时页面调用 /api/users 将返回模拟数据
        browser.close()



"""02 动态 Mocking 数据"""

# 基于请求参数的动态响应
def dynamic_mock_based_on_request(route):
    request = route.request
    # 根据查询参数返回不同数据
    if "user_id=1" in request.url:
        route.fulfill(
            status=200,
            body='{"id": 1, "name": "管理员", "role": "admin"}'
        )
    elif "user_id=2" in request.url:
        route.fulfill(
            status=200,
            body='{"id": 2, "name": "普通用户", "role": "user"}'
        )
    else:
        route.fulfill(status=404, body='{"error": "用户不存在"}')
page.route("**/api/user**", dynamic_mock_based_on_request)



# 基于请求体的动态响应
def mock_based_on_post_data(route):
    request = route.request
    if request.method == "POST" and request.post_data:
        post_data = request.post_data
        if "login" in request.url:
            # 解析登录数据
            if "admin" in post_data:
                route.fulfill(
                    status=200,
                    body='{"token": "admin-token", "user": {"role": "admin"}}'
                )
            else:
                route.fulfill(
                    status=200,
                    body='{"token": "user-token", "user": {"role": "user"}}'
                )
        else:
            route.continue_()
    else:
        route.continue_()
page.route("**/api/**", mock_based_on_post_data)


"""03 复杂业务场景 Mocking"""

# 完整的 CRUD 操作模拟

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

    def handle_post(self, route):
        # 创建用户
        post_data = json.loads(route.request.post_data)
        new_user = {
            "id": self.next_id,
            "name": post_data["name"],
            "email": post_data["email"]
        }

        self.users.append(new_user)
        self.next_id += 1
        route.fullfill(
            status=201,
            body=json.dumps(new_user)
        )

    def handle_put(self, route):
        # 更新用户
        user_id = int(route.request.url.split("/")[-1])
        user_data = json.loads(route.request.post_data)

        for user in self.users:
            if user['id'] == user_id:
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

    def handle_delete(self, route):
        # 删除用户
        user_id = int(route.request.url.split("/")[-1])
        self.users = [u for u in self.users if u["id"] == user_id]
        route.fullfill(
            status=204
        )


# 使用模拟服务
user_mock = UserServiceMock()
page.route("**/api/users**", user_mock.handle_user_routes)