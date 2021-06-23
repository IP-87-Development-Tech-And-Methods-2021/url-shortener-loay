  
import os
from pyramid.paster import get_appsettings
from pyramid.scripting import prepare
from pyramid.testing import DummyRequest, testConfig
import pytest
import webtest

from url_shortener.main import make_app
from url_shortener.config import Config



@pytest.fixture(scope='session')
def app():
    config = Config(base_url='http://127.0.0.1:6543',
                    port=6543,
                    user_db='test_users.json')
    return make_app(config)


@pytest.fixture
def testapp(app):
    testapp = webtest.TestApp(app)
    return testapp

    
@pytest.fixture
def glob():
    email1 = "test@tests.test"
    passw1 = "test-password"
    url1 = "https://google.com"
    url_short: str
    token1: str

    return locals()