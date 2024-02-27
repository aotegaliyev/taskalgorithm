import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    URL = os.getenv('APP_URL')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
