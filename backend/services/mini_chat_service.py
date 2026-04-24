import os
import json
import urllib.request
import urllib.error

SYSTEM_PROMPT = """You are a helpful finance assistant for the Loan Sale Agentic AI System.
Your job is to answer finance-related questions clearly and in simple language.

You specialise in:
- EMI (Equated Monthly Instalment) — what it is and how it's calculated
- Loan approval rules: credit score thresholds, pre-approved limits, salary checks
- Interest rates — fixed vs reducing balance, annual vs monthly
- Loan tenure — how it affects EMI and total interest paid
- Personal loan eligibility criteria
- Common reasons for loan rejection
- General financial literacy (savings, debt-to-income ratio, CIBIL score)

The EMI formula used in this system:
  EMI = P x r x (1+r)^n / ((1+r)^n - 1)
  where P = principal, r = monthly interest rate (annual rate / 12 / 100), n = tenure in months

Underwriting rules in this system:
  1. Credit score < 700 -> Rejected immediately
  2. Loan amount <= pre-approved limit -> Directly approved
  3. Loan amount between 1x and 2x pre-approved limit -> Salary slip required; approved only if EMI <= 50% of monthly salary
  4. Loan amount > 2x pre-approved limit -> Rejected

Guidelines:
- Be concise - answer in 3-6 sentences unless a detailed explanation is specifically needed
- Use simple, jargon-free language; explain any technical term you use
- Always be friendly and encouraging
- Do NOT discuss topics outside personal finance and loans
- If asked something completely unrelated (sports, politics, etc.), politely redirect to finance topics
"""


def _call_groq(query: str, history: list) -> str:
    """Call Groq API - llama3-8b-8192 (free tier, 14,400 req/day)."""
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set")

    url = "https://api.groq.com/openai/v1/chat/completions"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add history (last 6 exchanges to stay within token limit)
    for turn in history[-6:]:
        messages.append({"role": turn["role"], "content": turn["content"]})

    messages.append({"role": "user", "content": query})

    payload = json.dumps({
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read())

    return data["choices"][0]["message"]["content"].strip()


def _fallback_answer(query: str) -> str:
    """Rule-based fallback when no API key is configured."""
    q = query.lower()

    if any(w in q for w in ["emi", "equated monthly"]):
        return (
            "EMI stands for Equated Monthly Instalment - the fixed amount you repay each month "
            "to clear your loan. It covers both the principal and interest.\n\n"
            "Formula: **EMI = P x r x (1+r)^n / ((1+r)^n - 1)**\n"
            "where P = loan amount, r = monthly interest rate (annual rate / 1200), "
            "n = tenure in months.\n\n"
            "Example: Rs.5 lakh at 12.5% for 36 months -> EMI approx Rs.16,741/month."
        )
    if any(w in q for w in ["credit score", "cibil", "score"]):
        return (
            "A credit score (CIBIL score in India) is a 3-digit number from 300-900 that reflects "
            "your creditworthiness. Higher is better.\n\n"
            "In this system: **score >= 700 is required** to be eligible for a loan. "
            "A score below 700 results in immediate rejection. "
            "You can improve your score by paying EMIs on time and reducing credit card utilisation."
        )
    if any(w in q for w in ["interest rate", "interest"]):
        return (
            "An interest rate is the cost of borrowing money, expressed as a percentage per year (p.a.).\n\n"
            "This system uses **12.5% p.a. on a reducing balance basis** - meaning interest is "
            "calculated on the outstanding principal each month, not the original amount. "
            "This is cheaper than a flat-rate loan."
        )
    if any(w in q for w in ["reject", "rejected", "why"]):
        return (
            "Common reasons for loan rejection in this system:\n\n"
            "1. **Credit score < 700** - below the minimum threshold\n"
            "2. **Loan > 2x pre-approved limit** - exceeds maximum eligibility\n"
            "3. **EMI > 50% of monthly salary** - income insufficient for repayment\n"
            "4. **KYC mismatch** - identity verification failed\n\n"
            "Improving your credit score and applying for a smaller amount are the best first steps."
        )
    if any(w in q for w in ["tenure", "duration", "period", "years", "months"]):
        return (
            "Loan tenure is the repayment period - how long you take to pay back the loan.\n\n"
            "Longer tenure -> lower EMI but higher total interest paid.\n"
            "Shorter tenure -> higher EMI but less total interest.\n\n"
            "This system offers tenures from **12 to 60 months (1-5 years)**. "
            "A 5-year loan at 12.5% on Rs.5L costs ~Rs.2.08L in interest; a 2-year loan costs ~Rs.0.68L."
        )
    if any(w in q for w in ["approve", "approved", "eligible", "eligib"]):
        return (
            "Loan approval in this system follows these rules:\n\n"
            "1. **Credit score >= 700** - minimum requirement\n"
            "2. **Loan <= pre-approved limit** -> instant approval, no salary check needed\n"
            "3. **Loan between 1x and 2x limit** -> salary slip required; approved if EMI <= 50% salary\n"
            "4. **Loan > 2x limit** -> rejected regardless of income\n\n"
            "Meeting all criteria ensures a smooth, fast approval."
        )

    return (
        "I'm your finance assistant for the Loan Sale Agentic AI System! "
        "I can help with questions about EMI, interest rates, loan approval rules, "
        "credit scores, and general personal finance.\n\n"
        "Try asking: 'What is EMI?', 'How is my loan approved?', or 'Explain interest rate'."
    )


def get_mini_chat_response(query: str, history: list) -> dict:
    """
    Main entry point. Tries Groq -> fallback (rule-based).
    Returns {"answer": str, "source": str}
    """
    if os.environ.get("GROQ_API_KEY"):
        try:
            answer = _call_groq(query, history)
            return {"answer": answer, "source": "groq"}
        except Exception as e:
            print(f"[mini-chat] Groq error: {e}")

    # Fallback - rule-based
    return {"answer": _fallback_answer(query), "source": "fallback"}
