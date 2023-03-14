import os
import sys

import logging

from clients import notion_service_client

logger = logging.getLogger(__name__)

def cleanup_test_pages():
    """Clean up any pages that were created by this test"""
    pages = notion_service_client.get_todays_pages()

    for page in pages:
        tags = page['properties']['Tags']['multi_select']
        for tag in tags:
            logger.info(f"Found tag: {tag['name']}")
            if "unit_test" == tag['name']:
                notion_service_client.delete_page(page['id'])

def test_create_new_page_in_journal():
    """When a new page is created, it should come back with an id"""
    new_page = notion_service_client.create_new_page_for_today(["unit_test"])
    logger.info(f"Created page: {new_page}")
    cleanup_test_pages()
    assert new_page is not None
    assert new_page['id'] is not None

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
