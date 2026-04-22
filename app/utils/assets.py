import httpx
import logging

logger = logging.getLogger(__name__)

async def fetch_text_asset(url: str) -> str:
    """
    Fetches raw text content from an asset URL.
    In the future, add PDF parsing or HTML stripping here.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            
            # TODO: If response.headers['content-type'] is PDF, use PyMuPDF
            # TODO: If HTML, use BeautifulSoup to strip tags
            
            # Ensure we don't return massive binaries
            text = response.text
            if len(text) > 50000:
                logger.warning(f"Truncating massive asset from {url}")
                return text[:50000]
                
            return text
    except Exception as e:
        logger.error(f"Error fetching asset from {url}: {str(e)}")
        return f"Error fetching {url}: {str(e)}"
