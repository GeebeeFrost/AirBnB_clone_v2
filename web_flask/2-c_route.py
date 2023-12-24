#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Returns Hello HBNB for empty route"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Handles /hbnb route"""
    return "HBNB"


@app.route("/c/<string:text>")
def display_text(text):
    """Displays C followed by text string"""
    return "C {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run()
