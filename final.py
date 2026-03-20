from flask import Flask, render_template, request
import fitz
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return "JEE App Running 🚀"
@app.route("/", methods=["GET", "POST"])
def index():
    pages = []

    if request.method == "POST":
        file = request.files["pdf"]

        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")

            for page in doc:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                pages.append(img_base64)

    return render_template("FINAL JEE.html", pages=pages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)