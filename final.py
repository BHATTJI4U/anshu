from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "SERVER WORKING"

@app.route("/login")
def login():
    return "LOGIN WORKING"