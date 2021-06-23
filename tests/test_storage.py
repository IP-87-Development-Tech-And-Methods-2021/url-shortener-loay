import os

from url_shortener.storage import PermanentStorage
from url_shortener.storage import InMemoryStorage
from url_shortener.logic import Logic

email1 = "test@tests.test"
passw1 = "test-password"
url1 = "https://google.com"
url_short1 = 'test.com'

# Temporary storage:

def test_logic_add_remove_key():
    storage = PermanentStorage()
    storage_mem = InMemoryStorage()
    logic = Logic(storage=storage, storage_mem=storage_mem)

    assert logic.read_token(email1) is None

    logic.add_token(email1)
    assert logic.read_token(email1) is not None

    logic.remove_token(email1)
    assert logic.read_token(email1) is None

def test_logic_fails_to_save_when_key_already_exists():
    storage = PermanentStorage()
    storage_mem = InMemoryStorage()
    logic = Logic(storage=storage, storage_mem=storage_mem)

    logic.add_token("test")
    assert logic.read_token("test") is not None
    assert logic.add_token("test") is False


# Permanent storage:

def test_logic_add_remove_user():
    storage = PermanentStorage(filename_users='users_test.json')
    storage_mem = InMemoryStorage()
    logic = Logic(storage=storage, storage_mem=storage_mem)

    assert logic.read_user_data(email1) is None

    logic.add_user(email1, passw1)
    assert logic.read_user_data(email1) is not None
    assert logic.read_user_data(email1)['email'] == email1
    assert logic.read_user_data(email1)['password'] == passw1
    assert logic.read_user_data(email1)['url_list'] == {}

    logic.remove_user(email1)
    assert logic.read_user_data(email1) is None

def test_logic_authenticate_user():
    storage = PermanentStorage(filename_users='users_test.json')
    storage_mem = InMemoryStorage()
    logic = Logic(storage=storage, storage_mem=storage_mem)

    logic.add_user(email1, passw1)
    assert logic.read_user_data(email1) is not None

    logic.authenticate_user
    assert logic.authenticate_user(email1, passw1) == True

    logic.remove_user(email1)
    assert logic.read_user_data(email1) is None

def test_logic_add_remove_url():
    storage = PermanentStorage(filename_users='users_test.json')
    storage_mem = InMemoryStorage()
    logic = Logic(storage=storage, storage_mem=storage_mem)

    logic.add_user(email1, passw1)
    assert logic.read_user_data(email1) is not None

    logic.add_url(email1, url_short1, url1)
    assert logic.read_user_data(email1)['url_list'][url_short1] == url1

    logic.remove_url(email1, url_short1)

    os.remove(storage.filepath_users)