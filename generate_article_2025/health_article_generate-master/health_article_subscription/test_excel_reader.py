"""测试Excel读取功能"""
from excel_reader import ExcelReader

def test_excel_reader():
    """测试Excel读取器的各个功能"""
    print("=== 测试Excel读取器 ===\n")
    
    try:
        # 创建Excel读取器实例
        reader = ExcelReader('topics.xlsx')
        print("✓ Excel文件读取成功\n")
        
        # 测试读取完整数据
        print("1. 测试read_topics()方法:")
        topics_data = reader.read_topics()
        print(f"   读取到 {len(topics_data)} 条数据")
        for item in topics_data[:3]:  # 显示前3条
            print(f"   - ID: {item['id']}, Topic: {item['topic']}")
        print("   ...\n")
        
        # 测试获取topic列表
        print("2. 测试get_topics_list()方法:")
        topics_list = reader.get_topics_list()
        print(f"   Topic列表: {topics_list}\n")
        
        # 测试获取带ID的topic列表
        print("3. 测试get_topics_with_ids()方法:")
        topics_with_ids = reader.get_topics_with_ids()
        for id, topic in topics_with_ids[:3]:  # 显示前3条
            print(f"   - ({id}, {topic})")
        print("   ...\n")
        
        print("✓ 所有测试通过！")
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    test_excel_reader()