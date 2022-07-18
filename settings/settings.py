import pydantic


class Redis(pydantic.BaseSettings):
    """Redis related settings."""

    server: str = '127.0.0.1'
    port: int = 6379
    db_pubsub: int = 5
    db_storage: int = 4
    storage_pool_size = 10
    storage_prefix = 'my_fsm_key'
    subscribe_key: str = 'telegram_job_problem'

    class Config:
        case_sensitive = False
        env_prefix = 'REDIS_'


class TG(pydantic.BaseSettings):
    """Telegram related settings. """

    bot_token: str
    command_pause_second: int = 5

    class Config:
        case_sensitive = False
        env_prefix = 'TG_'


class DataBase(pydantic.BaseSettings):
    """Database related settings."""
    local_path: str = './database/LocalDB'
    mail_administrator: str = 'example@gmail.com'

    class Config:
        case_sensitive = False
        env_prefix = 'DATABASE_'
