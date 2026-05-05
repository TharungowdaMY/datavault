from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

def start_scheduler():
    def kill_switch():
        from app.database import SessionLocal
        from app.models.request import DataRequest
        db = SessionLocal()
        try:
            expired = db.query(DataRequest).filter(
                DataRequest.status == "accepted",
                DataRequest.access_expires_at <= datetime.utcnow()
            ).all()
            for r in expired:
                r.status = "expired"
                print(f"[Kill Switch] Request {r.id} access revoked.")
            db.commit()
        finally:
            db.close()

    scheduler.add_job(kill_switch, "interval", minutes=1, id="kill_switch")
    scheduler.start()
    print("[Scheduler] Kill Switch scheduler started.")