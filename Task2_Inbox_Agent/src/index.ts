import express, { Request, Response } from 'express';
import axios from 'axios';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';

dotenv.config();

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 8002;
const KNOWLEDGE_BRAIN_URL = process.env.KNOWLEDGE_BRAIN_URL || 'http://localhost:8001';

interface Email {
  id: string;
  sender: string;
  subject: string;
  body: string;
  category: string;
  receivedAt: string;
  status: 'pending' | 'drafted' | 'sent' | 'edited';
  draft?: string;
  finalReply?: string;
}

interface LearningState {
  categoryStreaks: Record<string, number>;
  autoPilotCategories: string[];
}

let emails: Email[] = [];
let learningState: LearningState = {
  categoryStreaks: {},
  autoPilotCategories: []
};

// Load initial emails
const emailsPath = path.join(__dirname, 'emails.json');
if (fs.existsSync(emailsPath)) {
  emails = JSON.parse(fs.readFileSync(emailsPath, 'utf-8'));
}

@app.get('/emails', (req: Request, res: Response) => {
  res.json(emails);
});

@app.post('/emails/:id/draft', async (req: Request, res: Response) => {
  const email = emails.find(e => e.id === req.params.id);
  if (!email) return res.status(404).send('Email not found');

  try {
    const kbResponse = await axios.post(`${KNOWLEDGE_BRAIN_URL}/ask`, {
      question: email.body
    });

    const draft = `Hello,\n\nThank you for reaching out. Based on your inquiry: "${email.body}", here is what I found:\n\n${kbResponse.data.answer}\n\nBest regards,\nAI Tech Consultant Team`;

    email.draft = draft;
    email.status = 'drafted';
    res.json({ draft, sources: kbResponse.data.sources });
  } catch (error) {
    console.error('Error drafting reply:', error);
    res.status(500).send('Error connecting to Knowledge Brain');
  }
});

@app.post('/emails/:id/send', (req: Request, res: Response) => {
  const email = emails.find(e => e.id === req.params.id);
  if (!email) return res.status(404).send('Email not found');

  const { reply, edited } = req.body;
  email.finalReply = reply;
  email.status = edited ? 'edited' : 'sent';

  // Learning logic
  const cat = email.category;
  if (!edited) {
    learningState.categoryStreaks[cat] = (learningState.categoryStreaks[cat] || 0) + 1;
    if (learningState.categoryStreaks[cat] >= 20 && !learningState.autoPilotCategories.includes(cat)) {
      learningState.autoPilotCategories.push(cat);
    }
  } else {
    learningState.categoryStreaks[cat] = 0;
    learningState.autoPilotCategories = learningState.autoPilotCategories.filter(c => c !== cat);
  }

  res.json({ status: 'success', autoPilot: learningState.autoPilotCategories.includes(cat) });
});

@app.get('/autopilot', (req: Request, res: Response) => {
  res.json(learningState);
});

app.listen(PORT, () => {
  console.log(`Inbox Agent running on port ${PORT}`);
});
