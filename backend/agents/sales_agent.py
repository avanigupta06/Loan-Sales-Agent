"""Sales Agent — collects loan requirements conversationally."""

from models.schemas import ConversationState, ConversationStage
from utils.finance import parse_amount, parse_tenure, format_currency


class SalesAgent:
    """Persuasive sales agent that collects loan amount and tenure."""

    GREETINGS = [
        "Great to have you here! 😊",
        "Wonderful! Let's explore the best loan options for you.",
        "Absolutely! You're in the right place.",
    ]

    def process(self, state: ConversationState, user_message: str) -> tuple[str, bool]:
        """
        Returns (response_text, is_complete).
        is_complete = True when both loan_amount and tenure are collected.
        """
        msg = user_message.lower().strip()

        # Step 1: Collect loan amount
        if state.loan_amount is None:
            return self._collect_loan_amount(state, user_message)

        # Step 2: Collect tenure
        if state.tenure_months is None:
            return self._collect_tenure(state, user_message)

        # Both collected
        return self._confirm_requirements(state), True

    def _collect_loan_amount(self, state: ConversationState, message: str) -> tuple[str, bool]:
        amount = parse_amount(message)
        attempts = state.attempts.get("loan_amount", 0)

        if amount and amount >= 10000:
            state.loan_amount = amount
            formatted = format_currency(amount)
            responses = [
                f"Excellent choice! {formatted} — that's a smart financial move. 💼\n\n"
                f"Now, how long would you like to repay this? I can offer tenures from **12 to 60 months**. "
                f"What works best for you? (e.g., '3 years' or '36 months')",

                f"Perfect! {formatted} it is. You have great financial instincts! 🎯\n\n"
                f"Let's talk repayment — what tenure would suit you? Options range from **1 to 5 years**. "
                f"What's your preference?",
            ]
            return responses[attempts % len(responses)], False

        # Couldn't parse — ask again
        state.attempts["loan_amount"] = attempts + 1
        if attempts == 0:
            return (
                "I'd love to help you with the perfect loan! 🌟\n\n"
                "Could you tell me **how much loan amount** you're looking for? "
                "For example: *'5 lakh'*, *'10 lakhs'*, or *'₹500000'*",
                False,
            )
        elif attempts == 1:
            return (
                "No worries! Just let me know the loan amount you have in mind. "
                "You can say something like **'3 lakh'** or **'₹300000'**. "
                "I'm here to get you the best deal! 💪",
                False,
            )
        else:
            return (
                "Let me help you out — our personal loans start from ₹50,000 up to ₹50 Lakhs. "
                "Which range interests you? Say **'2 lakh'** or **'500000'** and I'll take care of the rest!",
                False,
            )

    def _collect_tenure(self, state: ConversationState, message: str) -> tuple[str, bool]:
        tenure = parse_tenure(message)
        attempts = state.attempts.get("tenure", 0)

        if tenure and 6 <= tenure <= 84:
            state.tenure_months = tenure
            return self._confirm_requirements(state), True

        if tenure and tenure < 6:
            state.tenure_months = 12
            return (
                "For a comfortable repayment experience, I'd recommend a minimum of **12 months**. "
                "I've set the tenure to 12 months for you — great choice! ✅",
                True,
            )

        if tenure and tenure > 84:
            state.tenure_months = 60
            return (
                "Our maximum tenure is **60 months (5 years)**. "
                "I've set it to 60 months for the most affordable EMIs. ✅",
                True,
            )

        state.attempts["tenure"] = attempts + 1
        if attempts == 0:
            return (
                "Almost there! 🎉 Just tell me your preferred **repayment period**. "
                "You can say *'2 years'*, *'36 months'*, *'5 years'* — whatever fits your budget!",
                False,
            )
        else:
            return (
                "Let's keep it simple — popular choices are **2 years**, **3 years**, or **5 years**. "
                "Which sounds right for you?",
                False,
            )

    def _confirm_requirements(self, state: ConversationState) -> str:
        from utils.finance import format_currency, calculate_emi
        emi_est = calculate_emi(state.loan_amount, state.interest_rate, state.tenure_months)
        years = state.tenure_months // 12
        months_rem = state.tenure_months % 12
        tenure_str = f"{years} year{'s' if years != 1 else ''}" if months_rem == 0 else f"{state.tenure_months} months"
        return (
            f"Fantastic! Here's a quick summary of your loan request:\n\n"
            f"📋 **Loan Amount:** {format_currency(state.loan_amount)}\n"
            f"📅 **Tenure:** {tenure_str}\n"
            f"💰 **Estimated EMI:** {format_currency(emi_est)}/month *(at {state.interest_rate}% p.a.)*\n\n"
            f"Looks like a great plan! Let me now quickly **verify your KYC details** to proceed. "
            f"This is just a formality — takes less than a minute! 🚀"
        )

    def greet(self, customer_name: str) -> str:
        return (
            f"Wonderful to meet you, **{customer_name}**! 🌟 I'm your personal loan advisor at Loan Sale Agentic AI System.\n\n"
            f"I see we already have your profile on file. Let me help you find the **perfect loan** tailored just for you!\n\n"
            f"So, what are you planning? A home renovation, dream vacation, or maybe consolidating some expenses? "
            f"Tell me — **how much loan are you looking for today?** 💼"
        )
