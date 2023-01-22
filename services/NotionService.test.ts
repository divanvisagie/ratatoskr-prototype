import { createNotionService } from './NotionService'

describe('NotionService', () => {
  it("should get today's page", async () => {
    const notionService = createNotionService()
    const response = await notionService.getTodaysPage()
    expect(response).toBe({})
  })

  it('should add journal entry', async () => {
    const notionService = createNotionService()
    const response = await notionService.createPageForToday(['muninn_test'])
    expect(response).toBeDefined()
  })

  it('should add entry to todays page', async () => {
    const notionService = createNotionService()
    const response = await notionService.addEntryToTodaysPage(
      'This block was added by a test'
    )
    expect(response).toBe({})
  })
})
