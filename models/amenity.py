#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Defines an amenity"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        from models.place import place_amenity
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
                "Place", secondary=place_amenity, back_populates="amenities"
                )
    else:
        name = ""
