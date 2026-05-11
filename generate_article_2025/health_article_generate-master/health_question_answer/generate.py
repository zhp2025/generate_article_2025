import os
import random
import re
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# 修正原代码中的拼写错误 (prompt_tempalte -> prompt_template)
from utils.apis.api import get_instruction_response

prompt_template = open("prompt/prompt_template.txt").read()

def generate(topic):
    """生成文章内容"""
    paragarph_number = random.choice([2, 3, 4])
    prompt = prompt_template.replace("{{topic}}", topic).replace("{{paragraph_number}}", str(paragarph_number))
    # article = get_instruction_response(prompt, 'ds-r1')
    article = get_instruction_response(prompt, 'doubao')
    return topic + '\n\n' + article

def load_topic():
    """加载主题列表"""
    with open("topic.txt", 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def sanitize_filename(topic):
    """清理文件名中的非法字符"""
    return re.sub(r'[\\/*?:"<>|]', "", topic).strip()

def process_topic(topic, output_dir="output"):
    """处理单个主题的生成和保存"""
    try:
        # 生成文章内容
        article = generate(topic).replace("\n","\n\n").replace("\n\n#","\n#")
        
        # 创建安全文件名
        filename = f"{sanitize_filename(topic)}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article)
            
        return True, topic
    except Exception as e:
        # 打印错误日志但继续运行
        print(f"处理主题失败: {topic}\n错误: {str(e)}\n{traceback.format_exc()}")
        return False, topic

def main():
    # 确保输出目录存在
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载主题列表
    topics = load_topic()
    print(f"加载到 {len(topics)} 个主题")
    
    # 使用线程池处理
    with ThreadPoolExecutor(max_workers=5) as executor:  # 可调整线程数
        futures = {executor.submit(process_topic, topic, output_dir): topic for topic in topics}
        
        # 使用tqdm创建进度条
        success_count = 0
        with tqdm(total=len(topics), desc="生成文章") as pbar:
            for future in as_completed(futures):
                status, topic = future.result()
                if status:
                    success_count += 1
                pbar.update(1)
                pbar.set_postfix_str(f"成功: {success_count}/{len(topics)}")
    
    print(f"处理完成! 成功: {success_count}, 失败: {len(topics)-success_count}")

if __name__ == "__main__":
    main()