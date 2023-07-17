import os
import pytest
from api_catalog import PetFriends
from settings import long_string, russian, chinese, special_symb

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
    def test_get_petlist_valid(self, auth_key, filter):

        _, status, result = self.pf.get_list_of_pest(auth_key, filter)
        if len(result['pets']) == 0:
            assert status == 200
            assert len(result['pets']) == 0
        else:
            assert status == 200
            assert len(result['pets']) > 0

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
    def test_NEG_get_petlist(self, auth_key, filter):
        """параметризованный негативный тест с некорректными данными"""
        _, status, result = self.pf.get_list_of_pest(auth_key, filter)
        assert status == 400
