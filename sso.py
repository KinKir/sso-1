from app_factory import create_app
from blueprints import available_blueprints
from db import init_db_session_factory
from app_context import SSOAppContextGlobals

app = create_app(available_blueprints, app_ctx_globals_class=SSOAppContextGlobals)
init_db_session_factory(app.config['SQLALCHEMY_DB_URI'], app.config['SQLALCHEMY_DB_ECHO'])

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST_NAME'], port=app.config['SERVER_PORT'])
