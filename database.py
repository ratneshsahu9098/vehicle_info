import sqlite3

# Connect database
conn = sqlite3.connect("vehicles.db")

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    vehicle_number TEXT NOT NULL,

    expiry_date TEXT NOT NULL,

    phone TEXT NOT NULL,

    owner TEXT
)
""")

conn.commit()

print("Database and table created successfully.")

conn.close()