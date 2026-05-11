import json
import os


from utils.apis.api import get_instruction_response
from models.article_models import Article, Paragaraph
from article_utils import load_prompt, article_split_func, load_example

def llm_func_factory(model_name):
    """
    Factory function to create a function that calls the LLM API.
    """
    def llm_func(prompt, *args, **kwargs):
        return get_instruction_response(prompt, model=model_name, *args, **kwargs)
    return llm_func

def generate_backup_title(article:Article):
    prompt_tempalte = open("prompts/backup_title_generate.txt", "r", encoding="utf-8").read()
    prompt = prompt_tempalte.replace("{{article}}", article.convert_to_text())
    response = get_instruction_response(prompt, model='ds-r1')

    back_up_titles = response.split("\n")

    back_up_titles_list = []
    for title in back_up_titles:
        if title.strip("\n").strip() == '':
            continue
        if "段式" in title:
            continue

        back_up_titles_list.append(
            f"《{title}》"
        )
    backup_title = "\n".join(back_up_titles_list)
    return backup_title


def generate_article(data_dict:dict, prompt_dir_path:str, example_dir_path:str):
    print("load prompt ...")
    prompt_dict = load_prompt(prompt_dir_path)
    print("prompt load over")

    print("load example ...")
    example_dict = load_example(example_dir_path)
    print("example load over")

    extension_example_list = example_dict['extension_example_list']
    stylize_example_list = example_dict['stylize_example_list']


    # 开始构建大纲
    print("开始构建大纲")
    
    outline_generate_prompt = prompt_dict['outline_generate_prompt']
    outline_generate_prompt = outline_generate_prompt.replace(
        "{{topic}}", data_dict['topic']
    ).replace(
        "{{title}}", data_dict['title']
    ).replace(
        "{{content}}", data_dict['content']
    )

    outline_generate_func = llm_func_factory('doubao')

    article = Article(
        title=data_dict['title'],
        topic=data_dict['topic'],
        content=data_dict['content'],
        extension_example_list=extension_example_list,
        stylize_example_list=stylize_example_list
    )

    article.outline_generate(
        prompt=outline_generate_prompt,
        outline_func=outline_generate_func
    )

    print("大纲构建完成，开始解析大纲")
    article.outline_parse(
        outline_parse_func=article_split_func
    )

    print("大纲解析完成，解析结果如下：")
    print(article.parsed_outline)

    print("大纲解析完成，开始扩展段落")

    extension_prompt_base = prompt_dict['extension_prompt_base']
    extension_prompt_requirements_list = prompt_dict['extension_prompt_requirements_list']

    extension_prompt_list = []
    for i, prompt in enumerate(extension_prompt_requirements_list):
        if prompt is None:
            extension_prompt_list.append(None)
        else:
            extension_prompt = extension_prompt_base.replace(
                "{{content}}", article.parsed_outline[i].text
            ).replace(
                "{{requirement}}", prompt
            )
            if extension_example_list[i] is not None:
                extension_prompt = extension_prompt.replace(
                    "{{example}}", extension_example_list[i]
                )
            extension_prompt_list.append(extension_prompt)

    extension_func = llm_func_factory('ds-r1')
    article.extend_paragraphs(
        prompt_list=extension_prompt_list,
        reform_func=extension_func
    )

    print("段落扩展完成，开始美化段落")
    stylize_prompt_base = prompt_dict['stylize_prompt_base']
    stylize_prompt_requirements_list = prompt_dict['stylize_prompt_requirements_list']
    stylize_prompt_list = []
    for i, prompt in enumerate(stylize_prompt_requirements_list):
        if prompt is None:
            stylize_prompt_list.append(None)
        else:
            stylize_prompt = stylize_prompt_base.replace(
                "{{content}}", article.extended_paragraphs[i].text
            ).replace(
                "{{requirement}}", prompt
            )
            if stylize_example_list[i] is not None:
                stylize_prompt = stylize_prompt.replace(
                    "{{example}}", stylize_example_list[i]
                )
            stylize_prompt_list.append(stylize_prompt)

    stylize_func = llm_func_factory('ds-r1')
    article.stylize_paragraphs(
        prompt_list=stylize_prompt_list,
        stylize_func=stylize_func
    )
    print("段落美化完成")

    print("开始生成备选标题")
    article.backup_title = generate_backup_title(article)
    
    # 后处理，生成备选标题
    return article



if __name__ == "__main__":
    data_dict = {
        "title": "血压降了就停药，55岁工人身体亮红灯，真相让人意外",
        "topic": "高血压",
        "content": "李建国是一位55岁的工人，患有高血压。他认为血压降下来就不用再吃药了，平时也不注意改善生活方式。有一天，他突然感到头晕、胸闷，被紧急送往医院。检查发现他的血压波动很大，心脑血管受到了一定的损伤。文章将针对读者可能有的疑问，如血压降了是否还需要吃药、如何正确控制血压等进行科普，澄清高血压治疗的误区，并给出正确的做法。"
    }
    
    prompt_dir_path = "./prompts/structure1"
    example_dir_path = "./examples/structure1"

    article = generate_article(data_dict, prompt_dir_path, example_dir_path)

    json.dump(
        article.jsonify(),
        open("debug.json", "w"),
        ensure_ascii=False, indent=4
    )

    article_text = article.convert_to_text_with_backup_title()
    with open("debug.txt", "w", encoding="utf-8") as f:
        f.write(article_text)