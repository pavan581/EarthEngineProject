from flask import Flask
import os

from flask import request, render_template, redirect, url_for, Markup
from werkzeug.exceptions import HTTPException

from main import main
import variables as var
from scripts import plot_rtn, data_cons

app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def home():
    try:
        os.remove("static/temp-op.jpg")
    except:
        pass
    if request.method == "POST":
        var.DISTRICT = request.form.get("district")
        return redirect(url_for("disp", district=var.DISTRICT))
    else:
        return render_template("index.html")


@app.route("/disp")
def disp():
    obj = main()
    obj.compute()
    data_cons()
    plot_rtn()
    return render_template("display.html", name="temp-op.jpg")


@app.errorhandler(HTTPException)
def handle_exception(e):
    data = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
    return render_template("error.html", code=data["code"], description=data["description"])


if __name__ == "__main__":
    var.debug = True
    app.run(debug=True)
