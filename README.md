# Founder Reality-Check Agent

A lightweight agentic system built as a **capstone project** for the **Google x Kaggle Agentic AI** course.

This tool helps founders stop hand-waving startup ideas and instead forces:
- a clear, concrete target user,
- one executable distribution channel,
- a structured, testable hypothesis,
- and small, real-world validation experiments.

**Goal:** less storytelling, more proof.

---

## ✨ Key Features

- ✅ Enforces a **concrete target user**  
- ✅ Forces **exactly one primary distribution channel**  
- ✅ Generates a **testable hypothesis** with metric + timeframe  
- ✅ Tracks **idea versions across sessions**  
- ✅ Flags **silent pivots** in user, problem, or distribution  
- ✅ Suggests **minimal validation experiments**

---

## 🧠 Tech Stack

**Backend**
- Python 3.11 (recommended)
- FastAPI
- SQLite
- Gemini API (for live reasoning)

**Frontend**
- React + TypeScript
- Vite
- Tailwind CSS

---

## 🚀 Quick Start (Local)

1. Clone the Repository
git clone https://github.com/<your-username>/founder_reality-check.git
cd founder_reality-check

2. Set Up Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Backend runs at:
http://localhost:8000

3. Set Up Frontend
cd frontend
npm install
npm run dev
Frontend runs at:
http://localhost:5173


🔑 Environment Setup
Create a file named .env inside the backend/ folder:

GEMINI_API_KEY=your_api_key_here

FOUNDER_AGENT_MODE=real

For offline testing:
FOUNDER_AGENT_MODE=mock


🧪 How It Works

Enter a startup idea.

The system:

Extracts structured information,

Validates target user and distribution,

Enforces a structured hypothesis,

Detects drift between versions,

Generates real-world validation experiments.

You receive a clear Reality-Check Report.

📌 Status

This is v0 and actively evolving.
Built primarily as a learning project, structured to scale into a real product.

🙌 Acknowledgement

Inspired by the Google x Kaggle Agentic AI course.