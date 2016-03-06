import logging

from flask import Flask
from raven.contrib.flask import Sentry
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object('config')

if app.config.get('SENTRY_DSN'):
    Sentry(app, logging=True, level=logging.ERROR)

from app.views import publisher
app.register_blueprint(publisher)


@app.after_request
def cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

