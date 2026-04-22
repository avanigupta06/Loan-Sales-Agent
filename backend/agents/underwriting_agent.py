"""Underwriting Agent — applies credit and loan eligibility rules."""

from models.schemas import ConversationState
from services.mock_data import get_credit_score, get_preapproved_offer, get_salary
from utils.finance import calculate_emi, format_currency


class UnderwritingDecision:
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_SALARY = "needs_salary"


class UnderwritingAgent:
    """
    Business Rules:
    1. credit_score < 700  → Reject
    2. loan_amount ≤ preapproved_limit → Approve directly
    3. loan_amount ≤ 2× preapproved_limit:
        → Request salary slip
        → Calculate EMI
        → Approve if EMI ≤ 50% of salary
    4. loan_amount > 2× preapproved_limit → Reject
    """

    def evaluate(self, state: ConversationState) -> tuple[str, str]:
        """
        Returns (decision: UnderwritingDecision, message).
        """
        phone = state.phone

        # Fetch credit score
        credit_data = get_credit_score(phone)
        if not credit_data:
            return UnderwritingDecision.REJECTED, self._no_data_message()

        credit_score = credit_data["credit_score"]
        state.credit_score = credit_score

        # Fetch pre-approved offer
        offer_data = get_preapproved_offer(phone)
        preapproved_limit = offer_data["preapproved_limit"] if offer_data else 0
        interest_rate = offer_data.get("interest_rate", 12.5) if offer_data else 12.5
        state.preapproved_limit = preapproved_limit
        state.interest_rate = interest_rate

        loan_amount = state.loan_amount
        tenure = state.tenure_months

        # Rule 1: Credit score check
        if credit_score < 700:
            state.decision = UnderwritingDecision.REJECTED
            state.rejection_reason = "low_credit_score"
            return UnderwritingDecision.REJECTED, self._low_credit_message(credit_score)

        # Rule 4: Loan > 2× preapproved limit
        if loan_amount > 2 * preapproved_limit:
            state.decision = UnderwritingDecision.REJECTED
            state.rejection_reason = "exceeds_max_limit"
            return UnderwritingDecision.REJECTED, self._exceeds_limit_message(
                loan_amount, preapproved_limit
            )

        # Rule 2: Loan ≤ preapproved limit → Direct approval
        if loan_amount <= preapproved_limit:
            emi = calculate_emi(loan_amount, interest_rate, tenure)
            state.emi = emi
            state.decision = UnderwritingDecision.APPROVED
            return UnderwritingDecision.APPROVED, self._direct_approval_message(
                state, credit_score, emi
            )

        # Rule 3: Loan ≤ 2× preapproved limit → Need salary slip
        return UnderwritingDecision.NEEDS_SALARY, self._salary_required_message(
            loan_amount, preapproved_limit, credit_score
        )

    def evaluate_with_salary(self, state: ConversationState) -> tuple[str, str]:
        """Evaluate after salary slip is uploaded."""
        salary = state.salary or get_salary(state.phone) or 0
        state.salary = salary

        loan_amount = state.loan_amount
        tenure = state.tenure_months
        interest_rate = state.interest_rate

        emi = calculate_emi(loan_amount, interest_rate, tenure)
        state.emi = emi

        # EMI ≤ 50% of monthly salary
        if emi <= 0.5 * salary:
            state.decision = UnderwritingDecision.APPROVED
            return UnderwritingDecision.APPROVED, self._salary_approval_message(state, emi, salary)
        else:
            state.decision = UnderwritingDecision.REJECTED
            state.rejection_reason = "emi_exceeds_50_percent"
            return UnderwritingDecision.REJECTED, self._emi_rejection_message(emi, salary)

    # ── Message templates ──────────────────────────────────────────────────────

    def _low_credit_message(self, score: int) -> str:
        return (
            f"📊 **Credit Assessment Complete**\n\n"
            f"Your CIBIL Score: **{score}**\n\n"
            f"😔 I'm really sorry, but we're unable to process your loan application at this time. "
            f"Your current credit score of **{score}** is below our minimum threshold of **700**.\n\n"
            f"**What you can do:**\n"
            f"• Pay off existing EMIs and credit card dues on time\n"
            f"• Reduce your credit utilization below 30%\n"
            f"• Avoid multiple loan inquiries in a short period\n"
            f"• Check your CIBIL report for any errors\n\n"
            f"You can reapply once your score improves. We'd love to help you then! 💙"
        )

    def _exceeds_limit_message(self, loan: float, limit: float) -> str:
        max_eligible = format_currency(2 * limit)
        requested = format_currency(loan)
        return (
            f"📊 **Loan Eligibility Assessment**\n\n"
            f"Requested Amount: **{requested}**\n"
            f"Maximum Eligible Amount: **{max_eligible}**\n\n"
            f"😔 Unfortunately, the loan amount you've requested exceeds the maximum we can offer "
            f"based on your profile. Your maximum eligible loan is **{max_eligible}**.\n\n"
            f"Would you like to apply for a lower amount? I can help you find the right fit! 💡"
        )

    def _direct_approval_message(self, state: ConversationState, score: int, emi: float) -> str:
        name = state.kyc_data.get("name", "Customer") if state.kyc_data else "Customer"
        return (
            f"🎉 **Congratulations, {name}!**\n\n"
            f"📊 Credit Score: **{score}** ✅ Excellent!\n"
            f"✅ Loan Amount: Within your pre-approved limit\n\n"
            f"**Your loan is APPROVED!** 🎊\n\n"
            f"📋 **Loan Details:**\n"
            f"• Amount: **{format_currency(state.loan_amount)}**\n"
            f"• Tenure: **{state.tenure_months} months**\n"
            f"• Interest Rate: **{state.interest_rate}% p.a.**\n"
            f"• Monthly EMI: **{format_currency(emi)}**\n\n"
            f"I'm now generating your **Sanction Letter**. You'll be able to download it in just a moment! 📄"
        )

    def _salary_required_message(self, loan: float, limit: float, score: int) -> str:
        return (
            f"📊 **Credit Assessment Complete**\n\n"
            f"Credit Score: **{score}** ✅\n"
            f"Pre-approved Limit: **{format_currency(limit)}**\n"
            f"Requested Amount: **{format_currency(loan)}**\n\n"
            f"Great news — your credit score is excellent! However, since your requested loan amount "
            f"exceeds your pre-approved limit, we need to verify your income to complete the assessment.\n\n"
            f"📎 **Please upload your latest salary slip** to proceed. "
            f"We'll review it immediately and give you a decision!"
        )

    def _salary_approval_message(self, state: ConversationState, emi: float, salary: float) -> str:
        name = state.kyc_data.get("name", "Customer") if state.kyc_data else "Customer"
        emi_ratio = round((emi / salary) * 100, 1)
        return (
            f"✅ **Salary Verification Complete!**\n\n"
            f"Monthly Salary: **{format_currency(salary)}**\n"
            f"Monthly EMI: **{format_currency(emi)}**\n"
            f"EMI-to-Income Ratio: **{emi_ratio}%** ✅ *(within 50% limit)*\n\n"
            f"🎉 **Congratulations, {name}! Your loan is APPROVED!**\n\n"
            f"📋 **Loan Details:**\n"
            f"• Amount: **{format_currency(state.loan_amount)}**\n"
            f"• Tenure: **{state.tenure_months} months**\n"
            f"• Interest Rate: **{state.interest_rate}% p.a.**\n"
            f"• Monthly EMI: **{format_currency(emi)}**\n\n"
            f"Your **Sanction Letter** is being generated. You can download it shortly! 📄"
        )

    def _emi_rejection_message(self, emi: float, salary: float) -> str:
        emi_ratio = round((emi / salary) * 100, 1)
        max_emi = format_currency(salary * 0.5)
        return (
            f"📊 **Income Assessment Result**\n\n"
            f"Monthly Salary: **{format_currency(salary)}**\n"
            f"Required EMI: **{format_currency(emi)}**\n"
            f"EMI-to-Income Ratio: **{emi_ratio}%** ❌ *(exceeds 50% limit)*\n\n"
            f"😔 I'm sorry, but based on your monthly income, the EMI of **{format_currency(emi)}** "
            f"exceeds 50% of your salary. Our policy requires EMI to be within 50% of monthly income "
            f"to ensure comfortable repayment.\n\n"
            f"**Maximum affordable EMI for you:** {max_emi}/month\n\n"
            f"💡 **Suggestions:**\n"
            f"• Apply for a lower loan amount\n"
            f"• Increase the tenure to reduce EMI\n"
            f"• Wait for a salary increase\n\n"
            f"Would you like to try a different loan amount?"
        )

    def _no_data_message(self) -> str:
        return (
            "⚠️ We encountered an issue fetching your credit profile. "
            "Please try again or contact our support team at **1800-267-6060**."
        )
