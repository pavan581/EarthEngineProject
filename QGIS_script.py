import ee
import sys

# from ee_plugin import Map
from scripts import *
from variables import *

sys.path.append(r'D:/Study/"Major Project"/QGIS_test/')

try:
    ee.Initialize()
except:
    ee.Authenticate()
    ee.Initialize()
finally:
    print("INFO : Earth Engine Initialized.")

dict_feature = dict_collec.filter(f"DISTRICT == '{DISTRICT}'")
aoi = dict_feature.geometry()
# Map.addLayer(aoi, {}, "AOI")

DistArea = ee.Number(aoi.area()).divide(1e6).round().getInfo()
print("Area of East Godavari District :", DistArea, "Sq.Kms")

for year in range(
    START_DATE.get("year").getInfo(), END_DATE.get("year").getInfo() + 1
):
    for month in range(1, 13):
        image = (
            sentinel2.filterBounds(aoi)
            .filterDate(
                ee.Date(f"{year}-{month}-01"), ee.Date(f"{year}-{month}-28")
            )
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", CLD_PRT))
            .mean()
            .clip(aoi)
        )
        # Map.addLayer(image, vizParams, f'RGB---{year}--{month}')

        try:
            ndvi = image.normalizedDifference(["B8", "B4"])
            ndwi = image.normalizedDifference(["B3", "B8"])

            vegetation = ndvi.gt(0.45).selfMask()
            wet_land = ndwi.gt(0).selfMask()

            date = "/".join([str(month), str(year)])
            veg_area = area_calc(vegetation, aoi)
            wet_area = area_calc(wet_land, aoi)

            # Map.addLayer(ndvi, ndviParams, f'NDVI--{year}--{month}')
            # Map.addLayer(ndwi, ndwiParams, f'NDWI--{year}--{month}')

            print("INFO ", date, veg_area, wet_area, sep=":")

        except Exception as e:
            print("ERROR", e, month, year, sep=":")

print("Run successful.")
