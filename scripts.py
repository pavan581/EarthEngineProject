import ee
import pandas as pd
import variables as var
import matplotlib.pyplot as plt

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
        plt.savefig("static/temp-op.jpg")
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
