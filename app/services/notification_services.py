from fastapi import BackgroundTasks
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT

def send_email(to_email: str, subject: str, body: str):
    """Send email using SMTP"""
    print(f"DEBUG: Attempting to send email to {to_email} with subject: {subject}")
    
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print(f"DEBUG: Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT}")
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        print(f"DEBUG: Logging in with email: {SMTP_EMAIL}")
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        print(f"DEBUG: Sending email...")
        server.send_message(msg)
        server.quit()
        print(f"DEBUG: Email sent successfully to {to_email}")
    except Exception as e:
        print(f"DEBUG: Failed to send email to {to_email}: {str(e)}")
        print(f"DEBUG: SMTP_EMAIL: {SMTP_EMAIL}")
        print(f"DEBUG: SMTP_HOST: {SMTP_HOST}")
        print(f"DEBUG: SMTP_PORT: {SMTP_PORT}")

def send_task_assignment_email(task, user_email: str, background_tasks: BackgroundTasks):
    """Send task assignment email in background"""
    print(f"DEBUG: Preparing to send email to {user_email} for task: {task.title}")
    
    subject = f"New Task Assigned: {task.title}"
    body = f"""
Hello,

You have been assigned a new task.

Task: {task.title}
Description: {task.description}
Priority: {task.priority}
Due Date: {task.due_date}
Status: {task.status}

Please check your dashboard for more details.
"""
    print(f"DEBUG: Adding email task to background tasks for {user_email}")
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)
    print(f"DEBUG: Email task added to background tasks")
