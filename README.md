# Service Telegram Notifications

----
----
Microservice for telegram notification

## Getting Started

### Prerequisites

Service requires python 3.9 version to run. 
### Installing

Cloning project from git repository

```bash
git clone ...
```

Creating virtual environment for project

```bash
cd service_telegram_notification/
python3.9 -m venv venv
```

Installing Service dependencies

```bash
source venv/bin/activate
pip install --upgrade pip
pip3 install setuptools
pip3 install wheel
pip3 install -r requirements.txt
deactivate
```

When deploying redis locally, it is important to allow broadcasting to 0.0.0.0 in redis settings
```sudo nano /etc/redis/redis.conf```
Add:
```bind 0.0.0.0 ::1```

Launching Service:

```bash
source venv/bin/activate
python3.9 bot.py
```

or

```bash
docker run -v <path_to_your_local_directory_for_db>:/db/LocalDB -e TZ=Europe/Moscow debian date
```


Environmental Variables:
* **TG_BOT_TOKEN** - telegram bot token taken from @botFather. Required
* **DATABASE_LOCAL_PATH** - path to bd. For local deployment, the value can be anything, the default is ./database/LocalDB. Required in case of a docker: /db/LocalDB.
* **REDIS_SERVER** - host of redis service, default value '127.0.0.1'. Required in case of a docker use your address in net of your docker, you can watch this by ```ifconfig``` at area "docker0".  For example: '192.168.0.1'

* **REDIS_PORT** - port of redis service, default value 6379. Optional
* **REDIS_DB_PUBSUB** - logical databases redis, default value 5. Optional
* **REDIS_SUBSCRIBE_KEY** - name of channel at redis, default value 'telegram_job_problem'. Optional
* **TZ** - time zone. Recommended in case of a docker value Europe/Moscow

* The other parameters are specified in the settings and are optional


To locally test sending messages via redis, you can use the following script by placing it in the directory 
```./telegram/redis_test.py```
```python
"""
temporary script for send message to redis chanel
"""
import json

import redis

import settings

redis = redis.Redis(
    host=settings.Redis().server,
    port=settings.Redis().port,
    db=settings.Redis().db_pubsub
)
channel = settings.Redis().subscribe_key
test_result = {
    "username": <your_login>,
    "message": 'Warning: during Power Cycle Test for server: <b>0208200006</b> with motherboard: TEST_MBD\n'
               'Problem: SEL - Host system DC power is off - OK\n'
               '<a href=\"https://www.google.com/\">Results</a>\n'
               '<a href=\"https://www.google.com/\">Progress</a>\n'
               '<a href=\"https://www.google.com/\">Problems</a>'
}
redis.publish(channel=channel, message=str(json.dumps(test_result)))
```

## Built With

* [Aiogramm](https://docs.aiogram.dev/en/latest/) - is a pretty simple and fully asynchronous framework for Telegram Bot API written in Python 3.7 with asyncio and aiohttp

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **[Olga Pykhova](https://github.com/OlgaPy)**

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
