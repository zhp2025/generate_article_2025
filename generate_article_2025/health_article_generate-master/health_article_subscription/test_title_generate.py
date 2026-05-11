import json
from tqdm import tqdm
import os


from utils.apis.api import get_instruction_response
from models.article_models import Article, Paragaraph
from article_utils import load_prompt, article_split_func, load_example


def generate_backup_title(article:str):
    prompt_tempalte = open("prompts/backup_title_generate.txt", "r", encoding="utf-8").read()
    prompt = prompt_tempalte.replace("{{article}}", article)
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

    print(back_up_titles_list)

if __name__ == "__main__":
    base_dir = "/root/cyh/health_article_generate/health_article_subscription/output/2025-07-13/part_1/markdown_result"

    for name in os.listdir(base_dir):
        article = open(f"{base_dir}/{name}").read()

        print(generate_backup_title(article))
