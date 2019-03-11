# coding=utf-8

import logging
import os
import config
import shutil
from util import allowed_filename
from werkzeug.utils import secure_filename

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


def save_file_to_dir(dir, file):
    if file.filename == '' or not allowed_filename(file.filename):
        return
    path_to_file = os.path.join(*[config.ROOT_DIR, config.DATA_DIR, dir])
    try:
        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)
        file.save(os.path.join(path_to_file, file.filename))
        return os.path.join(dir, file.filename)
    except Exception as err:
        _logger.error(err)
        raise err
