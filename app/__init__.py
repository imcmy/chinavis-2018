import os
from flask import Flask
from flask_cors import CORS

from .models import db
from .views import view
from .chinavis_data import data


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(64),
        GITHUB_SECRET='4Qqk3NVez2Sea603c2ZwDqPb172SqOsIsEuzMvktDTnurIBKAI1SPoW5wHMCa71e',
        REPO_PATH='/usr/src/app',
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:chinavis2018@123.206.64.248/chinavis',
        debug=True
    )

    CORS(app)
    db.init_app(app)
    app.register_blueprint(views.view)
    app.register_blueprint(chinavis_data.data)

    return app
