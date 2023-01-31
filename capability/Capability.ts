import { Message } from '../Message'

// type AppliesToAsync = (inputMessage: Message) => Promise<boolean>
// type AppliesToSync = (inputMessage: Message) => boolean

export interface Capability {
  appliesTo: (inputMessage: Message) => Promise<boolean>
  process: (inputMessage: Message) => Promise<Response>
}

export type Response = {
  text?: string
  image?: Buffer
}
