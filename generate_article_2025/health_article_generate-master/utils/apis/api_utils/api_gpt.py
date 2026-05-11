from openai import OpenAI
import os
import time
import requests 

api_key = os.getenv("OPENAI_API_KEY")
def get_gpt_response(query):
    """
    封装的函数，用于调用 OpenAI 的聊天接口。

    参数：
        query (str): 用户的输入内容。

    返回：
        dict: 返回聊天模型生成的结果。
    """
    try:
        # 初始化 OpenAI 客户端
        client = OpenAI(
            base_url='https://api.openai-proxy.org/v1',
            api_key=api_key,
        )

        # 调用聊天模型
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model="gpt-4o",
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return {"error": str(e)}
