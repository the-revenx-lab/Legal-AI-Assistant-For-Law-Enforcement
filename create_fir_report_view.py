import mysql.connector
from config import get_db_config

create_complainants_table = """
CREATE TABLE IF NOT EXISTS fir_complainants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    nationality VARCHAR(50),
    occupation VARCHAR(100),
    address TEXT NOT NULL,
    contact VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_reports_table = """
CREATE TABLE IF NOT EXISTS fir_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fir_number VARCHAR(50) UNIQUE,
    police_station VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    fir_date DATE NOT NULL,
    complainant_id INT NOT NULL,
    info_type ENUM('Oral', 'Written') NOT NULL,
    place_of_occurrence TEXT NOT NULL,
    date_time_of_occurrence DATETIME NOT NULL,
    accused_details TEXT,
    property_details TEXT,
    property_value DECIMAL(15,2),
    complaint TEXT NOT NULL,
    sections_acts TEXT,
    status ENUM('Draft', 'Submitted', 'Under Review', 'Approved', 'Rejected') DEFAULT 'Draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (complainant_id) REFERENCES fir_complainants(id)
);
"""

create_view_sql = """
CREATE OR REPLACE VIEW fir_report_details AS
SELECT
    fr.id,
    fr.fir_number,
    fr.police_station,
    fr.district,
    fr.fir_date,
    fr.info_type,
    fr.place_of_occurrence,
    fr.date_time_of_occurrence,
    fr.accused_details,
    fr.property_details,
    fr.property_value,
    fr.complaint,
    fr.sections_acts,
    fr.status,
    fr.created_at,
    fr.updated_at,
    fc.name as complainant_name,
    fc.parent_name as complainant_parent_name,
    fc.age as complainant_age,
    fc.gender as complainant_gender,
    fc.nationality as complainant_nationality,
    fc.occupation as complainant_occupation,
    fc.address as complainant_address,
    fc.contact as complainant_contact
FROM fir_reports fr
JOIN fir_complainants fc ON fr.complainant_id = fc.id;
"""

try:
    db_config = get_db_config()
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(create_complainants_table)
    cursor.execute(create_reports_table)
    cursor.execute(create_view_sql)
    conn.commit()
    print("Tables and view created successfully.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close() 