# 健康文章订阅系统

一个基于大语言模型的健康科普文章自动生成系统，通过构建引人入胜的故事情节来传播健康知识，纠正常见的健康误区。

## 项目概述

本系统采用"话题生成→大纲构建→内容扩展→风格优化"的流程，自动生成高质量的健康科普文章。文章以40-65岁人群的真实生活场景为背景，通过悬念设置和故事化叙述，让读者在阅读过程中自然地获得健康知识。

## 核心特点

- **故事化叙述**：通过真实可信的人物和情节，提高文章吸引力
- **悬念设置**：保持读者阅读兴趣，提高完读率
- **科学准确**：内容基于医学常识，纠正常见健康误区
- **批量生成**：支持并行处理，高效生成大量文章
- **多格式输出**：支持JSON、Markdown、Pickle等多种格式

## 技术架构

### 核心模块

1. **话题生成模块** (`generate_topic.py`)
   - 基于输入的健康主题生成多个文章话题
   - 识别常见健康误区
   - 创建目标人群画像

2. **文章生成模块** (`generate_article.py`)
   - 生成文章大纲（4个章节）
   - 扩展段落内容
   - 优化文章风格
   - 生成多个备选标题

3. **主控制模块** (`main.py`)
   - 协调整个生成流程
   - 并行处理多篇文章
   - 管理输出文件

4. **数据模型** (`models/article_models.py`)
   - `Paragraph`：段落对象，管理文本转换
   - `Article`：文章对象，包含完整的文章结构和内容

5. **工具函数** (`article_utils.py`)
   - 加载提示词模板
   - 解析文章结构
   - 随机选择示例

### 文章生成流程

```
1. 话题生成
   输入：健康主题（如"尿控"）
   输出：包含人物、误区、标题的话题JSON

2. 大纲生成
   - 第一章：疾病概述与人物介绍
   - 第二章：症状表现与疾病进展
   - 第三章：医院诊断与核心悬念
   - 第四章：科普教育内容

3. 内容扩展
   - 根据大纲扩展每个章节
   - 使用示例指导写作风格
   - 保持故事连贯性

4. 风格优化
   - 调整语言流畅度
   - 确保段落衔接自然
   - 去除标注性内容

5. 标题生成
   - 生成5个备选标题
   - 采用4种标题公式
```

## 项目结构

```
health_article_subscription/
├── main.py                 # 主程序入口
├── generate_topic.py       # 话题生成
├── generate_article.py     # 文章生成
├── article_utils.py        # 工具函数
├── models/
│   └── article_models.py   # 数据模型
├── prompts/               # 提示词模板
│   ├── topic_generate.txt
│   ├── backup_title_generate.txt
│   └── structure1/
│       ├── meta.json
│       ├── topic_generate.txt
│       ├── title_generate.txt
│       ├── outline_generate.txt
│       ├── article_content_extension/
│       └── article_content_stylize/
├── examples/              # 示例数据
│   └── structure1/
│       ├── meta.json
│       ├── person_introduction.json
│       ├── problem.json
│       └── questionnaire.json
└── topic.txt             # 输入话题列表
```

## 使用方法

### 环境准备

```bash
# 安装依赖
pip install -r requirements.txt
```

### 基本使用

1. **准备话题**
   在 `topic.txt` 中添加健康主题，每行一个

2. **运行生成**
   ```bash
   python main.py
   ```

3. **查看输出**
   - 输出目录：`health_article_generate_[日期]/`
   - 包含JSON、Markdown和Pickle格式

### 配置参数

- **并行处理数**：`main.py` 中的 `max_workers=20`
- **批次大小**：`CHUNK_SIZE = 60`
- **LLM模型**：在 `generate_article.py` 中配置

## 输出格式

### JSON格式
```json
{
  "title": "文章标题",
  "paragraphs": [
    {
      "text": "段落内容",
      "reformed_text": "优化后的内容"
    }
  ],
  "backup_titles": ["备选标题1", "备选标题2", ...]
}
```

### Markdown格式
标准Markdown格式，包含标题和正文内容

## 数据模型

### Article类
- `outline_generate()`: 生成文章大纲
- `outline_parse()`: 解析大纲为段落
- `extend_paragraphs()`: 扩展段落内容
- `stylize_paragraphs()`: 优化段落风格
- `convert_to_text()`: 转换为文本格式
- `jsonify()`: 转换为JSON格式

### Paragraph类
- 存储原始文本和改写后的文本
- 记录使用的提示词
- 支持文本转换和格式化

## 注意事项

1. 确保LLM API配置正确
2. 文章内容基于医学常识，但不能替代专业医疗建议
3. 生成的文章需要人工审核后使用
4. 建议定期更新示例库以保持内容新鲜度

## 扩展开发

- 可以添加新的文章结构（在prompts目录下创建新结构）
- 可以自定义标题生成公式
- 可以调整段落扩展和风格优化的要求
- 支持接入不同的LLM服务商