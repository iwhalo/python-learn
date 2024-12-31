# 定义一个简单的问候类
class Greeter:
    def __init__(self, greet_word):
        # 保存问候语到对象属性中
        self.greet_word = greet_word

    def greet(self, name):
        # 使用对象的属性构造并输出完整的问候信息
        print(f"{self.greet_word}, {name}!")


# 通过类创建对象，并调用方法执行问候操作
greeter = Greeter("Hello")
greeter.greet("Alice")  # 输出：Hello, Alice!