"""This module contains various examples on how to implement an endpoint"""
import http.client as httplib
from url_shortener.logic import Logic

from pyramid.request import Request
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound


def create_user(request: Request) -> Response:
    logic: Logic = request.registry.logic

    try:
        email = request.json_body.get('email')
        password = request.json_body.get('password')
    except:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'email or password missing' })

    if logic.add_user(email, password):
        return Response(status=httplib.CREATED, json_body={
            'status': 'account created'})

    return Response(status=httplib.INTERNAL_SERVER_ERROR, json_body={
        'status': 'could not save user' })

# TODO: pyramid authentication

def login_user(request: Request) -> Response:
    logic: Logic = request.registry.logic

    try:
        email = request.json_body.get('email')
        password = request.json_body.get('password')
    except:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'email or password missing'})

    if logic.authenticate_user(email, password) == False:
        return Response(status=httplib.UNAUTHORIZED, json_body={
            'status': 'error',
            'description': 'wrong email or password'})

    try:
        logic.add_token(email)
    except:
        return Response(status=httplib.INTERNAL_SERVER_ERROR, json_body={
            'status': 'error',
            'description': 'could not save token' })

    token = logic.read_token(email)

    return Response(status=httplib.CREATED, json_body={
        'status': 'token created',
        'token': token })

# TODO: unique token, session cookie, swap token dict keys/values for better access?
def logout_user(request: Request) -> Response:
    logic: Logic = request.registry.logic

    try:
        email = request.json_body.get('email')
        token = request.json_body.get('token')
    except:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'email or token missing'})

    if logic.read_token(email) != token:
        return Response(status=httplib.UNAUTHORIZED, json_body={
            'status': 'error',
            'description': 'wrong email or token'})

    if logic.remove_token(email):
        return Response(status=httplib.OK, json_body={
            'status': 'logged out'})

    return Response(status=httplib.INTERNAL_SERVER_ERROR, json_body={
        'status': 'error',
        'description': 'could not revoke token'})

# TODO: unique token, session cookie, swap token dict keys/values for better access?
def shorten_url(request: Request) -> Response:
    logic: Logic = request.registry.logic

    try:
        email = request.json_body.get('email')
        token = request.json_body.get('token')
        url_orig = request.json_body.get('url')
    except:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'email, url or token missing'})

    if token != logic.read_token(email):
        return Response(status=httplib.UNAUTHORIZED, json_body={
            'status': 'error',
            'description': 'wrong email or token'})

    try:
        url_short = logic.get_valid_url_string(url_orig)
        if url_short == -1:
            return Response(status=httplib.REQUEST_TIMEOUT, json_body={
                'status': 'error',
                'description': 'url generation timed out'})
    except:
        return Response(status=httplib.INTERNAL_SERVER_ERROR, json_body={
            'status': 'error',
            'description': 'could not generate url'})

    try:
        logic.add_url(email, url_short, url_orig)
    except:
        return Response(status=httplib.INTERNAL_SERVER_ERROR, json_body={
            'status': 'error',
            'description': 'could not save url'})

    # Maybe add full url
    return Response(status=httplib.CREATED, json_body={
        'status': 'url created',
        'url': url_short})

def url_redirect(request: Request) -> Response:
    logic: Logic = request.registry.logic

    try:
        url_short = request.matchdict['url_short']
    except:
        return Response(status=httplib.BAD_REQUEST, json_body={
            'status': 'error',
            'description': 'url string missing'})

    try:
        url_orig = logic.get_original_url(url_short)
    except:
        return Response(status=httplib.NOT_FOUND, json_body={
            'status': 'error',
            'description': 'could not retrieve original url'})

    return HTTPFound(location=url_orig)

def notfound(request: Request) -> Response:
    return Response(status=httplib.NOT_FOUND, json_body={
        'status': 'error',
        'reason': 'Resource does not exist'
    })


def forbidden(request: Request) -> Response:
    return Response(status=httplib.FORBIDDEN, json_body={
        'status': 'error',
        'reason': 'Access denied'
    })