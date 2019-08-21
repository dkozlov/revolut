import os
import logging
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
api = Api()


def create_app(config_object='project.config.DevelopmentConfig', script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv(
        'APP_SETTINGS') or config_object
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    app.logger.setLevel(logging.INFO)
    migrate.init_app(app, db)

    # register blueprints
    from project.app import app_blueprint
    app.register_blueprint(app_blueprint)

    # set up API
    api.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db, 'api': api}

    return app
