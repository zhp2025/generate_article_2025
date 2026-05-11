import json
import pickle
import os
import re
import shutil
from pathlib import Path
import datetime

from generate_topic import generate_dialog_scenarios
from generate_article import generate_article
from markdown_to_word import MarkdownToWordConverter

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

# 清理文件名函数 - 保留安全字符
def clean_filename(name, max_length=100):
    """清理文件名，只保留字母、数字、汉字、下划线和连字符"""
    if not name:
        return "untitled"
    
    # 移除非法字符
    cleaned = re.sub(r'[^\w\u4e00-\u9fff-]', '_', name)
    
    # 缩短文件名
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned

def generate_article_chunk(data_dicts, prompt_dir_path, example_dir_path, max_workers=20):
    """
    并发处理多个数据字典生成文章
    
    参数:
        data_dicts (list): 包含多个数据字典的列表
        prompt_dir_path (str): prompt模板目录路径
        example_dir_path (str): 示例目录路径
        max_workers (int): 最大并发工作线程数，默认为10
        
    返回:
        list: 包含所有生成文章的列表，顺序与输入data_dicts一致
    """
    results = [None] * len(data_dicts)  # 预分配结果列表，保持顺序
    errors = []  # 收集错误信息
    
    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_index = {
            executor.submit(
                generate_article_safe,  # 使用安全包装函数
                data_dict, 
                prompt_dir_path, 
                example_dir_path,
                idx
            ): idx 
            for idx, data_dict in enumerate(data_dicts)
        }
        
        # 设置进度条
        with tqdm(total=len(data_dicts), desc="生成文章") as pbar:
            # 处理完成的任务
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result, error = future.result()
                    if error:
                        errors.append(error)
                    results[idx] = result
                except Exception as e:
                    error_msg = f"处理索引 {idx} 时发生未捕获异常: {str(e)}"
                    errors.append(error_msg)
                    results[idx] = None
                finally:
                    pbar.update(1)  # 更新进度条
    
    # 打印所有错误信息
    if errors:
        print("\n" + "="*50 + " 错误汇总 " + "="*50)
        for i, error in enumerate(errors, 1):
            print(f"错误 #{i}: {error}")
        print("="*110 + "\n")
    
    return results

def generate_article_safe(data_dict, prompt_dir_path, example_dir_path, index):
    """
    安全包装函数，捕获并返回异常信息
    
    参数:
        data_dict (dict): 输入数据字典
        prompt_dir_path (str): prompt模板目录路径
        example_dir_path (str): 示例目录路径
        index (int): 数据索引，用于错误追踪
        
    返回:
        tuple: (生成的文章或None, 错误信息或None)
    """
    try:
        article = generate_article(data_dict, prompt_dir_path, example_dir_path)
        return article, None
    except Exception as e:
        # 捕获详细错误信息
        error_msg = (
            f"索引 {index} 生成文章失败: {str(e)}\n"
            f"数据内容: {str(data_dict)[:200]}...\n"
            f"堆栈跟踪:\n{traceback.format_exc()}"
        )
        return None, error_msg


if __name__ == "__main__":
    prompt_dir_path = "./prompts/structure1"
    example_dir_path = "./examples/structure1"
    topic_file = "topic7.25.xlsx"
    chunk_size = 120  # 每个chunk的大小

    # 创建基础输出目录
    current_date = datetime.datetime.now().strftime("%Y-%m-%d") 
    output_dir = os.path.join("output", current_date)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 获取当前日期下的文件夹数量
    existing_parts = [d for d in os.listdir(output_dir) 
                     if os.path.isdir(os.path.join(output_dir, d)) and d.startswith("part_")]
    next_part_num = len(existing_parts) + 1
    
    # 2. 运行generate_topic获取数据字典
    print("生成话题数据...")
    data_dicts = generate_dialog_scenarios(topic_file=topic_file)
    print(f"共生成 {len(data_dicts)} 个话题数据")
    
    # 3. 将数据分块
    chunks = [data_dicts[i:i + chunk_size] 
             for i in range(0, len(data_dicts), chunk_size)]
    
    print(f"将数据分成 {len(chunks)} 个块，每块大小约 {chunk_size}")
    
    # 处理每个chunk
    for chunk_idx, chunk_data in enumerate(chunks, start=next_part_num):
        # 创建当前chunk的保存目录
        save_chunk_dir = os.path.join(output_dir, f"part_{chunk_idx}")
        os.makedirs(save_chunk_dir, exist_ok=True)
        
        # 创建子目录
        json_dir = os.path.join(save_chunk_dir, "json_result")
        md_dir = os.path.join(save_chunk_dir, "markdown_result")
        pkl_dir = os.path.join(save_chunk_dir, "pkl_result")
        word_dir = os.path.join(save_chunk_dir, "word_result")
        
        for dir_path in [json_dir, md_dir, pkl_dir, word_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        print(f"\n处理块 #{chunk_idx}，保存到: {save_chunk_dir}")
        
        # 生成文章
        articles = generate_article_chunk(
            data_dicts=chunk_data,
            prompt_dir_path=prompt_dir_path,
            example_dir_path=example_dir_path,
            max_workers=60
        )
        
        # 保存结果
        success_count = 0
        error_count = 0
        
        for idx, article in enumerate(articles):
            if not article:
                error_count += 1
                continue
            
            try:
                # 获取标题并清理文件名
                title = getattr(article, "title", f"article_{chunk_idx}_{idx}")
                clean_title = clean_filename(title)
                
                # 基本文件名
                base_filename = f"{chunk_idx}_{idx}_{clean_title}"
                
                # 保存JSON
                json_path = os.path.join(json_dir, f"{base_filename}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(article.jsonify(), f, ensure_ascii=False, indent=2)
                
                # 保存Markdown
                md_path = os.path.join(md_dir, f"{base_filename}.md")
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(article.convert_to_text_with_backup_title())
                
                # 保存Word文档
                word_path = os.path.join(word_dir, f"{base_filename}.docx")
                converter = MarkdownToWordConverter(Path(md_dir), Path(word_dir))
                converter.convert_md_to_word(Path(md_path), Path(word_path))
                
                # 保存Pickle
                pkl_path = os.path.join(pkl_dir, f"{base_filename}.pkl")
                with open(pkl_path, "wb") as f:
                    pickle.dump(article, f)
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"保存文章失败 (块 {chunk_idx} - 索引 {idx}): {str(e)}")
                traceback.print_exc()
        
        # 保存元数据
        meta_data = {
            "chunk_index": chunk_idx,
            "processed_at": datetime.datetime.now().isoformat(),
            "total_articles": len(articles),
            "success_count": success_count,
            "error_count": error_count,
            "chunk_size": len(chunk_data),
            "prompt_dir": prompt_dir_path,
            "example_dir": example_dir_path
        }
        
        meta_path = os.path.join(save_chunk_dir, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2)
        
        print(f"块 #{chunk_idx} 处理完成: "
              f"成功 {success_count}/{len(articles)} 篇文章, "
              f"失败 {error_count} 篇")
        
        # 创建下一个chunk目录的占位符
        next_chunk_dir = os.path.join(output_dir, f"part_{chunk_idx + 1}")
        Path(next_chunk_dir).mkdir(exist_ok=True)
    
    print("\n所有块处理完成!")