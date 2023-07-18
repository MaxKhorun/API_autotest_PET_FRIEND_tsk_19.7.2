import pytest
from api_catalog import PetFriends
from settings import long_string, russian, chinese, special_symb

xfail = pytest.mark.xfail
parametrize = pytest.mark.parametrize
@pytest.mark.apikey
class TestStartBasicApiKey:
    def setup_method(self):
        self.pf = PetFriends()
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
    def test_NEG_put_info_update_pet_WRNG_KEY(self, get_api_key, name='Duran_34', pet_type='Catty', age='6'):
        """7. PUT. Отправка запроса на update с неверным ключом, ожидаем в ответ 403 - wrong key"""
        _, mypets_list = self.pf.get_list_of_pest(get_api_key, 'my_pets')
        get_api_key = get_api_key + 'r'

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