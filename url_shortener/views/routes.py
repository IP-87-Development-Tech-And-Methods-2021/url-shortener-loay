from .handlers import (
    notfound,
    forbidden,
    create_user,
    login_user,
    logout_user,
    shorten_url,
    url_redirect
)

PROTECTED = 'url_shortener.auth.protected'


def setup_routes(config):
    """ Configures application routes"""

    # User registration
    config.add_route('create_user',
                     request_method='POST',
                     pattern='/register')
    config.add_view(create_user,
                    route_name='create_user')

    # User login
    config.add_route('login_user',
                     request_method='POST',
                     pattern='/login')
    config.add_view(login_user,
                    route_name='login_user')

    # User logout
    config.add_route('logout_user',
                     request_method='POST',
                     pattern='/logout')
    config.add_view(logout_user,
                    route_name='logout_user')

    # Shorten URL
    config.add_route('shorten_url',
                     request_method='POST',
                     pattern='/shorten_url')
    config.add_view(shorten_url,
                    route_name='shorten_url')

    # Redirect from shortened URL
    config.add_route('url_redirect',
                     request_method='GET',
                     pattern='/{url_short}')
    config.add_view(url_redirect,
                    route_name='url_redirect')

    # Add error views
    config.add_notfound_view(notfound)
    config.add_forbidden_view(forbidden)

    return config