from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from app.api import auth, tickets, bookings, ai, documents

app = FastAPI(title="CampusOS API")

app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(bookings.router)
app.include_router(ai.router)
app.include_router(documents.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def health_check_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
