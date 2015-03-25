from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.DevelConfig')

db = SQLAlchemy(app)


# importing applications into namespace
from library import views as lib_views
from library import models