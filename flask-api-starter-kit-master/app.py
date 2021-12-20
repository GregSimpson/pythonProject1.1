from flask import Flask
from flasgger import Swagger
from api.route.home import home_api


def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'RealPlay Auth0 Role Sync API',
    }
    swagger = Swagger(app)
     ## Initialize Config
    app.config.from_pyfile('config.py')
    app.register_blueprint(home_api, url_prefix='/api')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    print(" GJS GJS GJS in app.py - main")

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    #setup_logging()
    #logger = logging.getLogger("RealplaySync")

    app = create_app()

    #logger.debug('Hi, does logging work?')

    app.run(host='0.0.0.0', port=port)
