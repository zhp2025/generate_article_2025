from multiprocessing import Pool
from tqdm import tqdm

def batch_execute(func, args_list, num_processes=50):
    """
    使用进程池批量执行给定的函数，并显示进度条。

    :param func: 要执行的函数
    :param args_list: 参数列表，每个元素是一个元组，包含函数的参数
    :param num_processes: 进程池中的进程数量，默认为None（使用系统默认值）
    :return: 执行结果的列表
    """
    with Pool(processes=num_processes) as pool:
        # 使用 tqdm 包装 starmap，显示进度条
        results = list(tqdm(pool.starmap(func, args_list), total=len(args_list), desc="Processing"))
    return results


if __name__ == "__main__":
    from utils.apis.api import get_instruction_response
    args_list = [
        ("介绍下你自己", 'ds-r1'),
        ("介绍下你自己", 'ds-v3'),
        ("介绍下你自己", 'gpt')
    ]

    # 批量执行函数
    results = batch_execute(get_instruction_response, args_list)

    # 打印结果
    for result in results:
        print("-" * 50)
        print(result)