from flask import Flask
from flask_cors import CORS
from api.config import config
from api.core import all_exception_handler

def create_app():

    app=Flask(__name__)

    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
    app.config['SECRET_KEY'] = config.secret_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from api.models import db

    db.init_app(app)

    from api.views import main

    app.register_blueprint(main.main)

    app.register_error_handler(Exception, all_exception_handler)
    
    return app