import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
ADMINS = [os.getenv('FIRST_ADMIN_CHAT_ID')]
