from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.services.report_pdf import generate_report_pdf
from app.core.role_core import require_roles
from app.core.config_logging import logger

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/pdf")
def download_report_pdf(
    current_user = Depends(require_roles(["admin"]))
):
    logger.info(f"PDF report requested by user: {current_user.email} (role: {current_user.role})")

    try:
        # Get actual report data from database
        from app.db.session import get_db
        from sqlalchemy.orm import Session
        from app.services.reporting_services import (
            get_tasks_per_user,
            get_tasks_per_status,
            get_workload_distribution
        )

        # Create a database session
        db = next(get_db())

        logger.info("Fetching report data from database...")

        report_data = {
            "tasks_per_user": get_tasks_per_user(db),
            "tasks_per_status": get_tasks_per_status(db),
            "workload_distribution": get_workload_distribution(db)
        }

        logger.info(f"Report data collected: {len(report_data['tasks_per_user'])} users, {len(report_data['tasks_per_status'])} statuses, {len(report_data['workload_distribution'])} workload entries")

        logger.info("Generating PDF report...")
        pdf_buffer = generate_report_pdf(report_data)

        logger.info("PDF report generated successfully, returning streaming response")

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=task_report.pdf"}
        )

    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}", exc_info=True)
        raise
