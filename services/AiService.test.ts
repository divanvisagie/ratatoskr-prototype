import { createAiService } from './AiService'

describe('AiService', () => {
  it('should return true for a question', () => {
    const { isQuestion } = createAiService()
    const question = 'What is the meaning of life?'
    const answer = isQuestion(question)
    expect(answer).toBe(true)
  })

  it('should return false for a statement', () => {
    const { isQuestion } = createAiService()
    const statement = 'The meaning of life is 42.'
    const answer = isQuestion(statement)
    expect(answer).toBe(false)
  })

  it('should return true for a question where I ask it to draw', () => {
    const { isImageQuestion } = createAiService()
    const question = 'could you draw a picture of a dog running up a mountain?'
    const answer = isImageQuestion(question)
    expect(answer).toBe(true)
  })

  it('should return false for a non-image question', () => {
    const { isImageQuestion } = createAiService()
    const question = 'What is the meaning of life?'
    const answer = isImageQuestion(question)
    expect(answer).toBe(false)
  })

  it('should return true for a question where i ask for an image', () => {
    const { isImageQuestion } = createAiService()
    const question = 'could you show me a picture of norway?'
    const answer = isImageQuestion(question)
    expect(answer).toBe(true)
  })
})
