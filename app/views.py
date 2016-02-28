from flask import Blueprint, jsonify, request

from app.celery import publish_media_record

CONTENT_KEYS = {'data_file', 'category_slug', 'media_record_slug'}

publisher = Blueprint('publisher', __name__)


@publisher.route('/publish', methods=['POST'])
def index():
    content = request.get_json()

    if not isinstance(content, dict):
        msg = 'Request content is not a JSON object.'
        return jsonify({'result': 'failure', 'msg': msg})
        
    if set(content.keys()) != CONTENT_KEYS:
        msg = 'Incorrect or missing keys provided in request.'
        return jsonify({'result': 'failure', 'msg': msg})
      
    publish_media_record.delay(**content)

    return jsonify({'result': 'ok'})

