export const config: Config = {
  TELEGRAM_BOT_TOKEN: process.env.TELEGRAM_BOT_TOKEN || '',
  OPENAI_API_KEY: process.env.OPENAI_API_KEY || '',
  NOTION_JOURNAL_DB: process.env.NOTION_JOURNAL_DB || '',
}

export type Config = {
  TELEGRAM_BOT_TOKEN: string
  OPENAI_API_KEY: string
  NOTION_JOURNAL_DB: string
}
