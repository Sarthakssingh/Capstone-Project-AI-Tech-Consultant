from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import anthropic
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Meeting to SOW Agent")
client = anthropic.Anthropic()

KNOWLEDGE_BRAIN_URL = os.getenv("KNOWLEDGE_BRAIN_URL", "http://localhost:8001")

class MeetingTranscript(BaseModel):
    id: str
    content: str
    previous_sow_id: Optional[str] = None

class SOW(BaseModel):
    id: str
    scope_of_work: str
    task_list: List[dict]
    proposal: str
    changes_from_previous: Optional[str] = None

@app.post("/generate-sow", response_model=SOW)
async def generate_sow(meeting: MeetingTranscript):
    # 1. Analyze transcript with AI Senior Consultant
    # 2. Check technical feasibility via Task 1 API
    # 3. Generate structured SOW

    # Simple Technical Check
    tech_guidance = ""
    try:
        async with httpx.AsyncClient() as http_client:
            resp = await http_client.post(f"{KNOWLEDGE_BRAIN_URL}/ask", json={
                "question": f"Based on this meeting transcript, what existing product settings can be used: {meeting.content[:500]}"
            })
            if resp.status_code == 200:
                tech_guidance = resp.json().get("answer", "")
    except Exception as e:
        print(f"KB API Error: {e}")

    prompt = f"""You are a Team of AI Agents (Senior Consultant, Architect, Estimator).
Analyze the following meeting transcript and produce:
1. A Scope of Work (SOW)
2. A list of tasks with estimated hours
3. A professional proposal

Technical Guidance from Knowledge Brain:
{tech_guidance}

Transcript:
{meeting.content}

Return the result in structured format.
"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # In a real app, use structured output (Tool Calling / JSON mode)
        # Here we mock the parsing for brevity
        result_text = message.content[0].text

        return SOW(
            id=f"sow_{meeting.id}",
            scope_of_work=result_text,
            task_list=[{"task": "Implementation", "hours": 10}],
            proposal="Professional Proposal Based on Meeting"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
