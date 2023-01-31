import TelegramBot from 'node-telegram-bot-api'
import { createNotionService } from './services/NotionService'
import { createAiService } from './services/AiService'
import { config } from './config'

const bot = new TelegramBot(config.TELEGRAM_BOT_TOKEN, { polling: true })

const notionService = createNotionService()
const aiService = createAiService()

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
  if (msg.from?.username !== 'DivanVisagie') {
    console.warn('>>>', 'User is not Divan', msg)
    bot.sendMessage(msg.chat.id, 'You are not Divan, go away.')
    return
  }

  if (!msg.text) {
    bot.sendMessage(msg.chat.id, 'I can only accept text messages right now.')
    return
  }

  if (aiService.isQuestion(msg.text)) {
    if (aiService.isImageQuestion(msg.text)) {
      const image = await aiService.getImage(msg.text)

      if (image) {
        bot.sendPhoto(msg.chat.id, image)
        return
      } else {
        bot.sendMessage(msg.chat.id, 'I can not draw that.')
      }
      return
    }

    const answer = await aiService.getAnswer(msg.text)
    bot.sendMessage(
      msg.chat.id,
      answer || 'could not find an anwer from OpenAI'
    )
    return
  }

  console.log('>>>', 'sent a message', msg)

  const chatId = msg.chat.id

  try {
    const response = await notionService.addEntryToTodaysPage(msg.text || '')
  } catch (error) {
    bot.sendMessage(
      chatId,
      'I failed to save this Hávi, your fears are justified'
    )
  }

  bot.sendMessage(chatId, 'I shall save this Hávi')
})
