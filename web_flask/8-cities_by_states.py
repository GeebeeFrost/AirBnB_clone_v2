#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.teardown_appcontext
def close_session(self):
    """Removes the current SQLAlchemy session"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Displays a HTML page with list of states and cities linked to them"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda k: k.name)
    # Create a list of lists with inner list having state and list of cities
    state_and_cities = [[state, sorted(state.cities, key=lambda k: k.name)]
                        for state in sorted_states]
    return render_template("8-cities_by_states.html", states=state_and_cities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
