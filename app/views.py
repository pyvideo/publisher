from collections import OrderedDict
import hashlib
import os

from flask import Blueprint, jsonify, request

from app.celery import publish_media_record

CONTENT_KEYS = {'data_file', 'publish_key'}
SECRET_KEY = os.environ['SECRET_KEY']
REPO_PATH = os.environ['REPO_PATH']

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
       
    publish_media_record.delay(**content)

    return jsonify({'result': 'ok'})


def is_valid_content(content):
    """
    Check that data_file is valid.
    """
    data_file = os.path.join(REPO_PATH, content['data_file'])
    exists = os.path.exists(data_file)
    return exists


def is_valid_publish_key(content):
    """
    Check that publish key is valid
    """
    values = content['data_file'], SECRET_KEY 

    value_string = ';'.join(values)

    m = hashlib.md5()
    m.update(value_string.encode())
    digest = m.hexdigest()
    is_valid = digest == content['publish_key']
 
    return is_valid

