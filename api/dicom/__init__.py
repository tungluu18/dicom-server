# coding=utf-8
import logging
import datetime
import urllib.parse
from flask import request, jsonify, send_from_directory
from model import Annotation
from api import api_blueprint as app
import json
import os

_logger = logging.getLogger(__name__)


@app.route('/save_data_annotate', methods=['POST'])
def save_data_annotate():
	req_body = request.get_json()
	if req_body is None or "path_file" not in req_body:
		return abort(400)
	file_name = req_body["path_file"]
	if '..' in file_name:
		return abort(400)
	if "get" in req_body:
		try:
# 			print(req_body)
			sopiuid = req_body["sopiuid"]
			path_file = os.path.basename(req_body["path_file"])
			siuid = req_body["siuid"]

			file_auto_analysis = "/root/tuannm/dicom-server/data/json_machine/{}__{}__{}.json".format(siuid, sopiuid, path_file)
			
			print("Read Auto analysis file: {}".format(file_auto_analysis))
			_logger.info("Read Auto analysis file: {}".format(file_auto_analysis))

			with open(file_auto_analysis, 'r') as fr:
				data = json.load(fr)
			fr.close()
			
			return jsonify(status=True, data=data)
		except Exception as e:
			# _logger.info(f"GO TO get_auto_analysis: {req_body}")	
			_logger.error(e)
			return {'status': False, 'error': e}, 500
		
	try:
		req_body["timestamp"] = datetime.datetime.now().strftime("%s")
		savedfile_path, savedfile_location = Annotation.save(req_body)
		print("Saved file: {}".format(savedfile_path))
		_logger.info("Save file: {}".format(savedfile_path))
		return jsonify(status=True, data=urllib.parse.urljoin(
			request.host_url, urllib.parse.quote(savedfile_location)
		))
	except Exception as e:
		_logger.error(e)
		return {'status': False, 'error': e}, 500

@app.route('/get_file_dicom', methods=['POST'])
def get_file_dicom():
	req_body = request.get_json()

	if "siuid" in req_body and "path_file" in req_body:
		try:
			path_file = req_body["path_file"]
			siuid = req_body["siuid"]

			file_dicom_dir = "/root/tuannm/dicom-server/data/dicom_data/{}".format(siuid)
			path = os.path.basename(path_file)

			# path = "K3AA0H02"
			print("GET DICOM file: {}".format(os.path.join(file_dicom_dir, path) ))
			
			return send_from_directory(file_dicom_dir, path, as_attachment=True)


		except Exception as e:
			# _logger.info(f"GO TO get_auto_analysis: {req_body}")	
			_logger.error(e)
			print("ERROR: {}".format(e))
			return {'status': False, 'error': e}, 500
		
	else:
		return {'status': False, 'error': e}, 500


@app.route('/get_file_zip_study', methods=['POST'])
def get_file_zip_study():
	req_body = request.get_json()

	if "siuid" in req_body:
		try:
			file_dicom_dir = "/root/tuannm/dicom-server/data/dicom_data"
			path = "{}.zip".format(req_body["siuid"])
			print("Download file zip study: {}".format(os.path.join(file_dicom_dir, path) ))
			return send_from_directory(file_dicom_dir, path, as_attachment=True)

		except Exception as e:
			# _logger.info(f"GO TO get_auto_analysis: {req_body}")	
			_logger.error(e)
			print("ERROR: {}".format(e))
			return {'status': False, 'error': e}, 500
		
	else:
		return {'status': False, 'error': e}, 500
