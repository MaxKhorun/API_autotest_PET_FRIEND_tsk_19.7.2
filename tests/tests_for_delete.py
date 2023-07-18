import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass, enemy_login_pass, enemy_login_email

class TestDelete():

    def setup(self):
        self.pf = PetFriends()
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_delete_pet(self, get_api_key):

        _, _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(get_api_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
            _, _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(get_api_key, pet_ID)

        _, _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        assert status == 200
        assert pet_ID not in my_pets.values()

    @pytest.mark.api
    @pytest.mark.event
    def test_to_deleteEMall(self, get_api_key):
        _, _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            print('there mo pets in list')
            assert len(my_pets['pets']) == 0

        else:
            while len(my_pets['pets']) > 0:
                pet_ID = my_pets['pets'][0]['id']
                self.pf.delete_pet(get_api_key, pet_ID)
                _, _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')
                if len(my_pets['pets']) == 0:
                    print('there no pets in list')
                    break

            assert len(my_pets['pets']) == 0

    @pytest.mark.api
    @pytest.mark.event
    def test_NEG_auth_key_delete_pet(self, get_api_key):
        """403 - wrong key"""

        _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(get_api_key, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, my_pets = self.pf.get_list_of_pest(get_api_key, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        get_api_key = get_api_key + 'r'
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

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
        _, get_api_key = self.pf.get_api_key(enemy_login_email,
                                             enemy_login_pass)  # здесь получаем не свой апи с данными другого аккаунта
        status, _ = self.pf.delete_pet(auth_key, pet_ID)

        _, my_pets = self.pf.get_list_of_pest(auth_key, 'my_pets')

        assert status == 403