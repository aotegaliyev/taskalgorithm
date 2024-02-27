import logging

import instructor
from openai import OpenAI

from settings import Config
from . import schemas

logging.basicConfig(level=logging.DEBUG)

client = instructor.patch(
    OpenAI(api_key=Config.OPENAI_API_KEY), mode=instructor.Mode.MD_JSON
)


async def divide_task_to_algo(task: str) -> schemas.TaskDetail | None:
    try:
        return client.chat.completions.create(
            model='gpt-4',
            response_model=schemas.TaskDetail,
            max_retries=3,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You can convert your task to algorithms with its order and text.'
                    ),
                },
                {
                    'role': 'user',
                    'content': (
                        f'I have a task: {task}.'
                        'Please help me to convert it to algorithms.'
                    )
                },
            ],
            max_tokens=3000,
        )
    except Exception as e:
        logging.error(e)
        return None
