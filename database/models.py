from peewee import CharField, Model, PrimaryKeyField, BigIntegerField, ForeignKeyField

from .db_manager import DBManager


class BaseModel(Model):  # pylint: disable=too-few-public-methods
    class Meta:  # pylint: disable=too-few-public-methods
        database = DBManager.database


class SystemUsers(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Table with users at master's system
    """
    id = PrimaryKeyField()
    ms_login = CharField(unique=True)


class TgUsers(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Table with telegram users
    """
    id = PrimaryKeyField()
    tg_id = BigIntegerField(unique=True)


class Subscriptions(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Table subscriptions. For comparison users telegram to master system
    """
    id = PrimaryKeyField()
    tg_user = ForeignKeyField(TgUsers)
    ms_users = ForeignKeyField(SystemUsers)
