import httpx
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import asyncio
from typing import List, Dict, Optional
import os
import json
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoliteScraper:
    def __init__(self, base_url: str, delay: float = 1.0, state_file: str = "scraper_state.json"):
        self.base_url = base_url
        self.delay = delay
        self.state_file = state_file
        self.visited_urls = set()
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    self.visited_urls = set(data.get("visited", []))
            except Exception as e:
                logger.error(f"Error loading state: {e}")

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump({"visited": list(self.visited_urls)}, f)

    async def get_sitemap_urls(self, sitemap_url: str) -> List[str]:
        urls = []
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                resp = await client.get(sitemap_url)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.content)
                    # Support standard sitemap namespace
                    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                    for url in root.findall('.//ns:url', namespaces):
                        loc = url.find('ns:loc', namespaces)
                        if loc is not None and loc.text:
                            urls.append(loc.text.strip())
                    # If empty, try without namespaces
                    if not urls:
                        for loc in root.findall('.//loc'):
                            if loc.text:
                                urls.append(loc.text.strip())
        except Exception as e:
            logger.error(f"Failed to fetch/parse sitemap: {e}")
        return urls

    async def scrape_article(self, url: str) -> Optional[Dict]:
        if url in self.visited_urls:
            return None

        await asyncio.sleep(self.delay) # Polite delay

        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    return None

                soup = BeautifulSoup(resp.text, 'html.parser')

                # Title
                title = soup.title.string if soup.title else ""
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text(strip=True)

                # Content - adjust selectors based on typical support sites
                content_div = soup.find('article') or soup.find('div', class_='article-body') or soup.find('main')
                if not content_div:
                    content_div = soup.body

                # Images
                images = []
                if content_div:
                    for img in content_div.find_all('img'):
                        src = img.get('src')
                        if src:
                            if not src.startswith('http'):
                                src = f"{urlparse(url).scheme}://{urlparse(url).netloc}/{src.lstrip('/')}"
                            images.append(src)

                text_content = content_div.get_text(separator='\n', strip=True) if content_div else ""

                self.visited_urls.add(url)
                self.save_state()

                return {
                    "url": url,
                    "title": title,
                    "content": text_content,
                    "images": images
                }
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
