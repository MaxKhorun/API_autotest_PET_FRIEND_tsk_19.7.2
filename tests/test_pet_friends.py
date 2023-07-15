import os
import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass, enemy_login_pass, enemy_login_email

# def logger(func):
#     def wrapper(*args):
#         file_cont = (f'<{func.__name__}>  <{args}> \n')
#         with open('log.txt', 'a', encoding='utf-8') as file:
#             file.write(file_cont)
#         return func(*args)
#     return wrapper

@pytest.mark.apikey
class TestStartBasicApiKey:
    def setup_method(self):
        self.pf = PetFriends()

    @pytest.mark.skip(reason='Есть проверка в фикстуре, лежит про запас')
    def test_api_key_for_valid_user(self, email=login_email, passw=login_pass):
        '''тест с получением ключа с сервера для работы с прочими АПИ-командами'''
        status, result = self.pf.get_api_key(email, passw)
        assert status == 200
        assert 'key' in result

    @pytest.mark.api
    @pytest.mark.apikey
    def test_api_key_for_ENEMY_user(self, email=enemy_login_email, passw=enemy_login_pass):
        """Получение ключа от другого аккаунта"""
        status, result = self.pf.get_api_key(email, passw)
        assert status == 200
        assert 'key' in result

    @pytest.mark.api
    @pytest.mark.apikey
    def test_api_key_if_keys_DIFFER(self, email=login_email, passw=login_pass,
                                    enemy_login=enemy_login_email, enemy_passw=enemy_login_pass):
        """Првоерка, что ключи разные"""
        status_1, api_key_1 = self.pf.get_api_key(email, passw)
        status_2, api_key_2 = self.pf.get_api_key(enemy_login, enemy_passw)
        # assert status_1, status_2 == 200
        assert api_key_2 != api_key_1

    def teardown_method(self):
        print('Running Basic tests for get API key')


@pytest.mark.pos
class TestPositiveForPets(TestStartBasicApiKey):
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_get_petlist_wth_auth_key(self, get_api_key, filter='my_pets'):

        status, result = self.pf.get_list_of_pest(get_api_key, filter)
        if len(result['pets']) == 0:
            assert status == 200
            assert len(result['pets']) == 0
        else:
            assert status == 200
            assert len(result['pets']) > 0

    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_post_new_pet(self, get_api_key, name='5', pet_type='Canary',
                          age='4', pet_photo='images\kenar-vitek.jpg'):

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        status, result = self.pf.post_newPet(get_api_key, name, pet_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_new_pet_wtht_photo(self, get_api_key, name='Катерпилларик', pet_type='Cat', age='7'):

        status, result = self.pf.create_simple_pet(get_api_key, name, pet_type, age)

        assert status == 200
        assert result['name'] == name

    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_added_photo(self, get_api_key, pet_photo='images\kenar-vitek.jpg'):

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, no_photo_pet = self.pf.create_simple_pet(get_api_key, 'Pet Friend N1', 'friend', '2')
        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(get_api_key, pet_ID, pet_photo)

        assert status == 200
        assert len(result['pet_photo']) > 0

    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_delete_pet(self, get_api_key):
        auth_key = get_api_key
        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 200
        assert pet_ID not in my_pets.values()

    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_put_info_update_pet(self, get_api_key, name='Duran_34', pet_type='Catty', age='6'):
        _, mypets_list = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(get_api_key, mypets_list['pets'][0]['id'],
                                                         name, pet_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception('There are no pets in the list')

    @pytest.mark.api
    @pytest.mark.event
    def test_to_deleteEMall(self, get_api_key):
        _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            print('there mo pets in list')
            assert len(my_pets['pets']) == 0

        else:
            while len(my_pets['pets']) > 0:
                pet_ID = my_pets['pets'][0]['id']
                self.pf.delete_pet(get_api_key, pet_ID)
                _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')
                if len(my_pets['pets']) == 0:
                    print('there no pets in list')
                    break

            assert len(my_pets['pets']) == 0

    def teardown_method(self):
        print('Running positive tests')


@pytest.mark.neg
class TestNegativeForPets(TestStartBasicApiKey):

    @pytest.mark.api
    @pytest.mark.apikey
    def test_NEG_api_key_for_WRONG_email(self, email='', passw=login_pass):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 403

    @pytest.mark.api
    @pytest.mark.apikey
    def test_NEG_api_key_for_WRONG_pass(self, email=login_email, passw=login_pass + '2'):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 403


    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_get_petlist_wth_WRONG_auth_key(self, get_api_key, filter='my_pets'):
        """403 - wrong key"""
        auth_key = get_api_key + 'r'
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_get_petlist_wth_WRONG_data(self, get_api_key, filter='my_pets_'):
        """400 wrong filter"""
        status, result = self.pf.get_list_of_pest(get_api_key, filter)
        assert status == 500

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_get_petlist_HDRS_TO_LONG(self, get_api_key, filter='my_pets'):
        """400 Длина поля заголовка"""
        auth_key = get_api_key * 150
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 400

    '''3. New_PET'''

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_post_new_pet_wth_WRONG_key(self, get_api_key, name='Viktor', pet_type='Canary', age='4',
                                            pet_photo=r'images\kenar-vitek.jpg'):
        """403 - wrong auth_key"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = get_api_key + 'r'
        status, result = self.pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_post_new_pet_NODATA_photoOK(self, get_api_key, name='',
                                             pet_type='', age='', pet_photo='images\DSC_0810.jpg'):
        """400 - empty data except photo"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.pf.post_newPet(get_api_key, name, pet_type, age, pet_photo)
        assert status == 400

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_post_new_pet_INFINITE_name(self, get_api_key, name='vitya' * 20000,
                                            pet_type='', age='', pet_photo='images\DSC_0810.jpg'):
        """400 - infinite name"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.pf.post_newPet(get_api_key, name, pet_type, age, pet_photo)
        assert status == 400

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_post_new_pet_NODATA_DOCfile(self, get_api_key, name='', pet_type='', age='',
                                             pet_photo=r'images\codes.docx'):
        """400 - empty data, wrong file for photo"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.pf.post_newPet(get_api_key, name, pet_type, age, pet_photo)
        assert status == 400

    '''4. NEW_PET_no_PHOTO'''

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_new_pet_wtht_photo_wth_WRONG_KEY(self, get_api_key, name='Duran_12', pet_type='Cat', age='4'):
        """403 wrong auth_key"""
        auth_key = get_api_key + 'r'
        status, result = self.pf.create_simple_pet(auth_key, name, pet_type, age)

        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_new_pet_wtht_photo_NODATA_atALL(self, get_api_key, name='', pet_type='', age=''):
        """400 wrong data"""
        status, result = self.pf.create_simple_pet(get_api_key, name, pet_type, age)

        assert status == 400

    '''5. ADD photo to pet'''

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_upload_photo_WRNG_KEY(self, get_api_key, pet_photo=r'images\kenar-vitek.jpg'):
        """403 - wrong key"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, no_photo_pet = self.pf.create_simple_pet(get_api_key, 'Test_pet', 'friend', '2')

        auth_key = get_api_key + 'r'
        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_upload_photo_WRNG_DATA(self, get_api_key, pet_photo=r'images\codes.docx'):
        """400 wrong data"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, no_photo_pet = self.pf.create_simple_pet(get_api_key, 'Test_pet', 'friend', '2')

        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(get_api_key, pet_ID, pet_photo)

        assert status == 400

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_put_info_update_pet_WRNG_KEY(self, get_api_key, name='Duran_34', pet_type='Catty', age='6'):
        """7. PUT. Отправка запроса на update с неверным ключом, ожидаем в ответ 403 - wrong key"""
        _, mypets_list = self.pf.get_list_of_pest(get_api_key, 'my_pets')
        auth_key = get_api_key + 'r'

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                         name, pet_type, age)
            assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_put_info_update_pet_WRNG_DATA_(self, get_api_key, name='Duran_45', pet_type='CattyCat', age='6.3'):
        """Отправка запроса на update с неверными данными, ожидаем в ответ 400 wrong data - incorrect "id\""""
        _, mypets_list = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(get_api_key, mypets_list['pets'][0]['name'],
                                                         name, pet_type, age)
            assert status == 400

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400-ю, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_put_info_update_pet_WRNG_DATA_(self, get_api_key, name='Duran_45', pet_type='CattyCat' * 2000,
                                                age='6.3'):
        """400 infinite anymal type - to long string"""
        _, mypets_list = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(get_api_key, mypets_list['pets'][0]['id'],
                                                         name, pet_type, age)
            assert status == 400

    '''6. DELETE'''

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_auth_key_delete_pet(self, get_api_key):
        """403 - wrong key"""

        _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(get_api_key, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        auth_key = get_api_key + 'r'
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400-ю, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_auth_key_delete_pet_ENEMY_KEY(self, get_api_key):
        """Not my API_key"""
        _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(get_api_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        _, auth_key = self.pf.get_api_key(enemy_login_email,
                                          enemy_login_pass)  # здесь получаем не свой апи с данными другого аккаунта
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        assert status == 403

    def teardown_method(self):

        print('Running NEGATIVE tests')
