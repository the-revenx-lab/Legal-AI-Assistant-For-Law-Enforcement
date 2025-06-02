from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Set, Dict, Optional, Union
import os
import datetime
import json
from api_client import RasaClient
from fastapi import FastAPI 
from fir_api import router as fir_router
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import pooling, Error as MySQLError
import urllib.parse
import logging
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool, Error as PostgresError
import contextlib

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
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

# Templates configuration with error handling
try:
    templates = Jinja2Templates(directory=static_dir)
    logger.info("Template directory configured successfully")
except Exception as e:
    logger.error(f"Failed to configure templates: {str(e)}")
    templates = None

# User authentication from environment variables
users = {
    os.environ.get('ADMIN_USERNAME', 'admin'): os.environ.get('ADMIN_PASSWORD', 'admin123'),
    os.environ.get('USER_USERNAME', 'user'): os.environ.get('USER_PASSWORD', 'user123')
}

# Store active WebSocket connections and their session IDs
active_connections: Dict[WebSocket, str] = {}

# Database connection pools
db_pool: Optional[Union[psycopg2.pool.SimpleConnectionPool, mysql.connector.pooling.MySQLConnectionPool]] = None

def init_db_pool():
    """Initialize the database connection pool"""
    global db_pool
    
    try:
        if 'DATABASE_URL' in os.environ:
            # PostgreSQL pool configuration
            url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
            pg_config = {
                'host': url.hostname,
                'user': url.username,
                'password': url.password,
                'database': url.path[1:],
                'port': url.port or 5432
            }
            db_pool = psycopg2.pool.SimpleConnectionPool(1, 20, **pg_config)
            logger.info("PostgreSQL connection pool created successfully")
        else:
            # MySQL pool configuration
            mysql_config = {
                'pool_name': 'mypool',
                'pool_size': 20,
                'host': os.environ.get('DB_HOST', 'localhost'),
                'user': os.environ.get('DB_USER', 'root'),
                'password': os.environ.get('DB_PASSWORD', 'pass'),
                'database': os.environ.get('DB_NAME', 'legal_ai'),
                'autocommit': True
            }
            db_pool = mysql.connector.pooling.MySQLConnectionPool(**mysql_config)
            logger.info("MySQL connection pool created successfully")
    except (PostgresError, MySQLError) as e:
        logger.error(f"Failed to create database pool: {str(e)}")
        db_pool = None
        raise HTTPException(status_code=500, detail="Database configuration error")

# Initialize the database pool
init_db_pool()

@contextlib.contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        if not db_pool:
            raise HTTPException(status_code=500, detail="Database pool not initialized")
            
        if 'DATABASE_URL' in os.environ:
            conn = db_pool.getconn()
        else:
            conn = db_pool.get_connection()
            
        yield conn
        
    except (PostgresError, MySQLError) as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        if conn:
            try:
                if 'DATABASE_URL' in os.environ:
                    db_pool.putconn(conn)
                else:
                    conn.close()
            except Exception as e:
                logger.error(f"Error closing database connection: {str(e)}")

@app.get('/api/chat/history')
async def get_chat_history():
    """Get all chat sessions with message counts"""
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT 
                    s.id, 
                    s.session_name, 
                    s.created_at, 
                    COUNT(m.id) as message_count
                FROM chat_sessions s 
                LEFT JOIN chat_messages m ON s.id = m.session_id
                GROUP BY s.id, s.session_name, s.created_at
                ORDER BY s.created_at DESC
            ''')
            sessions = cursor.fetchall()
            return sessions
        except (PostgresError, MySQLError) as e:
            logger.error(f"Error fetching chat history: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch chat history")
        finally:
            cursor.close()

@app.delete('/api/chat/history/{session_id}')
async def delete_chat_history(session_id: int):
    """Delete a chat session and its messages"""
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            # Delete messages first due to foreign key constraint
            cursor.execute('DELETE FROM chat_messages WHERE session_id = %s', (session_id,))
            cursor.execute('DELETE FROM chat_sessions WHERE id = %s', (session_id,))
            conn.commit()
            return {'status': 'success', 'message': f'Session {session_id} deleted successfully'}
        except (PostgresError, MySQLError) as e:
            logger.error(f"Error deleting chat history: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete chat history")
        finally:
            cursor.close()

@app.get("/api/chat/history/{session_id}/messages")
async def get_chat_messages(session_id: int):
    """Get all messages for a specific chat session"""
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT sender, content, timestamp 
                FROM chat_messages 
                WHERE session_id = %s 
                ORDER BY timestamp ASC
            ''', (session_id,))
            messages = cursor.fetchall()
            if not messages:
                logger.warning(f"No messages found for session {session_id}")
            return messages
        except (PostgresError, MySQLError) as e:
            logger.error(f"Error fetching chat messages: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch chat messages")
        finally:
            cursor.close()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main application page"""
    try:
        # First try using template response
        if templates:
            return templates.TemplateResponse("index.html", {"request": request})
        
        # Fallback to direct file reading
        try:
            index_path = os.path.join(static_dir, "index.html")
            if not os.path.exists(index_path):
                raise FileNotFoundError(f"index.html not found in {static_dir}")
                
            with open(index_path, "r", encoding='utf-8') as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
            
        except Exception as file_error:
            logger.error(f"Failed to read index.html: {str(file_error)}")
            # Return a basic HTML response as last resort
            return HTMLResponse(
                content="""
                <html>
                    <head><title>Legal AI Assistant</title></head>
                    <body>
                        <h1>Welcome to Legal AI Assistant</h1>
                        <p>Service is starting up...</p>
                    </body>
                </html>
                """
            )
            
    except Exception as e:
        logger.error(f"Root route error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(static_dir, "favicon.ico"))

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in users and users[username] == password:
        return RedirectResponse(url="/chat", status_code=303)
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/fir", response_class=HTMLResponse)
async def fir_page(request: Request):
    return templates.TemplateResponse("fir.html", {"request": request})

@app.get("/fir/admin", response_class=HTMLResponse)
async def fir_admin_page(request: Request):
    return templates.TemplateResponse("fir_admin.html", {"request": request})

@app.get("/ipc/admin", response_class=HTMLResponse)
async def ipc_admin_page(request: Request):
    return templates.TemplateResponse("ipc_admin.html", {"request": request})

@app.get("/fir/{fir_id}", response_class=HTMLResponse)
async def fir_details_page(request: Request, fir_id: int):
    return templates.TemplateResponse("saverate.html", {"request": request, "fir_id": fir_id})

@app.get("/chat/history", response_class=HTMLResponse)
async def chat_history_page(request: Request):
    return templates.TemplateResponse("chat_history.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/health")
async def health_check():
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "127.0.0.1")
    uvicorn.run(app, host=host, port=port)