from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, grey
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

def generate_pdf(
    report,
    app_name="FreeMind AI",
    creator_name="Created by FreeMind AI Team",
    logo_path="logo.png"  # path to logo image
):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # ---------------- COLORS ----------------
    primary = HexColor("#1E7F6D")   # teal
    secondary = HexColor("#333333")

    # ---------------- HEADER ----------------
    if logo_path:
        try:
            pdf.drawImage(
                logo_path,
                40,
                height - 90,
                width=60,
                height=60,
                mask="auto"
            )
        except:
            pass

    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColor(primary)
    pdf.drawString(120, height - 60, app_name)

    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(secondary)
    pdf.drawString(120, height - 78, creator_name)

    pdf.setStrokeColor(primary)
    pdf.setLineWidth(1)
    pdf.line(40, height - 100, width - 40, height - 100)

    # ---------------- REPORT META ----------------
    y = height - 130
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Medical Report")

    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(
        width - 40,
        y,
        f"Date: {datetime.now().strftime('%d %b %Y')}"
    )

    y -= 30
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(40, y, "Patient Name:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(140, y, report.patient)

    y -= 20
    pdf.setStrokeColor(grey)
    pdf.line(40, y, width - 40, y)

    # ---------------- PROBLEMS ----------------
    y -= 30
    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(primary)
    pdf.drawString(40, y, "Problems Identified")

    y -= 20
    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(secondary)

    for problem in report.problems_identified:
        if y < 80:
            pdf.showPage()
            y = height - 60
        pdf.drawString(60, y, f"• {problem}")
        y -= 18

    # ---------------- REMEDIES ----------------
    y -= 15
    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(primary)
    pdf.drawString(40, y, "Suggested Remedies")

    y -= 20
    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(secondary)

    for remedy in report.remedies:
        if y < 80:
            pdf.showPage()
            y = height - 60
        pdf.drawString(60, y, f"• {remedy}")
        y -= 18

    # ---------------- FOOTER ----------------
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.setFillColor(grey)
    pdf.drawCentredString(
        width / 2,
        40,
        "This report is generated for supportive guidance only and is not a medical diagnosis."
    )

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
