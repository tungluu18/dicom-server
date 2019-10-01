# coding=utf-8
import logging
import datetime
import urllib.parse
from flask import request, jsonify
from model import Annotation
from api import api_blueprint as app

_logger = logging.getLogger(__name__)


@app.route('/save_data_annotate', methods=['POST'])
def save_data_annotate():
    req_body = request.get_json()
    if req_body is None or "path_file" not in req_body:
        return abort(400)
    file_name = req_body["path_file"]
    if '..' in file_name:
        return abort(400)
    try:
        req_body["timestamp"] = datetime.datetime.now().strftime("%s")
        savedfile_path, savedfile_location = Annotation.save(req_body)
        print("Saved file: {}".format(savedfile_path))
        _logger.info("Save file: {}".format(savedfile_path))
        return jsonify(data=urllib.parse.urljoin(
            request.host_url, urllib.parse.quote(savedfile_location)
        ))
    except Exception as e:
        _logger.error(e)
        return {'error': e}, 500
