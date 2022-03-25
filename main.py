import ee
import variables as var
from scripts import area_calc, get_gif


class main:
    def __init__(self):
        try:
            ee.Initialize()
        except ee.EEException:
            ee.Authenticate()
            ee.Initialize()
        finally:
            if var.debug:
                print("INFO : Earth Engine Initialized.")

        self.dict_collec = ee.FeatureCollection(var.feat_path)
        self.dict_feature = self.dict_collec.filter(f"DISTRICT == '{var.DISTRICT}'")
        self.aoi = self.dict_feature.geometry()

        if var.debug:
            var.tot_area = area_calc(self.aoi)
            print(f"Area of {var.DISTRICT} District :{var.tot_area} Sq.Kms")

    def compute(self):
        for year in range(
            var.START_DATE.get("year").getInfo(),
            var.END_DATE.get("year").getInfo() + 1,
        ):
            for month in range(1, 13):
                image = (
                    ee.ImageCollection("COPERNICUS/S2_SR")
                    .filterBounds(self.aoi)
                    .filterDate(
                        ee.Date(f"{year}-{month}-01"),
                        ee.Date(f"{year}-{month}-28"),
                    )
                    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", var.CLD_PRT))
                    .mean()
                    .clip(self.aoi)
                )
                try:
                    ndvi = image.normalizedDifference(["B8", "B4"])
                    ndwi = image.normalizedDifference(["B3", "B8"])

                    vegetation = ndvi.gt(0.45).selfMask()
                    wet_land = ndwi.gt(0).selfMask()

                    date = "-".join([str(month), str(year)])
                    veg_area = area_calc(vegetation, self.aoi)
                    wet_area = area_calc(wet_land, self.aoi)

                    var.data["date"].append(date)
                    var.data["veg_area"].append(veg_area)
                    var.data["wet_area"].append(wet_area)

                    var.veg_imgs.append(vegetation)
                    var.wet_imgs.append(wet_land)
                except Exception as e:
                    if var.debug:
                        print(e, month, year, sep="--")

        get_gif(var.veg_imgs, self.aoi, "green", "veg")
        get_gif(var.wet_imgs, self.aoi, "blue", "wet")
