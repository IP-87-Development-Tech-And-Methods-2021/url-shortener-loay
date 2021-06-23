"""
This module is responsible for reading application config from environment variables
"""
import logging
import os
import sys
from typing import NamedTuple

import trafaret as t

__all__ = (
    'Config',
    'load_config',
)

log = logging.getLogger(__name__)

_Port = t.Int(gt=0, lt=65535)

_CONFIG_VALIDATOR = t.Dict(
    {
        t.Key('PORT', optional=True, default="6543") >> 'port':
        _Port,
        t.Key('BASE_URL',
              optional=True,
              default="http://127.0.0.1:6543",
              to_name='base_url'):
        t.URL,
        t.Key('USER_DB',
              optional=True,
              default="users.json",
              to_name='user_db'):
        t.String,
    },
    ignore_extra='*')


class Config(NamedTuple):
    base_url: str
    port: int
    user_db: str


def load_config(app_config) -> Config:
    try:
        app_config_validated = _CONFIG_VALIDATOR.check(app_config)
        return Config(**app_config_validated)
    except t.DataError as e:
        log.exception('Invalid configuration. Errors: %s', e.as_dict())
        sys.exit(os.EX_CONFIG)