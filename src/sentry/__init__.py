from flask import Flask, render_template


def create_app():

    """ Application config """

    app = Flask(__name__)

    """ Route definitions """

    @app.route("/")
    def route_home():
        return render_template("home/index.html")


    @app.route("/heroes")
    def route_heroes():
        return render_template("heroes/index.html")


    @app.route("/heroes/meta")
    def route_heroes_meta():
        return render_template("heroes/meta/index.html")


    @app.route("/heroes/draft")
    def route_heroes_draft():
        return render_template("heroes/draft/index.html")


    return app


