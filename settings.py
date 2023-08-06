import os
from dotenv import load_dotenv
load_dotenv()

login_email = os.getenv('login_email')
login_pass = os.getenv('login_pass')

enemy_login_email = os.getenv('enemy_login_email')
enemy_login_pass = os.getenv('enemy_login_pass')

def russian():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def english():
    return 'qwertyuioplkjhgfdsazxcvbnm'


def chinese():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_symb():
    return r'~!@#$%^&*()_+{}|:”>?<Ё!”№;%:?*()_+/Ъ,/.,;’[]\|'


def long_string(n):
    return "x" * n


def check_age(age):
    return age.isdigit() and 0 < int(age) < 50 \
        and float(age) == int(age)
