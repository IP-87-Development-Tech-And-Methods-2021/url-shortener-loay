import random, string
import time

import trafaret as t

from threading import Lock
from typing import Optional
from os import urandom
from base64 import b64encode

from url_shortener.storage import PermanentStorage, InMemoryStorage
from url_shortener.dto import User


class Logic:
    """This class implements application logic"""

    def __init__(self, storage: PermanentStorage, storage_mem: InMemoryStorage):
        self._storage: PermanentStorage = storage
        self._storage_mem: InMemoryStorage = storage_mem
        self._check_and_write_lock: Lock = Lock()
        self.t_email = t.Email
        self.t_pwd   = t.String(min_length=6, max_length=63)

    # TODO: add logging
    #       implement trafaret checking in every method
    def read_user_data(self, email: str):
        return self._storage.get_user_data(email)

    def add_user(self, email:str, password: str):
        try:
            self.t_email.check(email)
            self.t_pwd.check(password)
        except:
            print("password or email not fulfilling requirements")
            return False

        if self._storage.get_user_data(email) is not None:
            print("email already in use")
            return False

        self._storage.add_user(email, password)
        return True

    def remove_user(self, email: str):
        self._storage.remove_user(email)

    def authenticate_user(self, email: str, password: str):
        user_data = self._storage.get_user_data(email)
        if password != user_data['password']:
            return False
        return True

    # def authenticate_token(self, email: str, password: str):

    # def read_url(email:str, url_short: str):
    #    self._storage.read_url(
    def add_url(self, email:str, url_short: str, url_orig: str):
        self._storage.add_url(email, url_short, url_orig)

    def remove_url(self, email:str, url_short: str):
        self._storage.remove_url(email, url_short)

    def get_valid_url_string(self, url_short: str):
        url_list = self._storage.get_all_urls()
        generate_string = lambda: ''.join(random.choice(string.ascii_uppercase +
                                          string.ascii_lowercase +
                                          string.digits
                                     ) for _ in range(8))
        
        timeout = time.time() + 10
        while time.time() < timeout:
            new_url = generate_string()
            for url in url_list:
                if new_url == url:
                    continue
            return new_url

        return -1

    def get_original_url(self, url_short: str):
        url_list = self._storage.get_all_urls()
        url_orig = url_list[url_short]
        return url_orig

    # Token operations
    def read_token(self, email: str):
        return self._storage_mem.read(email)

    def add_token(self, email: str):
        if self._storage_mem.read(email) is not None:
            return False
        self._storage_mem.write(email, b64encode(urandom(128)).decode('utf-8'))
        print(self._storage_mem.read(email))
        return True

    def remove_token(self, email: str): 
        if self._storage_mem.read(email) is None:
            return False
        self._storage_mem.write(email, None)
        return True

    def get_working_db(self):
        return self._storage.filepath_users


"""
    def find_user_by_token(self, token: str) -> Optional[User]:
        # TODO: implement actual checking logic
        if token.strip():
            return User(email='implementme@example.com')
        return None
"""