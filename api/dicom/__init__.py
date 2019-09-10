# coding=utf-8
import os
import json
import datetime
import urllib.parse
from flask import request, jsonify
from model.dicom import Dicom
from api import api_blueprint as app


@app.route('/save_data_annotate', methods=['POST'])
def save_data_annotate():
    value = request.get_json()
    if value is None or "path_file" not in value:
        return abort(400)
    file_name = value["path_file"]
    if '..' in file_name:
        return abort(400)

    file_name = file_name.replace("/storage/emulated/0/Download/", "")
    file_name = file_name.replace("/", "__")

    deviceID = str(value.get("deviceID", "nodevice"))
    path_to_foder_deviceID = "./data/json_data/" + deviceID
    # check folder not exist then create
    if (not os.path.exists(path_to_foder_deviceID)):
        os.makedirs(path_to_foder_deviceID, exist_ok=True)

    file_name = "{file_name}_{timestamp}.json".format(
        file_name=file_name,
        timestamp=datetime.datetime.now().strftime("%s")
    )
    file_path = "{path}/{file_name}".format(
        path=path_to_foder_deviceID,
        file_name=file_name
    )

    Dicom.save_data_annotate(pathFile=file_path, **value)

    fw = open(file_path, "w")
    fw.write(json.dumps(value))
    fw.close()

    return jsonify(data=urllib.parse.urljoin(request.host_url, file_path))
