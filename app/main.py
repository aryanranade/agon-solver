import logging
from fastapi import FastAPI
from app.api.routes import router

# Setup simple logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI(
    title="Agon API Solver",
    description="A hackathon submission API for the Agon AI Evaluation Dashboard.",
    version="1.0.0"
)

# Include our API routes
app.include_router(router)

@app.get("/")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "Agon Solver API is running"}

if __name__ == "__main__":
    import uvicorn
    # This allows running the file directly for simple development
    uvicorn.run(app, host="0.0.0.0", port=8000)
