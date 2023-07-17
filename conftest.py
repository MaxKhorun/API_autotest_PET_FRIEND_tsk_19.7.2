from datetime import datetime
import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass


@pytest.fixture(autouse=True)
def request_fixt(request):
    # print(f'\nИмя работающей фикстуры: {request.fixturename}')
    print('\nscope - ', request.scope)
    print('\nFunc name - ', request.function.__name__)
    print('\nClass name - ', request.cls.__name__)
    print(f'\nПуть к тесту: {request.fspath}')
    # print(request.module.__name__)
    if isinstance(request.function, request.cls):
        return f'\nУ теста {request.function.__name__} есть класс {request.cls.__name__}'
    else:
        return f'\nУ теста {request.function.__name__} нет класса'


@pytest.fixture(scope="class")
def auth_key():
    _, status, pytest.key = PetFriends().get_api_key(email=login_email, password=login_pass)
    assert status == 200
    assert 'key' in pytest.key
    return pytest.key['key']


@pytest.fixture(autouse=True)
def time_for_test():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f'\nВремя выполнения теста: {end_time - start_time}')