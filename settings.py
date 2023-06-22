import os
from dotenv import load_dotenv

load_dotenv()

login_email = os.getenv('login_email')
login_pass = os.getenv('login_pass')


'''
 #pet_photo = r"C:\\Users\M.Kh\PycharmProjects\Study_Python_testing\Practice_19\PET_API_autotest\\tests\images\kenar-vitek.jpg"
        #photo_file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
'''

'''загрузка фото

data = {
       'name': name,
       'animal_type': animal_type,
       'age': age,
   }
headers = {'auth_key': auth_key['key']}
file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)

def test_get_by_petID(pet_ID=91827837565):
     status, result = pf.get_by_ID(pet_ID)
     assert status == 200
     assert result['id'] == pet_ID

'''