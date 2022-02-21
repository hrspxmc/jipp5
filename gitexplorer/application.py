from ensurepip import bootstrap
from flask import Flask
from flask_bootstrap import Bootstrap5

from .containers import Container
from . import views

def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/", "index", views.index, methods = ['GET', 'POST'])

    bootstrap = Bootstrap5()
    bootstrap.init_app(app)

    return app