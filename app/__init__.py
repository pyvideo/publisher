from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app.views import publisher
app.register_blueprint(publisher)


@app.after_request
def cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

