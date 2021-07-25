import os

from flask import Flask
from flask.globals import g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
# Factory Pattern

global_config = None

def create_app():
    global global_config
    app = Flask(__name__)
    app_settings = os.getenv(
        'APP_SETTINGS',
        'milestone.config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)
    print("called")
    global_config = app.config.copy()
    print(global_config)
    # Third party apps
    CORS(app)
    bcrypt.init_app(app)
    db.init_app(app)
    with app.app_context():
                db.create_all()

    from milestone.restaurantApp.routes import restaurant_blueprint
    from milestone.authApp.routes import auth_blueprint
    app.register_blueprint(restaurant_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

from .models import *