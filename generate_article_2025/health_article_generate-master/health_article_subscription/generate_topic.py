import os 
from datetime import datetime
import random
import json
import csv
from tqdm import tqdm
from utils.multi_processing_tool import batch_execute
from utils.apis.api import get_instruction_response
from utils.tools_json.extract import extract_and_parse_json
from excel_reader import ExcelReader

def generate_dialog_scenarios(topic_file="topics.xlsx", prompt_path="./prompts/topic_generate.txt"):
    """
    生成对话场景数据
    
    参数:
        topic_file: 包含话题列表的文件路径（支持.txt和.xlsx格式）
        prompt_path: prompt模板文件路径
        
    返回:
        list: 包含字典的列表，每个字典包含topic, title, content三个键
    """
    # 打印调试信息
    print("当前工作目录:", os.getcwd())
    print("脚本绝对路径:", __file__)
    
    # 根据文件扩展名选择读取方式
    if topic_file.endswith('.xlsx') or topic_file.endswith('.xls'):
        # 使用Excel读取器
        excel_reader = ExcelReader(topic_file)
        topics_data = excel_reader.read_topics()
        topic_list = [item['topic'] for item in topics_data]
        topic_ids = [item['id'] for item in topics_data]
        print(f"从Excel文件找到 {len(topic_list)} 个话题")
    else:
        # 兼容原有的txt文件读取方式
        with open(topic_file, "r") as f:
            topic_list = [line.strip() for line in f if line.strip()]
        topic_ids = list(range(1, len(topic_list) + 1))  # 为txt文件生成默认ID
        print(f"从文本文件找到 {len(topic_list)} 个话题")
    
    print(f"话题列表: {topic_list}")
    
    # 读取prompt模板
    with open(prompt_path, "r") as f:
        prompt_template = f.read()
    
    def sample_occupations():
        occupations = [
            "快递员", "外卖骑手", "保洁员", "退休教师", "建筑工人", "工人",
            "销售", "程序员", "出租车司机", "保安", "货车司机", "服务员", "农民", "清洁工"
        ]
        return random.sample(occupations, k=8)
    
    # 构造prompt列表
    prompt_list = []
    for topic in topic_list:
        prompt = prompt_template.replace("{{topic}}", topic)
        role_list = sample_occupations()
        role_str = ", ".join(role_list)
        prompt = prompt.replace("{{role_list}}", role_str)
        prompt_list.append(prompt)
    
    # 批量执行
    args_list = [(prompt, 'doubao') for prompt in prompt_list]
    results = batch_execute(get_instruction_response, args_list, num_processes=10)
    
    # 准备输出数据结构
    output_data = []
    
    # 创建输出目录
    current_time = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output_topic_response/{current_time}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 计算文件序号
    file_count = len([f for f in os.listdir(output_dir) 
                     if os.path.isfile(os.path.join(output_dir, f))])
    
    # 文件路径
    csv_path = f"{output_dir}/topic_response_{file_count}.csv"
    jsonl_path = f"{output_dir}/topic_response_{file_count}.jsonl"
    
    # 处理结果并写入文件
    with open(csv_path, "w", newline='', encoding='utf-8') as csv_file, \
         open(jsonl_path, "w", encoding='utf-8') as jsonl_file:
        
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["topic_id", "topic", "title", "content"])
        
        # 使用tqdm添加进度条
        for topic_id, topic, response in tqdm(zip(topic_ids, topic_list, results), 
                                  total=len(topic_list), 
                                  desc="处理话题"):
            try:
                # 保存原始响应
                jsonl_file.write(json.dumps(response, ensure_ascii=False) + "\n")
                
                # 解析JSON数据
                response_dict = extract_and_parse_json(response)
                
                # 处理每个场景
                for title, content in response_dict.items():
                    # 添加到输出数据
                    output_data.append({
                        "topic_id": topic_id,
                        "topic": topic,
                        "title": title,
                        "content": content
                    })
                    # 写入CSV
                    csv_writer.writerow([topic_id, topic, title, content])
                    
            except Exception as e:
                print(f"解析失败 ({topic}): {e}")
                # 添加空数据
                output_data.append({
                    "topic_id": topic_id,
                    "topic": topic,
                    "title": "",
                    "content": ""
                })
                csv_writer.writerow([topic_id, topic, "", ""])
    
    print(f"处理完成! 结果已保存到: {csv_path} 和 {jsonl_path}")
    return output_data

# 使用示例
if __name__ == "__main__":
    scenarios = generate_dialog_scenarios()
    print(f"共生成 {len(scenarios)} 个对话场景")
    for item in scenarios[:5]:
        print(f"Topic: {item['topic']}, Title: {item['title']}, Content: {item['content'][:50]}...")