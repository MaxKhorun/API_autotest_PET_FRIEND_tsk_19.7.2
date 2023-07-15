from datetime import datetime
import requests
import functools
import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass


@pytest.fixture(autouse=True)
def request_fixt(request):
    # print(request.fixturename)
    print('\nscope - ', request.scope)
    print('Func name - ', request.function.__name__)
    print('Class name - ', request.cls)
    print(request.fspath)
    # print(request.module.__name__)
    if request.cls:
        return f'\nУ теста {request.function.__name__} есть класс {request.cls.__name__}'
    else:
        return f'\nУ теста {request.function.__name__} есть класс {request.cls.__name__}'


@pytest.fixture(scope="function")
def get_api_key(request_fixt):
    status, result = PetFriends().get_api_key(email=login_email, password=login_pass)
    assert status == 200
    assert 'key' in result
    return result['key']


@pytest.fixture(autouse=True)
def time_for_test():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f'\nВремя выполнения теста: {end_time - start_time}')

# @pytest.fixture()
# def logger_func(func, request_fixt):
#     def wrap_logger(*args, **kwargs):
#         with open('log_tests.txt', 'wr', encoding='utf-8') as lf:
#             logfile = lf.write(request_fixt.function.__name__)
#             logfile = lf.write(request_fixt.fspath)
#             logfile = lf.close()
#     return wrap_logger


# @pytest.fixture(autouse=True)
# def decor_logger(func):
#     @functools.wraps(func)
#     def wrap_logger(*args, **kwargs):
#         resp = func(*args, **kwargs)
#         resp_head = resp.requests.headers
#         resp_data = resp.requests.content
#         with open('logfile.txt', 'wr', encoding='utf-8') as lf:
#             lf.write("Start logging")
#             lf.write(func.__name__)
#             lf.write(f'Headers: {resp_head}\n')
#             lf.write(f'Data in request: {resp_data}\n')
#             lf.close()
#
#         return resp
#
#     return wrap_logger