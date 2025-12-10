# 1. 导入第三方库
from openai import OpenAI
import os

"""
# OPENAI_API_KEY 是你想要设置的环境变量的名称
# api_key 代表该变量的值
# /M 选项将变量添加到系统环境变量中，而不是仅在当前会话中使用

 setx OPENAI_API_KEY "api_key" /M
"""


# 2. 设置API密钥的多种方式
def setup_openai_client():
    """
    尝试多种方式设置OpenAI客户端
    优先级：环境变量 > .env文件 > 直接输入
    """
    api_key = None

    # 方式1：检查系统环境变量
    api_key = os.getenv('OPENAI_API_KEY')
    print(api_key)

    # 方式2：如果没有，尝试从文件读取
    if not api_key:
        try:
            from dotenv import load_dotenv, find_dotenv
            load_dotenv(find_dotenv())
            api_key = os.getenv('OPENAI_API_KEY')
        except:
            pass

    # 方式3：如果还没有，提示用户输入
    if not api_key:
        print("⚠️ 未找到API密钥，请选择以下方式之一：")
        print("1. 在代码中直接设置（临时）")
        print("2. 创建.env文件并设置OPENAI_API_KEY")
        print("3. 设置系统环境变量OPENAI_API_KEY")

        # 临时方案：直接在这里输入（仅用于测试）
        # api_key = "your-api-key-here"  # 取消注释并填入你的API密钥

        # 或者让用户输入
        api_key = input("请输入你的OpenAI API密钥: ").strip()

        if not api_key:
            raise ValueError("未设置OpenAI API密钥")

    return OpenAI(api_key=api_key,base_url="https://api.deepseek.com")


# 3. 创建客户端
try:
    client = setup_openai_client()
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    print("\n请按照以下步骤操作：")
    print("1. 获取OpenAI API密钥: https://platform.openai.com/api-keys")
    print("2. 在项目根目录创建.env文件，添加: OPENAI_API_KEY=你的密钥")
    print("3. 或者直接在代码中设置api_key变量")
    exit(1)


# 4. 一个封装 OpenAI 接口的函数
def get_completion(prompt, model="deepseek-chat"):
    try:
        messages = [{"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"请求失败: {str(e)}"


# 5. 测试代码
if __name__ == "__main__":
    text = """
你应该提供尽可能清晰、具体的指示，以表达你希望模型执行的任务。
这将引导模型朝向所需的输出，并降低收到无关或不正确响应的可能性。
不要将写清晰的提示与写简短的提示混淆。
在许多情况下，更长的提示可以为模型提供更多的清晰度和上下文信息，从而导致更详细和相关的输出。
"""

#     prompt = f"""
# 把用三个反引号括起来的文本总结成一句话。
# ```{text}```
# """

    prompt = f"""
帮我写一个预测天气的python工程
    """

    print("正在请求AI...")
    response = get_completion(prompt)
    print("\n总结结果:")
    # print(response)

    # 将 response 写入 Python 文件
    with open('response_output.py','w',encoding='utf-8') as file:
        file.write(response)

    print("已保存到response_output.py文件")