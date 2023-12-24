#!/usr/bin/python3
"""This module contains the engine for database storage"""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session

env = getenv("HBNB_ENV")
user = getenv("HBNB_MYSQL_USER")
pwd = getenv("HBNB_MYSQL_PWD")
host = getenv("HBNB_MYSQL_HOST")
dbase = getenv("HBNB_MYSQL_DB")

classes = {
    "Amenity": Amenity, "City": City, "Place": Place, "Review": Review,
    "State": State, "User": User
}


class DBStorage:
    """Defines the database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                user, pwd, host, dbase), pool_pre_ping=True
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries on the current database session all objects
        depending on the class name"""
        dict_objs = {}
        if cls:
            if type(cls) is str and cls in classes:
                for obj in self.__session.query(classes[cls]):
                    key = obj.__class__.__name__ + '.' + obj.id
                    dict_objs[key] = obj
            elif cls in classes.values():
                for obj in self.__session.query(cls):
                    key = obj.__class__.__name__ + '.' + obj.id
                    dict_objs[key] = obj
        else:
            for cln in classes.values():
                for obj in self.__session.query(cln):
                    key = cln.__name__ + '.' + obj.id
                    dict_objs[key] = obj
        return dict_objs

    def new(self, obj):
        """Adds an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and a database session"""
        from models.city import City
        from models.state import State
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)

    def close(self):
        """Closes the current session"""
        self.__session.remove()
