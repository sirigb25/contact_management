import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("contacts.db")
cur = conn.cursor()

# Drop old contacts table if it exists
cur.execute("DROP TABLE IF EXISTS contacts")

# Create table without UNIQUE constraint on email
cur.execute('''
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    address TEXT,
    email TEXT,
    phone TEXT
)
''')

conn.commit()
conn.close()

print("✅ Database created successfully without UNIQUE constraint on email.")
