#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv

type_storage = getenv('HBNB_TYPE_STORAGE')

if type_storage == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if type_storage == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(
                DateTime, nullable=False, default=datetime.utcnow()
                )
        updated_at = Column(
                DateTime, nullable=False, default=datetime.utcnow()
                )

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs and len(kwargs) > 0:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                setattr(self, k, v)
                if type(self.created_at) is str:
                    self.created_at = datetime.strptime(
                            self.created_at, "%Y-%m-%dT%H:%M:%S.%f"
                            )
                if type(self.updated_at) is str:
                    self.updated_at = datetime.strptime(
                            self.updated_at, "%Y-%m-%dT%H:%M:%S.%f"
                            )

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary['__class__'] = self.__class__.__name__
        if "_sa_instance_state" in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)
