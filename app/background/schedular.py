# from apscheduler.schedulers.background import BackgroundScheduler
# from app.background.escalation import esclate_tasks
# from app.background.deadline_checker import check_deadlines
# from app.db.session import SessionLocal

# scheduler = BackgroundScheduler()

# def run_jobs():
#     """
#     Function that runs all background jobs.
#     Called periodically by the scheduler.
#     """
#     db = SessionLocal()
#     try:
#         # Example: escalate overdue tasks
#         esclate_tasks(db)

#         # Example: check deadlines
#         check_deadlines(db)

#         print("Background jobs executed successfully")
#     except Exception as e:
#         print(f"Error running background jobs: {e}")
#     finally:
#         db.close()

# def start_scheduler(app):
#     # """
#     # Starts the APScheduler in the background.
#     # Call this from main.py during FastAPI startup.
#     # """
#     # scheduler = BackgroundScheduler()
    
#     # # Run `run_jobs` every hour
#     # scheduler.add_job(run_jobs, 'interval', hours=1)
    
#     # scheduler.start()
#     # print("Scheduler started")
#      """
#     Starts the APScheduler in the background.
#     Call this from FastAPI startup event.
#     """
#     # Only add jobs if scheduler not already running
#      if not scheduler.running:
#         # Run `run_jobs` every hour
#         scheduler.add_job(run_jobs, 'interval', hours=1)
#         scheduler.start()
#         logger.info("Scheduler started")


from apscheduler.schedulers.background import BackgroundScheduler
from app.background.escalation import esclate_tasks
from app.background.deadline_checker import check_deadlines
from app.db.session import SessionLocal
from app.core.config_logging import logger

scheduler = BackgroundScheduler()

def run_jobs():
    """
    Function that runs all background jobs.
    Called periodically by the scheduler.
    """
    db = SessionLocal()
    try:
        esclate_tasks(db)
        check_deadlines(db)
        logger.info("Background jobs executed successfully")
    except Exception as e:
        logger.error(f"Error running background jobs: {e}")
    finally:
        db.close()

def start_scheduler():
    """
    Starts the APScheduler in the background.
    Call this from FastAPI startup event.
    """
    # Only add jobs if scheduler not already running
    if not scheduler.running:
        # Run `run_jobs` every hour
        scheduler.add_job(run_jobs, 'interval', hours=1)
        scheduler.start()
        logger.info("Scheduler started")

