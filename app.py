from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.DevelConfig')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# importing applications into namespace
from library import views as lib_views
from library import models