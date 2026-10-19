from fastapi import FastAPI, BackgroundTasks, HTTPException
from .models import KnowledgeQuery, KnowledgeResponse, Article
from .memory import KnowledgeMemory
from .scraper import PoliteScraper
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Knowledge Brain API")
memory = KnowledgeMemory()
scraper = PoliteScraper(base_url="https://support.brilliantdirectories.com")

@app.get("/")
async def root():
    return {"status": "online", "message": "Knowledge Brain API is running"}

@app.post("/ask", response_model=KnowledgeResponse)
async def ask_question(query: KnowledgeQuery):
    response = await memory.ask_question(query.question)
    return response

@app.post("/sync")
async def sync_knowledge(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_sync)
    return {"status": "started", "message": "Knowledge synchronization started in background"}

async def run_sync():
    sitemap_url = "https://support.brilliantdirectories.com/support/sitemap.xml"
    urls = await scraper.get_sitemap_urls(sitemap_url)

    for url in urls:
        if url not in scraper.visited_urls:
            art_data = await scraper.scrape_article(url)
            if art_data:
                article = Article(
                    url=art_data["url"],
                    title=art_data["title"],
                    content=art_data["content"],
                    images=art_data["images"]
                )
                memory.add_article(article)

    return {"status": "completed", "count": len(urls)}

@app.get("/stats")
async def get_stats():
    return {
        "article_count": len(memory.articles),
        "visited_urls": len(scraper.visited_urls)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
