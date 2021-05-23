from dotenv import load_dotenv
import os
from src import init_logger

logger = init_logger("Config")

load_dotenv(override=True)


def getKey(key: str, default_value=None):
    value = os.getenv(key)
    if default_value is None and value is None:
        logger.critical("{} is not defined.".format(key))
        exit(1)
    return value


DISCORD_TOKEN = getKey("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = getKey("DISCORD_CHANNEL_ID")
TWITTER_CONSUMER_KEY = getKey("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = getKey("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = getKey("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = getKey("TWITTER_ACCESS_TOKEN_SECRET")
SEND_PREFIX = getKey("SEND_PREFIX", "")
SEND_SUFFIX = getKey("SEND_SUFFIX", "")
