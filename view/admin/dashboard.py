import logging
import urllib
from flask import request

from services import dicom_service
from view.admin import app, jinja_env
from view.routes import routing_table

_logger = logging.getLogger(__name__)


@app.route(routing_table['admin']['dashboard'])
def dashboard():
    dashboard_template = jinja_env.get_template('dashboard.html')
    overview, by_date_and_user = dicom_service.stat.stat_on_folder()
    for row in overview:
        row['url'] = urllib.parse.urljoin(
            request.host_url, 'data/json_data/{}'.format(row['path']))
    for row in overview:
        deviceID = row['device']
        filename = row['url'].split('/')[-1].replace('.json', '')
        gif_url = dicom_service.view.get_gif_url(filename, deviceID)
        row['gif_url'] = urllib.parse.urljoin(
            request.host_url, gif_url) if gif_url else None
        row['gif_name'] = "{}__{}.gif".format(deviceID, filename)
    return dashboard_template.render({
        'data': (overview, by_date_and_user)
    })
