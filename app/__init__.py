from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import app_config


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    Bootstrap(app)

    from app import models

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
