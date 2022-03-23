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
    if data["code"] == 404:
        code = """
            <img id="error-404" src='../static/404.gif' onerror="this.style.display='none';">
        """
        return render_template("error.html", code=Markup(code))
    code = """
        <div class="center" id="oops">
            <i class="fa-solid fa-triangle-exclamation fa-beat-fade fa-9x" style="color: #D82148;"></i>
            <h1>Oops!! something went wrong.</h1>
        </div>
    """
    return render_template("error.html", code=Markup(code))


if __name__ == "__main__":
    var.debug = True
    app.run(debug=True)
