import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Hello World"

@app.route('/hello/<username>', methods=['GET'])
def hello(username):
    return "Hello," + username

app.run()