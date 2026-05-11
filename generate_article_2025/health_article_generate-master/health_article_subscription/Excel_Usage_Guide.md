# Excel读取功能使用指南

## 功能概述

项目已升级支持从Excel文件读取话题数据，相比原有的txt文件方式，Excel提供了更好的数据管理和扩展性。

## 主要改进

1. **新增Excel读取模块** (`excel_reader.py`)
   - 支持读取包含`id`和`topic`列的Excel文件
   - 自动验证文件格式和必需列
   - 提供多种数据访问方式

2. **更新generate_topic.py**
   - 默认使用Excel文件（`topics.xlsx`）
   - 兼容原有txt文件格式
   - 输出数据增加`topic_id`字段

## Excel文件格式

Excel文件必须包含以下两列：
- `id`: 话题的唯一标识符（整数）
- `topic`: 话题内容（文本）

示例：
```
| id | topic                    |
|----|--------------------------|
| 1  | 高血压                   |
| 2  | 冠心病                   |
| 3  | 脑卒中                   |
| 4  | 糖尿病                   |
| 5  | 骨质疏松                 |
| 6  | 老年性痴呆（阿尔茨海默病）|
```

## 使用方法

### 1. 创建Excel文件

运行提供的脚本创建示例Excel文件：
```bash
python create_sample_excel.py
```

或手动创建包含`id`和`topic`列的Excel文件。

### 2. 使用Excel文件生成话题

在`generate_topic.py`中指定Excel文件：
```python
scenarios = generate_dialog_scenarios(topic_file="topics.xlsx")
```

### 3. 兼容性

如果需要使用原有的txt文件，仍然支持：
```python
scenarios = generate_dialog_scenarios(topic_file="topic.txt")
```

## API参考

### ExcelReader类

```python
from excel_reader import ExcelReader

# 创建读取器
reader = ExcelReader('topics.xlsx')

# 读取完整数据（返回字典列表）
topics_data = reader.read_topics()
# [{'id': 1, 'topic': '高血压'}, ...]

# 仅获取topic列表
topics_list = reader.get_topics_list()
# ['高血压', '冠心病', ...]

# 获取(id, topic)元组列表
topics_with_ids = reader.get_topics_with_ids()
# [(1, '高血压'), (2, '冠心病'), ...]
```

## 测试

运行测试脚本验证功能：
```bash
# 测试Excel读取器
python test_excel_reader.py

# 测试集成功能
python test_excel_simple.py
```

## 注意事项

1. 确保已安装必要的依赖：
   - pandas
   - openpyxl

2. Excel文件必须包含`id`和`topic`两列，否则会报错

3. 生成的输出文件（CSV和JSONL）现在包含`topic_id`字段