"""Master Agent — orchestrates the full loan sales conversation flow.

Changes v2:
  - Rebranded: "Loan Sale Agentic AI System" / "Digital Sales Assistant"
  - Added AUTH stage: verifies phone + name/DOB before proceeding
  - Added SANCTION_CONFIRM stage: asks user consent before PDF generation
  - Removed demo-number hints from error messages
  - More human-like conversation transitions
"""

import re
from models.schemas import ConversationState, ConversationStage, ChatResponse
from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent, UnderwritingDecision
from agents.sanction_agent import generate_sanction_letter
from services.mock_data import get_customer_by_phone
from utils.finance import format_currency

PHONE_RE = re.compile(r"(?<!\d)(\d{10})(?!\d)")

# ── Auth helpers ──────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def _check_auth(customer: dict, user_input: str) -> bool:
    """Returns True if user_input matches name OR date-of-birth/age."""
    inp = _normalize(user_input)
    full_name = _normalize(customer.get("name", ""))
    first_name = full_name.split()[0] if full_name else ""
    if inp == full_name or inp == first_name or inp in full_name:
        return True
    age = str(customer.get("age", ""))
    dob = customer.get("dob", "")
    inp_digits = re.sub(r"\D", "", inp)
    if age and (inp == age or inp_digits == age):
        return True
    if dob:
        dob_digits = re.sub(r"\D", "", dob)
        if inp_digits == dob_digits:
            return True
    return False


class MasterAgent:
    """Brain of the system."""

    def __init__(self):
        self.sales_agent = SalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()

    def process(self, state: ConversationState, user_message: str) -> ChatResponse:
        stage = state.stage

        if stage == ConversationStage.GREETING:
            return self._handle_greeting(state)
        if stage == ConversationStage.COLLECT_PHONE:
            return self._handle_phone_collection(state, user_message)
        if stage == ConversationStage.AUTH:
            return self._handle_auth(state, user_message)
        if stage == ConversationStage.SALES:
            return self._handle_sales(state, user_message)
        if stage == ConversationStage.VERIFICATION:
            return self._handle_verification(state)
        if stage == ConversationStage.UNDERWRITING:
            return self._handle_underwriting(state)
        if stage == ConversationStage.SALARY_UPLOAD:
            return self._handle_salary_upload_prompt(state)
        if stage == ConversationStage.SANCTION_CONFIRM:
            return self._handle_sanction_confirm(state, user_message)
        if stage == ConversationStage.DECISION:
            return self._ask_sanction_consent(state)
        if stage == ConversationStage.COMPLETE:
            return self._handle_complete(state)

        return self._error_response(state, "I seem to have lost track. Please refresh to start fresh.")

    # ── Handlers ──────────────────────────────────────────────────────────────

    def _handle_greeting(self, state: ConversationState) -> ChatResponse:
        state.stage = ConversationStage.COLLECT_PHONE
        msg = (
            "👋 **Welcome to the Loan Sale Agentic AI System!**\n\n"
            "I'm your **Digital Sales Assistant**, here to guide you through a seamless, "
            "100% digital personal loan journey.\n\n"
            "To get started, please share your **10-digit registered mobile number**. 📱"
        )
        return ChatResponse(session_id=state.session_id, message=msg,
                            stage=state.stage, agent="master")

    def _handle_phone_collection(self, state: ConversationState, user_message: str) -> ChatResponse:
        phone_match = PHONE_RE.search(user_message.strip())
        if not phone_match:
            return ChatResponse(
                session_id=state.session_id,
                message="I didn't catch that. Please enter your **10-digit registered mobile number**.",
                stage=state.stage, agent="master",
            )

        phone = phone_match.group(1)
        customer = get_customer_by_phone(phone)

        if not customer:
            attempts = state.attempts.get("phone", 0) + 1
            state.attempts["phone"] = attempts
            if attempts >= 3:
                state.stage = ConversationStage.COMPLETE
                return ChatResponse(
                    session_id=state.session_id,
                    message=(
                        "Unable to locate your account after multiple attempts. 😔\n\n"
                        "Please contact support at **1800-267-6060**. Thank you!"
                    ),
                    stage=state.stage, agent="master",
                )
            return ChatResponse(
                session_id=state.session_id,
                message=(
                    f"I couldn't find any account linked to **{phone}**. 🔍\n\n"
                    "Please verify the number and try again."
                ),
                stage=state.stage, agent="master",
            )

        state.phone = phone
        state.customer_data = customer
        state.stage = ConversationStage.AUTH
        return ChatResponse(
            session_id=state.session_id,
            message=(
                f"I found an account for **{phone}**. 🔐\n\n"
                "For your security, I need to verify your identity.\n\n"
                "Please enter your **full name** or **date of birth (DD/MM/YYYY)** "
                "as registered with us."
            ),
            stage=state.stage, agent="master",
        )

    def _handle_auth(self, state: ConversationState, user_message: str) -> ChatResponse:
        customer = state.customer_data
        attempts = state.attempts.get("auth", 0)

        if _check_auth(customer, user_message):
            state.auth_verified = True
            state.stage = ConversationStage.SALES
            greeting = self.sales_agent.greet(customer["name"])
            return ChatResponse(session_id=state.session_id, message=greeting,
                                stage=state.stage, agent="sales")

        state.attempts["auth"] = attempts + 1
        if attempts + 1 >= 3:
            state.stage = ConversationStage.COMPLETE
            return ChatResponse(
                session_id=state.session_id,
                message=(
                    "🔒 **Identity Verification Failed**\n\n"
                    "We could not verify your identity after 3 attempts. "
                    "This session has been blocked for security.\n\n"
                    "Please call **1800-267-6060** for assistance."
                ),
                stage=state.stage, agent="master", loan_decision="rejected",
            )

        remaining = 3 - (attempts + 1)
        return ChatResponse(
            session_id=state.session_id,
            message=(
                f"⚠️ That doesn't match our records. Please try again.\n\n"
                f"Enter your **full name** or **date of birth** (DD/MM/YYYY). "
                f"**{remaining} attempt{'s' if remaining > 1 else ''}** remaining."
            ),
            stage=state.stage, agent="master",
        )

    def _handle_sales(self, state: ConversationState, user_message: str) -> ChatResponse:
        response_text, is_complete = self.sales_agent.process(state, user_message)
        if is_complete:
            state.stage = ConversationStage.VERIFICATION
            return self._handle_verification(state, prefix=response_text + "\n\n")
        return ChatResponse(session_id=state.session_id, message=response_text,
                            stage=state.stage, agent="sales")

    def _handle_verification(self, state: ConversationState, prefix: str = "") -> ChatResponse:
        is_verified, message = self.verification_agent.verify(state)
        if not is_verified:
            state.stage = ConversationStage.COMPLETE
            return ChatResponse(
                session_id=state.session_id,
                message=prefix + message,
                stage=state.stage, agent="verification", loan_decision="rejected",
            )
        state.stage = ConversationStage.UNDERWRITING
        return self._handle_underwriting(state, prefix=prefix + message + "\n\n")

    def _handle_underwriting(self, state: ConversationState, prefix: str = "") -> ChatResponse:
        decision, message = self.underwriting_agent.evaluate(state)

        if decision == UnderwritingDecision.APPROVED:
            state.stage = ConversationStage.SANCTION_CONFIRM
            name = state.kyc_data.get("name", "there") if state.kyc_data else "there"
            consent_msg = (
                f"{prefix}{message}\n\n"
                "---\n"
                f"🎉 **Excellent news, {name}! You're eligible for this loan.**\n\n"
                "Great choice! Let me quickly summarise — everything checks out perfectly. ✅\n\n"
                "Would you like to **proceed with the loan sanction** and generate "
                "your official Sanction Letter?\n\n"
                "👉 Reply **Yes** to proceed · **No** to decline for now"
            )
            return ChatResponse(
                session_id=state.session_id,
                message=consent_msg,
                stage=state.stage, agent="underwriting",
            )

        elif decision == UnderwritingDecision.REJECTED:
            state.stage = ConversationStage.COMPLETE
            return ChatResponse(
                session_id=state.session_id,
                message=prefix + message,
                stage=state.stage, agent="underwriting", loan_decision="rejected",
            )

        else:  # NEEDS_SALARY
            state.stage = ConversationStage.SALARY_UPLOAD
            return ChatResponse(
                session_id=state.session_id,
                message=prefix + message,
                stage=state.stage, agent="underwriting", requires_upload=True,
            )

    def _handle_salary_upload_prompt(self, state: ConversationState) -> ChatResponse:
        return ChatResponse(
            session_id=state.session_id,
            message=(
                "⏳ **Waiting for your salary slip...**\n\n"
                "Please use the 📎 **Upload** button below to attach your latest salary slip "
                "(PDF or image). This helps us complete your income verification!"
            ),
            stage=state.stage, agent="underwriting", requires_upload=True,
        )

    def process_salary_upload(self, state: ConversationState) -> ChatResponse:
        state.salary_slip_uploaded = True
        salary = state.customer_data.get("salary") if state.customer_data else None
        if salary:
            state.salary = salary

        decision, message = self.underwriting_agent.evaluate_with_salary(state)

        if decision == UnderwritingDecision.APPROVED:
            state.stage = ConversationStage.SANCTION_CONFIRM
            name = state.kyc_data.get("name", "there") if state.kyc_data else "there"
            consent_msg = (
                f"{message}\n\n"
                "---\n"
                f"🎉 **You're eligible for this loan, {name}!**\n\n"
                "Would you like to **proceed with the loan sanction**?\n\n"
                "👉 Reply **Yes** to generate your Sanction Letter · **No** to decline"
            )
            return ChatResponse(
                session_id=state.session_id, message=consent_msg,
                stage=state.stage, agent="underwriting",
            )
        else:
            state.stage = ConversationStage.COMPLETE
            return ChatResponse(
                session_id=state.session_id, message=message,
                stage=state.stage, agent="underwriting", loan_decision="rejected",
            )

    def _handle_sanction_confirm(self, state: ConversationState, user_message: str) -> ChatResponse:
        msg = user_message.strip().lower()
        positive = any(w in msg for w in [
            "yes", "y", "yeah", "yep", "sure", "ok", "okay",
            "proceed", "go ahead", "confirm", "generate", "continue", "haan", "ha"
        ])
        negative = any(w in msg for w in [
            "no", "n", "nope", "nahi", "not now", "decline",
            "cancel", "later", "think", "skip", "maybe later"
        ])

        if positive:
            return self._generate_sanction(state)

        if negative:
            state.stage = ConversationStage.COMPLETE
            name = state.kyc_data.get("name", "there") if state.kyc_data else "there"
            return ChatResponse(
                session_id=state.session_id,
                message=(
                    f"Understood, {name}! No problem at all. 😊\n\n"
                    "Your loan offer is **valid for 30 days**. Whenever you're ready, "
                    "start a new session and we'll pick right up.\n\n"
                    "Thank you for using the **Loan Sale Agentic AI System**. Have a wonderful day! 🙏"
                ),
                stage=state.stage, agent="master",
            )

        return ChatResponse(
            session_id=state.session_id,
            message=(
                "I didn't quite catch that. 😊\n\n"
                "Please reply **Yes** to proceed with sanction, or **No** to decline for now."
            ),
            stage=state.stage, agent="master",
        )

    def _generate_sanction(self, state: ConversationState) -> ChatResponse:
        try:
            pdf_path = generate_sanction_letter(state)
            state.stage = ConversationStage.COMPLETE
            name = state.kyc_data.get("name", "there") if state.kyc_data else "there"
            return ChatResponse(
                session_id=state.session_id,
                message=(
                    f"🎊 **Congratulations, {name}! Your Loan has been Sanctioned!**\n\n"
                    f"📄 Your official **Sanction Letter is ready for download.**\n\n"
                    f"Click the **Download Sanction Letter** button below. Our relationship manager "
                    f"will contact you within **24 hours** to complete disbursement.\n\n"
                    f"Thank you for choosing the **Loan Sale Agentic AI System**! 🙏"
                ),
                stage=state.stage, agent="sanction",
                loan_decision="approved", pdf_ready=True,
                metadata={"pdf_path": pdf_path},
            )
        except Exception as e:
            state.stage = ConversationStage.COMPLETE
            return ChatResponse(
                session_id=state.session_id,
                message=(
                    "✅ **Loan Sanctioned Successfully!** 🎉\n\n"
                    "There was a minor issue generating the PDF. "
                    "Our team will email your Sanction Letter within 2 hours.\n\n"
                    f"*(Note: {str(e)})*"
                ),
                stage=state.stage, agent="sanction",
                loan_decision="approved", pdf_ready=False,
            )

    def _ask_sanction_consent(self, state: ConversationState) -> ChatResponse:
        state.stage = ConversationStage.SANCTION_CONFIRM
        return ChatResponse(
            session_id=state.session_id,
            message=(
                "✅ **Your loan has been approved!** 🎉\n\n"
                "Would you like to proceed with the sanction and generate your official letter?\n\n"
                "👉 Reply **Yes** to proceed · **No** to decline"
            ),
            stage=state.stage, agent="underwriting",
        )

    def _handle_complete(self, state: ConversationState) -> ChatResponse:
        if state.decision == "approved":
            msg = "Your loan application is complete! 🎉 Download your Sanction Letter above or start a **New Chat**."
        else:
            msg = "Your session has ended. Thank you for using the **Loan Sale Agentic AI System**. Call **1800-267-6060** for help."
        return ChatResponse(
            session_id=state.session_id, message=msg,
            stage=state.stage, agent="master",
            loan_decision=state.decision,
            pdf_ready=(state.decision == "approved"),
        )

    def _error_response(self, state: ConversationState, message: str) -> ChatResponse:
        return ChatResponse(session_id=state.session_id, message=message,
                            stage=state.stage, agent="master")
