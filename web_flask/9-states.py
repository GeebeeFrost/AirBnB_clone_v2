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


@app.route("/states", strict_slashes=False)
def display_states():
    """Displays a HTML page with a list of states present in database"""
    states = storage.all(State).values()
    return render_template('9-states.html', mode='all', states=states)


@app.route("/states/<id>", strict_slashes=False)
def display_state_cities(id):
    """Displays a HTML page with a state and cities linked to that state"""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template(
                    '9-states.html', mode='single', single_state=state
                    )
    return render_template('9-states.html', mode='none')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
