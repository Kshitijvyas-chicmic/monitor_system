from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from app.core.config_logging import logger

def generate_report_pdf(report_data:dict):
    logger.info("Starting PDF generation...")

    try:
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setFont("Helvetica", 12)

        # Title
        pdf.drawString(50, 800, "Task Management System Report")
        pdf.setFont("Helvetica", 10)

        y = 750

        # Tasks per user section
        pdf.drawString(50, y, "TASKS PER USER:")
        y -= 20

        tasks_per_user = report_data.get("tasks_per_user", [])
        logger.info(f"Processing {len(tasks_per_user)} user records")

        for user_data in tasks_per_user:
            if hasattr(user_data, 'user_email'):
                pdf.drawString(70, y, f"User: {user_data.user_email}, Tasks: {user_data.task_count}")
            else:
                pdf.drawString(70, y, str(user_data))
            y -= 15
            if y < 50:  # New page if needed
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

        y -= 20

        # Tasks per status section
        pdf.drawString(50, y, "TASKS PER STATUS:")
        y -= 20

        tasks_per_status = report_data.get("tasks_per_status", [])
        logger.info(f"Processing {len(tasks_per_status)} status records")

        for status_data in tasks_per_status:
            if hasattr(status_data, 'status'):
                pdf.drawString(70, y, f"Status: {status_data.status}, Count: {status_data.count}")
            else:
                pdf.drawString(70, y, str(status_data))
            y -= 15
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

        y -= 20

        # Workload distribution section
        pdf.drawString(50, y, "WORKLOAD DISTRIBUTION:")
        y -= 20

        workload_data = report_data.get("workload_distribution", [])
        logger.info(f"Processing {len(workload_data)} workload records")

        for workload in workload_data:
            if hasattr(workload, 'user_email'):
                pdf.drawString(70, y, f"User: {workload.user_email}, Workload: {workload.workload_percentage}%")
            else:
                pdf.drawString(70, y, str(workload))
            y -= 15
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        logger.info("PDF generation completed successfully")
        return buffer

    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
        raise