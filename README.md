# 🤖 Loan Sale Agentic AI System

A production-ready, full-stack AI-powered loan sales chatbot system. Built with **FastAPI** (backend) and **React** (frontend), featuring a Master Agent that orchestrates multiple specialized Worker Agents — plus a floating **Mini Finance Chatbot** powered by Gemini / Groq AI.

---

## 🏗️ Architecture Overview

```
User Browser (React)
        │
        ▼
   FastAPI Backend
        │
   Master Agent  ◄─── Orchestrator (routes messages, maintains state)
        │
   ┌────┼──────────────────┬──────────────────┐
   ▼    ▼                  ▼                  ▼
Sales  Verification   Underwriting        Sanction Letter
Agent    Agent           Agent              Generator
  │        │                │                   │
Loan    Mock CRM      Credit Bureau          reportlab PDF
Params   (KYC)        + Offer Mart
                                    ┌──────────────────────┐
                                    │  Mini Finance         │
                                    │  Chatbot (FAB)        │
                                    │  Groq →      │
                                    │  Built-in Rules       │
                                    └──────────────────────┘
```

### Agent Responsibilities

| Agent | Role |
|---|---|
| **Master Agent** | Controls flow, maintains state, routes to workers |
| **Sales Agent** | Collects loan amount & tenure conversationally |
| **Verification Agent** | Fetches & validates KYC from mock CRM |
| **Underwriting Agent** | Applies credit rules, EMI calculation |
| **Sanction Agent** | Generates PDF sanction letter |

---

## 📂 Project Structure

```
loan-sales-agent/
├── backend/
│   ├── main.py                     # FastAPI app — all routes including /mini-chat
│   ├── requirements.txt
│   ├── agents/
│   │   ├── master_agent.py         # Orchestrator
│   │   ├── sales_agent.py          # Loan requirements collection
│   │   ├── verification_agent.py   # KYC validation
│   │   ├── underwriting_agent.py   # Business logic + EMI
│   │   └── sanction_agent.py       # PDF generator (reportlab)
│   ├── models/
│   │   └── schemas.py              # Pydantic models + ConversationStage enum
│   ├── services/
│   │   ├── mock_data.py            # Mock CRM / Credit Bureau / Offer Mart
│   │   └── mini_chat_service.py    # ★ Groq + fallback AI service
│   └── utils/
│       ├── finance.py              # EMI formula, currency formatting
│       └── session_store.py        # In-memory session management
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx                 # Main app — Fragment wraps loan chat + FAB
        ├── index.css               # Global styles + header CSS classes
        ├── utils/
        │   ├── api.js              # API service layer
        │   ├── markdown.js         # Bold/italic/list markdown renderer
        │   └── miniFaqs.js         # ★ 7 quick-tap FAQ suggestions
        └── components/
            ├── Header.jsx          # Redesigned — grid layout + progress dots
            ├── Sidebar.jsx         # Loan journey steps + underwriting legend
            ├── MessageBubble.jsx   # Chat bubbles with agent labels
            ├── TypingIndicator.jsx # Animated 3-dot typing effect
            ├── ChatInput.jsx       # Auto-resize textarea + send button
            ├── FileUpload.jsx      # Drag & drop salary slip uploader
            ├── DecisionBanner.jsx  # Approval 🎉 / Rejection ❌ + PDF download
            └── MiniChatbot.jsx     # ★ Floating Finance Assistant chatbot
```

---

## 🧠 Business Logic (Underwriting Rules)

```
1. Credit Score < 700         → REJECT (low credit)
2. Loan ≤ Pre-approved Limit  → APPROVE directly
3. Loan ≤ 2× Pre-approved     → Request salary slip
                                 EMI = P×r×(1+r)^n / ((1+r)^n - 1)
                                 If EMI ≤ 50% salary → APPROVE
                                 Else                → REJECT
4. Loan > 2× Pre-approved     → REJECT (exceeds max)
```

---

## 💬 Mini Finance Chatbot (NEW)

A floating AI-powered help assistant — completely separate from the main loan flow. Accessible via the **blue chat bubble** at the bottom-right corner of the screen.

### What it can answer

| Topic | Example Query |
|---|---|
| EMI explanation | "What is EMI and how does it work?" |
| Loan approval rules | "How is a loan approved in this system?" |
| Interest rate | "Explain interest rate in simple terms" |
| EMI formula | "How do you calculate EMI? Show the formula" |
| Rejection reasons | "Why was my loan rejected?" |
| Credit score | "What is a CIBIL score and why does it matter?" |
| Tenure vs EMI | "How does tenure affect my EMI?" |

### AI Provider Hierarchy

The system tries providers in this order — only **one key needed**:

```
1. Groq llama3-8b-8192      →  Free tier: 14,400 req/day
2. Built-in rule-based       →  Zero API key needed — always works
```


### Setup (takes 2 minutes)

** Groq:**
1. Go to [console.groq.com](https://console.groq.com) → Sign up free → Create API key
2. Open `backend/.env` and add:
```
GROQ_API_KEY=your_key_here
```

> ℹ️ If neither key is set, the built-in rule-based fallback handles the 7 most common finance questions automatically — no configuration needed.

---


## 🔄 Full Conversation Flow

```
User opens app
     │
     ▼
Master Agent → Greeting + ask phone number
     │
User enters 10-digit phone
     │
     ▼
Auth Check → Enter name OR date of birth
     │ (3 attempts max — wrong = blocked)
     ▼
Sales Agent → "How much loan do you need?" → collect amount
           → "What tenure?" → collect tenure
     │
     ▼
Verification Agent → Fetch KYC → Validate phone + address
     │
     ▼
Underwriting Agent → Fetch credit score + offer
                  → Apply business rules
                  ├── Rejected → Show reason + suggestions
                  ├── Needs salary → Upload salary slip prompt
                  │        │
                  │   User uploads file
                  │        │
                  │   EMI ≤ 50% salary → Eligible
                  │   EMI > 50% salary → Rejected
                  │
                  └── Eligible → Ask: "Proceed with sanction?" ← NEW
                           │
                    User replies YES → Generate PDF + Download
                    User replies NO  → End politely, offer valid 30 days
```

---

## 👥 Demo Customers (10 profiles)

| Phone | Name | City | Auth (name/age) | Score | Limit | Expected Flow |
|---|---|---|---|---|---|---|
| 9876543210 | Arjun Sharma | Mumbai | "Arjun" / "34" | 762 | ₹5L | Direct Approve |
| 9123456780 | Priya Nair | Bangalore | "Priya" / "29" | 810 | ₹10L | Direct Approve |
| 9988776655 | Rohit Verma | Delhi | "Rohit" / "41" | 645 | ₹3L | Reject (low score) |
| 9871234560 | Sneha Patel | Ahmedabad | "Sneha" / "27" | 720 | ₹2L | Salary check |
| 9765432100 | Karan Mehta | Pune | "Karan" / "38" | 835 | ₹20L | VIP Approve |
| 9654321009 | Divya Iyer | Chennai | "Divya" / "32" | 698 | ₹4L | Reject (score < 700) |
| 9321009876 | Vikram Singh | Jaipur | "Vikram" / "36" | 745 | ₹7L | Salary verification |
| 9210098765 | Ananya Krishnan | Kochi | "Ananya" / "31" | 710 | ₹3.5L | Depends on amount |

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend Setup

```bash
cd loan-sales-agent/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

Edit .env → GROQ_API_KEY

# Start the server
python main.py
# OR
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs at: **http://localhost:8000**
Swagger API docs: **http://localhost:8000/docs**

### Frontend Setup

```bash
cd loan-sales-agent/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:3000**

---

## ⭐ Features

### Core Loan Flow
- ✅ Multi-agent orchestration (Master → Sales → KYC → Underwriting → Sanction)
- ✅ Phone + Name/DOB two-factor identity verification
- ✅ Human-like conversational sales with persuasion
- ✅ Smart amount/tenure parsing (`"5 lakh"`, `"3 years"`, `"₹300000"`)
- ✅ EMI formula: `P×r×(1+r)^n / ((1+r)^n - 1)`
- ✅ Salary slip upload with drag-and-drop (PDF/JPG/PNG)
- ✅ User consent gate before PDF generation
- ✅ Professional PDF sanction letter via reportlab

### UI / Frontend
- ✅ Redesigned header — CSS Grid layout + 8-step progress dots
- ✅ Real-time stage indicator (colour-coded per agent)
- ✅ Agent-labelled message bubbles
- ✅ Animated typing indicator
- ✅ Loan journey sidebar with underwriting rules
- ✅ Approval 🎉 / Rejection ❌ decision banner + PDF download

### Mini Finance Chatbot ★ NEW
- ✅ Floating chat bubble (bottom-right, clears main input bar)
- ✅ Slide-up panel with smooth open/close animation
- ✅ 4 one-tap FAQ chips for instant answers
- ✅ Conversation history passed with every request
- ✅ Gemini → Groq → Built-in rules fallback chain
- ✅ Typing indicator while AI responds
- ✅ Clear chat button
- ✅ Works with zero API keys (built-in rule engine)

---
