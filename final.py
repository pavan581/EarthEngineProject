import ee
import pandas as pd
import matplotlib.pyplot as plt

try:
    ee.Initialize()
except ee.EEException:
    ee.Authenticate()
    ee.Initialize()
finally:
    print("INFO : Earth Engine Initialized.")


def area_calc(img):
    areaImage = img.multiply(ee.Image.pixelArea())
    area = areaImage.reduceRegion(reducer=ee.Reducer.sum(), geometry=aoi, scale=500, maxPixels=1e10)
    area_cover = ee.Number(area.get("nd")).divide(1e6).round().getInfo()
    return area_cover


dict_collec = ee.FeatureCollection("users/sairamg581/ap_districts")
dict_feature = dict_collec.filter("DISTRICT == 'East Godavari'")
aoi = dict_feature.geometry()

# Map.addLayer(aoi, {}, 'AOI')
DistArea = ee.Number(aoi.area()).divide(1e6).round().getInfo()
print("Area of East Godavari District :", DistArea, "Sq.Kms")

# Define the visualization parameters.
vizParams = {"bands": ["B4", "B3", "B2"], "min": 0.0, "max": 4000}
ndviParams = {"min": -1, "max": 1, "palette": ["yellow", "white", "green"]}
ndwiParams = {"min": -1, "max": 1, "palette": ["red", "green", "blue"]}

data = {"date": [], "veg_area": [], "wet_area": []}

for month in range(1, 13):
    image = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(aoi)
        .filterDate(ee.Date(f"2021-{month}-01"), ee.Date(f"2021-{month}-28"))
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 5))
        .mean()
        .clip(aoi)
    )
    try:
        ndvi = image.normalizedDifference(["B8", "B4"])
        ndwi = image.normalizedDifference(["B3", "B8"])

        vegetation = ndvi.gt(0.45).selfMask()
        wet_land = ndwi.gt(0).selfMask()

        date = "-".join([str(month), str(2021)])
        veg_area = area_calc(vegetation)
        wet_area = area_calc(wet_land)

        data["date"].append("-".join([str(month), str(2021)]))
        data["veg_area"].append(veg_area)
        data["wet_area"].append(wet_area)

    except Exception as e:
        print(e, month, 2021, sep="--")
data = pd.DataFrame(data)
data["date"] = pd.to_datetime(data["date"])
data = data.set_index("date")

print(data.iloc[-1])


def plot_rtn():
    fig, axs = plt.subplots(2, 1, figsize=(15, 7))
    data["veg_area"].plot(ax=axs[0])
    axs[0].set(
        xlabel="Timeline",
        ylabel="Vegetation area in Sq.Km",
        title="Vegetation Area trend",
    )

    data["wet_area"].plot(ax=axs[1])
    axs[1].set(
        xlabel="Timeline",
        ylabel="Wet land area in Sq.Km",
        title="Wet land Area trend",
    )
    fig.tight_layout()
    plt.savefig("static/temp-beta-fig.png")
    print("Plot saved successfully.")


print("Run successful.")
