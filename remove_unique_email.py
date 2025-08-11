import sqlite3

# Connect to existing DB
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

# Rename old table
cursor.execute("ALTER TABLE contacts RENAME TO contacts_old;")

# Create new table without UNIQUE constraint on email
cursor.execute("""
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    address TEXT,
    email TEXT,
    phone TEXT
)
""")

# Copy data from old table
cursor.execute("""
INSERT INTO contacts (first_name, last_name, address, email, phone)
SELECT first_name, last_name, address, email, phone FROM contacts_old
""")

# Drop old table
cursor.execute("DROP TABLE contacts_old;")
conn.commit()
conn.close()

print("✅ UNIQUE constraint removed from email. You can now add duplicate emails.")
