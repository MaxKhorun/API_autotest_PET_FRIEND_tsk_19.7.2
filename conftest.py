from datetime import datetime
import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass, enemy_login_pass, enemy_login_email


def break_auth_key():
    _, _, auth_key = PetFriends().get_apikey(login_email, login_pass)
    auth_key_broken = auth_key['key'] + 'r'
    return auth_key_broken


def enemy_key():
    _, _, enemy_token = PetFriends().get_apikey(enemy_login_email, enemy_login_pass)
    return enemy_token['key']


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
def get_api_kei():
    _, status, result = PetFriends().get_apikey(email=login_email, password=login_pass)
    assert status == 200
    assert 'key' in result
    return result['key']


# @pytest.fixture(autouse=True)
# def time_for_test():
#     start_time = datetime.now()
#     _, _, my_pets = PetFriends().get_list_of_pets(get_api_kei, 'my_pets')
#     print('Длинна списка питомцев - ', len(my_pets['pets']))
#     yield
#     _,_,my_pets = PetFriends().get_list_of_pets(get_api_kei, 'my_pets')
#     if len(my_pets['pets']) == 0:
#         print('there mo pets in list')
#         assert len(my_pets['pets']) == 0
#
#     else:
#         while len(my_pets['pets']) > 0:
#             pet_ID = my_pets['pets'][0]['id']
#             PetFriends().delete_pet(get_api_kei, pet_ID)
#             _, _, my_pets = PetFriends().get_list_of_pets(get_api_kei, 'my_pets')
#             if len(my_pets['pets']) == 0:
#                 print('there no pets in list')
#                 break
#     end_time = datetime.now()
#     print(f'\nВремя выполнения теста: {end_time - start_time}')
