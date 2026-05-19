import sqlite3

DB_FILE = "vehicles.db"

conn = sqlite3.connect(
    DB_FILE
)

cursor = conn.cursor()

cursor.execute(
    """

    ALTER TABLE vehicles

    ADD COLUMN vahan_owner_name TEXT

"""
)

conn.commit()

conn.close()

print(
    "vahan_owner_name column added"
)