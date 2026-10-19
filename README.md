# AI Tech Consultant Capstone Project

This project implements an AI Tech Consultant system consisting of three integrated tasks:
1. **The Knowledge Brain**: A RAG-based memory system built from product help centers.
2. **The Inbox Agent**: An intelligent email assistant that learns from human feedback.
3. **Meeting to Scope of Work**: A multi-agent team that turns transcripts into SOWs, estimates, and proposals.

## How to Run

1. **Prerequisites**:
   - Python 3.10+
   - Node.js 18+
   - Anthropic API Key (set in `.env` file)

2. **Setup**:
   - Create a `.env` file in the root directory:
     ```env
     ANTHROPIC_API_KEY=your_key_here
     KNOWLEDGE_BRAIN_URL=http://localhost:8001
     ```
   - Install Python dependencies:
     ```bash
     pip install fastapi uvicorn httpx beautifulsoup4 pydantic anthropic python-dotenv
     ```
   - Install Node.js dependencies for Task 2:
     ```bash
     cd Task2_Inbox_Agent
     npm install
     cd ..
     ```

3. **Run All Services**:
   ```bash
   python run.py
   ```

## Services
- **Task 1 (Knowledge Brain)**: Port 8001
- **Task 2 (Inbox Agent)**: Port 8002
- **Task 3 (Meeting SOW)**: Port 8003
