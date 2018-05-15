import os
from flask import Flask
from flask_cors import CORS

from .models import db
from .views import view


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(64),
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:chinavis2018@123.206.64.248/chinavis',
        debug=True
    )

    CORS(app)
    db.init_app(app)
    app.register_blueprint(views.view)

    return app
