"""FastAPI main application — Tata Capital AI Loan Chatbot backend."""

import os
import sys
import uuid

# Ensure local packages are importable
sys.path.insert(0, os.path.dirname(__file__))

# Load .env file if present (for local development)
try:
    _env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(_env_path):
        with open(_env_path) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _, _v = _line.partition("=")
                    if _v.strip() and not os.environ.get(_k.strip()):
                        os.environ[_k.strip()] = _v.strip()
except Exception:
    pass


from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from models.schemas import ChatRequest, ChatResponse, ConversationStage
from agents.master_agent import MasterAgent
from utils.session_store import get_session, save_session

app = FastAPI(
    title="Tata Capital Loan Chatbot API",
    description="Agentic AI-based loan sales chatbot system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

master_agent = MasterAgent()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ── Health check ─────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Tata Capital Loan Chatbot"}


# ── Chat endpoint ─────────────────────────────────────────────────────────────

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chatbot endpoint. Manages session and routes to master agent."""
    session_id = request.session_id
    user_message = request.message.strip()

    state = get_session(session_id)

    # Append user message to history
    state.messages.append({"role": "user", "content": user_message})

    # Process through master agent
    response = master_agent.process(state, user_message)

    # Append assistant message to history
    state.messages.append({"role": "assistant", "content": response.message})

    save_session(state)
    return response


# ── New session endpoint ──────────────────────────────────────────────────────

@app.post("/session/new")
async def new_session():
    """Create a new session and return the greeting."""
    session_id = str(uuid.uuid4())
    state = get_session(session_id)

    response = master_agent.process(state, "")
    state.messages.append({"role": "assistant", "content": response.message})
    save_session(state)

    return {**response.dict(), "session_id": session_id}


# ── Salary slip upload ────────────────────────────────────────────────────────

@app.post("/upload", response_model=ChatResponse)
async def upload_salary_slip(
    session_id: str = Form(...),
    file: UploadFile = File(...),
):
    """Receive salary slip and trigger underwriting re-evaluation."""
    state = get_session(session_id)

    if state.stage != ConversationStage.SALARY_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail="Upload not expected at this stage.",
        )

    # Save uploaded file
    allowed_types = {"application/pdf", "image/jpeg", "image/png", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF or image files are accepted.",
        )

    safe_name = f"{session_id[:8]}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, safe_name)
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    # Process through master agent salary upload handler
    response = master_agent.process_salary_upload(state)
    state.messages.append({"role": "assistant", "content": response.message})
    save_session(state)

    return response


# ── PDF download ──────────────────────────────────────────────────────────────

@app.get("/generate-pdf/{session_id}")
async def get_sanction_letter(session_id: str):
    """Return the generated PDF sanction letter."""
    filename = f"sanction_letter_{session_id[:8]}.pdf"
    filepath = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(filepath):
        # Try to regenerate
        state = get_session(session_id)
        if state.decision != "approved":
            raise HTTPException(status_code=404, detail="No approved loan found for this session.")
        try:
            from agents.sanction_agent import generate_sanction_letter
            filepath = generate_sanction_letter(state, UPLOAD_DIR)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename="Tata_Capital_Sanction_Letter.pdf",
    )


# ── Mock API endpoints (CRM, Credit Bureau, Offer Mart) ──────────────────────

@app.get("/mock/crm/{phone}")
async def mock_crm(phone: str):
    """Mock CRM API — returns KYC data."""
    from services.mock_data import get_kyc_data
    data = get_kyc_data(phone)
    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return data


@app.get("/mock/credit-bureau/{phone}")
async def mock_credit_bureau(phone: str):
    """Mock Credit Bureau API — returns credit score."""
    from services.mock_data import get_credit_score
    data = get_credit_score(phone)
    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return data


@app.get("/mock/offer-mart/{phone}")
async def mock_offer_mart(phone: str):
    """Mock Offer Mart API — returns pre-approved loan offer."""
    from services.mock_data import get_preapproved_offer
    data = get_preapproved_offer(phone)
    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return data


@app.get("/mock/customers")
async def mock_customers():
    """Returns list of all demo customers (for testing)."""
    from services.mock_data import CUSTOMERS
    return [
        {"phone": p, "name": c["name"], "city": c["city"],
         "credit_score": c["credit_score"], "preapproved_limit": c["preapproved_limit"]}
        for p, c in CUSTOMERS.items()
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# ── Mini Finance Chatbot ──────────────────────────────────────────────────────

from pydantic import BaseModel as _BaseModel
from typing import List as _List

class MiniChatMessage(_BaseModel):
    role: str        # "user" | "assistant"
    content: str

class MiniChatRequest(_BaseModel):
    query: str
    history: _List[MiniChatMessage] = []

class MiniChatResponse(_BaseModel):
    answer: str
    source: str      # "groq" | "fallback"

@app.post("/mini-chat", response_model=MiniChatResponse)
async def mini_chat(request: MiniChatRequest):
    """Mini Finance Chatbot — answers EMI, loan rules, finance FAQs."""
    from services.mini_chat_service import get_mini_chat_response

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    history = [{"role": m.role, "content": m.content} for m in request.history]
    result = get_mini_chat_response(request.query.strip(), history)
    return MiniChatResponse(**result)
