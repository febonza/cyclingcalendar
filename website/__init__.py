from flask import Flask
import sqlite3
from cs50 import SQL
# from flask_googlemaps import GoogleMaps
# from flask_sqlalchemy import SQLAlchemy
# from flask_datepicker import datepicker
# from flask_bootstrap import Bootstrap
# from markupsafe import Markup 

# Database configurarions
db = SQL("sqlite:///database.db")
DB_NAME = 'database.db'

# Upload configurations
UPLOAD_FOLDER = '/website/static/race_images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ufeahfiuaehfuihjd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # GoogleMaps(app)
    # db.init_app(app)
    # datepicker(app)
    # Bootstrap(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    return app

