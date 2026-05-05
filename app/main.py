from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.database import engine
from app.models import User, Brand, DataSource, DataRequest, Transaction
from app.database import Base
from app.routers import auth, user, brand, admin
from app.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

security = HTTPBearer()

app = FastAPI(
    title="DataVault",
    description="Consent-first personal data marketplace — own your data, earn from it.",
    version="1.0.0",
)

# THIS IS THE FIX — allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,  prefix="/auth",  tags=["Auth"])
app.include_router(user.router,  prefix="/user",  tags=["User"])
app.include_router(brand.router, prefix="/brand", tags=["Brand"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.get("/")
def root():
    return {
        "project": "DataVault",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }