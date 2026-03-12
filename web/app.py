import os

from flask import Flask, render_template

from web.routes.results import results_bp
from web.routes.run import run_bp
from web.routes.upload import upload_bp


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.environ.get("AAID_SECRET_KEY") or os.urandom(32)

    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(run_bp, url_prefix="/run")
    app.register_blueprint(results_bp, url_prefix="/results")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
