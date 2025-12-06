import os


def get_db_config():
    """
    Central database configuration for the application.

    Defaults are set to match your local MySQL setup:
    - host: localhost
    - user: root1
    - password: pass
    - database: legal_ai

    These can still be overridden via environment variables if needed.
    """
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "user": os.environ.get("DB_USER", "root1"),
        "password": os.environ.get("DB_PASSWORD", "pass"),
        "database": os.environ.get("DB_NAME", "legal_ai"),
        "autocommit": True,
    }
