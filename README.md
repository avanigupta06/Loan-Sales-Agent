# 🏦 Loan Sales Agentic AI System

A production-ready, full-stack AI-powered loan sales chatbot system inspired by Tata Capital NBFC. Built with **FastAPI** (backend) and **React** (frontend), featuring a Master Agent that orchestrates multiple specialized Worker Agents.

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
   ┌────┼──────────────────┐
   ▼    ▼                  ▼
Sales  Verification   Underwriting   Sanction Letter
Agent    Agent           Agent          Generator
  │        │                │               │
Loan    Mock CRM      Credit Bureau     reportlab PDF
Params   (KYC)        + Offer Mart
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
loan-chatbot/
├── backend/
│   ├── main.py                   # FastAPI app, all routes
│   ├── requirements.txt
│   ├── agents/
│   │   ├── master_agent.py       # Orchestrator
│   │   ├── sales_agent.py        # Loan requirements collection
│   │   ├── verification_agent.py # KYC validation
│   │   ├── underwriting_agent.py # Business logic + EMI
│   │   └── sanction_agent.py     # PDF generator (reportlab)
│   ├── models/
│   │   └── schemas.py            # Pydantic models
│   ├── services/
│   │   └── mock_data.py          # Mock CRM / Credit Bureau / Offer Mart
│   └── utils/
│       ├── finance.py            # EMI formula, currency formatting
│       └── session_store.py      # In-memory session management
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx               # Main app, state management
        ├── index.css             # Global styles + CSS variables
        ├── utils/
        │   ├── api.js            # API service layer
        │   └── markdown.js       # Simple markdown renderer
        └── components/
            ├── Header.jsx        # Top bar with stage indicator
            ├── Sidebar.jsx       # Demo customers + loan status
            ├── MessageBubble.jsx # Chat bubbles with agent labels
            ├── TypingIndicator.jsx
            ├── ChatInput.jsx     # Auto-resize textarea
            ├── FileUpload.jsx    # Drag & drop salary slip uploader
            └── DecisionBanner.jsx # Approval/rejection + PDF download
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

## 👥 Demo Customers (10 profiles)

| Phone | Name | City | Score | Limit | Expected Flow |
|---|---|---|---|---|---|
| 9876543210 | Arjun Sharma | Mumbai | 762 | ₹5L | Direct Approve |
| 9123456780 | Priya Nair | Bangalore | 810 | ₹10L | Direct Approve |
| 9988776655 | Rohit Verma | Delhi | 645 | ₹3L | Reject (low score) |
| 9871234560 | Sneha Patel | Ahmedabad | 720 | ₹2L | Salary check needed |
| 9765432100 | Karan Mehta | Pune | 835 | ₹20L | VIP — direct approve |
| 9654321009 | Divya Iyer | Chennai | 698 | ₹4L | Reject (score < 700) |
| 9543210098 | Amit Joshi | Hyderabad | 790 | ₹30L | Premium — direct approve |
| 9432100987 | Meera Reddy | Kolkata | 580 | ₹1.5L | Reject (very low score) |
| 9321009876 | Vikram Singh | Jaipur | 745 | ₹7L | Salary verification |
| 9210098765 | Ananya Krishnan | Kochi | 710 | ₹3.5L | Depends on loan amount |

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend Setup

```bash
cd loan-chatbot/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
# OR
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs at: **http://localhost:8000**
API docs at: **http://localhost:8000/docs**

### Frontend Setup

```bash
cd loan-chatbot/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:3000**



---

## 🔄 Full Conversation Flow

```
User opens app
     │
     ▼
Master Agent → Greeting + ask phone number
     │
User enters phone
     │
     ▼
Master Agent → Lookup customer in mock CRM
     │
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
                  ├── Approved → Generate PDF
                  ├── Rejected → Show reason
                  └── Needs salary → Upload prompt
                           │
                    User uploads file
                           │
                    Re-evaluate with EMI check
                    ├── EMI ≤ 50% salary → Approve + PDF
                    └── EMI > 50% salary → Reject
```

---

## ⭐ Bonus Features Implemented

- ✅ Human-like sales conversation with persuasion
- ✅ Smart amount/tenure parsing (e.g., "5 lakh", "3 years")
- ✅ Detailed PDF sanction letter with reportlab
- ✅ Typing animation for realism
- ✅ Agent-labeled message bubbles
- ✅ Drag-and-drop file upload
- ✅ Sidebar with all demo customers + clickable phone numbers
- ✅ Real-time stage tracking in header
- ✅ Edge case handling (missing KYC, low score, over-limit)
- ✅ Mock API endpoints for CRM, Credit Bureau, Offer Mart

---


