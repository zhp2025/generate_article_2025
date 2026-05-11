from .api_utils.api_deepseek import get_deepseek_response
from .api_utils.api_gpt import get_gpt_response
from .api_utils.api_doubao import get_doubao_response
from .api_utils.api_doubao_1_6 import get_doubao_response_1_6


def get_instruction_response(prompt, model='ds-r1', max_retries=5, return_cot=False)->str:
    supported_models = ['ds-r1', 'ds-v3', 'gpt', 'doubao', "doubao-1.6"]
    if return_cot:
        assert model == 'ds-r1', "When return_cot is True, model must be 'ds-r1'."

    if model not in supported_models:
        raise ValueError(f"Unsupported model: {model}. Supported models are: {supported_models}")

    if model == 'ds-r1':
        return get_deepseek_response(prompt, max_retries=max_retries, return_cot=return_cot, model_name='deepseek-reasoner')

    elif model == 'ds-v3':
        return get_deepseek_response(prompt, max_retries=max_retries, model_name='deepseek-chat')

    elif model == 'gpt':
        return get_gpt_response(prompt)

    elif model == 'doubao':
        return get_doubao_response(prompt, max_retries=max_retries)

    elif model == 'doubao-1.6':
        return get_doubao_response_1_6(prompt, max_retries=max_retries)

    
        

if __name__ == "__main__":
    print(get_instruction_response("介绍你自己", model='ds-r1'))
    print("" + "="*50)
    print(get_instruction_response("介绍你自己", model='ds-v3'))
    print("" + "="*50)
    print(get_instruction_response("介绍你自己", model='gpt'))
    print("" + "="*50)
    print(get_instruction_response("介绍你自己", model='doubao'))
