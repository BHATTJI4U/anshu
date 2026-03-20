import uuid
from flask import Flask, render_template, request, redirect, session, url_for
import fitz
import base64

app = Flask(__name__)
app.secret_key = "secret123"   # required for login sessions

# 🔐 SIMPLE USER DATABASE (for now)
USERS = {
    "Anshumaan": "AnshuOP",
    "Rohan": "yamete",
    "Raghav": "coolguy"
}

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("home"))

        return "Invalid credentials ❌"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", user=session["user"])


# ---------------- YOUR EXISTING TEST (SAFE) ----------------
@app.route("/test", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
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

    return render_template("index.html",
                           total_pages=0,
                           filename="")


# ---------------- PAGE FETCH ----------------
@app.route("/get_page/<filename>/<int:page_num>")
def get_page(filename, page_num):
    filepath = "uploads/" + filename
    doc = fitz.open(filepath)

    if page_num < 0 or page_num >= len(doc):
        doc.close()
        return "Invalid page"

    page = doc[page_num]
    pix = page.get_pixmap(matrix=fitz.Matrix(0.7, 0.7))

    img_bytes = pix.tobytes("png")
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    doc.close()

    return img_base64


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)