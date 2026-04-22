"""Sanction Letter Generator — produces a PDF using reportlab."""

import os
from datetime import datetime, timedelta
from models.schemas import ConversationState
from utils.finance import format_currency, calculate_emi


def generate_sanction_letter(state: ConversationState, output_dir: str = "uploads") -> str:
    """Generate sanction letter PDF and return the file path."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    except ImportError:
        raise RuntimeError("reportlab is not installed. Run: pip install reportlab")

    os.makedirs(output_dir, exist_ok=True)
    session_id = state.session_id
    filename = f"sanction_letter_{session_id[:8]}.pdf"
    filepath = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    # ── Style definitions ────────────────────────────────────────────────────
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "Header",
        parent=styles["Normal"],
        fontSize=22,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a3c6e"),
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    subheader_style = ParagraphStyle(
        "SubHeader",
        parent=styles["Normal"],
        fontSize=11,
        fontName="Helvetica",
        textColor=colors.HexColor("#4a6fa5"),
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontSize=14,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a3c6e"),
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8,
    )
    normal_style = ParagraphStyle(
        "MyNormal",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#333333"),
        spaceAfter=6,
    )
    bold_style = ParagraphStyle(
        "Bold",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a3c6e"),
    )
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        fontName="Helvetica",
        textColor=colors.HexColor("#888888"),
        alignment=TA_CENTER,
        spaceBefore=6,
    )

    # ── Data extraction ──────────────────────────────────────────────────────
    kyc = state.kyc_data or {}
    name = kyc.get("name", "Customer")
    address = kyc.get("address", "N/A")
    pan = kyc.get("pan", "N/A")
    phone = state.phone or "N/A"
    loan_amount = state.loan_amount or 0
    tenure = state.tenure_months or 0
    interest_rate = state.interest_rate or 12.5
    emi = state.emi or calculate_emi(loan_amount, interest_rate, tenure)

    today = datetime.now()
    sanction_date = today.strftime("%d %B %Y")
    valid_until = (today + timedelta(days=30)).strftime("%d %B %Y")
    ref_no = f"TC/PL/{today.year}/{session_id[:8].upper()}"

    total_payable = emi * tenure
    total_interest = total_payable - loan_amount

    # ── Content building ─────────────────────────────────────────────────────
    content = []

    # Logo / Header
    content.append(Paragraph("LOAN SALE AGENTIC AI SYSTEM", header_style))
    content.append(Paragraph("AI-Powered Loan Platform", subheader_style))
    content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a3c6e")))
    content.append(Spacer(1, 4 * mm))

    # Reference info
    ref_data = [
        [Paragraph(f"<b>Ref No:</b> {ref_no}", normal_style),
         Paragraph(f"<b>Date:</b> {sanction_date}", normal_style)],
        [Paragraph(f"<b>Valid Until:</b> {valid_until}", normal_style), ""],
    ]
    ref_table = Table(ref_data, colWidths=["55%", "45%"])
    ref_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    content.append(ref_table)
    content.append(Spacer(1, 4 * mm))

    # Title
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    content.append(Paragraph("LOAN SANCTION LETTER", title_style))
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    content.append(Spacer(1, 4 * mm))

    # Salutation
    content.append(Paragraph(f"Dear <b>{name}</b>,", normal_style))
    content.append(Spacer(1, 2 * mm))
    content.append(Paragraph(
        "We are pleased to inform you that your Personal Loan application has been reviewed and "
        "<b>APPROVED</b> subject to the terms and conditions mentioned herein.",
        normal_style,
    ))
    content.append(Spacer(1, 4 * mm))

    # Customer details table
    content.append(Paragraph("CUSTOMER DETAILS", bold_style))
    content.append(Spacer(1, 2 * mm))
    customer_data = [
        ["Full Name", name],
        ["Mobile Number", phone],
        ["PAN Number", pan],
        ["Address", address],
    ]
    customer_table = Table(customer_data, colWidths=["35%", "65%"])
    customer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2f7")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a3c6e")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    content.append(customer_table)
    content.append(Spacer(1, 5 * mm))

    # Loan details table
    content.append(Paragraph("LOAN DETAILS", bold_style))
    content.append(Spacer(1, 2 * mm))
    loan_data = [
        ["Loan Type", "Personal Loan"],
        ["Loan Amount", format_currency(loan_amount)],
        ["Interest Rate", f"{interest_rate}% p.a. (Reducing Balance)"],
        ["Loan Tenure", f"{tenure} Months"],
        ["Monthly EMI", format_currency(emi)],
        ["Total Interest Payable", format_currency(total_interest)],
        ["Total Amount Payable", format_currency(total_payable)],
        ["Processing Fee", "1% of loan amount + GST"],
        ["Prepayment Charges", "Nil after 12 EMIs"],
    ]
    loan_table = Table(loan_data, colWidths=["45%", "55%"])
    loan_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2f7")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a3c6e")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        # Highlight EMI row
        ("BACKGROUND", (0, 4), (-1, 4), colors.HexColor("#d4edda")),
        ("FONTNAME", (0, 4), (-1, 4), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 4), (-1, 4), colors.HexColor("#155724")),
    ]))
    content.append(loan_table)
    content.append(Spacer(1, 5 * mm))

    # Approval stamp area
    approval_data = [
        [Paragraph(
            '<font color="#155724"><b>✓ LOAN APPROVED</b></font>',
            ParagraphStyle("Approval", parent=styles["Normal"], fontSize=14,
                           fontName="Helvetica-Bold", alignment=TA_CENTER)
        )]
    ]
    approval_table = Table(approval_data, colWidths=["100%"])
    approval_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#d4edda")),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor("#28a745")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    content.append(approval_table)
    content.append(Spacer(1, 5 * mm))

    # Terms
    content.append(Paragraph("TERMS & CONDITIONS", bold_style))
    content.append(Spacer(1, 2 * mm))
    terms = [
        "1. This sanction letter is valid for 30 days from the date of issue.",
        "2. Disbursement is subject to submission of all required documents.",
        "3. The loan amount will be disbursed directly to your bank account on record.",
        "4. EMI payments are due on the 5th of every month.",
        "5. Non-payment of EMI will attract penal interest @ 2% per month.",
        "6. Tata Capital reserves the right to recall the loan at any time.",
    ]
    for term in terms:
        content.append(Paragraph(term, ParagraphStyle(
            "Term", parent=styles["Normal"], fontSize=8, fontName="Helvetica",
            textColor=colors.HexColor("#555555"), spaceAfter=3,
        )))
    content.append(Spacer(1, 6 * mm))

    # Signature block
    sig_data = [
        [Paragraph("Authorized Signatory", normal_style),
         Paragraph("Customer Acceptance", normal_style)],
        [Paragraph("<b>Loan Sale Agentic AI System Pvt. Ltd.</b>",
                   ParagraphStyle("Sig", parent=styles["Normal"], fontSize=9,
                                  fontName="Helvetica-Bold", textColor=colors.HexColor("#1a3c6e"))),
         Paragraph(f"<b>{name}</b>",
                   ParagraphStyle("Sig2", parent=styles["Normal"], fontSize=9,
                                  fontName="Helvetica-Bold", textColor=colors.HexColor("#1a3c6e")))],
    ]
    sig_table = Table(sig_data, colWidths=["50%", "50%"])
    sig_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        ("LINEABOVE", (0, 0), (-1, 0), 1, colors.HexColor("#333333")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    content.append(sig_table)
    content.append(Spacer(1, 4 * mm))

    # Footer
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    content.append(Paragraph(
        "Loan Sale Agentic AI System Pvt. Ltd. | CIN: U65910MH2010PLC213028 | "
        "NBFC Reg. No.: N-13.02190 | www.tatacapital.com | 1800-267-6060",
        footer_style,
    ))

    doc.build(content)
    return filepath
