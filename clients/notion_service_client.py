import logging
import os
from typing import List, Optional
import datetime

from notion_client import Client

from log_factory.logger import create_logger

database_id = os.environ.get('NOTION_JOURNAL_DB')
notion = Client(auth=os.environ.get('NOTION_TOKEN'))

logger = create_logger(__name__)

def get_day_of_week() -> str:
    dow =  datetime.datetime.now().strftime('%A')
    logger.info(f'Today is {dow}')
    return dow

def get_time() -> str:
    return datetime.datetime.now().strftime('%H:%M')

def delete_page(page_id: str):
    children = notion.blocks.children.list(block_id=page_id).get("results")
    for child in children:
        notion.blocks.delete(block_id=child["id"])
    response = notion.blocks.delete(block_id=page_id)
    return response

def get_todays_pages() -> List[dict]:
    """Returns a list of pages for today in the user's chosen journal database"""
    try:
        response = notion.databases.query(
            database_id=database_id,
            filter={
                'property': 'Date',
                'date': {
                    'on_or_after': datetime.datetime.now().strftime('%Y-%m-%d')
                }
            },
            sorts=[
                {
                    'property': 'Date',
                    'direction': 'descending'
                }
            ]
        )
        logger.info(f"Found {len(response)} pages for today")
        return response['results']
    except Exception as error:
        logger.error('Failed to get page for today', error)
        return []

def get_todays_existing_page() -> Optional[dict]:
    """Returns the page for today if it exists, otherwise returns None"""
    try:
       response = get_todays_pages()
       answer = response[0]
       return answer
    except Exception as error:
        logger.error('Failed to get page for today', error)
        return None

def create_new_page_for_today(extra_tags: List[str]):
    """Creates a new page for today in the user's chosen journal database"""
    try:
        new_page = {
            "Date": {
                "date": {
                    "start": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "end": None,
                    "time_zone": None,
                }
            },
            "Tags": {
                "multi_select": [
                    {"name": "Muninn"},
                    *[{"name": tag} for tag in extra_tags],
                ]
            },
            "title": {
                "title": [
                    {
                        "text": {
                            "content": get_day_of_week()
                        }
                    }
                ]
            }
        }

        response = notion.pages.create(
            parent={"database_id": database_id}, properties=new_page
        )
        return response
    except Exception as error:
        logger.error("Failed to create page for today", error)
        print(error)

def add_entry_to_todays_page(text: str) -> str:
    time = datetime.datetime.now().strftime("%H:%M")
    notion = Client(auth=os.environ.get("NOTION_TOKEN"))

    todays_page = get_todays_existing_page()
    page_id = None
    if todays_page is None:
        res = create_new_page_for_today([])
        page_id = res['id']
    else:
        logger.info(f"Found page for today {todays_page}")
        page_id = todays_page['id']

    if page_id is None:
        raise Exception("Could not find or create page for today")

    new_content = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": f"From muninn at: {time}"
                        },
                        "annotations": 
                            {
                                "bold": True
                            }
                        
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [
                    {
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }
    ]
  
    page  = notion.blocks.retrieve(page_id)
    logger.info(f"page before {page}")

    notion.blocks.children.append(block_id=page_id, children=new_content)

    return todays_page['url']
