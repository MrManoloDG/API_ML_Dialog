import flask

application = flask.Flask(__name__)
application.config["DEBUG"] = True


@application.route('/', methods=['GET'])
def home():
    return "Hello World"

@application.route('/hello/<username>', methods=['GET'])
def hello(username):
    return "Hello," + username

if __name__ == "__main__":
    application.run(host='127.0.0.1')


