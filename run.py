import logging
import json

import waitress

from url_shortener.config import Config, load_config
from url_shortener.logging import configure_logging
from url_shortener.main import make_app

log = logging.getLogger(__name__)

if __name__ == '__main__':
    with open("config.json", "r") as config_file:
        config_dict = json.loads(config_file.read())
    configure_logging()
    app_config: Config = load_config(config_dict["app"])
    app = make_app(app_config)

    log.info('Wake up, Samurai! We have an app to build!')
    waitress.serve(app, host='0.0.0.0', port=app_config.port)