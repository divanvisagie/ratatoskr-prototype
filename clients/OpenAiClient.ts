import nlp from 'compromise'
import { Configuration, ImagesResponseDataInner, OpenAIApi } from 'openai'

const appiKey = process.env.OPENAI_API_KEY || ''

const config = new Configuration({
  apiKey: appiKey,
})
const openAi = new OpenAIApi(config)

const model = 'text-davinci-003'

export const createOpenAiClient = () => {
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

  const generateImage = async (
    prompt: string
  ): Promise<ImagesResponseDataInner | undefined> => {
    const response = await openAi.createImage({
      prompt,
      n: 1,
    })

    const first = response.data.data[0]
    console.log('openai generateImage >', first)

    return first
  }

  return {
    getAnswer,
    generateImage,
  }
}

export type OpenAiClient = ReturnType<typeof createOpenAiClient>
