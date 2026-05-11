from models.article_models import Article, Paragaraph
import random
import json


def load_prompt(prompt_dir_path:str):
    prompt_meta_infor = json.load(open(f"{prompt_dir_path}/meta.json", "r", encoding="utf-8"))

    outline_generate_prompt = open(f"{prompt_dir_path}/{prompt_meta_infor['outline_generate_prompt']}", "r", encoding="utf-8").read()

    extension_prompt_base = open(f"{prompt_dir_path}/{prompt_meta_infor['extension_prompt']['base']}", "r", encoding="utf-8").read()
    extension_prompt_requirements_path_list = prompt_meta_infor['extension_prompt']['requirements_list']
    extension_prompt_requirements_list = []
    for path in extension_prompt_requirements_path_list:
        if path is None:
            extension_prompt_requirements_list.append(None)
        else:
            extension_prompt_requirements_list.append(open(f"{prompt_dir_path}/{path}", "r", encoding="utf-8").read())

    stylize_prompt_base = open(f"{prompt_dir_path}/{prompt_meta_infor['stylize_prompt']['base']}", "r", encoding="utf-8").read()
    stylize_prompt_requirements_path_list = prompt_meta_infor['stylize_prompt']['requirements_list']
    stylize_prompt_requirements_list = []
    for path in stylize_prompt_requirements_path_list:
        if path is None:
            stylize_prompt_requirements_list.append(None)
        else:
            stylize_prompt_requirements_list.append(open(f"{prompt_dir_path}/{path}", "r", encoding="utf-8").read())

    return {
        "outline_generate_prompt": outline_generate_prompt,
        "extension_prompt_base": extension_prompt_base,
        "extension_prompt_requirements_list": extension_prompt_requirements_list,
        "stylize_prompt_base": stylize_prompt_base,
        "stylize_prompt_requirements_list": stylize_prompt_requirements_list
    }

def article_split_func(article:str)->dict:
    """
    分割文章
    """
    article = article.strip("\n").strip("")
    paragraphs = []

    for item in article.split("\n---"):
        item = item.strip()
        item = item.strip("\n")
        item = item.strip('-')
        item = item.strip("\n")
        item = item.strip()

        if item == "":
            continue

        paragraphs.append(item.strip())

    assert len(paragraphs) == 5, "文章段落数不等于5"

    title = paragraphs[0]
    paragraphs = paragraphs[1:]

    paragarph_list = []
    for i, paragraph in enumerate(paragraphs):
        paragarph_list.append(Paragaraph(text=paragraph, prompt=None, index=i))

    return paragarph_list

def select_random_example(example_list:[str])->str:
    return random.choice(example_list)

def load_example(example_dir_path:str):
    example_meta_infor = json.load(open(f"{example_dir_path}/meta.json", "r", encoding="utf-8"))
    extension_example_list = []
    stylize_example_list = []
    for example_path in example_meta_infor['extension_example']['examples_list']:
        if example_path is None:
            extension_example_list.append(None)
        else:
            with open(f"{example_dir_path}/{example_path}", "r", encoding="utf-8") as f:
                example_list = json.load(f)
                extension_example_list.append(select_random_example(example_list))

    for i, example_path in enumerate(example_meta_infor['stylize_example']['examples_list']):
        if example_path is None:
            stylize_example_list.append(None)
        elif example_path == "keep_same":
            stylize_example_list.append(extension_example_list[i])
        else:
            with open(f"{example_dir_path}/{example_path}", "r", encoding="utf-8") as f:
                example_list = json.load(f)
                stylize_example_list.append(select_random_example(example_list))

    return {
        "extension_example_list": extension_example_list,
        "stylize_example_list": stylize_example_list
    }