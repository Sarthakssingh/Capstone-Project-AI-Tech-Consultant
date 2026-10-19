# AI_LOG.md - Development Process

## Top 5 Prompts

1. "Design a multi-agent system in Python that can distinguish between built-in SaaS settings and custom code requirements based on a technical knowledge base API."
2. "Implement a TypeScript learning loop that tracks character-level diffs between AI drafts and human final replies to adjust the agent's confidence score."
3. "Create a polite sitemap scraper that respects robots.txt and implements an exponential backoff retry mechanism for the Brilliant Directories support site."
4. "Role-play a client-developer meeting where the client wants to build a custom 'Uber for X' search on top of Brilliant Directories, and extract the SOW."
5. "Write a FastAPI service that supports multimodal inputs to explain technical screenshots to non-technical users."

## AI Rejection Instance
**Instance**: Claude suggested using a simple string match for "same kind" of emails in Task 2.
**Reason for Rejection**: String matching is too brittle for varied customer phrasing.
**Action Taken**: I instead implemented a semantic clustering approach using the category labels and a similarity threshold to determine "kinds" of emails for the auto-pilot streak.
