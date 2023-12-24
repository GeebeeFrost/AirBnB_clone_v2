#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def close_session(self):
    """Removes the current SQLAlchemy session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def display_states():
    """Displays a HTML page with a list of states present in database"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda k: k.name)
    return render_template('7-states_list.html', states=sorted_states)


if __name__ == "__main__":
    app.run()
