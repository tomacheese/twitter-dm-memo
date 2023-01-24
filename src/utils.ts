import fs from 'node:fs'
import { TwitterApi } from 'twitter-api-v2'
import axios from 'axios'

export const PATH = {
  CONFIG_FILE: process.env.CONFIG_FILE || 'data/config.json',
  NOTIFIED_FILE: process.env.NOTIFIED_FILE || 'data/notified.json',
}

export interface Configuration {
  /** Twitter API keys */
  twitter: {
    /** Twitter API (v1) consumer key */
    consumer_key: string
    /** Twitter API (v1) consumer secret */
    consumer_secret: string
    /** Twitter API (v1) access token */
    access_token: string
    /** Twitter API (v1) access token secret */
    access_token_secret: string
  }
  /** Discord webhook URL or bot token */
  discord: {
    /** Discord webhook URL (required if using webhook) */
    webhook_url?: string
    /** Discord bot token (required if using bot) */
    token?: string
    /** Discord channel ID (required if using bot) */
    channel_id?: string
    /** Discord message prefix */
    prefix?: string
    /** Discord message suffix */
    suffix?: string
  }
}

export function loadConfig(): Configuration {
  return JSON.parse(fs.readFileSync(PATH.CONFIG_FILE, 'utf8'))
}

export function loadTwitterApi(config: Configuration): TwitterApi {
  return new TwitterApi({
    appKey: config.twitter.consumer_key,
    appSecret: config.twitter.consumer_secret,
    accessToken: config.twitter.access_token,
    accessSecret: config.twitter.access_token_secret,
  })
}

export async function sendDiscordMessage(
  config: Configuration,
  text: string
): Promise<void> {
  // webhook or bot
  if (config.discord.webhook_url) {
    // webhook
    const response = await axios.post(config.discord.webhook_url, {
      content: `${text}`,
    })
    if (response.status !== 204) {
      throw new Error(`Discord webhook failed (${response.status})`)
    }
    return
  }
  if (config.discord.token && config.discord.channel_id) {
    // bot
    const response = await axios.post(
      `https://discord.com/api/channels/${config.discord.channel_id}/messages`,
      {
        content: `${text}`,
      },
      {
        headers: {
          Authorization: `Bot ${config.discord.token}`,
        },
      }
    )
    if (response.status !== 200) {
      throw new Error(`Discord bot failed (${response.status})`)
    }
  }
}
