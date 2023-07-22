import os

import pytest
from api_catalog import PetFriends
from settings import long_string, russian, chinese, special_symb, english
from conftest import break_auth_key, enemy_key

xfail = pytest.mark.xfail
parametrize = pytest.mark.parametrize


def photo_path(path):
    if path:
        photo = os.path.join(os.path.dirname(__file__), path)
        return photo
    else:
        return path


class TestClassForPost:

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
    def test_crt_simple_POS(self, get_api_kei, name, pet_type, age):
        _, status, result = self.pf.create_simple_pet(get_api_kei, name, pet_type, age)

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
    @xfail(reasson='status == 200')
    def test_create_simple_NEG(self, get_api_kei, name, pet_type, age):
        _, status, result = self.pf.create_simple_pet(get_api_kei, name, pet_type, age)

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
    def test_new_pet_POS(self, get_api_kei, name, pet_type, age, pet_photo):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, status, result = self.pf.post_newPet(get_api_kei, name, pet_type, age, pet_photo)
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
    @parametrize("pet_photo", [photo_path(r'images\codes.docx'), photo_path('')], ids=['.doc file', 'empty'])
    # @parametrize("auth_key", [long_string(18), ''], ids=['broken key', 'empty'])
    @xfail(reason='AssertionError')
    def test_new_pet_NEG(self, get_api_kei, name, pet_type, age, pet_photo):
        _, status, result = self.pf.post_newPet(get_api_kei, name, pet_type, age, pet_photo)
        assert status == 403

    @pytest.mark.pos
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_add_photo_POS(self, get_api_kei, pet_photo=r'images\kenar-vitek.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, _, no_photo_pet = self.pf.create_simple_pet(get_api_kei, 'Pet Friend N1', 'friend', '2')
        pet_ID = no_photo_pet['id']
        _, status, result = self.pf.upload_photo(get_api_kei, pet_ID, pet_photo)

        assert status == 200
        assert len(result['pet_photo']) > 0

    @pytest.mark.neg
    @pytest.mark.api
    @pytest.mark.event
    # @parametrize("auth_key", ['', long_string(25), enemy_key()],
    #              ids=['empty', 'incorrect key', 'enemy_key'])
    @parametrize("pet_ID", ['', long_string(15), russian(), special_symb(), english(), long_string(1000)],
                 ids=['empty', 'invalid Value', 'russian', 'specials', 'english', '1000 symbols'])
    @parametrize("pet_photo", [photo_path(r'images\codes.docx'), photo_path('')],
                 ids=['.doc file', 'empty'])
    @xfail(reason='AssertionError')
    def test_add_photo_NEG(self, get_api_kei, pet_ID, pet_photo):
        _, status, result = self.pf.upload_photo(get_api_kei, pet_ID, pet_photo)

        assert status == 400

    @pytest.mark.neg
    @pytest.mark.api
    @parametrize('auth_key', ['', enemy_key(), break_auth_key()], ids=['empty', 'enemy key', 'broken key'])
    def test_add_photo_Wrong_Key(self, auth_key, pet_photo=photo_path(r'images\kenar-vitek.jpg')):
        _, _, no_photo_pet = self.pf.create_simple_pet(auth_key, 'Pet Friend N1', 'friend', '2')
        pet_ID = no_photo_pet['id']

        _, status, result = self.pf.upload_photo(auth_key, pet_ID, pet_photo)

        assert status == 403
