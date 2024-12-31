class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserManager:
    def __init__(self):
        # 使用字典存储用户数据，键为用户名，值为 User 对象
        self.user_dict = {}

    def register(self, username, password):
        if username in self.user_dict:
            print("用户名已存在，请选择其他用户名。")
        else:
            self.user_dict[username] = User(username, password)
            print("注册成功！")

    def login(self, username, password):
        user = self.user_dict.get(username)
        if user and user.password == password:
            print("登录成功！")
            print(f"当前注册用户数量：{len(self.user_dict)}")
        else:
            print("用户名或密码错误。")

    def run(self):
        while True:
            print("\n1. 登录  2. 注册  Q. 退出")
            choice = input("请选择功能：").strip().upper()

            if choice == 'Q':
                break
            elif choice == '1':
                username = input("请输入用户名：")
                password = input("请输入密码：")
                self.login(username, password)
            elif choice == '2':
                username = input("请输入新用户名：")
                password = input("请输入密码：")
                self.register(username, password)
            else:
                print("无效选择，请重新输入！")


# 启动用户管理系统
if __name__ == '__main__':
    manager = UserManager()
    manager.run()