import os
from dotenv import load_dotenv

load_dotenv()

login_email = os.getenv('login_email')
login_pass = os.getenv('login_pass')

enemy_login_email = os.getenv('enemy_login_email')
enemy_login_pass = os.getenv('enemy_login_pass')