from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import backend.core.logger # Initialize centralized logger
from backend.core.db import engine, Base
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure vector extension is created and tables are initialized
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    # Need to import models so Base knows about them
    import backend.models.document
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="AI Estimating Assistant API",
    description="API for Document Ingestion, Scope Gaps, RFIs, and Takeoff",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware to allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.api import upload
from backend.api.v1.endpoints import ai_agent

app.include_router(upload.router, prefix="/api/v1")
app.include_router(ai_agent.router, prefix="/api/v1/agent")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Estimating Assistant API is running"}
