import { Request, Response } from 'express'
import { NotionService } from '../../../services/NotionService'

const createPostHandler =
  (notionService: NotionService) => async (req: Request, res: Response) => {
    const { title, body } = req.body
    const response = await notionService.createPageForToday(title, body)
    res.json(response)
  }
