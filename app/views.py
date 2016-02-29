from collections import OrderedDict
import hashlib
import os

from flask import Blueprint, jsonify, request

from app.celery import publish_media_record

CONTENT_KEYS = {'data_file', 'category_slug', 'media_record_slug', 'publish_key'}
SECRET_KEY = os.environ['SECRET_KEY']

publisher = Blueprint('publisher', __name__)


@publisher.route('/publish', methods=['POST'])
def index():
    content = dict(request.form)

    content = OrderedDict((k, content[k][0]) for k in sorted(content.keys()))

    if set(content.keys()) != CONTENT_KEYS:
        msg = 'Incorrect or missing keys provided in request.'
        return jsonify({'result': 'failure', 'msg': msg})

    valid_publish_key = is_valid_content(content)
    if not valid_publish_key: 
        msg = 'Incorrect Publish Key.'
        return jsonify({'result': 'failure', 'msg': msg})
 
    valid_publish_key = is_valid_publish_key(content)
    if not valid_publish_key: 
        msg = 'Incorrect Publish Key.'
        return jsonify({'result': 'failure', 'msg': msg})
       
    publish_media_record.delay(**content)

    return jsonify({'result': 'ok'})


def is_valid_content(content):
    """
    Check that data_file, category_slug, media_record_slug are valid.
    """
    return True


def is_valid_publish_key(content):
    """
    Check that publish key is valid
    """
    values = content['data_file'], content['category_slug'], content['media_record_slug'] 

    values += (SECRET_KEY,)
    
    value_string = ';'.join(values)

    m = hashlib.md5()
    m.update(value_string.encode())
    digest = m.hexdigest()
    is_valid = digest == content['publish_key']
 
    return is_valid

