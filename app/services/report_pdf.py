from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from datetime import datetime
from app.core.config_logging import logger


def generate_report_pdf(report_data: dict):
    logger.info("Starting PDF generation...")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    def new_page():
        nonlocal y
        pdf.showPage()
        pdf.setFont("Helvetica", 10)
        y = height - 50

    #  HEADER 
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Task Management System Report")
    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Generated on: {datetime.now().strftime('%d %B %Y %H:%M')}")
    y -= 30

    # TASKS PER USER
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "1. Tasks Per User")
    y -= 15

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "User Email")
    pdf.drawString(350, y, "Total Tasks")
    y -= 10
    pdf.line(50, y, 550, y)
    y -= 15

    pdf.setFont("Helvetica", 10)
    for row in report_data["tasks_per_user"]:
        if y < 60:
            new_page()

        pdf.drawString(50, y, row.email)
        pdf.drawString(350, y, str(row.total_tasks))
        y -= 15

    y -= 20

    #  TASKS PER STATUS
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "2. Tasks Per Status")
    y -= 15

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "Status")
    pdf.drawString(350, y, "Total Tasks")
    y -= 10
    pdf.line(50, y, 550, y)
    y -= 15

    pdf.setFont("Helvetica", 10)
    for row in report_data["tasks_per_status"]:
        if y < 60:
            new_page()

        pdf.drawString(50, y, row.status.capitalize())
        pdf.drawString(350, y, str(row.total_tasks))
        y -= 15

    y -= 20

    #  WORKLOAD DISTRIBUTION
   
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "3. Workload Distribution")
    y -= 15

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "User Email")
    pdf.drawString(300, y, "Open Tasks")
    pdf.drawString(420, y, "Completed Tasks")
    y -= 10
    pdf.line(50, y, 550, y)
    y -= 15

    pdf.setFont("Helvetica", 10)
    for row in report_data["workload_distribution"]:
        if y < 60:
            new_page()

        pdf.drawString(50, y, row.email)
        pdf.drawString(320, y, str(row.open_tasks))
        pdf.drawString(450, y, str(row.completed_tasks))
        y -= 15

    #  FOOTER
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(50, 30, "Confidential - Generated for Admin Use Only")

    pdf.save()
    buffer.seek(0)

    logger.info("PDF generation completed successfully")
    return buffer
