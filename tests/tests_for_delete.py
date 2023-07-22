import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass, enemy_login_pass, enemy_login_email, long_string,\
    russian, chinese, special_symb
from conftest import break_auth_key, enemy_key
parametrize = pytest.mark.parametrize

class TestDelete:

    def setup(self):
        self.pf = PetFriends()

    @pytest.mark.pos
    @pytest.mark.api
    @pytest.mark.ui
    @pytest.mark.event
    def test_delete_pet(self, get_api_kei):

        _, _, my_pets = self.pf.get_list_of_pets(get_api_kei, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(get_api_kei, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, _, my_pets = self.pf.get_list_of_pets(get_api_kei, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        _, status, _ = self.pf.delete_pet(get_api_kei, pet_ID)

        _, _, my_pets = self.pf.get_list_of_pets(get_api_kei, 'my_pets')

        assert status == 200
        assert pet_ID not in my_pets.values()

    @pytest.mark.neg
    @pytest.mark.api
    @parametrize("auth_key", ['', break_auth_key(), enemy_key()],
                 ids=['empty', 'break key', 'enemy key'])
    def test_delete_pet_Wrong_key(self, get_api_kei, auth_key):
        """403 - wrong key"""

        _, _, my_pets = self.pf.get_list_of_pets(get_api_kei, 'my_pets')

        if len(my_pets['pets']) == 0:
            self.pf.post_newPet(get_api_kei, 'Some_pet_to_test', 'Canary', '3', r'images\kenar-vitek.jpg')
            _, _, my_pets = self.pf.get_list_of_pets(get_api_kei, 'my_pets')

        pet_ID = my_pets['pets'][0]['id']
        _, status, _ = self.pf.delete_pet(auth_key, pet_ID)

        assert status == 403

    @pytest.mark.api
    @pytest.mark.event
    def test_to_deleteEMall(self, get_api_kei):
        _, _, my_pets = self.pf.get_list_of_pets(get_api_kei, 'my_pets')

        if len(my_pets['pets']) == 0:
            print('there mo pets in list')
            assert len(my_pets['pets']) == 0

        else:
            while len(my_pets['pets']) > 0:
                pet_ID = my_pets['pets'][0]['id']
                self.pf.delete_pet(get_api_kei, pet_ID)
                _, _, my_pets = self.pf.get_list_of_pets(get_api_kei, 'my_pets')
                if len(my_pets['pets']) == 0:
                    print('there no pets in list')
                    break

            assert len(my_pets['pets']) == 0