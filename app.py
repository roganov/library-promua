from flask import Flask

app = Flask(__name__)

app.config.from_object('config')


# importing applications into namespace
from library import views as lib_views
