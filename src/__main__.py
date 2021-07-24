from src import config, init_logger, get_my_direct_messages, load_notified_ids, send_discord_message, add_notified_id

logger = init_logger()


def main():
    notified_ids = load_notified_ids()
    isFirst = len(notified_ids) == 0

    direct_messages = get_my_direct_messages(config.TWITTER_CONSUMER_KEY,
                                             config.TWITTER_CONSUMER_SECRET,
                                             config.TWITTER_ACCESS_TOKEN,
                                             config.TWITTER_ACCESS_TOKEN_SECRET)

    for direct_message in direct_messages:
        if direct_message.id in notified_ids:
            continue

        message_data = direct_message.message_create.message_data
        text = message_data.text
        entities_urls = message_data.entities_urls

        for entities_url in entities_urls:
            text = str(text).replace(entities_url.url, entities_urls.expanded_url)

        text = config.SEND_PREFIX + text + config.SEND_SUFFIX

        if not isFirst:
            send_discord_message(config.DISCORD_TOKEN, config.DISCORD_CHANNEL_ID, text)

        add_notified_id(direct_message.id)


if __name__ == "__main__":
    main()
