from flask import Flask

from flask import request, render_template, redirect, url_for

from main import main
import variables as var
from scripts import plot_rtn, data_cons

app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        DISTRICT = request.form.get("district")
        return redirect(url_for("disp", district=DISTRICT))
    return render_template("index.html")


@app.route("/disp/<district>")
def disp(district):
    obj = main()
    obj.compute()
    data_cons()
    plot_rtn()
    return render_template("display.html", name="temp-op.jpg")


if __name__ == "__main__":
    var.debug = True
    app.run(debug=True)
