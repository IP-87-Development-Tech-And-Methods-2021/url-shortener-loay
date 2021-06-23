import os

from threading import Lock
from typing import Dict, Optional

from tinydb import TinyDB, Query

class PermanentStorage():
    def __init__(self, filename_users='users.json'):
        dirname = os.path.join(os.path.dirname(__file__), 'db/')
        filepath_users = os.path.join(dirname, filename_users)
        self.filepath_users = filepath_users
        self._write_lock: Lock = Lock()
        self.users = TinyDB(filepath_users)
        self.User = Query()

    def get_user_data(self, email: str):
        try:
            user_data = self.users.search(self.User.email == email)[0]
        except:
            return None

        return user_data

    def add_user(self, email: str, password):
        with self._write_lock:
            self._write_lock: Lock = Lock()
            self.users.insert({"email": email, "password": password, "url_list": {}})

    def remove_user(self, email: str):
        with self._write_lock:
            self.users.remove(self.User.email == email)

    # Maybe clean this up
    def get_all_urls(self):
        url_dict_list = [user.get('url_list') for user in self.users.search(self.User.url_list.exists())]
        url_dict = {}
        for document in url_dict_list:
            url_dict.update(document)
        return url_dict

    def get_user_urls(self, email: str, url_short: str):
        user_data = self.users.search(self.User.email == email)
        return user_data.url_list

    def add_url(self, email: str, url_short: str, url_orig):
        with self._write_lock:
            user_data = self.users.search(self.User.email == email)[0]
            user_data['url_list'][url_short] = url_orig
            self.users.update({"url_list": user_data['url_list']}, self.User.email == email)

    def remove_url(self, email: str, url_short: str):
        with self._write_lock:
            user_data = self.users.search(self.User.email == email)[0]
            user_data['url_list'].pop("url_short", None)


class InMemoryStorage():
    """ Simple in-memory implementation of key-value storage.
    Note, how it is inherited from abstract `Storage` class
    and implements all its abstract methods. This is done this way
    in order to make some guarantees regarding class public API
    """

    def __init__(self):
        self._write_lock: Lock = Lock()
        self._data: Dict[str, str] = {}

    def read(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def write(self, key: str, value: str):
        with self._write_lock:
            self._data[key] = value
