import pytest
from api_catalog import PetFriends
from settings import long_string, russian, chinese, special_symb
from conftest import break_auth_key, enemy_key

xfail = pytest.mark.xfail
parametrize = pytest.mark.parametrize


@pytest.mark.apikey
class TestStartBasicApiKey:
    def setup_method(self):
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
    def test_update_pet_POS(self, get_api_kei, name, pet_type, age):
        _, _, mypets_list = self.pf.get_list_of_pest(get_api_kei, 'my_pets')

        if len(mypets_list['pets']) == 0:
            self.pf.post_newPet(get_api_kei, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, status, result = self.pf.put_info_update_pet(get_api_kei, mypets_list['pets'][0]['id'],
                                                            name, pet_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            _, status, result = self.pf.put_info_update_pet(get_api_kei, mypets_list['pets'][0]['id'],
                                                            name, pet_type, age)
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
    def test_update_pet_NEG(self, get_api_kei, name, pet_type, age):
        _, _, mypets_list = self.pf.get_list_of_pest(get_api_kei, 'my_pets')

        if len(mypets_list['pets']) == 0:
            self.pf.post_newPet(get_api_kei, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, status, result = self.pf.put_info_update_pet(get_api_kei, mypets_list['pets'][0]['id'],
                                                            name, pet_type, age)
            assert status == 400
            assert result['name'] == name
        else:
            _, status, result = self.pf.put_info_update_pet(get_api_kei, mypets_list['pets'][0]['id'],
                                                            name, pet_type, age)
            assert status == 400
            assert result['name'] == name

    @pytest.mark.neg
    @pytest.mark.api
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
    @parametrize("auth_key", [long_string(18), ''], ids=['broken key', 'empty'])
    def test_update_pet_Wrong_key(self, get_api_kei, auth_key, name, pet_type, age):
        _, _, mypets_list = self.pf.get_list_of_pest(get_api_kei, 'my_pets')

        if len(mypets_list['pets']) == 0:
            self.pf.post_newPet(get_api_kei, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                            name, pet_type, age)
            assert status == 403
        else:
            _, status, result = self.pf.put_info_update_pet(auth_key, mypets_list['pets'][0]['id'],
                                                            name, pet_type, age)
            assert status == 403
