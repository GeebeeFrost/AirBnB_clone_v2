#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City

type_storage = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """Defines a state"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if type_storage == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", cascade="all, delete-orphan", backref="state"
        )
    else:
        name = ""

    if type_storage != 'db':
        @property
        def cities(self):
            """Returns list of city instances with state_id
            equal to the current State.id"""
            all_cities = models.storage.all(City)
            state_cities = [
                city for city in all_cities.values()
                if city.state_id == self.id
            ]
            return state_cities
