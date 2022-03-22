import ee
from datetime import date

try:
    ee.Initialize()
except ee.EEException:
    ee.Authenticate()
    ee.Initialize()

DISTRICT = "East Godavari"
START_DATE = ee.Date("2017-03-28")
END_DATE = ee.Date(str(date.today()))
CLD_PRT = 5

# Define the visualization parameters.
vizParams = {"bands": ["B4", "B3", "B2"], "min": 0.0, "max": 255}
ndviParams = {"min": -1, "max": 1, "palette": ["yellow", "white", "green"]}
ndwiParams = {"min": -1, "max": 1, "palette": ["red", "green", "blue"]}

data = {"date": [], "veg_area": [], "wet_area": []}

debug = False

feat_path = "users/sairamg581/ap_districts"
