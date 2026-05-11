import pandas as pd
from typing import List, Dict, Tuple
import os


class ExcelReader:
    """Excel文件读取器，用于读取包含id和topic的Excel文件"""
    
    def __init__(self, file_path: str):
        """
        初始化Excel读取器
        
        Args:
            file_path: Excel文件路径
        """
        self.file_path = file_path
        self._validate_file()
    
    def _validate_file(self):
        """验证文件是否存在且为Excel格式"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"文件不存在: {self.file_path}")
        
        if not self.file_path.endswith(('.xlsx', '.xls')):
            raise ValueError(f"文件必须是Excel格式 (.xlsx 或 .xls): {self.file_path}")
    
    def read_topics(self) -> List[Dict[str, any]]:
        """
        读取Excel文件中的topics
        
        Returns:
            包含id和topic的字典列表
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(self.file_path)
            
            # 检查必需的列
            required_columns = ['id', 'topic']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Excel文件缺少必需的列: {missing_columns}")
            
            # 过滤空值
            df = df.dropna(subset=['id', 'topic'])
            
            # 转换为字典列表
            topics = []
            for _, row in df.iterrows():
                topics.append({
                    'id': int(row['id']),
                    'topic': str(row['topic']).strip()
                })
            
            return topics
            
        except Exception as e:
            raise Exception(f"读取Excel文件时出错: {str(e)}")
    
    def get_topics_list(self) -> List[str]:
        """
        获取所有topic的列表（仅topic内容）
        
        Returns:
            topic字符串列表
        """
        topics_data = self.read_topics()
        return [item['topic'] for item in topics_data]
    
    def get_topics_with_ids(self) -> List[Tuple[int, str]]:
        """
        获取带有ID的topic列表
        
        Returns:
            (id, topic) 元组列表
        """
        topics_data = self.read_topics()
        return [(item['id'], item['topic']) for item in topics_data]