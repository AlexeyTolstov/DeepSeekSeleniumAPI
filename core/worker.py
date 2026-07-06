from core import get_prompt, prompts
from services import DeepseekParser
from models import field_locators_RU, field_locators_EN
import atexit


def worker_func():
    deepseek = DeepseekParser(field_locators_RU)
    prompt = None
    atexit.register(deepseek.close)
    
    while True:
        try:
            if prompt is None:
                prompt = get_prompt()

            if prompt is None:
                continue

            print(f"{prompt.id} - Обрабатывается")
            
            deepseek.create_new_chat()
            prompts[prompt.id] = deepseek.send(prompt.query)
            print(f"{prompt.id} - Обработан")

            prompt = None
        except:
            try:
                deepseek = DeepseekParser(field_locators_RU)
                print('DeepSeek успешно перезапущен')
            except:
                print('Не удалось перезапустить')
                continue