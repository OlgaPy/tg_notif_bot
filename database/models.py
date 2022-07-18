from peewee import CharField, Model, PrimaryKeyField, BigIntegerField, ForeignKeyField

from .db_manager import DBManager


class BaseModel(Model):
    class Meta:
        database = DBManager.database


class SystemUsers(BaseModel):
    """
    Table with users at master's system
    """
    id = PrimaryKeyField()
    ms_login = CharField(unique=True)


class TgUsers(BaseModel):
    """
    Table with telegram users
    """
    id = PrimaryKeyField()
    tg_id = BigIntegerField(unique=True)


class Subscriptions(BaseModel):
    """
    Table subscriptions. For comparison users telegram to master system
    """
    id = PrimaryKeyField()
    tg_user = ForeignKeyField(TgUsers)
    ms_users = ForeignKeyField(SystemUsers)
