import pathlib
from flask import Flask, render_template, request, redirect, url_for

from .airtable import AirTable
from . import constants

BASE_DIR = pathlib.Path(__file__).parent

TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, template_folder=str(TEMPLATES_DIR), static_folder=str(STATIC_DIR))
app.url_map.strict_slashes = constants.APPEND_SLASH
app.debug = constants.DEBUG
app.secret_key = constants.SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def homeView():
    sent = None
    print("request.method", request.method)
    if request.method == "POST":
        email = request.form.get("email")
        airtableClient = AirTable(
            baseId=constants.AIRTABLE_BASE_ID,
            apiKey=constants.AIRTABLE_API_KEY,
            tableName=constants.AIRTABLE_TABLE_NAME,
        )
        status = airtableClient.createRecords(email=email)
        if status in range(200, 250):
            sent = True
            return redirect(url_for("successView"), code=302)
        sent = False
        return redirect(url_for("errorView"), code=302)
    return render_template("pages/index.html", sent=sent)


@app.route("/success")
def successView():
    return render_template("pages/success.html")


@app.route("/<error>")
def errorView(*args):

    return render_template("pages/404.html")
