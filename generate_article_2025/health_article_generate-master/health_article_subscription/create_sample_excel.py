import pandas as pd
import os

def create_sample_topics_excel():
    """创建示例topics Excel文件"""
    
    # 准备数据
    topics_data = {
        'id': [1, 2, 3, 4, 5, 6],
        'topic': [
            '高血压',
            '冠心病',
            '脑卒中',
            '糖尿病',
            '骨质疏松',
            '老年性痴呆（阿尔茨海默病）'
        ]
    }
    
    # 创建DataFrame
    df = pd.DataFrame(topics_data)
    
    # 保存为Excel文件
    excel_path = 'topics.xlsx'
    df.to_excel(excel_path, index=False, engine='openpyxl')
    
    print(f"示例Excel文件已创建: {excel_path}")
    print("\n文件内容:")
    print(df)
    
    return excel_path

if __name__ == "__main__":
    create_sample_topics_excel()