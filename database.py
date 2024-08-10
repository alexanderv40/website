import sqlite3

# Connect to SQLite database (it will create a new database if it does not exist)
conn = sqlite3.connect('usersss.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a new table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idd INTEGER ,
    name TEXT ,
    password TEXT,
    balance INTEGER
)
''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Database created and table initialized.")
