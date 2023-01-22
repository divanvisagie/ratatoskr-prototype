import nlp from 'compromise'
import { Configuration, OpenAIApi } from 'openai'

const appiKey = process.env.OPENAI_API_KEY || ''

const config = new Configuration({
  apiKey: appiKey,
})
const openAi = new OpenAIApi(config)

const model = 'text-davinci-003'

export const createOpenAiService = () => {
  const isQuestion = (text: string) => {
    const questions = nlp(text).sentences().isQuestion().out('array')
    if (questions.length > 0) {
      return true
    } else {
      return false
    }
  }

  const getAnswer = async (question: string) => {
    const response = await openAi.createCompletion({
      prompt: `${question}`,
      model,
      temperature: 0.5,
      max_tokens: 250,
      n: 1,
      stop: '.',
    })

    const choices = response.data.choices

    for (const choice of choices) {
      console.log('choice >', choice.text)
    }

    if (choices.length > 0) {
      return choices[0].text
    }
  }
  return {
    getAnswer,
    isQuestion,
  }
}

export type OpenAiService = ReturnType<typeof createOpenAiService>
