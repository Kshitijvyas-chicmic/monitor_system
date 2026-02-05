from apscheduler.schedulers.background import BackgroundScheduler
from app.backhround.escalation import esclate_tasks
from app.backhround.deadline_checker import check_deadlines
from app.db.session import SessionLocal

def run_jobs():
    """
    Function that runs all background jobs.
    Called periodically by the scheduler.
    """
    db = SessionLocal()
    try:
        # Example: escalate overdue tasks
        esclate_tasks(db)

        # Example: check deadlines
        check_deadlines(db)

        print("Background jobs executed successfully")
    except Exception as e:
        print(f"Error running background jobs: {e}")
    finally:
        db.close()

def start_scheduler(app):
    """
    Starts the APScheduler in the background.
    Call this from main.py during FastAPI startup.
    """
    scheduler = BackgroundScheduler()
    
    # Run `run_jobs` every hour
    scheduler.add_job(run_jobs, 'interval', hours=1)
    
    scheduler.start()
    print("Scheduler started")
