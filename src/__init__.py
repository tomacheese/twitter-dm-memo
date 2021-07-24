import datetime
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import requests
import tweepy


def init_logger(child_name: str = None) -> logging.Logger:
    _logger = logging.getLogger("TwitterDMMemo")
    if child_name is not None:
        _logger = _logger.getChild(child_name)
    dt = datetime.datetime.now().date()
    date_time = dt.strftime("%Y-%m-%d")

    if not os.path.exists("logs/"):
        os.mkdir("logs/")

    rotatedHandler = TimedRotatingFileHandler(
        filename="logs/%s.log" % date_time,
        encoding="UTF-8",
        when="MIDNIGHT",
        backupCount=30
    )
    rotatedHandler.setLevel(logging.INFO)
    rotatedHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s'))
    _logger.addHandler(rotatedHandler)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s'))
    _logger.addHandler(streamHandler)

    return _logger


logger = init_logger()


def send_discord_message(token: str, channelId: str, message: str = "", embed: dict = None):
    logger.debug("sendDiscordMessage: {message}".format(message=message))
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bot {token}".format(token=token),
        "User-Agent": "Bot"
    }
    params = {
        "content": message,
        "embed": embed
    }
    response = requests.post(
        "https://discord.com/api/channels/{channelId}/messages".format(channelId=channelId), headers=headers,
        json=params)
    logger.debug("response: {code}".format(code=response.status_code))
    logger.debug("response: {message}".format(message=response.text))


def get_my_direct_messages(ck: str, cs: str, at: str, ats: str) -> list:
    logger.debug("get_my_direct_messages()")
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(at, ats)
    api = tweepy.API(auth)

    my_direct_messages = []

    my_user = api.me()
    direct_messages = api.list_direct_messages(count=200)
    for direct_message in direct_messages:
        if direct_message.type != "message_create":
            continue
        if direct_message.message_create.sender_id != my_user.id:
            continue
        if direct_message.message_create.target.recipient_id != my_user.id:
            continue

        my_direct_messages.append(direct_message)

    return my_direct_messages


def load_notified_ids() -> list:
    logger.debug("load_notified_ids()")
    notified_ids = []
    if os.path.exists("notified_ids.json"):
        with open("notified_ids.json", "r") as f:
            notified_ids = json.load(f)
    return notified_ids


def add_notified_id(notified_id):
    notified_ids = load_notified_ids()
    notified_ids.append(notified_id)
    save_notified_ids(notified_ids)


def save_notified_ids(notified_ids: list):
    logger.debug("save_notified_ids()")
    with open("notified_ids.json", "w") as f:
        f.write(json.dumps(notified_ids))
