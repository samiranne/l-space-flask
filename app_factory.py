import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import DevelopmentConfig, TestConfig


def create_app(testing=False):
    app = Flask(__name__)
    if not testing:
        app.config.from_object(
            os.environ.get('APP_SETTINGS', DevelopmentConfig))
        app.secret_key = app.config['SECRET_KEY']
    else:
        app.config.from_object(TestConfig)
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = u'Please log in to access this page.'
    login_manager.login_message_category = 'error'
    return app, db, login_manager, bcrypt


app, db, login_manager, bcrypt = create_app()
