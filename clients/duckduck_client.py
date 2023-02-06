import logging
import requests
from urllib.parse import quote
from duckduckgo_search import ddg  

logger = logging.getLogger(__name__)

def sentence_to_query(sentence: str) -> str:
    """Convert a sentence to a query for DuckDuckGo."""
    return quote(f'{sentence}')

class DuckDuckGoClient():
    
    def get_duckduckgo_answer(self,question: str) -> str:
        """Get answer from DuckDuckGo for a query."""
        try:
            keywords = question
            results = ddg(keywords, region='wt-wt', safesearch='Off', time='y')
            logger.info(f"Got answer from DuckDuckGo: {results}")
            for result in results:
                logger.info(f'title: {result["title"]}')
                logger.info(f'body: {result["body"]}')
                logger.info(f'href: {result["href"]}')
                return result["href"]
        except Exception as e:
            logger.error(f"Error getting answer from DuckDuckGo: {e}")
            return None

