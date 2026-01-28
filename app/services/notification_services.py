from fastapi import BackgroundTasks
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT


def send_welcome_email(user_email: str, background_tasks: BackgroundTasks, user_name: str):
    subject = "Welcome to Task Management System"
    body = f"""
Hello {user_name},

Welcome! Your account has been successfully created.

You can now log in and start managing your tasks.
"""
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)


def send_login_alert_email(user_email: str, background_tasks: BackgroundTasks, user_name: str):
    subject = "Login Alert"
    body = f"""
Hello {user_name},

Your account was just logged in. If this wasn't you, please secure your account immediately.
"""
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)


def send_role_change_email(user_email: str, background_tasks: BackgroundTasks, user_name: str, new_role: str):
    subject = "Role Updated"
    body = f"""
Hello {user_name},

Your account role has been changed to '{new_role}'.

Please contact your administrator if you have any questions.
"""
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)


def send_password_change_email(user_email: str, background_tasks: BackgroundTasks, user_name: str):
    subject = "Password Changed"
    body = f"""
Hello {user_name},

Your password has been successfully updated.

If you did not perform this action, please reset your password immediately.
"""
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)


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

def send_task_overdue_email(task, user_email: str, background_tasks: BackgroundTasks):
    """Send overdue notification email"""
    subject = f"Task Overdue: {task.title}"
    body = f"""
Hello,

Your task is now overdue.

Task: {task.title}
Description: {task.description}
Priority: {task.priority}
Due Date: {task.due_date}
Status: {task.status}

Please take immediate action.
"""
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)


def send_task_escalation_email(task, user_email: str, background_tasks: BackgroundTasks):
    """Send escalation notification email"""
    subject = f"Task Escalated: {task.title}"
    body = f"""
Hello,

Your task has been escalated due to inactivity.

Task: {task.title}
Description: {task.description}
Priority: {task.priority}
Due Date: {task.due_date}
Status: {task.status}

Please address this task immediately.
"""
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)


def send_verification_email(user_email: str, token: str, background_tasks: BackgroundTasks):
    """Send verification token email in background"""
    subject = "Your Verification Token"
    body = f"""
Hello,

Your email verification token is: {token}

It will expire in 5 minutes.
"""
    background_tasks.add_task(send_email, to_email=user_email, subject=subject, body=body)