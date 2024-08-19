
from dotenv import load_dotenv
import os

def load_config():
    load_dotenv("../config/config.env")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key
