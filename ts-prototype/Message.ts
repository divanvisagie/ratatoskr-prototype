import TelegramBot from 'node-telegram-bot-api'

export type Message = {
  text: string
}

export const fromTelegramBotMessage = (msg: TelegramBot.Message): Message => {
  return {
    text: msg.text ?? '',
  }
}
