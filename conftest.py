from datetime import datetime

import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass


@pytest.fixture(scope='class')
def get_apikey():
    status, result = PetFriends().get_api_key(email=login_email, password=login_pass)
    assert status == 200
    assert 'key' in result
    return result['key']


@pytest.fixture(autouse=True)
def request_fixt(request):
    # print(request.fixturename)
    print('\nscope - ', request.scope)
    print('Func name - ', request.function.__name__)
    print('Class name - ', request.cls)
    # print(request.fspath)
    # print(request.module.__name__)
    if request.cls:
        return f'\nУ теста {request.function.__name__} есть класс {request.cls.__name__}'
    else:
        return f'\nУ теста {request.function.__name__} есть класс {request.cls.__name__}'


@pytest.fixture(autouse=True)
def time_for_test():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f'\nВремя выполнеия теста: {end_time - start_time}')
