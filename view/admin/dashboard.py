import logging
import urllib
from flask import request

from services.dicom_service import stat
from view.admin import app, jinja_env
from view.routes import routing_table

_logger = logging.getLogger(__name__)


@app.route(routing_table['admin']['dashboard'])
def dashboard():
    dashboard_template = jinja_env.get_template('dashboard.html')
    overview, by_date_and_user = stat.stat_on_folder()
    for row in overview:
        row['url'] = urllib.parse.urljoin(
            request.host_url, 'data/json_data/{}'.format(row['path']))
    return dashboard_template.render({
        'data': (overview, by_date_and_user)
    })
