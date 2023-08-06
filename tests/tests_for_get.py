import os
import pytest
from api_catalog import PetFriends
from settings import long_string, russian, chinese, special_symb
from conftest import break_auth_key, enemy_key

xfail = pytest.mark.xfail
parametrize = pytest.mark.parametrize


class TestGEtPets:

    def setup(self):
        self.pf = PetFriends()

    @pytest.mark.pos
    @pytest.mark.api
    @pytest.mark.event
    @parametrize('filter',
                 ['', 'my_pets'],
                 ids=['empty string', 'normal param'])
    def test_get_petlist_valid(self, get_api_kei, filter):

        _, status, result = self.pf.get_list_of_pets(get_api_kei, filter)
        if len(result['pets']) == 0:
            assert status == 200
            assert len(result['pets']) == 0
        else:
            assert status == 200
            assert len(result['pets']) > 0

    @pytest.mark.neg
    @pytest.mark.api
    @pytest.mark.event
    @parametrize('filter',
                 ['', 'my_pets'],
                 ids=['empty string', 'normal param'])
    # @parametrize('auth_key', [break_auth_key(), ''], ids=['incorrect key', 'empty'])
    def test_get_petlist_WrongKey(self, get_api_kei, filter):

        _, status, result = self.pf.get_list_of_pets(get_api_kei, filter)

        assert status == 403


    @pytest.mark.neg
    @pytest.mark.api
    @pytest.mark.event
    @parametrize("filter",
                 [long_string(255), long_string(1001), russian(),
                  russian().upper(), chinese(), special_symb()
                  ],
                 ids=['255 symbols',
                      '>1000 symbols', 'russian', 'russianUPS', 'chinese', 'specials'])
    @xfail(reason='status == 500')
    def test_NEG_get_petlist(self, get_api_kei, filter):
        """параметризованный негативный тест с некорректными данными"""
        _, status, result = self.pf.get_list_of_pets(get_api_kei, filter)
        assert status == 400
