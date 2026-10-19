from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime

class Article(BaseModel):
    url: str
    title: str
    content: str
    category: Optional[str] = None
    folder: Optional[str] = None
    images: List[str] = []
    last_updated: datetime = datetime.now()

class KnowledgeQuery(BaseModel):
    question: str
    session_id: Optional[str] = None

class KnowledgeResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    needs_human: bool = False

class SitemapItem(BaseModel):
    loc: str
    lastmod: Optional[str] = None
