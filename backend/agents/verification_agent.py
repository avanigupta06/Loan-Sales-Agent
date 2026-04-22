"""Verification Agent — fetches and validates KYC data from mock CRM."""

from models.schemas import ConversationState
from services.mock_data import get_kyc_data


class VerificationAgent:
    """Validates customer KYC data fetched from mock CRM."""

    def verify(self, state: ConversationState) -> tuple[bool, str]:
        """
        Returns (is_verified, message).
        Fetches KYC from CRM and validates phone + address.
        """
        if not state.phone:
            return False, (
                "⚠️ I couldn't find a phone number to verify. "
                "Could you please provide your registered mobile number?"
            )

        kyc = get_kyc_data(state.phone)

        if not kyc:
            return False, (
                f"❌ I couldn't find any KYC records for **{state.phone}** in our system.\n\n"
                "This could mean:\n"
                "• You may not have an account with us yet\n"
                "• The number might be registered under a different account\n\n"
                "Please contact our helpline at **1800-267-6060** or visit your nearest Loan Sale Agentic AI System branch."
            )

        # Validate phone match
        if kyc.get("phone") != state.phone:
            return False, (
                "⚠️ Phone number mismatch in our records. "
                "Please ensure you're using your registered mobile number."
            )

        # Validate address exists
        if not kyc.get("address") or len(kyc["address"].strip()) < 10:
            return False, (
                "⚠️ Your address details appear to be incomplete in our records. "
                "Please update your KYC at your nearest branch before proceeding."
            )

        # All checks passed
        state.kyc_data = kyc
        if state.customer_data:
            state.kyc_data["salary"] = state.customer_data.get("salary", 0)

        name = kyc.get("name", "Customer")
        city = kyc.get("city", "")
        address_short = kyc["address"][:50] + "..." if len(kyc["address"]) > 50 else kyc["address"]

        return True, (
            f"✅ **KYC Verification Successful!**\n\n"
            f"Here's what we've verified:\n"
            f"👤 **Name:** {name}\n"
            f"📱 **Phone:** {state.phone}\n"
            f"📍 **City:** {city}\n"
            f"🏠 **Address:** Verified ✓\n"
            f"🪪 **PAN:** Verified ✓\n\n"
            f"Great news, {name}! Your identity checks out perfectly. "
            f"Now let me run a quick **credit assessment** — this is the exciting part! 🎯"
        )
