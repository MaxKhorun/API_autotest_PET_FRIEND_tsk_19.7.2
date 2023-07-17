import pytest
from api_catalog import PetFriends
from settings import login_email, login_pass, enemy_login_pass, enemy_login_email


@pytest.mark.apikey
class TestStartBasicApiKey:
    def setup_method(self):
        self.pf = PetFriends()

    @pytest.mark.skip(reason='Есть проверка в фикстуре, лежит про запас')
    def test_api_key_for_valid_user(self, email=login_email, passw=login_pass):
        '''тест с получением ключа с сервера для работы с прочими АПИ-командами'''
        _, status, result = self.pf.get_api_key(email, passw)
        assert status == 200
        assert 'key' in result

    @pytest.mark.api
    @pytest.mark.apikey
    def test_api_key_for_ENEMY_user(self, email=enemy_login_email, passw=enemy_login_pass):
        """Получение ключа от другого аккаунта"""
        _, status, result = self.pf.get_api_key(email, passw)
        assert status == 200
        assert 'key' in result

    @pytest.mark.api
    @pytest.mark.apikey
    def test_api_key_if_keys_DIFFER(self, email=login_email, passw=login_pass,
                                    enemy_login=enemy_login_email, enemy_passw=enemy_login_pass):
        """Првоерка, что ключи разные"""
        _, status_1, api_key_1 = self.pf.get_api_key(email, passw)
        _, status_2, api_key_2 = self.pf.get_api_key(enemy_login, enemy_passw)
        # assert status_1, status_2 == 200
        assert api_key_2 != api_key_1

    def teardown_method(self):
        print('Running Basic tests for get API key')


    @pytest.mark.api
    @pytest.mark.apikey
    def test_NEG_api_key_for_WRONG_email(self, email='', passw=login_pass):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 403

    @pytest.mark.api
    @pytest.mark.apikey
    def test_NEG_api_key_for_WRONG_pass(self, email=login_email, passw=login_pass + '2'):
        status, result = self.pf.get_api_key(email, passw)
        assert status == 403