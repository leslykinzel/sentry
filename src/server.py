from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def route_home():
    return render_template("home/index.html")

@app.route("/drafts")
def route_drafts():
    return render_template("drafts/index.html")
