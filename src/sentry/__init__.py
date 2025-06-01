from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import opendota


def create_app():

    """ Application config """

    config = {
        "DEBUG": True,
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 60
    }

    app = Flask(__name__)
    app.config.from_mapping(config)

    cache = Cache(app)
    limiter = Limiter(get_remote_address, app=app)

    api = opendota.OpenDota()

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


    @cache.cached(timeout=30)
    @limiter.limit("10 per minute")
    @app.route("/api/live-games")
    def api_live_games():
        return jsonify(api.get_live())

    return app


