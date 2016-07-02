from app_factory import create_app
from blueprints import available_blueprints

app = create_app(available_blueprints)


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST_NAME'], port=app.config['SERVER_PORT'])
