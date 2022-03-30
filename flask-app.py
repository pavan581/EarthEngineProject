from flask import Flask
import os

from flask import request, render_template, redirect, url_for
from werkzeug.exceptions import HTTPException

from main import main
import variables as var
from scripts import plot_rtn, data_cons

app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def home():
    try:
        os.remove("static/temp-series.jpg")
        os.remove("static/temp-veg.gif")
        os.remove("static/temp-wet.gif")
    except Exception as e:
        print("ERROR: ", e)
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
    dt = var.data.index[-1]
    veg_area = var.data.iloc[-1].veg_area
    wet_area = var.data.iloc[-1].wet_area
    return render_template(
        "display.html",
        district=var.DISTRICT,
        month=dt.month_name(),
        year=dt.year,
        veg_area=veg_area,
        wet_area=wet_area,
        tot_area=var.tot_area,
    )


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
