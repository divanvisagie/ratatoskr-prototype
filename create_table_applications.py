import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("data/muninn.db")

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS app (
    id INTEGER PRIMARY KEY,
    app_name TEXT NOT NULL
)
""")

# Commit the changes
conn.commit()

# Fetch all the rows
rows = cursor.fetchall()

# Iterate over the rows
for row in rows:
    print(row)

# Close the cursor
cursor.close()

# Close the connection
conn.close()
