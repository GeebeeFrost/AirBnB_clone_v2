#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.teardown_appcontext
def close_session(self):
    """Removes the current SQLAlchemy session"""
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays a HTML page like the AirBnB clone
    with places from the database"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template(
            '100-hbnb.html', states=states, amenities=amenities, places=places
            )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
