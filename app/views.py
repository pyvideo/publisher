from flask import Blueprint, jsonify, request

from . import app
from .celery import publish_media_record


publisher = Blueprint('publisher', __name__)


@publisher.route('/', methods=['POST'])
def index():
    content = request.get_json()

    print(content)

    return jsonify({'result': 'ok'})

