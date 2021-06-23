import os

from url_shortener.storage import PermanentStorage


def test_post_create_user(testapp, app, glob):
    os.remove(app.registry.logic.get_working_db()) # clean up

    res = testapp.post_json('/register', dict(
        email=glob['email1'],
        password=glob['passw1']))
    assert res.json_body['status'] == 'account created'
    assert app.registry.logic.read_user_data(glob['email1']) == dict(
            email=glob['email1'],
            password=glob['passw1'],
            url_list={})

def test_post_login_user(testapp, app, glob):
    res = testapp.post_json('/login', dict(
        email=glob['email1'],
        password=glob['passw1']))

    token = res.json_body['token']
    assert app.registry.logic.read_token(glob['email1']) == token


# logout user


def test_post_shorten_url(testapp, app, glob):
    token = app.registry.logic.read_token(glob['email1'])

    res = testapp.post_json('/shorten_url', dict(
        email=glob['email1'],
        token=token,
        url=glob['url1']))

    url_short = res.json_body['url']

    assert app.registry.logic.read_user_data(glob['email1'])['url_list'] \
            == {url_short: glob['url1']}

def test_post_logout(testapp, app, glob):
    token = app.registry.logic.read_token(glob['email1'])

    res = testapp.post_json('/logout', dict(
        email=glob['email1'],
        token=token))

    assert app.registry.logic.read_token(glob['email1']) is None


def test_get_redirect(testapp, app, glob):
    url_short = 'test'
    app.registry.logic.add_url(glob['email1'], url_short, glob['url1'])

    res = testapp.get('/' + url_short, status=302)
    assert 'https://google.com' in res.location



def test_get_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404