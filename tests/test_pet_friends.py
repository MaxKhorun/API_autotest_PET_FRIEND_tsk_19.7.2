import os
import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass, enemy_login_pass, enemy_login_email, \
    long_string, russian, chinese, special_symb, check_age

xfail = pytest.mark.xfail
parametrize = pytest.mark.parametrize


# @pytest.mark.pos
class TestPositiveForPets():

    def setup(self):
        self.pf = PetFriends()




    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_delete_pet(self, auth_key):


        _, _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 200
        assert pet_ID not in my_pets.values()

    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_put_info_update_pet(self, auth_key, name='Duran_34', pet_type='Catty', age='6'):
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                         name, pet_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception('There are no pets in the list')

    @pytest.mark.api
    @pytest.mark.event
    def test_to_deleteEMall(self, auth_key):
        _, _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            print('there mo pets in list')
            assert len(my_pets['pets']) == 0

        else:
            while len(my_pets['pets']) > 0:
                pet_ID = my_pets['pets'][0]['id']
                self.pf.delete_pet(auth_key, pet_ID)
                _, _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')
                if len(my_pets['pets']) == 0:
                    print('there no pets in list')
                    break

            assert len(my_pets['pets']) == 0

    def teardown_method(self):
        print('Running positive tests')




    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_get_petlist_wth_WRONG_auth_key(self, auth_key, filter='my_pets'):
        """403 - wrong key"""
        auth_key = auth_key + 'r'
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_post_new_pet_wth_WRONG_key(self, auth_key, name='Viktor', pet_type='Canary', age='4',
                                            pet_photo=r'images\kenar-vitek.jpg'):
        """403 - wrong auth_key"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = auth_key + 'r'
        status, result = self.pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
        assert status == 403


    '''4. NEW_PET_no_PHOTO'''

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_new_pet_wtht_photo_wth_WRONG_KEY(self, auth_key, name='Duran_12', pet_type='Cat', age='4'):
        """403 wrong auth_key"""
        auth_key = auth_key + 'r'
        status, result = self.pf.create_simple_pet(auth_key, name, pet_type, age)

        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_new_pet_wtht_photo_NODATA_atALL(self, auth_key, name='', pet_type='', age=''):
        """400 wrong data"""
        status, result = self.pf.create_simple_pet(auth_key, name, pet_type, age)

        assert status == 400

    '''5. ADD photo to pet'''

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_upload_photo_WRNG_KEY(self, auth_key, pet_photo=r'images\kenar-vitek.jpg'):
        """403 - wrong key"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, no_photo_pet = self.pf.create_simple_pet(auth_key, 'Test_pet', 'friend', '2')

        auth_key = auth_key + 'r'
        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_upload_photo_WRNG_DATA(self, auth_key, pet_photo=r'images\codes.docx'):
        """400 wrong data"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, no_photo_pet = self.pf.create_simple_pet(auth_key, 'Test_pet', 'friend', '2')

        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert status == 400

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_put_info_update_pet_WRNG_KEY(self, auth_key, name='Duran_34', pet_type='Catty', age='6'):
        """7. PUT. Отправка запроса на update с неверным ключом, ожидаем в ответ 403 - wrong key"""
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')
        auth_key = auth_key + 'r'

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                         name, pet_type, age)
            assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_put_info_update_pet_WRNG_DATA_(self, auth_key, name='Duran_45', pet_type='CattyCat', age='6.3'):
        """Отправка запроса на update с неверными данными, ожидаем в ответ 400 wrong data - incorrect "id\""""
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['name'],
                                                         name, pet_type, age)
            assert status == 400

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400-ю, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_put_info_update_pet_WRNG_DATA_(self, auth_key, name='Duran_45', pet_type='CattyCat' * 2000,
                                                age='6.3'):
        """400 infinite anymal type - to long string"""
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                         name, pet_type, age)
            assert status == 400

    '''6. DELETE'''

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_auth_key_delete_pet(self, auth_key):
        """403 - wrong key"""

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        auth_key = auth_key + 'r'
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    @pytest.mark.xfail(reason='ожидаем 400-ю, так как не отправляем данные на сервер, но приходит 200')
    def test_NEG_auth_key_delete_pet_ENEMY_KEY(self, auth_key):
        """Not my API_key"""
        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        _, auth_key = self.pf.get_api_key(enemy_login_email,
                                          enemy_login_pass)  # здесь получаем не свой апи с данными другого аккаунта
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 403

    def teardown_method(self):

        print('Running NEGATIVE tests')
