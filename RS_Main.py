from flask import Flask

myapp = Flask(__name__)


@myapp.route("/")
def hello():
    return 'RS Service ........'

@myapp.route("/test")
def test():
    return 'RS test !!  ...'
