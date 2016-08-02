from flask import Blueprint

from blueprints.sso.views.login import login_view
from blueprints.sso.views.submit import submit_view

sso_blueprint = Blueprint('sso', __name__, url_prefix='/sso')
sso_blueprint.add_url_rule('/login', endpoint='sso_login', view_func=login_view, methods=['GET'])
sso_blueprint.add_url_rule('/login/submit', endpoint='sso_login_submit', view_func=submit_view, methods=['GET'])

