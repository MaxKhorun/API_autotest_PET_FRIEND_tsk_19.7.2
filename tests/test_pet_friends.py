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


    def teardown_method(self):
        print('Running positive tests')



    X

    '''5. ADD photo to pet'''





    '''6. DELETE'''



    def teardown_method(self):

        print('Running NEGATIVE tests')
