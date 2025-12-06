#!/bin/bash
# Database Initialization Script
# Run this after MySQL is deployed in Coolify

set -e

echo "🗄️  Initializing Legal AI Database"
echo "===================================="

# Database connection details (update these)
DB_HOST="${DB_HOST:-legal-ai-mysql}"
DB_USER="${DB_USER:-legal_ai_user}"
DB_PASSWORD="${DB_PASSWORD:-!SeG@DZk&4yor3NXusrY1G$#i!b@NTBx}"
DB_NAME="${DB_NAME:-legal_ai}"

echo "Connecting to: $DB_HOST"
echo "Database: $DB_NAME"
echo ""

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
until mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" "$DB_NAME" &>/dev/null; do
    echo "Waiting for MySQL..."
    sleep 2
done

echo "✓ MySQL is ready"
echo ""

# Import SQL files in order
echo "Importing schema.sql..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < schema.sql
echo "✓ schema.sql imported"

echo "Importing fir_schema.sql..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < fir_schema.sql
echo "✓ fir_schema.sql imported"

echo "Importing chathistory.sql..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < chathistory.sql
echo "✓ chathistory.sql imported"

echo ""
echo "✅ Database initialization complete!"
echo ""
echo "Tables created:"
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "SHOW TABLES;"

