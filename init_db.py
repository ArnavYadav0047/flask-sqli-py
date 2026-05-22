# init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Drop table if it exists (for reset)
    cur.execute("DROP TABLE IF EXISTS users")

    # Create table
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Insert a demo user
    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("alice", "password123")
    )

    conn.commit()
    conn.close()
    print("Database initialized with demo user: alice / password123")

if __name__ == "__main__":
    init_db()