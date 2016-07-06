from flask import Flask


def create_app(blueprints, default_config_obj='config.default', config_filename='development.py',
               app_ctx_globals_class=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(default_config_obj)
    app.config.from_pyfile(config_filename)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    if app_ctx_globals_class is not None:
        app.app_ctx_globals_class = app_ctx_globals_class

    return app

