from .queues import (
    main_queue, fast_queue, 
    add_fast_prompt, add_main_prompt,
    get_prompt, Prompt, prompts
)

from .worker import worker_func