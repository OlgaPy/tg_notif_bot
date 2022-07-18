import importlib
import inspect
import typing

import peewee
from peewee import Model

import settings


class DBManager:
    """DB manager"""

    DATABASE = settings.DataBase().local_path
    database = peewee.SqliteDatabase(DATABASE)

    @classmethod
    def get_models(cls) -> typing.List[typing.Type[Model]]:
        """
        Returns list with all DB models
        """
        return [
            member[1] for member in inspect.getmembers(
                importlib.import_module('database.models'),
                lambda m: inspect.isclass(m) and Model in m.__mro__ and not m.__subclasses__())
        ]

    @classmethod
    def create_tables(cls) -> None:
        """
        Create tables
        """
        cls.database.create_tables(cls.get_models(), safe=True)

    @classmethod
    def initialize_db(cls) -> None:
        cls.database.connect()
        cls.create_tables()
