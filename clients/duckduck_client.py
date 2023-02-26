import logging
import requests
from urllib.parse import quote
from duckduckgo_search import ddg  

logger = logging.getLogger(__name__)

def sentence_to_query(sentence: str) -> str:
    """Convert a sentence to a query for DuckDuckGo."""
    return quote(f'{sentence}')

def result_to_markdown(result: dict) -> str:   
    """Convert a DuckDuckGo result to markdown."""
    try:
        title = result['title']
        body = result['body']
        href = result['href']

        md_header = f"**[{title}]({href})**"
        md_body = f"{body}"
        return f"{md_header}\n{md_body}"
    except Exception as e:
        logger.error(f"Error converting result to markdown: {e}")
        return None

class DuckDuckGoClient():
    
    def search(self,search_query: str) -> str:
        """Get answer from DuckDuckGo for a query."""
        try:
            keywords = search_query
            results = ddg(keywords, region='wt-wt', safesearch='On', time='y')
            #logger.info(f"Got answer from DuckDuckGo: {results}")

            count = 0
            result_message = ""
            for result in results:
                try:
                    logger.info(f'title: {result["title"]}')
                    logger.info(f'body: {result["body"]}')
                    logger.info(f'href: {result["href"]}')
                    md = result_to_markdown(result)
                    if md is not None:
                        count += 1
                        if count > 1:
                            break
                        result_message += md + '\n\n'    
                
                except Exception as e:
                    logger.error(f"Error appending answer: {e}")
                    continue

            return result_message
        except Exception as e:
            logger.error(f"Error getting answer from DuckDuckGo: {e}")
            return 'Could not get an answer from DuckDuckGo.'

