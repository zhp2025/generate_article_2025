
import time
import random
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
import os

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def get_deepseek_response(prompt: str, max_retries: int = 5, return_cot = False, model_name='deepseek-reasoner') -> str:
    if return_cot:
        assert model_name == 'deepseek-reasoner', "When return_cot is True, model_name must be 'deepseek-reasoner'."
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                stream=False,
                temperature=1.0
            )

            if return_cot:
                return response.choices[0].message.content, response.choices[0].message.reasoning_content
            return response.choices[0].message.content
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                sleep_duration = random.uniform(0.8, 1.2)
                time.sleep(sleep_duration)
            else:
                raise RuntimeError("All retries failed.") from e

if __name__ == "__main__":
    a =  get_r1_original_response("你叫啥", return_cot=True)
    print(a)
