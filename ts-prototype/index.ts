import TelegramBot from 'node-telegram-bot-api'
import { config } from './config'
import { Capability } from './capability/Capability'
import { createNotionCapability } from './capability/NotionCapability'
import { createQuestionCapability } from './capability/QuestionCapability'
import { fromTelegramBotMessage } from './Message'
import { createImageGenerationCapability } from './capability/ImageGenerationCapability'

const allowed = require('../data/allowed.json')

const bot = new TelegramBot(config.TELEGRAM_BOT_TOKEN, { polling: true })

const userAllowed = (user: TelegramBot.User | undefined): boolean => {
  if (!user) return false
  return allowed.includes(user.username)
}

const capabilities: Capability[] = [
  createQuestionCapability(createImageGenerationCapability()),
  // createNotionCapability(),
]

bot.onText(/\/start/, (msg: any) => {
  console.log('>>>', 'User started the bot')
  const chatId = msg.chat.id
  bot.sendMessage(chatId, 'Munnin flies again!')
})

bot.onText(/\/echo (.+)/, (msg: any, match: any) => {
  console.log('>>>', 'User sent a message', msg)
  const chatId = msg.chat.id
  const resp = match[1]
  bot.sendMessage(chatId, resp)
})

bot.on('message', async (msg: TelegramBot.Message) => {
  if (userAllowed(msg.from) === false) {
    console.warn('>>>', 'User is not Divan', msg)
    bot.sendMessage(msg.chat.id, 'You are not a friend, go away.')
    return
  }

  if (!msg.text) {
    bot.sendMessage(msg.chat.id, 'I can only accept text messages right now.')
    return
  }

  const message = fromTelegramBotMessage(msg)
  for (const command of capabilities) {
    if (await command.appliesTo(message)) {
      const response = await command.process(message)

      if (response.text) {
        bot.sendMessage(msg.chat.id, response.text)
      } else if (response.image) {
        bot.sendPhoto(msg.chat.id, response.image)
      } else {
        bot.sendMessage(msg.chat.id, '...')
      }
      return
    }
  }
})

console.log('>>', 'Bot started')
