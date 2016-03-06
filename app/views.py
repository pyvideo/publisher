from collections import OrderedDict
import os

from flask import Blueprint, jsonify, request

from app.celery import publish_media_record
from app.utils import is_valid_content, is_valid_publish_key


CONTENT_KEYS = {'data_file', 'publish_key'}


publisher = Blueprint('publisher', __name__)


@publisher.route('/publish', methods=['POST'])
def index():
    content = dict(request.form)

    content = OrderedDict((k, content[k][0]) for k in sorted(content.keys()))

    if set(content.keys()) != CONTENT_KEYS:
        msg = 'Incorrect or missing keys provided in request.'
        return jsonify({'result': 'failure', 'msg': msg})

    valid_content = is_valid_content(content)
    if not valid_content: 
        msg = 'Invalid content.'
        return jsonify({'result': 'failure', 'msg': msg})
 
    valid_publish_key = is_valid_publish_key(content)
    if not valid_publish_key: 
        msg = 'Incorrect Publish Key.'
        return jsonify({'result': 'failure', 'msg': msg})
       
    publish_media_record.delay(content['data_file'])

    return jsonify({'result': 'ok'})

