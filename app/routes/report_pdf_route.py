from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.services.report_pdf import generate_report_pdf
from app.core.role_core import require_roles
from app.db.session import get_db
from app.services.reporting_services import (
    get_tasks_per_user,
    get_tasks_per_status,
    get_workload_distribution
)

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/pdf")
def download_report_pdf(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    report_data = {
        "tasks_per_user": get_tasks_per_user(db),
        "tasks_per_status": get_tasks_per_status(db),
        "workload_distribution": get_workload_distribution(db),
    }

    pdf_buffer = generate_report_pdf(report_data)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=task_report.pdf"
        },
    )

