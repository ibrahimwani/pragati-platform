import sqlite3
import os

def fix_database():
    db_path = 'c:\\Users\\ibrah\\Desktop\\pragati-platform\\instance\\pragati.db'
    # Check if instance folder exists, otherwise check root
    if not os.path.exists(db_path):
        db_path = 'c:\\Users\\ibrah\\Desktop\\pragati-platform\\pragati.db'
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Adding 'otp' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN otp VARCHAR(6)")
    except sqlite3.OperationalError:
        print("Column 'otp' already exists or error occurred.")

    try:
        print("Adding 'otp_expiry' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN otp_expiry DATETIME")
    except sqlite3.OperationalError:
        print("Column 'otp_expiry' already exists or error occurred.")

    conn.commit()
    conn.close()
    print("Database schema updated successfully!")

if __name__ == "__main__":
    fix_database()
