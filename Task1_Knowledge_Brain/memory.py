import os
import json
import logging
from typing import List, Dict, Optional
from .models import Article, KnowledgeResponse
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

class KnowledgeMemory:
    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        self.articles_file = os.path.join(storage_dir, "articles.json")
        self.articles: Dict[str, Article] = {}
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.articles_file):
            try:
                with open(self.articles_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for url, art_data in data.items():
                        self.articles[url] = Article(**art_data)
            except Exception as e:
                logging.error(f"Error loading memory: {e}")

    def save_memory(self):
        with open(self.articles_file, "w", encoding="utf-8") as f:
            json.dump({url: art.model_dump(mode='json') for url, art in self.articles.items()}, f, indent=2)

    def add_article(self, article: Article):
        self.articles[article.url] = article
        self.save_memory()

    def remove_article(self, url: str):
        if url in self.articles:
            del self.articles[url]
            self.save_memory()

    def search(self, query: str, limit: int = 5) -> List[Article]:
        # Simple keyword search for now
        # In a real app, use a Vector DB like Chroma or Qdrant
        results = []
        query_words = query.lower().split()

        for art in self.articles.values():
            score = 0
            text = (art.title + " " + art.content).lower()
            for word in query_words:
                if word in text:
                    score += 1
            if score > 0:
                results.append((score, art))

        results.sort(key=lambda x: x[0], reverse=True)
        return [art for score, art in results[:limit]]

    async def ask_question(self, question: str) -> KnowledgeResponse:
        relevant_articles = self.search(question)

        if not relevant_articles:
            return KnowledgeResponse(
                answer="I'm sorry, I couldn't find any information about that in the help center.",
                sources=[],
                confidence=0.0,
                needs_human=True
            )

        context = ""
        for i, art in enumerate(relevant_articles):
            context += f"Source {i+1} ({art.url}):\nTitle: {art.title}\n{art.content[:2000]}\n\n"

        prompt = f"""You are an AI Tech Consultant for Brilliant Directories.
Use the following context from the official help center to answer the user's question.
If the answer is not in the context, say honestly that you don't know and it will be escalated to a human.

Context:
{context}

Question: {question}

Provide a clear, helpful answer. At the end, list the sources (URLs) used.
If you are unsure or the answer is incomplete, suggest escalating to a human expert.
"""

        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Simple parsing for response
            answer_text = message.content[0].text
            sources = [art.url for art in relevant_articles]

            # Simple logic to detect if human needed
            needs_human = "escalate to a human" in answer_text.lower() or "don't know" in answer_text.lower()

            return KnowledgeResponse(
                answer=answer_text,
                sources=sources,
                confidence=0.9 if not needs_human else 0.4,
                needs_human=needs_human
            )
        except Exception as e:
            logging.error(f"Error calling Claude: {e}")
            return KnowledgeResponse(
                answer="Error processing your request.",
                sources=[],
                confidence=0.0,
                needs_human=True
            )
