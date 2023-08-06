import requests
import json
import datetime
import functools
from requests_toolbelt.multipart.encoder import MultipartEncoder


def logger(func):
    def wrapper(*args, **kwargs):
        func_res, status, f_res = func(*args, **kwargs)
        func_h = func_res['api_response']
        # file_head = func_res.requests.headers
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write(f'\n--\n--\nТестовая сессия началась - {datetime.datetime.now()}')
            file.write('\n\nREQUEST DATA:\n')
            file.write(f'\nПуть запроса: \n{func_h.url}\n-----')
            file.write(f'\nMethod запроса: \n{func_h.request}\n-----')
            file.write(f'\nЗаголовки запроса: \n{func_res["headers"]}\n-----')
            file.write(f'\nДанные запроса: \n{func_res["data"]}\n')
            file.write(f'\n\nRESPONSE DATA:\n|\nv')
            file.write(f'\nСтатус ответа: {status}')
            file.write(f'\nТело ответа: {func_h.content} \n')
        return func(*args, **kwargs)

    return wrapper


class PetFriends:
    def __init__(self):
        self.base_url = r'https://petfriends.skillfactory.ru/'

    @logger
    def get_apikey(self, email: str, password: str) -> json:
        """Метод отправляет запрос к API; возвращает статус и результата в установленных переменных 
        в формате json с уникальным ключом пользователя, найденным по отправленным email и password"""

        headers = {
            'accept': 'application/json',
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        req_data = {
            'headers': headers,
            'data': (email, password),
            'api_response': res
        }
        try:
            result = res.json()
        except:
            result = res.text
        print(email, '\n', password, '\n', result)
        return req_data, status, result

    @logger
    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        """Метод отправляет завпрос к API с ключом пользователя и возварщает спсиок питомцев с учётом
        параметров filter"""
        headers = {
            'accept': 'application/json',
            'auth_key': auth_key
        }
        filter = {
            'filter': filter
        }

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        req_data = {
            'headers': headers,
            'data': filter,
            'api_response': res
        }
        try:
            result = res.json()
        except:
            result = res.text
        # print(f"\nДлина списка питомцев: \n", len(result['pets']))
        # print(result)
        return req_data, status, result

    @logger
    def post_newPet(self, auth_key: json, name: str, pet_type: str, age: str, pet_photo: str) -> json:
        ''''Добавляет питомца через отправку запроса к API;
        вводим строковые данные: имя, статус и фото_урл'''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': pet_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg') if pet_photo else ''
            })
        headers = {'accept': 'application/json',
                   'auth_key': auth_key,
                   'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        req_data = {
            'headers': headers,
            'data': data,
            'api_response': res
        }
        try:
            result = res.json()
        except:
            result = res.text
        # print(result)
        return req_data, status, result

    @logger
    def delete_pet(self, auth_key: json, pet_ID: str) -> json:
        '''Метод удаляет питомца. Принмает ID, также нужен уникальный API_key'''
        headers = {
            'accept': 'application/json',
            'auth_key': auth_key
        }
        res = requests.delete(self.base_url + f'api/pets/{pet_ID}', headers=headers)
        status = res.status_code
        result = ''
        req_data = {
            'headers': headers,
            'data': pet_ID,
            'api_response': res
        }
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return req_data, status, result

    @logger
    def create_simple_pet(self, auth_key: json, name: str, pet_type: str, age: str) -> json:
        '''Метод создаёт простого питомца без фотографии. Принмает имя, тип питомца, возроаст'''
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': pet_type,
                'age': age
            })
        header = {
            'accept': 'application/json',
            'auth_key': auth_key,
            'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=header, data=data)
        status = res.status_code
        result = ""
        req_params = {
            'headers': header,
            'data': data,
            'api_response': res
        }
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return req_params, status, result

    @logger
    def upload_photo(self, auth_key: json, pet_ID: str, pet_photo: str) -> json:
        '''Метод загружает фотографию к созданному питомцу. Передаёт ключ АПИ, ай-ди питомца и фото'''

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg') if pet_photo else ''
            })
        headers = {'accept': 'application/json',
                   'auth_key': auth_key,
                   'Content-Type': data.content_type
                   }
        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_ID}',
                            headers=headers, data=data)
        status = res.status_code
        result = ""
        req_params = {
            'headers': headers,
            'data': data,
            'api_response': res
        }
        try:
            result = res.json()
        except:
            result = res.text
        # print(result)
        return req_params, status, result

    @logger
    def put_info_update_pet(self, auth_key: json, pet_ID: str, name: str, pet_type: str, age: str) -> json:
        '''Метод обновляет данные конкретног питомца. Принимает ключ АПИ, айди питомца и новые данные:
        имя, тип питомца, возраст'''

        headers = {
            'accept': 'application/json',
            'auth_key': auth_key
        }
        data = {
            'name': name,
            'animal_type': pet_type,
            'age': age
        }

        res = requests.put(self.base_url + f'api/pets/{pet_ID}', headers=headers, data=json.dumps(data))
        status = res.status_code
        result = ''
        req_params = {
            'headers': headers,
            'data': data,
            'api_response': res
        }
        try:
            result = res.json()
        except:
            result = res.text
        return req_params, status, result


# PetFriends.create_simple_pet('a0c37e1478f4082229bb26b283990b0883a790bd46dc99282d27e6bf', 'f', 'f', '7')