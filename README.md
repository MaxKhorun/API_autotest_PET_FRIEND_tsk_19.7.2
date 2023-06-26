# PET_API_autotest
testing API

Итоговое выполнение задания 19.7.2

Описание методов API находится в папке: \PET_API_autotest\api_catalog.py
Описание тестов находится в папке: \PET_API_autotest\tests\test_pet_friends.py
Тестовые данные в виде картинок для загрузки в базу: \PET_API_autotest\tests\images


Результат получения основного ключа.
PASSED [100%]sea-of-max@yandex.ru
 Seemann
 {'key': 'a0c37e1478f4082229bb26b283990b0883a790bd46dc99282d27e6bf'}

Результат получения вражеского ключа:
 PASSED [100%]candurin.club@yandex.ru
 not_QWERTY.98765
 {'key': '77399c1a2b640b329cd426ad6fa3aaa0300d9f106540fe97b050219a'}
Running POSITIVE tests

Каталог тестов:
Positive_BLOCK:

1. def test_api_key_for_valid_user()
  get api key

3. def test_get_petlist_wth_auth_key()
  get pet list wint api key and filter^ '' or 'my_pets'

4. def test_post_new_pet()
  add new pet with full data including photo

6. def test_new_pet_wtht_photo()
  add new pet without photo

8. def test_added_photo()
  upload photo for specific pet with pet_ID

10. def test_delete_pet()
  delete specific pet with pet_ID

12. def test_put_info_update_pet()
  updating info for specific pet, except photo

Negative_BLOCK

1. API
  def test_NEG_api_key_for_WRONG_email()
  
  def test_NEG_api_key_for_WRONG_pass()


2. PETLIST
  '''403 wrong key'''
  def test_NEG_get_petlist_wth_WRONG_auth_key()
  
  '400 0r 500 wrong filter'
  def test_NEG_get_petlist_wth_WRONG_data()
  
  '''400 Длина поля заголовка'''
  def test_NEG_get_petlist_HDRS_TO_LONG()


3. New_PET
  '''403 - wrong auth_key'''
  def test_NEG_post_new_pet_wth_WRONG_key()
      
  '''400 - empty data except photo'''
  @pytest.mark.xfail
  def test_NEG_post_new_pet_NODATA_photoOK()
  
  '''400 - infinite name'''
  @pytest.mark.xfail
  def test_NEG_post_new_pet_INFINITE_nsme()
  
  '''400 - empty data, wrong file for photo'''
  @pytest.mark.xfail
  def test_NEG_post_new_pet_NODATA_DOCfile()

4. NEW_PET_no_PHOTO
  '''403 wrong auth_key'''
  def test_NEG_new_pet_wtht_photo_wth_WRONG_KEY()
  
  '''400 wrong data'''
  @pytest.mark.xfail
  def test_NEG_new_pet_wtht_photo_NODATA_atALL()

5. ADD photo to pet

  '''403 - wrong key'''
  def test_NEG_upload_photo_WRNG_KEY()
  
  '''400 wrong data'''
  @pytest.mark.xfail
  def test_NEG_upload_photo_WRNG_DATA()

6. DELETE
  '''403 - wrong key'''
  def test_NEG_auth_key_delete_pet()

7. PUT

  '''403 - wrong key'''
  def test_NEG_put_info_update_pet_WRNG_KEY()
  
  '''400 wrong data - incorrect "id"'''
  def test_NEG_put_info_update_pet_WRNG_DATA_()
  
  '''400 infinite anymal type - to long string'''
  @pytest.mark.xfail
  def test_NEG_put_info_update_pet_WRNG_DATA_()
