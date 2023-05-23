import sqlite3

def create_db(file_path):
    # Create a connection to the database (or create a new one if it doesn't exist)
    conn = sqlite3.connect(file_path)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create the 'image' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS image (
                        md5 TEXT PRIMARY KEY,
                        name TEXT,
                        long_name TEXT
                    )''')

    # Create the 'comps' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS comps (
                        comp_key INTEGER PRIMARY KEY AUTOINCREMENT,
                        ssim REAL,
                        histogram REAL,
                        mse REAL
                    )''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

