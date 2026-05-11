"""测试generate_topic.py的Excel功能"""
import os
from generate_topic import generate_dialog_scenarios

def test_generate_topic_with_excel():
    """测试使用Excel文件生成话题"""
    print("=== 测试generate_topic.py的Excel功能 ===\n")
    
    try:
        # 确保Excel文件存在
        if not os.path.exists('topics.xlsx'):
            print("✗ topics.xlsx文件不存在！")
            return False
        
        print("✓ 找到topics.xlsx文件")
        print("开始生成对话场景...\n")
        
        # 调用generate_dialog_scenarios，使用Excel文件
        scenarios = generate_dialog_scenarios(topic_file="topics.xlsx")
        
        print(f"\n✓ 成功生成 {len(scenarios)} 个对话场景")
        
        # 显示前几个结果
        if scenarios:
            print("\n前3个场景示例:")
            for i, scenario in enumerate(scenarios[:3], 1):
                print(f"\n场景 {i}:")
                print(f"  Topic ID: {scenario.get('topic_id', 'N/A')}")
                print(f"  Topic: {scenario['topic']}")
                print(f"  Title: {scenario['title']}")
                print(f"  Content: {scenario['content'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_generate_topic_with_excel()
    if success:
        print("\n✓ Excel读取功能测试完成！")
    else:
        print("\n✗ 测试失败，请检查错误信息。")