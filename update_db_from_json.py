import json
import mysql.connector

from config import get_db_config


def main() -> None:
    # Load the cleaned JSON data
    with open("ipc_sections.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Connect to MySQL using shared config (root1 / pass / legal_ai by default)
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()

    for section in data.get("sections", []):
        section_number = section.get("section_number")
        title = section.get("title", "")
        description = section.get("description", "")
        punishment = section.get("punishment", "")

        # Skip if no section number
        if not section_number:
            continue

        # Check if section exists
        cursor.execute(
            "SELECT id FROM ipc_sections WHERE section_number = %s",
            (section_number,),
        )
        exists = cursor.fetchone()

        if exists:
            # Update existing record
            cursor.execute(
                """
                UPDATE ipc_sections
                SET title = %s,
                    description = %s,
                    punishment = %s
                WHERE section_number = %s
                """,
                (title, description, punishment, section_number),
            )
        else:
            # Insert new record
            cursor.execute(
                """
                INSERT INTO ipc_sections (section_number, title, description, punishment)
                VALUES (%s, %s, %s, %s)
                """,
                (section_number, title, description, punishment),
            )

    conn.commit()
    cursor.close()
    conn.close()
    print("MySQL database updated from ipc_sections.json.")


if __name__ == "__main__":
    main()
