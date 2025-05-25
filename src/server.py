from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def r_home():
    return render_template("home/index.html")

@app.route("/drafts")
def r_draft():
    return render_template("drafts/index.html")
