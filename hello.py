from flask import Flask

myapp = Flask(__name__)


@myapp.route("/")
def hello():
    return 'Hello World! ...???'

@myapp.route("/test")
def test():
    return 'Robert test'
