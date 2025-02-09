from fastapi import FastAPI
from app.api.endpoints import profile

# Create FastAPI app instance
app = FastAPI(
    title="AI Resume Generator API",
    description="An API for generating resumes and cover letters based on user profiles and job descriptions.",
    version="1.0.0"
)

# Include API routers
app.include_router(profile.router, prefix="/profile", tags=["Profile Management"])

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to AI Resume Generator API"}

