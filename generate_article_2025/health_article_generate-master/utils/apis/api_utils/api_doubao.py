import requests
import json
import os

api_key = os.getenv("DOUBAO_API_KEY")

def get_doubao_response(prompt, max_retries=5):
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": "ep-20250225110519-6hpgz",
        "messages": [
            {"role": "system", "content": "你是人工智能助手。"},
            {"role": "user", "content": prompt}
        ]
    }
    
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # 检查 HTTP 错误状态码
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("Max retries reached, returning None.")
                return None
    return None

if __name__ == "__main__":
    a = get_doubao_response("详细介绍一下你自己")
    print(a)