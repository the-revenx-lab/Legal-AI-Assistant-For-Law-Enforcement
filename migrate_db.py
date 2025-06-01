import os
from urllib.parse import urlparse
import psycopg2
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    if 'DATABASE_URL' in os.environ:
        # PostgreSQL (Render)
        url = urlparse(os.environ['DATABASE_URL'])
        return psycopg2.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],
            port=url.port or 5432
        )
    else:
        # MySQL (Local)
        return mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'pass'),
            database=os.environ.get('DB_NAME', 'legal_ai')
        )

def migrate():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create chat_sessions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id SERIAL PRIMARY KEY,
            session_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create chat_messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
            sender VARCHAR(50),
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("✅ Database migration completed successfully!")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    migrate() 