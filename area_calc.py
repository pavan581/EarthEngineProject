import ee
import requests as req
from ee_plugin import Map

data = req.get('https://raw.githubusercontent.com/pavan581/earth-git/master/2011_Dist.json').json()

for dist in data['features']:
    if dist["properties"]["DISTRICT"] == 'East Godavari':
        aoi_data = dist
        break

aoi_coords = aoi_data["geometry"]["coordinates"]
aoi = ee.Geometry.Polygon(aoi_coords)

#Define the visualization parameters.
vizParams = {'bands': ['B4', 'B3', 'B2'], 'min': 0.0,'max': 4000}
ndviParams = {'min': -1, 'max': 1, 'palette': ['yellow', 'white', 'green']}
ndwiParams = {'min': -1, 'max': 1, 'palette': ['red', 'green', 'blue']}

image = ee.ImageCollection("COPERNICUS/S2_SR")\
            .filterBounds(aoi)\
            .filterDate(ee.Date(f'2021-01-01'), ee.Date(f'2021-01-28'))\
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))\
            .mean()\
            .clip(aoi)

img_area = image.multiply(ee.Image.pixelArea())
area = img_area.reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry=aoi,
            scale=500,
            maxPixels=1e10
)

#print(ee.Number(area).divide(1e6).round().getInfo())