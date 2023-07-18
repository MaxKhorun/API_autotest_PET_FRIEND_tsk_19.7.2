import os

import pytest
from api_catalog import PetFriends
from settings import long_string, russian, chinese, special_symb, login_pass, \
    english, login_email, enemy_login_pass, enemy_login_email

xfail = pytest.mark.xfail
parametrize = pytest.mark.parametrize


def break_auth_key():
    auth_key = PetFriends().get_api_key(login_email, login_pass)
    auth_key_broken = auth_key['key'] + 'r'
    return auth_key_broken


def enemy_key():
    enemy_token = PetFriends().get_api_key(enemy_login_email, enemy_login_pass)
    return enemy_token['key']


class TestPostPets():

    def setup(self):
        self.pf = PetFriends()

    @pytest.mark.pos
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    @parametrize("name",
                 [long_string(255), long_string(1001), russian(),
                  russian().upper(), chinese(), special_symb(), '123'],
                 ids=['255 symbols', '>1000 symbols', 'russian', 'russianUPS', 'chinese', 'specials',
                      'digits'])
    @parametrize("pet_type",
                 [long_string(255), long_string(1001), russian(), russian().upper(), chinese(),
                  special_symb(), '123'],
                 ids=['255 symbols', '>1000 symbols', 'russian', 'russianUPS', 'chinese', 'specials',
                      'digits'])
    @parametrize("age",
                 ['1'],
                 ids=['just one'])
    def test_new_pet_NO_photo(self, get_api_key, name, pet_type, age):
        _, status, result = self.pf.create_simple_pet(get_api_key, name, pet_type, age)

        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == pet_type
        assert result['age'] == age

    @pytest.mark.neg
    @parametrize("name", [''], ids=['empty'])
    @parametrize("pet_type", [''], ids=['empty'])
    @parametrize("age",
                 ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_symb(), russian(),
                  russian().upper(), chinese()],
                 ids=['empty', 'neg', 'zero', 'a hundred', 'float', 'in_max', 'int_max + 1', 'specials',
                      'russians', 'RUSSIANS', 'chinese'])
    def test_new_pet_NO_photo(self, get_api_key, name, pet_type, age):
        _, status, result = self.pf.create_simple_pet(get_api_key, name, pet_type, age)

        assert status == 400

    @pytest.mark.pos
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    @parametrize("name",
                 [long_string(255), long_string(1001), russian(),
                  russian().upper(), chinese(), special_symb(), '123'],
                 ids=['255 symbols', '>1000 symbols', 'russian', 'russianUPS', 'chinese', 'specials',
                      'digits'])
    @parametrize("pet_type",
                 [long_string(255), long_string(1001), russian(), russian().upper(), chinese(),
                  special_symb(), '123'],
                 ids=['255 symbols', '>1000 symbols', 'russian', 'russianUPS', 'chinese', 'specials',
                      'digits'])
    @parametrize("age", ['1'], ids=['just one'])
    @parametrize("pet_photo", [r"images\kenar-vitek.jpg"], ids=['image'])
    def test_post_new_pet(self, get_api_key, name, pet_type, age, pet_photo):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, status, result = self.pf.post_newPet(get_api_key, name, pet_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    @pytest.mark.neg
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    @parametrize("name", [''], ids=['empty'])
    @parametrize("pet_type", [''], ids=['empty'])
    @parametrize("age",
                 ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_symb(), russian(),
                  russian().upper(), chinese()],
                 ids=['empty', 'neg', 'zero', 'a hundred', 'float', 'in_max', 'int_max + 1', 'specials',
                      'russians', 'RUSSIANS', 'chinese'])
    @parametrize("pet_photo", [r"images\codes.docx", ""], ids=['.doc file', 'empty'])
    @parametrize("get_api_key", [break_auth_key()], ids='broken key')
    def test_post_new_pet(self, get_api_key, name, pet_type, age, pet_photo):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, status, result = self.pf.post_newPet(get_api_key, name, pet_type, age, pet_photo)
        assert status == 400

    @pytest.mark.pos
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_added_photo(self, get_api_key, pet_photo=r'images\kenar-vitek.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, _, no_photo_pet = self.pf.create_simple_pet(get_api_key, 'Pet Friend N1', 'friend', '2')
        pet_ID = no_photo_pet['id']
        _, status, result = self.pf.upload_photo(get_api_key, pet_ID, pet_photo)

        assert status == 200
        assert len(result['pet_photo']) > 0

    @pytest.mark.neg
    @pytest.mark.api
    @pytest.mark.event
    @parametrize("auth_key", ['', break_auth_key(), enemy_key()],
                 ids=['empty', 'incorrect key', 'enemy key'])
    @parametrize("pet_ID", ['', long_string(15), russian(), special_symb(), english(), long_string(1000)],
                 ids=['empty', 'invalid Value', 'russian', 'specials', 'english', '1000 symbols'])
    @parametrize("pet_photo", ['', r'images\codes.docx'],
                 ids=['empty', '.doc file'])
    def test_added_photo(self, auth_key, pet_ID, pet_photo):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert status == 400


    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_get_petlist_wth_WRONG_auth_key(self, get_api_key, filter='my_pets'):
        """403 - wrong key"""
        get_api_key = get_api_key + 'r'
        status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_upload_photo_WRNG_KEY(self, get_api_key, pet_photo=r'images\kenar-vitek.jpg'):
        """403 - wrong key"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, no_photo_pet = self.pf.create_simple_pet(get_api_key, 'Test_pet', 'friend', '2')

        get_api_key = get_api_key + 'r'
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