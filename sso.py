from app import create_app

app = create_app([])

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST_NAME'], port=app.config['SERVER_PORT'])
