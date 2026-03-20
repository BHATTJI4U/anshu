from flask import Flask, render_template, request
import fitz
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["pdf"]

        if file:
            file.save("temp.pdf")   # ✅ save file

            doc = fitz.open("temp.pdf")
            total_pages = len(doc)

            return render_template("index.html", total_pages=total_pages)

    return render_template("index.html", total_pages=0)


@app.route("/get_page/<int:page_num>")
def get_page(page_num):
    doc = fitz.open("temp.pdf")

    if page_num < 0 or page_num >= len(doc):
        return "Invalid page"

    page = doc[page_num]
    pix = page.get_pixmap()

    img_bytes = pix.tobytes("png")
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    return img_base64

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)