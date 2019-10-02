import logging
import urllib
from flask import request

from services import dicom_service
from view.admin import app, jinja_env
from view.routes import routing_table
import util

_logger = logging.getLogger(__name__)


@app.route(routing_table['admin']['dashboard'])
def dashboard():
    dashboard_template = jinja_env.get_template('dashboard.html')
    # sort by date
    date_order = request.args.get('date_order', 'asc', type=str)
    # pagination
    page = request.args.get('page', 1, type=int)
    # load stat data
    overview, by_date_and_user = dicom_service.stat.stat_on_folder()
    overview.sort(key=lambda x: x['date'], reverse=(date_order == 'desc'))
    by_date_and_user.sort(
        key=lambda x: x['date'], reverse=(date_order == 'desc'))
    overview, current_page, pages = util.paginate(overview, page)
    # get json and gif 's url
    for row in overview:
        row['url'] = urllib.parse.urljoin(
            request.host_url,
            urllib.parse.quote('data/json_data/{}'.format(row['path']))
        )
    for row in overview:
        deviceID = row['device']
        filename = row['path'].split('/')[-1].replace('.json', '')
        gif_url = dicom_service.view.get_gif_url(filename, deviceID)
        row['filename'] = filename
        row['gif_url'] = urllib.parse.urljoin(
            request.host_url, urllib.parse.quote(gif_url)) if gif_url else None
        row['gif_name'] = "{}__{}.gif".format(deviceID, filename)
    return dashboard_template.render({
        'data': (overview, by_date_and_user),
        'pagination': dict({
            'current_page': current_page,
            'pages': pages,
        }),
        'show_path': request.args.get('show_path', False, type=bool),
        'date_order': date_order,
    })
