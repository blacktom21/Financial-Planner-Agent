from memory.db import get_connection

with open("memory/schema.sql", "r") as f:
    schema = f.read()

conn = get_connection()
conn.executescript(schema)
conn.close()

print("Database initialized.")
