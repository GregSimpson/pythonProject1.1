from flask import Flask
from flasgger import Swagger
from api.route.home import home_api, logger


def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'RealPlay Auth0 Role Sync API',
    }
    swagger = Swagger(app)
     ## Initialize Config
    app.config.from_pyfile('config.py')
    app.register_blueprint(home_api, url_prefix='/api')

    setup_logging()

    return app


#-----
import os
import logging.config
import logging
import yaml
logger = logging.getLogger("RealplaySync")

def setup_logging(
    default_path='logging.yaml',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """

    #logger = logging.getLogger("RealplaySync")

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    logger.info("app.py - setup_logging")
    logger.debug("app.py - setup_logging")
#-----


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    #setup_logging()
    #logger = logging.getLogger("RealplaySync")
    logger.error(" app.py logging")
    #logger.debug('Hi, does logging work?')

    app.run(host='0.0.0.0', port=port)
