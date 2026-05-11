from tqdm import tqdm
from typing import Callable, List, Dict, Any

class Paragaraph:
    """
    paragarph 仅作为文章段落的容器类，包含文本和其他属性。
    可以对paragraph的文本进行修改。并且，将reform使用的prompt，reform前后的结果存放在其属性当中。
    值得注意的是，一个paragraph仅支持被reform一次。
    """
    def __init__(self, text, **kwargs):
        self.text = text
        self.attributes = kwargs

    def reform(self, prompt, reform_func, *args, **kwargs):
        """
        reform paragraph text using the provided function and prompt.
        This method should only be called once per paragraph.
        """        
        self.reform_prompt = prompt
        self.reformed_text = reform_func(prompt, *args, **kwargs)
        return self.reformed_text

    def __str__(self):
        if hasattr(self, 'reformed_text'):
            return self.reformed_text
        return self.text

    def jsonify(self):
        """
        Convert the paragraph to a dictionary representation.
        """
        data = {
            'text': self.text,
            'attributes': self.attributes
        }
        if hasattr(self, 'reform_prompt'):
            data['reform_prompt'] = self.reform_prompt
            data['reformed_text'] = self.reformed_text
        return data

def concat_paragraph_to_text(paragraphs: List[Paragaraph]) -> str:
    """
    如果有reform过的文本，则使用reformed_text，否则使用text。
    """
    return "\n\n".join(str(p) for p in paragraphs)

class Article:
    """
    Article 类用于存储文章的标题、作者、段落等信息。
    包含对文章段落的增删改查功能。
    """
    def __init__(self, title, topic, content,  **kwargs):
        self.title = title
        self.topic = topic
        self.content = content
        self.attributes = kwargs

    def outline_generate(self, prompt, outline_func, *args, **kwargs):
        """
        Generate an outline for the article using the provided function.
        """
        self.outline = outline_func(prompt, *args, **kwargs)
        self.outline_prompt = prompt

    def outline_parse(self, outline_parse_func, *args, **kwargs):
        """
        Parse the generated outline using the provided function.
        """
        assert hasattr(self, 'outline'), "Outline must be generated before parsing."
        try:
            self.parsed_outline = outline_parse_func(self.outline, *args, **kwargs)
            
            return self.parsed_outline
        except Exception as e:
            raise ValueError(f"Error parsing outline: {e}")


    def extend_paragraphs(self, prompt_list:[str], reform_func, *args, **kwargs):
        """
        自回归地进行段落扩展。方式是每一次扩展之后，将扩展后的部分和未扩展的部分进行拼接，形成新的{{aritlce}}变量，然后拼接到prompt当中。
        """
        if not hasattr(self, 'extended_paragraphs'):
            self.extended_paragraphs = []

        assert len(prompt_list) == len(self.parsed_outline), "Number of prompts must match the number of outline items."

        for i, prompt in tqdm(enumerate(prompt_list)):
            if i >= len(self.parsed_outline):
                raise IndexError("Prompt index exceeds the number of outline items.")
            
            already_reformed_paragraph_list = self.extended_paragraphs + self.parsed_outline[i:]
            already_reformed_article = concat_paragraph_to_text(already_reformed_paragraph_list)

            paragraph = Paragaraph(text=self.parsed_outline[i].text)

            if prompt is None:
                # 如果prompt为None，则不进行reform
                paragraph.reform_prompt = None
                paragraph.reformed_text = paragraph.text
            else:
                prompt = prompt.replace("{{aritlce}}", already_reformed_article)

                # 如果prompt不为None，则进行reform
                paragraph.reform_prompt = prompt
                paragraph.reform(prompt, reform_func, *args, **kwargs)

            self.extended_paragraphs.append(paragraph)

        return self.extended_paragraphs

    def stylize_paragraphs(self, prompt_list:[str], stylize_func, *args, **kwargs):
        """
        Stylize the paragraphs using the provided function and prompts.
        """
        if not hasattr(self, 'extended_paragraphs'):
            raise ValueError("No paragraphs to stylize. Please extend paragraphs first.")

        self.stylized_paragraphs = []

        assert len(prompt_list) == len(self.extended_paragraphs), "Number of prompts must match the number of extended paragraphs."

        for i, prompt in tqdm(enumerate(prompt_list)):
            if i >= len(self.extended_paragraphs):
                raise IndexError("Prompt index exceeds the number of extended paragraphs.")
            paragraph = Paragaraph(text=self.extended_paragraphs[i].reformed_text)

            alreayd_stylized_paragraph_list = self.stylized_paragraphs + self.extended_paragraphs[i:]
            already_stylized_article = concat_paragraph_to_text(alreayd_stylized_paragraph_list)
            if prompt is None:
                # 如果prompt为None，则不进行reform
                paragraph.reform_prompt = None
                paragraph.reformed_text = paragraph.text
            else:
                prompt = prompt.replace("{{article}}", already_stylized_article)
                # 如果prompt不为None，则进行reform
                paragraph.reform(prompt, stylize_func, *args, **kwargs)
            self.stylized_paragraphs.append(paragraph)
            

    def convert_to_text(self):
        # 将stylized_paragraphs转换为文本，使用\n\n分隔
        if not hasattr(self, 'stylized_paragraphs'):
            raise ValueError("No stylized paragraphs to convert to text.")
        return "\n\n".join(str(p) for p in self.stylized_paragraphs)
    

    def convert_to_text_with_backup_title(self):
        """
        Convert the article to text format with a backup title.
        If the backup title is not set, it will return the original title.
        """
        if hasattr(self, 'backup_title') and self.backup_title:
            return self.backup_title +  '\n\n---------------------\n\n' + self.convert_to_text()

        return self.title + '\n\n---------------------\n\n' + self.convert_to_text()


    def jsonify(self):
        """
        Convert the article to a dictionary representation.
        """
        data = {
            'title': self.title,
            'topic': self.topic,
            'attributes': self.attributes
        }
        if hasattr(self, 'outline'):
            data['outline'] = self.outline
        if hasattr(self, 'parsed_outline'):
            data['parsed_outline'] = [p.jsonify() for p in self.parsed_outline]
        if hasattr(self, 'extended_paragraphs'):
            data['extended_paragraphs'] = [p.jsonify() for p in self.extended_paragraphs]
        if hasattr(self, 'stylized_paragraphs'):
            data['stylized_paragraphs'] = [p.jsonify() for p in self.stylized_paragraphs]
        return data

    