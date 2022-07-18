from enum import Enum


class TgMessages(Enum):
    """
    Class for content messages
    """
    HELP_MSG = (
        "\n"
        "/start - run the bot. \n"
        "/add i.ivanov - start receiving messages for user ms with login i.ivanov. \n"
        "/del i.ivanov - end receiving messages for user ms with login i.ivanov. \n"
        "/help - call help. \n"
    )

    INCORRECT_LOGIN = (
        "\n"
        "Incorrect command format. \n"
        "For example: \n"
        "/add i.ivanov \n"
    )

    DELTA_FAIL = (
        "\n"
        "Command will be available in {remaining_time_second} seconds. \n"
    )

    START_KNOWN_USER = (
        "\n"
        "Hi, {tg_username}. \n"
        "Nice to see you again! \n"
        "You are subscribed to messages {ms_logins}"
    )

    START_UNKNOWN_USER = (
        "\n"
        "Hi. \n "
        "I'm the bot to send messages about detected problems during test procedures in ms-system. \n"
        "In order to start getting test results - enter your login to ms with the /add command. \n"
        "For example: \n"
        "/add i.ivanov\n"
    )

    ADD_REJECT = (
        "\n"
        "You are already receiving messages for the user with login {ms_login}. \n"
    )

    CONTACT_ADMINISTRATOR = (
        "\n"
        "There was an error: {ex}. The operation has not been executed. \n"
        "Contact your administrator: {email}. \n"
    )

    ADD_SUCCESS = (
        "\n"
        "The ms-login is set. \n"
        "You start receiving messages for {ms_login}. \n"
    )

    UNKNOWN_MESSAGE = (
        "\n"
        "Message not recognized. \n"
        "In order to find out the capabilities of the bot use the command /help \n"
    )
    DEL_SUCCESS = (
        "\n"
        "You will no longer receive messages for {ms_login} \n"
    )

    DEL_REJECT = (
        "\n"
        "You are not subscribed to the user {ms_login}"
    )
