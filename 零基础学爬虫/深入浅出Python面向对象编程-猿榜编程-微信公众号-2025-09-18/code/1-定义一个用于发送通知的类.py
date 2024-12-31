# 定义一个用于发送通知的类
class Notifier:
    def __init__(self, message):
        # 使用 __init__ 方法在对象初始化时保存消息内容
        self.msg = message

    def send_email(self, email_address):
        # 模拟发送邮件的功能
        print(f"正在向 {email_address} 发送邮件，内容是: {self.msg}")

    def send_sms(self, phone_number):
        # 模拟发送短信的功能
        print(f"正在向 {phone_number} 发送短信，内容是: {self.msg}")


# 创建 Notifier 类的实例，并调用相应方法
notifier = Notifier("欢迎注册我们的系统！")
notifier.send_email("user@example.com")
notifier.send_sms("123-456-7890")