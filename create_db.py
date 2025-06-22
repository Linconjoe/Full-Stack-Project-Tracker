import sqlite3

# Connect to the SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('gmc_sierra_progress.db')
cursor = conn.cursor()

# Create the 'tasks' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        cost REAL
    )
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("SQLite database 'gmc_sierra_progress.db' and 'tasks' table created successfully!")