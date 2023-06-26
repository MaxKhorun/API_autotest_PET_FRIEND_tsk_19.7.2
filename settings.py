import os
from dotenv import load_dotenv

load_dotenv()

login_email = os.getenv('login_email')
login_pass = os.getenv('login_pass')