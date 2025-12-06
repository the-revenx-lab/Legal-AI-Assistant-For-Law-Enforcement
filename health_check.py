"""
Health check endpoint for FastAPI
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import mysql.connector
from config import get_db_config

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_config = get_db_config()
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            conn.close()
            db_status = "connected"
        else:
            db_status = "disconnected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JSONResponse({
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "service": "legal_ai_fastapi"
    })
