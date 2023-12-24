#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Returns Hello HBNB for empty route"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Handles /hbnb route"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """Displays C followed by text string"""
    return "C {}".format(escape(text.replace('_', ' ')))


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is_cool"):
    """Displays Python followed by text string or 'is cool'"""
    return "Python {}".format(escape(text.replace('_', ' ')))


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """Displays text only if n is a number"""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run()
