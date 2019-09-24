# coding=utf-8
import logging
import datetime
import json
import os

from model import db, Basemodel, ma

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


class Annotation(Basemodel):
    __tablename__ = 'annotations'

    deviceID = db.Column(db.String(50), index=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_location = db.Column(db.String(255), nullable=False)

    def __init__(self, deviceID, file_path, file_location):
        """ Params:
                str: file_path: file's path on remote's device
                str: file_location: file's path on server
            Return:
        """
        self.deviceID = deviceID
        self.file_path = file_path
        self.file_location = file_location

    @classmethod
    def save(self, annotate_data):
        """ Params:
                dict: annotate_data
            Return file's location on server
        """
        file_path = annotate_data["path_file"]
        file_name = file_path.replace(
            "/storage/emulated/0/Download/", "").replace("/", "__")
        deviceID = str(annotate_data.get("deviceID", "nodevice"))
        path_to_foder_deviceID = "./data/json_data/" + deviceID
        file_name = "{}_{}.json".format(
            file_name, datetime.datetime.now().strftime("%s"))
        file_location = "{}/{}".format(path_to_foder_deviceID, file_name)

        try:
            # check folder not exist then create
            if (not os.path.exists(path_to_foder_deviceID)):
                os.makedirs(path_to_foder_deviceID, exist_ok=True)
            savefile = open(file_location, "w")
            savefile.write(json.dumps(annotate_data))
            savefile.close()

            annotattion = Annotation(
                deviceID=deviceID, file_path=file_path,
                file_location=file_location
            )
            db.session.add(annotattion)
            db.session.commit()

            return file_path, file_location
        except Exception as e:
            _logger.error(e)
            db.session.rollback()
            raise e
