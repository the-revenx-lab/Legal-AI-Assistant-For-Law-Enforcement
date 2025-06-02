from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "legal-ai-assistant"
    } 