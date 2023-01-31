import { Message } from '../Message'
import { createAiService } from '../services/AiService'
import { Capability } from './Capability'

export const createImageGenerationCapability = (): Capability => {
  const aiService = createAiService()
  return {
    appliesTo: async (inputMessage: Message) => {
      const applies = aiService.isImageQuestion(inputMessage.text)
      return Promise.resolve(applies)
    },
    process: async (inputMessage: Message) => {
      return {
        image: await aiService.getImage(inputMessage.text),
      }
    },
  }
}
export type ImageGenerationCapability = ReturnType<
  typeof createImageGenerationCapability
>
