from core import get_prompt, prompts
from services import DeepseekParser
from models import field_locators_RU, field_locators_EN
import atexit


def worker_func():
    deepseek = DeepseekParser(field_locators_EN)
    cnt = 0
    prompt = None
    atexit.register(deepseek.close)
    
    while True:
        try:
            if prompt is None:
                prompt = get_prompt()

            if prompt is None:
                continue

            print(f"{prompt.id} - Обрабатывается")
            cnt += 1
            prompts[prompt.id] = deepseek.send(prompt.query)
            print(f"{prompt.id} - Обработан")

            prompt = None
            if cnt >= 10:
                deepseek.create_new_chat()
                cnt = 0
        except:
            try:
                deepseek = DeepseekParser(field_locators_RU)
                print('DeepSeek успешно перезапущен')
            except:
                print('Не удалось перезапустить')
                continue