import nlp from 'compromise'
import { createOpenAiClient } from '../clients/OpenAiClient'
import axios from 'axios'

const openAiClient = createOpenAiClient()

export const createAiService = () => {
  const isQuestion = (text: string): boolean => {
    const questions = nlp(text).sentences().isQuestion().out('array')
    return questions.length > 0
  }

  const isImageQuestion = (text: string) => {
    console.log('isImageQuestion >', text)
    const doc = nlp(text)

    const verbMatch = doc.verbs().match('#Verb').out('array')
    const nounMatch = doc.nouns().match('#Noun').out('array')
    doc.verbs()
    console.log('verbMatch >', verbMatch)
    console.log('nounMatch >', nounMatch)

    return (
      verbMatch.includes('draw') ||
      (nounMatch.includes('picture') && verbMatch.includes('show'))
    )
  }

  const getAnswer = async (question: string) => {
    return openAiClient.getAnswer(question)
  }

  const getImage = async (question: string): Promise<Buffer | undefined> => {
    const img = await openAiClient.generateImage(question)

    if (img?.url) {
      let response = await axios.get(img.url, {
        responseType: 'arraybuffer',
      })
      let buf = Buffer.from(response.data, 'binary')
      return buf
    }
  }

  return {
    getAnswer,
    getImage,
    isImageQuestion,
    isQuestion,
  }
}

export type AiService = ReturnType<typeof createAiService>
