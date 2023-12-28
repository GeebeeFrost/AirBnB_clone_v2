#!/usr/bin/python3
"""This script starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def close_session(self):
    """Removes the current SQLAlchemy session"""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays a HTML page like AirBnB clone with filters from database"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template(
            '10-hbnb_filters.html', states=states, amenities=amenities
            )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
