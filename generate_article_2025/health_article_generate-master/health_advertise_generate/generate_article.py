import os
import random
import json
from utils.apis.api import get_instruction_response
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from datetime import datetime


# 读取模板
prompt_template = open("prompt/尿控.txt", "r", encoding="utf-8").read()

def construct_prompt():
    begin_list = json.load(open("example/尿控/开头样例.json", "r", encoding="utf-8"))
    infor_dict = json.load(open("example/尿控/尿控_parsed.json", "r", encoding="utf-8"))
    character = json.load(open("example/尿控/人物.json", "r", encoding="utf-8"))

    # 从infor_dict的keys()中随机选择一个key作为主题
    theme = random.choice(list(infor_dict.keys()))
    disabled_dict = infor_dict[theme]
    character = random.choice(character[theme])
    begin = random.choice(begin_list)
    
    prompt = prompt_template.replace("{{开头样例}}", begin).replace("{{疾病}}", theme).replace("{{症状}}", disabled_dict["症状"]).replace("{{病因}}", disabled_dict["病因"]).replace("{{检查}}", disabled_dict["检查"]).replace("{{骶神经调节术}}", disabled_dict["骶神经调节术"]).replace("{{角色设定}}", character)

    return prompt

def write_one_article(index):
    prompt = construct_prompt()
    response = get_instruction_response(prompt, model='doubao-1.6')
    if '【以下正文】' in response:
        response = response.split('【以下正文】')[1].strip()
    else:
        return 'error'

    title_prompt_template = open("prompt/title_generate.txt", "r", encoding="utf-8").read()
    title_prompt = title_prompt_template.replace("{{article}}", response)
    title = get_instruction_response(title_prompt, model='doubao-1.6')

    # 保存文章到文件
    output_dir = f"output/尿控/dt={datetime.now().strftime('%Y-%m-%d')}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_path = os.path.join(output_dir, f"article_{index + 1}_{title}.txt")

    response = title + "\n\n" + response
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response)
    
    return file_path

def generate_articles():
    # 使用线程池并发生成文章
    with ThreadPoolExecutor(max_workers=10) as executor:  # 可以调整 max_workers 根据系统能力
        # 使用 tqdm 来显示进度条
        results = list(tqdm(executor.map(write_one_article, range(30)), total=30))

    return results

# 运行生成文章函数
if __name__ == "__main__":
    generate_articles()
