from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Dict
import os
import datetime
import json
from api_client import RasaClient
from fastapi import FastAPI 
from fir_api import router as fir_router
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import urllib.parse
import logging
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Rasa client with environment variable
RASA_SERVER_URL = os.environ.get('RASA_SERVER_URL', 'http://localhost:5005')
rasa_client = RasaClient(base_url=RASA_SERVER_URL)

# Get the absolute path to the static directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount FIR API routes under /api
app.include_router(fir_router, prefix="/api")

# Templates
templates = Jinja2Templates(directory=static_dir)

# User authentication from environment variables
users = {
    os.environ.get('ADMIN_USERNAME', 'admin'): os.environ.get('ADMIN_PASSWORD', 'admin123'),
    os.environ.get('USER_USERNAME', 'user'): os.environ.get('USER_PASSWORD', 'user123')
}

# Store active WebSocket connections and their session IDs
active_connections: Dict[WebSocket, str] = {}

def get_chat_db():
    """Get database connection based on environment"""
    try:
        if 'DATABASE_URL' in os.environ:
            # PostgreSQL connection
            url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
            return psycopg2.connect(
                host=url.hostname,
                user=url.username,
                password=url.password,
                database=url.path[1:],
                port=url.port or 5432
            )
        else:
            # MySQL connection for local development
            return mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', 'pass'),
                database=os.environ.get('DB_NAME', 'legal_ai')
            )
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get('/api/chat/history')
async def get_chat_history():
    """Get chat history with message counts"""
    conn = None
    try:
        conn = get_chat_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT s.id, s.session_name, s.created_at, COUNT(m.id) as message_count
            FROM chat_sessions s 
            LEFT JOIN chat_messages m ON s.id = m.session_id
            GROUP BY s.id, s.session_name, s.created_at
            ORDER BY s.created_at DESC
        ''')
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat history")
    finally:
        if conn:
            conn.close()

@app.delete('/api/chat/history/{session_id}')
async def delete_chat_history(session_id: int):
    """Delete chat session and its messages"""
    conn = None
    try:
        conn = get_chat_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM chat_messages WHERE session_id = %s', (session_id,))
        cursor.execute('DELETE FROM chat_sessions WHERE id = %s', (session_id,))
        conn.commit()
        return {'status': 'success'}
    except Exception as e:
        logger.error(f"Error deleting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete chat history")
    finally:
        if conn:
            conn.close()

@app.get("/api/chat/history/{session_id}/messages")
async def get_chat_messages(session_id: int):
    """Get messages for a specific chat session"""
    conn = None
    try:
        conn = get_chat_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sender, content, timestamp FROM chat_messages WHERE session_id = %s ORDER BY timestamp ASC",
            (session_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching chat messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat messages")
    finally:
        if conn:
            conn.close()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main application page"""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        # Return a basic HTML response
        return HTMLResponse(
            content="""
            <html>
                <head>
                    <title>Legal AI Assistant</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; }
                        h1 { color: #333; }
                    </style>
                </head>
                <body>
                    <h1>Welcome to Legal AI Assistant</h1>
                    <p>Service is starting up...</p>
                </body>
            </html>
            """
        )

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    try:
        return FileResponse(os.path.join(static_dir, "favicon.ico"))
    except Exception:
        return JSONResponse(status_code=404, content={"message": "Favicon not found"})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Handle user login"""
    if username in users and users[username] == password:
        return RedirectResponse(url="/chat", status_code=303)
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Serve chat page"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/fir", response_class=HTMLResponse)
async def fir_page(request: Request):
    """Serve FIR page"""
    return templates.TemplateResponse("fir.html", {"request": request})

@app.get("/fir/admin", response_class=HTMLResponse)
async def fir_admin_page(request: Request):
    """Serve FIR admin page"""
    return templates.TemplateResponse("fir_admin.html", {"request": request})

@app.get("/ipc/admin", response_class=HTMLResponse)
async def ipc_admin_page(request: Request):
    """Serve IPC admin page"""
    return templates.TemplateResponse("ipc_admin.html", {"request": request})

@app.get("/fir/{fir_id}", response_class=HTMLResponse)
async def fir_details_page(request: Request, fir_id: int):
    """Serve FIR details page"""
    return templates.TemplateResponse("saverate.html", {"request": request, "fir_id": fir_id})

@app.get("/chat/history", response_class=HTMLResponse)
async def chat_history_page(request: Request):
    """Serve chat history page"""
    return templates.TemplateResponse("chat_history.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """Serve about page"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "service": "legal-ai-assistant"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Parse session_id from query params if present
    await websocket.accept()
    session_id = None
    parsed = urllib.parse.urlparse(str(websocket.url))
    params = urllib.parse.parse_qs(parsed.query)
    if 'session_id' in params:
        try:
            session_id = int(params['session_id'][0])
            logging.info(f"WebSocket: Received session_id from URL: {session_id}")
        except Exception:
            session_id = None
    active_connections[websocket] = session_id
    chat_db_conn = get_chat_db()
    chat_db_cur = chat_db_conn.cursor()
    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.datetime.now().isoformat()
            log_entry = f"{timestamp} - {data}\n"
            with open("chat.log", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)

            # --- Chat History DB logic ---
            # Only create a new session if session_id is not provided or does not exist
            if session_id:
                chat_db_cur.execute("SELECT id FROM chat_sessions WHERE id = %s", (session_id,))
                row = chat_db_cur.fetchone()
                if not row:
                    chat_db_cur.execute("INSERT INTO chat_sessions (session_name) VALUES (%s)", (None,))
                    session_id = chat_db_cur.lastrowid
                    active_connections[websocket] = session_id
                    chat_db_conn.commit()
                    logging.info(f"WebSocket: Created new session (ID: {session_id}) because provided session_id did not exist.")
                else:
                    logging.info(f"WebSocket: Using existing session (ID: {session_id})")
            else:
                chat_db_cur.execute("INSERT INTO chat_sessions (session_name) VALUES (%s)", (None,))
                session_id = chat_db_cur.lastrowid
                active_connections[websocket] = session_id
                chat_db_conn.commit()
                logging.info(f"WebSocket: Created new session (ID: {session_id}) because no session_id was provided.")
            # Save user message
            chat_db_cur.execute("INSERT INTO chat_messages (session_id, sender, content, timestamp) VALUES (%s, %s, %s, %s)", (session_id, 'user', data, timestamp))
            chat_db_conn.commit()
            logging.info(f"WebSocket: Saved user message to session {session_id}: {data}")

            # Get response from Rasa
            rasa_response = rasa_client.send_message(data, session_id)
            # Send user message back to all clients
            for connection in active_connections:
                if connection != websocket:
                    await connection.send_text(json.dumps({
                        "type": "user_message",
                        "text": data
                    }))
            # Send Rasa response to the sender
            if rasa_response:
                combined_response = []
                for message in rasa_response:
                    if "text" in message:
                        combined_response.append(message["text"])
                        # Save bot message to DB
                        chat_db_cur.execute("INSERT INTO chat_messages (session_id, sender, content, timestamp) VALUES (%s, %s, %s, %s)", (session_id, 'bot', message["text"], datetime.datetime.now().isoformat()))
                        chat_db_conn.commit()
                        logging.info(f"WebSocket: Saved bot message to session {session_id}: {message['text']}")
                formatted_response = "\n\n".join(combined_response)
                await websocket.send_text(json.dumps({
                    "type": "bot_message",
                    "text": formatted_response
                }))
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "text": "I'm sorry, I couldn't process your request at the moment."
                }))
    except WebSocketDisconnect:
        if websocket in active_connections:
            del active_connections[websocket]
    finally:
        chat_db_cur.close()
        chat_db_conn.close()

# For Vercel serverless deployment
app = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "127.0.0.1")
    uvicorn.run(app, host=host, port=port)