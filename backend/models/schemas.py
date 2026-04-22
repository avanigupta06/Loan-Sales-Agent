"""Pydantic models for request/response schemas."""

from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class AgentType(str, Enum):
    MASTER = "master"
    SALES = "sales"
    VERIFICATION = "verification"
    UNDERWRITING = "underwriting"
    SANCTION = "sanction"


class ConversationStage(str, Enum):
    GREETING = "greeting"
    COLLECT_PHONE = "collect_phone"
    AUTH = "auth"                        # NEW: name/DOB verification
    SALES = "sales"
    VERIFICATION = "verification"
    UNDERWRITING = "underwriting"
    SALARY_UPLOAD = "salary_upload"
    SANCTION_CONFIRM = "sanction_confirm"  # NEW: ask user before generating PDF
    DECISION = "decision"
    COMPLETE = "complete"


class ChatRequest(BaseModel):
    session_id: str
    message: str
    phone: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    message: str
    stage: str
    agent: str
    requires_upload: bool = False
    loan_decision: Optional[str] = None  # "approved" | "rejected" | None
    pdf_ready: bool = False
    metadata: Optional[dict] = None


class UploadRequest(BaseModel):
    session_id: str


class ConversationState(BaseModel):
    session_id: str
    stage: ConversationStage = ConversationStage.GREETING
    phone: Optional[str] = None
    auth_verified: bool = False          # NEW: tracks if name/DOB matched
    auth_input: Optional[str] = None    # NEW: stores what user entered
    customer_data: Optional[dict] = None
    kyc_data: Optional[dict] = None
    credit_score: Optional[int] = None
    preapproved_limit: Optional[float] = None
    loan_amount: Optional[float] = None
    tenure_months: Optional[int] = None
    interest_rate: float = 12.5
    emi: Optional[float] = None
    salary: Optional[float] = None
    salary_slip_uploaded: bool = False
    decision: Optional[str] = None  # "approved" | "rejected"
    rejection_reason: Optional[str] = None
    messages: list = []
    attempts: dict = {}
