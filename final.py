import os
import uuid
import base64
import fitz
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
# 👇 DATABASE FUNCTION
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

# 👇 CALL IT HERE
init_db()
# make uploads folder if not exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ---------------- HOME (LOGIN PAGE) ----------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    conn.close()

    if user:
        return render_template("index.html", total_pages=0, filename="")
    else:
        return "Invalid login"

@app.route("/update_users")
def update_users():
    import sqlite3
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    users = [
        ("anshu", "1234"),
        ("rohan", "bade_sahab"),
        ("raghav", "bade_sir")
    ]

    for u in users:
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", u)
        except:
            c.execute("UPDATE users SET password=? WHERE username=?", (u[1], u[0]))

    conn.commit()
    conn.close()

    return "Users inserted/updated"

    
# ---------------- UPLOAD PDF ----------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["pdf"]

    if file:
        filename = str(uuid.uuid4()) + ".pdf"
        filepath = "uploads/" + filename

        file.save(filepath)

        doc = fitz.open(filepath)
        total_pages = len(doc)
        doc.close()

        return render_template("index.html",
                               total_pages=total_pages,
                               filename=filename)

    return "No file uploaded"


# ---------------- GET PAGE ----------------
@app.route("/get_page/<filename>/<int:page_num>")
def get_page(filename, page_num):
    filepath = "uploads/" + filename

    if not os.path.exists(filepath):
        return "File not found"

    doc = fitz.open(filepath)

    if page_num < 0 or page_num >= len(doc):
        return "Invalid page"

    page = doc[page_num]
    pix = page.get_pixmap()

    img_bytes = pix.tobytes("png")
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    doc.close()

    return img_base64


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)