import nlp from 'compromise'
import { Message } from '../Message'
import { createAiService } from '../services/AiService'
import { Capability, Response } from './Capability'

type QAPair = {
  question: string
  answer: string
}

function buildContext(context: QAPair[]): string {
  let contextString = ''
  for (const qa of context) {
    contextString += `Question: ${qa.question}\nAnswer: ${qa.answer}\n`
  }
  return contextString
}

const BUFFER_SIZE = 100

export const createQuestionCapability = (
  ...capabilities: Capability[]
): Capability => {
  const aiService = createAiService()

  let context: QAPair[] = []

  return {
    appliesTo: async (inputMessage: Message) => {
      return Promise.resolve(true)
      // if (!inputMessage.text) return false
      // const questions = nlp(inputMessage.text)
      //   .sentences()
      //   .isQuestion()
      //   .out('array')
      // return Promise.resolve(questions.length > 0)
    },

    process: async (inputMessage: Message): Promise<Response> => {
      for (const capability of capabilities) {
        if (await capability.appliesTo(inputMessage)) {
          return capability.process(inputMessage)
        }
      }
      let inputText = inputMessage.text
      if (context.length > 0) {
        const bc = buildContext(context)
        const contextString = `Given the context: ${bc}\n\n${inputMessage.text}`
        inputText = `${contextString}\n${inputText}`
      }
      console.log('Asking OpenAI >', inputText)

      try {
        const answer = await aiService.getAnswer(inputText)

        if (context.length >= BUFFER_SIZE) {
          context = []
        } else {
          context.push({
            question: inputMessage.text,
            answer: answer || 'No answer',
          })
        }

        return {
          text: answer,
        }
      } catch (error) {
        console.error(error)
        return {
          text: "Something seems to have gone wrong. I'm sorry.",
        }
      }
    },
  }
}
export type QuestionCapability = ReturnType<typeof createQuestionCapability>
