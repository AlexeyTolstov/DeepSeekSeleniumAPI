from collections import deque
from typing import Optional


class Prompt:
    def __init__(self, id: int, query: str):
        self.id = id
        self.query = query


prompts = {}
fast_queue = deque()        # Срочная очередь
main_queue = deque()        # Основная очередь


# Можно привязать Redis

def add_fast_prompt(prompt: Prompt):
    fast_queue.append(prompt)
    prompts[prompt.id] = 202
    print(f"{prompt.id} - добавлен в очередь")


def add_main_prompt(prompt: Prompt):
    main_queue.append(prompt)
    prompts[prompt.id] = 202
    print(f"{prompt.id} - добавлен в очередь")


def get_prompt() -> Optional[Prompt]:
    if len(fast_queue):
        return fast_queue.popleft()
    
    if len(main_queue):
        return main_queue.popleft()
    
    return None

def set_prompt(id : int, answer: str):
    prompts[id] = answer