#!/bin/bash
set -e
DB_FILE="/app/lattes_db.sqlite3"

if [ -f "$DB_FILE" ]; then
    echo "✓ Database already exists: $DB_FILE"
    echo "✓ Skipping initialization"
else
    echo "⚠ Database not found: $DB_FILE"
    echo "⚠ Running database creation script..."
    echo ""
    
    cd /app/src/db
    python create.py
    
    if [ -f "$DB_FILE" ]; then
        echo ""
        echo "✓ Database successfully created!"
    else
        echo ""
        echo "✗ ERROR: Database creation failed!"
        exit 1
    fi
fi
