import {
  DirectMessageCreateV1,
  EDirectMessageEventTypeV1,
  TwitterApi,
} from 'twitter-api-v2'
import { Notified } from './notified'
import { loadConfig, loadTwitterApi, PATH, sendDiscordMessage } from './utils'

async function getNotifiableDirectMessages(
  twitterApi: TwitterApi,
  notified: Notified,
): Promise<DirectMessageCreateV1[]> {
  const me = await twitterApi.v1.verifyCredentials()

  const events = await twitterApi.v1.listDmEvents({ count: 200 })

  return events.events.filter((event) => {
    return (
      // メッセージ送信イベント
      event.type === EDirectMessageEventTypeV1.Create &&
      // 自分が送信したメッセージ
      event[EDirectMessageEventTypeV1.Create].sender_id === me.id_str &&
      // 自分宛てのメッセージ
      event[EDirectMessageEventTypeV1.Create].target.recipient_id ===
        me.id_str &&
      // 既に通知済みのメッセージではない
      !notified.isNotified(event.id)
    )
  })
}

async function main() {
  const notified = new Notified(PATH.NOTIFIED_FILE)
  const isFirst = notified.isFirst()
  const config = loadConfig()
  const twitterApi = loadTwitterApi(config)
  const events = await getNotifiableDirectMessages(twitterApi, notified)

  if (events.length === 0) {
    console.log('❌ No new direct messages.')
    notified.save()
    return
  }

  console.log('✅ New direct messages found.')
  for (const event of events) {
    const directMessage = event[EDirectMessageEventTypeV1.Create]
    const messageData = directMessage.message_data
    let text = messageData.text
    if (messageData.entities.urls) {
      for (const url of messageData.entities.urls) {
        text = text.replaceAll(url.url, url.expanded_url)
      }
    }

    const sendText =
      (config.discord.prefix ?? '') + text + (config.discord.suffix ?? '')

    if (!isFirst) {
      await sendDiscordMessage(config, sendText)
    }

    notified.add(event.id)
  }

  notified.save()
}

;(async () => {
  await main()
})()
