# app.py
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
DB_PATH = "database.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

# ------------- INSECURE VERSION (demo only) -------------

@app.route("/login_insecure", methods=["GET", "POST"])
def login_insecure():
    message = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        cur = conn.cursor()

        # VULNERABLE: user input concatenated directly into SQL
        # Do NOT use this in real apps.
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("Insecure query:", query)

        try:
            cur.execute(query)
            row = cur.fetchone()
            if row:
                message = f"Logged in as {row['username']} (INSECURE CHECK)"
            else:
                message = "Invalid credentials (insecure check)"
        except sqlite3.Error as e:
            # Shows the error; can reveal SQL details
            message = f"Database error (insecure): {e}"

        conn.close()

    return render_template("login_insecure.html", message=message)

# ------------- SECURE VERSION (fixed) -------------

@app.route("/login_secure", methods=["GET", "POST"])
def login_secure():
    message = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        cur = conn.cursor()

        # SAFE: parameterized query keeps data separate from SQL structure
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        print("Secure query:", query, "params:", (username, password))

        cur.execute(query, (username, password))
        row = cur.fetchone()

        if row:
            message = f"Logged in as {row['username']} (SECURE CHECK)"
        else:
            message = "Invalid credentials (secure check)"

        conn.close()

    return render_template("login_secure.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)