import os
from urllib.parse import urlparse

def get_db_config():
    # Check if we have a DATABASE_URL (Render provides this)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Parse the DATABASE_URL
        db_url = urlparse(database_url)
        return {
            'host': db_url.hostname,
            'user': db_url.username,
            'password': db_url.password,
            'database': db_url.path[1:],  # Remove leading slash
            'port': db_url.port or 5432,  # Default PostgreSQL port
            'autocommit': True,
            'engine': 'postgresql'
        }
    else:
        # Default MySQL configuration
        return {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'user': os.environ.get('DB_USER', 'root'),
            'password': os.environ.get('DB_PASSWORD', 'pass'),
            'database': os.environ.get('DB_NAME', 'legal_ai'),
            'autocommit': True,
            'engine': 'mysql'
        } 