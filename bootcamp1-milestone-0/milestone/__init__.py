import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
# Factory Pattern
def create_app():
    
    app = Flask(__name__)
    app_settings = os.getenv(
        'APP_SETTINGS',
        'milestone.config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)
    
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