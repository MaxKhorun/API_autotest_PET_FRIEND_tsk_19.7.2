import os
import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass, enemy_login_pass, enemy_login_email

class Test_pet_POSITIVE:

    def setup(self):
        self.pf = PetFriends()
    '''тест с получением ключа с сервера для работы с прочими АПИ-командами'''

    def test_api_key_for_valid_user(self, email=login_email, passw=login_pass):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 200
        assert 'key' in result

    '''Получение ключа от другого аккаунта'''
    def test_api_key_for_ENEMY_user(self, email=enemy_login_email, passw=enemy_login_pass):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 200
        assert 'key' in result
    '''Првоерка, что ключи разные'''
    def test_api_key_if_keys_DIFFER(self, email=login_email, passw=login_pass,
                                    enemy_login=enemy_login_email, enemy_passw=enemy_login_pass):
        status_1, api_key_1 = self.pf.get_api_key(email, passw)
        status_2, api_key_2 = self.pf.get_api_key(enemy_login, enemy_passw)
        # assert status_1, status_2 == 200
        assert api_key_2 != api_key_1

    def test_get_petlist_wth_auth_key(self, filter='my_pets'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0
    def test_post_new_pet(self, name='Viktor', pet_type='Canary', age='4', pet_photo='images\kenar-vitek.jpg'):

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
    def test_new_pet_wtht_photo(self, name='Duran_12', pet_type='Cat', age='4'):

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.create_simple_pet(auth_key, name, pet_type, age)

        assert status == 200
        assert result['name'] == name
    def test_added_photo(self, pet_photo='images\kenar-vitek.jpg'):

        _, auth_key = self.pf.get_api_key(login_email, login_pass)

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, no_photo_pet = self.pf.create_simple_pet(auth_key, 'Pet Friend N1', 'friend', '2')
        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert  status == 200
        assert len(result['pet_photo']) > 0
    def test_delete_pet(self):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 200
        assert pet_ID not in my_pets.values()
    def test_put_info_update_pet(self, name='Duran_34', pet_type='Catty', age='6'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                    name, pet_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception('There are no pets in the list')
    def teardown(self):
        print('Running POSITIVE tests')
class Test_pet_NEGATIVE(Test_pet_POSITIVE):

    '''1. API'''
    def test_NEG_api_key_for_WRONG_email(self, email='gfhfh@mail.com', passw=login_pass):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 403
    def test_NEG_api_key_for_WRONG_pass(self, email=login_email, passw=login_pass + '2'):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 403
    def test_every_key_the_same(self, email):
        pass
        '''PET_list'''



    '''2. PETLIST'''
    '''403 - wrong key'''
    def test_NEG_get_petlist_wth_WRONG_auth_key(self, filter='my_pets'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        auth_key['key'] = auth_key['key'] + 'r'
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 403

    '400 wrong filter'
    def test_NEG_get_petlist_wth_WRONG_data(self, filter='my_pets_'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 500

    '''400 Длина поля заголовка'''
    def test_NEG_get_petlist_HDRS_TO_LONG(self, filter='my_pets'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        auth_key['key'] = auth_key['key'] * 150
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 400

    '''3. New_PET'''
    '''403 - wrong auth_key'''
    def test_NEG_post_new_pet_wth_WRONG_key(self, name='Viktor', pet_type='Canary', age='4',
                                            pet_photo='images\kenar-vitek.jpg'):

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        auth_key['key'] = auth_key['key'] + 'r'
        status, result = self.pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
        assert status == 403

    '''400 - empty data except photo'''
    @pytest.mark.xfail
    def test_NEG_post_new_pet_NODATA_photoOK(self, name='',
                                             pet_type='', age='', pet_photo='images\DSC_0810.jpg'):

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
        assert status == 400

    '''400 - infinite name'''
    @pytest.mark.xfail
    def test_NEG_post_new_pet_INFINITE_name(self, name='vitya' * 20000,
                                            pet_type='', age='', pet_photo='images\DSC_0810.jpg'):

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
        assert status == 400

    '''400 - empty data, wrong file for photo'''
    @pytest.mark.xfail
    def test_NEG_post_new_pet_NODATA_DOCfile(self, name='', pet_type='', age='', pet_photo='images\codes.docx'):

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
        assert status == 400

    '''4. NEW_PET_no_PHOTO'''
    '''403 wrong auth_key'''
    def test_NEG_new_pet_wtht_photo_wth_WRONG_KEY(self, name='Duran_12', pet_type='Cat', age='4'):

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        auth_key['key'] = auth_key['key'] + 'r'

        status, result = self.pf.create_simple_pet(auth_key, name, pet_type, age)

        assert status == 403

    '''400 wrong data'''
    @pytest.mark.xfail
    def test_NEG_new_pet_wtht_photo_NODATA_atALL(self, name='', pet_type='', age=''):

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        status, result = self.pf.create_simple_pet(auth_key, name, pet_type, age)

        assert status == 400

    '''5. ADD photo to pet'''
    '''403 - wrong key'''
    def test_NEG_upload_photo_WRNG_KEY(self,pet_photo='images\kenar-vitek.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, no_photo_pet = self.pf.create_simple_pet(auth_key, 'Test_pet', 'friend', '2')

        auth_key['key'] = auth_key['key'] + 'r'
        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert status == 403

    '''400 wrong data'''
    @pytest.mark.xfail
    def test_NEG_upload_photo_WRNG_DATA(self, pet_photo='images\codes.docx'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, no_photo_pet = self.pf.create_simple_pet(auth_key, 'Test_pet', 'friend', '2')

        pet_ID = no_photo_pet['id']
        status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert status == 400

    '''6. DELETE'''
    '''403 - wrong key'''
    def test_NEG_auth_key_delete_pet(self):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        auth_key['key'] = auth_key['key'] + 'r'
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 403

    '''Not my API_key'''
    @pytest.mark.xfail
    def test_NEG_auth_key_delete_pet_ENEMY_KEY(self):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        _, auth_key = self.pf.get_api_key(enemy_login_email, enemy_login_pass) #здесь получаем не свой апи с данными другого аккаунта
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 403

    '''7. PUT'''
    '''403 - wrong key'''
    def test_NEG_put_info_update_pet_WRNG_KEY(self, name='Duran_34', pet_type='Catty', age='6'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')
        auth_key['key'] = auth_key['key'] + 'r'

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                    name, pet_type, age)
            assert status == 403

    '''400 wrong data - incorrect "id"'''
    def test_NEG_put_info_update_pet_WRNG_DATA_(self, name='Duran_45', pet_type='CattyCat', age='6.3'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['name'],
                                                    name, pet_type, age)
            assert status == 400

    '''400 infinite anymal type - to long string'''
    @pytest.mark.xfail
    def test_NEG_put_info_update_pet_WRNG_DATA_(self, name='Duran_45', pet_type='CattyCat' * 2000, age='6.3'):
        _, auth_key = self.pf.get_api_key(login_email, login_pass)
        _, mypets_list = self.pf.get_list_of_pest(auth_key, 'my_pets')

        if len(mypets_list['pets']) > 0:
            status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                    name, pet_type, age)
            assert status == 400
    def teardown(self):
        print('Running NEGATIVE tests')