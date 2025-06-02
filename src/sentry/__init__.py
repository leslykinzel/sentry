from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import opendota


def create_app():

    """ Application config """

    config = {
        "DEBUG": True,
        "CACHE_TYPE": "MemcachedCache",
        "CACHE_DEFAULT_TIMEOUT": 60,
        "CACHE_MEMCACHED_SERVERS": ["memcached:11211"]
    }

    app = Flask(__name__)
    app.config.from_mapping(config)

    cache = Cache(app)
    limiter = Limiter(get_remote_address, app=app)

    dota = opendota.OpenDota()

    """ User Routes """

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

    """ Data Routes """

    @app.route("/api/live-games")
    @cache.cached(timeout=60)
    @limiter.limit("10/minute")
    def api_live_games():
        return jsonify(dota.get_live())

    return app
