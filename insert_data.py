import sqlite3

conn = sqlite3.connect("vehicles.db")

cursor = conn.cursor()

vehicles = [

    ("MH40DC2282", "2026-05-25", "919098222330", "Ratnesh"),

    ("MH40CM2082", "2026-05-19", "919098222330", "Ratnesh"),

    ("MH40DC2082", "2026-05-15", "919098222330", "Ratnesh")
]

cursor.executemany("""

INSERT INTO vehicles (
    vehicle_number,
    expiry_date,
    phone,
    owner
)

VALUES (?, ?, ?, ?)

""", vehicles)

conn.commit()

print("Sample data inserted.")

conn.close()