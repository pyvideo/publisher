from flask import Flask

from app.views import publisher


app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(publisher)

