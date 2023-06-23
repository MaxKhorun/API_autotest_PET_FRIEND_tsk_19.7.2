import os
from ..api_catalog import PetFriends
from ..settings import login_email, login_pass

pf = PetFriends()
'''тест с получением ключа с сервера для работы с прочими АПИ-командами'''
def test_api_key_for_valid_user(email=login_email, passw=login_pass):
    status, result = pf.get_api_key(email, passw)
    assert status == 200
    assert 'key' in result


    '''403 - incorrect login & pass
    The error code means that provided combination of user email and password is incorrect'''
def test_api_key_for_valid_user(email='gfhfh@mail.com', passw=login_pass):
    status, result = pf.get_api_key(email, passw)
    assert status == 403

def test_get_petlist_wth_auth_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(login_email, login_pass)
    status, result = pf.get_list_of_pest(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

    '''403 incorrect auth_key'''

def test_get_petlist_wth_auth_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(login_email, login_pass)
    status, result = pf.get_list_of_pest(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

    '''[POST] / api / pets — добавление информации о новом питомце;'''
def test_post_new_pet(name='Viktor', pet_type='Canary', age='4', pet_photo='images\kenar-vitek.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(login_email, login_pass)
    status, result = pf.post_newPet(auth_key, name, pet_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
def test_new_pet_wtht_photo(name='Duran_12', pet_type='Cat', age='4'):

    _, auth_key = pf.get_api_key(login_email, login_pass)

    status, result = pf.create_simple_pet(auth_key, name, pet_type, age)


    assert status == 200
    assert result['name'] == name
def test_added_photo(pet_photo='images\kenar-vitek.jpg'):

    _, auth_key = pf.get_api_key(login_email, login_pass)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, no_photo_pet = pf.create_simple_pet(auth_key, 'Pet Friend N1', 'friend', '2')
    pet_ID = no_photo_pet['id']
    status, result = pf.upload_photo(auth_key, pet_ID, pet_photo)

    assert  status == 200
    assert len(result['pet_photo']) > 0

'''[DELETE] / api / pets / {pet_id} — удаление питомца из базы данных;'''
def test_delete_pet():
    _, auth_key = pf.get_api_key(login_email, login_pass)
    _, my_pets = pf.get_list_of_pest(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
        _, my_pets = pf.get_list_of_pest(auth_key, 'my_pets')

    pet_ID = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_ID)

    _, my_pets = pf.get_list_of_pest(auth_key, 'my_pets')

    assert status == 200
    assert pet_ID not in my_pets.values()


    '''403 - code means that provided auth_key is incorrect'''
def test_NEG_auth_key_delete_pet():
    _, auth_key = pf.get_api_key(login_email, login_pass)
    _, my_pets = pf.get_list_of_pest(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.post_newPet(auth_key, 'Some_pet_to_test', 'Canary', '3', 'images\kenar-vitek.jpg')
        _, my_pets = pf.get_list_of_pest(auth_key, 'my_pets')

    pet_ID = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_ID)

    _, my_pets = pf.get_list_of_pest(auth_key, 'my_pets')

    assert status == 200
    assert pet_ID not in my_pets.values()


'''400 provided data is incorrect:
could be: 
- incorrect login/pass
- no photo in request
- no pets in a list'''

def test_NEG_upload_photo(pet_photo='images\kenar-vitek.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(login_email, login_pass)
    _, no_photo_pet = pf.create_simple_pet(auth_key, 'Test_pet', 'friend', '2')

    auth_key = {'key': '3456dfiug7'}

    pet_ID = no_photo_pet['id']
    status, result = pf.upload_photo(auth_key, pet_ID, pet_photo)

    assert status == 403