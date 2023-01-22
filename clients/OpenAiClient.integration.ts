import { createOpenAiClient } from './OpenAiClient'

describe('OpenAiClient', () => {
  it('should return an answer', async () => {
    const { getAnswer } = createOpenAiClient()
    const answer = await getAnswer('What is the meaning of life?')
    expect(answer).toBeDefined()
  })

  it('should return an image', async () => {
    const { generateImage } = createOpenAiClient()
    const answer = await generateImage('A dog is running')
    expect(answer).toBeDefined()
  })
})
