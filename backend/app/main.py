from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routes import auth, users

# Create tables (development only — use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FreelanceUSTA API",
    description="Marketplace para estudiantes universitarios verificados",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "FreelanceUSTA API"}
