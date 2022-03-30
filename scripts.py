import ee
import pandas as pd
import variables as var
import matplotlib.pyplot as plt
import requests

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from skforecast.ForecasterAutoreg import ForecasterAutoreg

try:
    ee.Initialize()
except ee.EEException:
    ee.Authenticate()
    ee.Initialize()


def area_calc(obj=None, aoi=None):
    if isinstance(obj, ee.geometry.Geometry):
        return ee.Number(obj.area()).divide(1e6).round().getInfo()

    elif isinstance(obj, ee.image.Image):
        areaImage = obj.multiply(ee.Image.pixelArea())
        area = areaImage.reduceRegion(reducer=ee.Reducer.sum(), geometry=aoi, scale=500, maxPixels=1e10)
        area_cover = ee.Number(area.get("nd")).divide(1e6).round().getInfo()
        return area_cover
    else:
        print(
            "WARNING: Couldn't compute the area. Object is not an instance of ee.geometry.Geometry or ee.image.Image"
        )
        return None


def plot_rtn():
    try:
        fig, axs = plt.subplots(2, 1, figsize=(15, 7), sharex=True)
        var.data["veg_area"].plot(ax=axs[0], marker="v")
        axs[0].set(
            xlabel="Timeline", ylabel="Vegetation area in Sq.Km", title="Vegetation Area trend", xticks=var.data.index
        )

        var.data["wet_area"].plot(ax=axs[1], marker="v")
        axs[1].set(
            xlabel="Timeline", ylabel="Wet land area in Sq.Km", title="Wet land Area trend", xticks=var.data.index
        )
        fig.tight_layout()
        plt.savefig("static/temp-series.jpg")
    except Exception as e:
        print("ERROR: ", e)
    finally:
        if var.debug:
            print("Plot saved.")


def data_cons():
    try:
        var.data = pd.DataFrame(var.data)
        var.data["date"] = pd.to_datetime(var.data["date"])
        var.data = var.data.set_index("date")
    except Exception as e:
        print("ERROR: ", e)


def get_gif(collec, aoi, color, fname):
    try:
        collec = ee.ImageCollection(collec)
        video_args = {
            "dimensions": 500,
            "region": aoi,
            "crs": "EPSG:3857",
            "bands": ["nd"],
            "palette": color,
            "min": 0,
            "max": 1,
            "framesPerSecond": 3,
        }
        url = collec.getVideoThumbURL(video_args)
        with open(f"./static/temp-{fname}.gif", "wb") as f:
            f.write(requests.get(url).content)
    except Exception as e:
        print("ERROR: ", e)
        return "./static/error.svg"


def get_img(image):
    url = image.select(["B4", "B3", "B2"]).getThumbURL({"min": 0, "max": 5000, "dimensions": 500})
    with open("./static/temp-true.jpg", "wb") as f:
        f.write(requests.get(url).content)


def forecast(type="wet"):

    steps = int(len(var.data) / 2)
    data_train = var.data[:-steps]
    data_test = var.data[-steps:]

    col = f"{type}_area"

    forecaster = ForecasterAutoreg(regressor=RandomForestRegressor(random_state=123), lags=6)
    forecaster.fit(y=data_train[col])

    predictions = forecaster.predict(steps=steps)
    predictions.index = var.data[-steps:].index

    fig, ax = plt.subplots(figsize=(9, 4))
    data_train[col].plot(ax=ax, label="train")
    data_test[col].plot(ax=ax, label="test")
    predictions.plot(ax=ax, label="predictions")
    plt.title(f"{type} Forecast")
    plt.ylabel(f"{type} land area in Sq.Kms")
    plt.xlabel("Timeline")
    ax.legend()

    plt.savefig(f"static/temp-{type}_fc.jpg")

    error_mse = mean_squared_error(y_true=data_test[col], y_pred=predictions)
    print(f"Test error (mse): {error_mse}")
