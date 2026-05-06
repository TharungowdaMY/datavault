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
            db.commit()
        except Exception as e:
            print(f"Kill switch error: {e}")
        finally:
            db.close()

    try:
        scheduler.add_job(kill_switch, "interval", minutes=1, id="kill_switch")
        scheduler.start()
        print("[Scheduler] Kill Switch started.")
    except Exception as e:
        print(f"[Scheduler] Failed to start: {e}")