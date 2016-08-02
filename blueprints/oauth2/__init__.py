from flask import Blueprint

from blueprints.oauth2.views.auth import auth_view
from blueprints.oauth2.views.submit import submit_view
from blueprints.oauth2.views.token import token_view, revoke_view, info_view

oauth2_blueprint = Blueprint('oauth2', __name__, url_prefix='/oauth2')
oauth2_blueprint.add_url_rule('/auth', endpoint='oauth2_auth', view_func=auth_view, methods=['GET'])
oauth2_blueprint.add_url_rule('/auth/submit', endpoint='oauth2_auth_submit', view_func=submit_view, methods=['GET'])
oauth2_blueprint.add_url_rule('/token', endpoint='oauth2_token', view_func=token_view, methods=['POST'])
oauth2_blueprint.add_url_rule('/token/revoke', endpoint='oauth2_token_revoke', view_func=revoke_view, methods=['POST'])
oauth2_blueprint.add_url_rule('/token/info', endpoint='oauth2_token_info', view_func=info_view, methods=['GET'])

