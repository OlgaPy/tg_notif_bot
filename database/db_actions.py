from typing import List

from .models import Subscriptions, TgUsers, SystemUsers


def get_tg_ids_by_vat_login(ms_login: str) -> List[int]:
    """
    Get all telegram ids subscribers by master system-login
    """
    return list(
        Subscriptions.select(
            TgUsers.tg_id
        )
        .join(TgUsers).switch(Subscriptions)
        .join(SystemUsers)
        .where(SystemUsers.ms_login == ms_login)
        .objects(lambda tg_id: tg_id)
        .execute()
    )


def get_ms_logins_by_tg_id(tg_id: int) -> List[str]:
    """
    Get all logins' subscriber by telegram id
    """
    return list(
        Subscriptions.select(
            SystemUsers.ms_login
        )
        .join(SystemUsers).switch(Subscriptions)
        .join(TgUsers)
        .where(TgUsers.tg_id == tg_id)
        .objects(lambda ms_login: ms_login)
        .execute()
    )


def delete_subscription(tg_id: int, ms_login: str) -> None:
    """
    Delete subscribing user from tg db. Return message about successfully operation
    """
    (
        Subscriptions.
        delete().
        where(
            (Subscriptions.ms_users == SystemUsers.get(ms_login=ms_login)) &
            (Subscriptions.tg_user == TgUsers.get(tg_id=tg_id))
        ).
        execute()
    )
    #TODO: Fix it! Do not put a breakpoint here or on the line above!
    # Sometimes The contents of the entire table are dropped when running in the debug


def add_subscription(tg_id: int, ms_login: str) -> None:
    """
    Add subscription to master system login for telegram ID
    """
    Subscriptions.get_or_create(
        tg_user=TgUsers.get_or_create(tg_id=tg_id)[0],
        ms_users=SystemUsers.get_or_create(ms_login=ms_login)[0]
    )
