import mysql.connector

from config import get_db_config


def run_sql_file(cursor, filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        sql = f.read()
    # Split on semicolon, filter out empty statements
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    for stmt in statements:
        cursor.execute(stmt)


def main() -> None:
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    run_sql_file(cursor, "chathistory.sql")
    conn.commit()
    cursor.close()
    conn.close()
    print("Chat history tables created/updated successfully!")


if __name__ == "__main__":
    main()
