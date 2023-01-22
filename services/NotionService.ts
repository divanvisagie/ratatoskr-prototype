import { Client } from '@notionhq/client'
import {
  CreatePageResponse,
  PartialPageObjectResponse,
} from '@notionhq/client/build/src/api-endpoints'

function getDayOfWeek(): string {
  const date = new Date()
  const dayOfWeek = date.getDay()
  return isNaN(dayOfWeek)
    ? 'Journal Entry'
    : [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
      ][dayOfWeek]
}

export const createNotionService = () => {
  const databaseId = process.env.NOTION_JOURNAL_DB || ''

  const notion = new Client({ auth: process.env.NOTION_TOKEN })

  const getTodaysPage = async (): Promise<
    PartialPageObjectResponse | undefined
  > => {
    try {
      const response = await notion.databases.query({
        database_id: databaseId,
        filter: {
          property: 'Date',
          date: {
            on_or_after: new Date().toISOString().split('T')[0],
          },
        },
        sorts: [
          {
            property: 'Date',
            direction: 'descending',
          },
        ],
      })
      if (response.results.length > 0) {
        return response.results[0]
      } else {
        return undefined
      }
    } catch (error) {
      console.error(error)
    }
  }

  const createPageForToday = async (
    extra_tags: string[]
  ): Promise<CreatePageResponse | undefined> => {
    try {
      const response = await notion.pages.create({
        parent: { database_id: databaseId },
        properties: {
          Date: {
            date: {
              start: new Date().toISOString().split('T')[0],
              end: null,
              time_zone: null,
            },
          },
          Tags: {
            multi_select: [
              { name: 'Muninn' },
              ...extra_tags.map((tag) => ({ name: tag })),
            ],
          },
          title: {
            title: [
              {
                text: {
                  content: getDayOfWeek(),
                },
              },
            ],
          },
        },
      })

      return response
    } catch (error) {
      console.error(error)
    }
  }
  return {
    createPageForToday,
    getTodaysPage,
    async addEntryToTodaysPage(text: string) {
      const time = new Date().toLocaleString('en-se', {
        hour: '2-digit',
        minute: '2-digit',
      })

      let pageId: string | undefined = undefined
      const todaysPage = await getTodaysPage()
      if (todaysPage === undefined) {
        const res = await createPageForToday([])
        pageId = res?.id ?? undefined
      } else {
        pageId = todaysPage.id
      }

      if (pageId === undefined) {
        throw new Error('Could not find or create page for today')
      }

      const response = await notion.blocks.children.append({
        block_id: pageId,
        children: [
          {
            object: 'block',
            type: 'paragraph',
            paragraph: {
              rich_text: [
                {
                  text: { content: `From muninn at: ${time}` },
                  annotations: { bold: true },
                },
              ],
            },
          },
          {
            object: 'block',
            type: 'quote',
            quote: { rich_text: [{ text: { content: text } }] },
          },
        ],
      })

      return response
    },
  }
}
export type NotionService = ReturnType<typeof createNotionService>
