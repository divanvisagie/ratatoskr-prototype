import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("data/muninn.db")

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_username TEXT NOT NULL,
    allowed BOOLEAN NOT NULL
)
""")

# Add some data to the table
cursor.execute("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("DivanVisagie", True))
cursor.execute("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("DaisyTheDeadWeed", True))
cursor.execute("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("danielwebb", True))
cursor.execute("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("temporalix", True))

# Commit the changes
conn.commit()

# Retrieve the data
cursor.execute("SELECT * FROM users")

# Fetch all the rows
rows = cursor.fetchall()

# Iterate over the rows
for row in rows:
    print(row)

# Close the cursor
cursor.close()

# Close the connection
conn.close()
