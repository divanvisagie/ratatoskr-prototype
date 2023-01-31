import { Message } from '../Message'
import { createNotionService } from '../services/NotionService'
import { Capability } from './Capability'

export const createNotionCapability = (): Capability => {
  const notionService = createNotionService()
  return {
    appliesTo: async (_inputMessage: Message) => Promise.resolve(true),

    process(inputMessage) {
      notionService.addEntryToTodaysPage(inputMessage.text)

      return Promise.resolve({
        text: 'I shall save this Hávi',
      })
    },
  }
}
export type NotionCapability = ReturnType<typeof createNotionCapability>
