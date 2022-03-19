import ee
import requests as req
from ee_plugin import Map

dict_collec = ee.FeatureCollection('users/sairamg581/ap_districts')
dict_feature = dict_collec.filter("DISTRICT == 'East Godavari'")
aoi = dict_feature.geometry()

Map.addLayer(aoi, {}, 'AOI')
DistArea = ee.Number(aoi.area()).divide(1e6).round().getInfo()
print("Area of East Godavari District :", DistArea,"Sq.Kms")

#Define the visualization parameters.
vizParams = {'bands': ['B4', 'B3', 'B2'], 'min': 0.0,'max': 4000}
ndviParams = {'min': -1, 'max': 1, 'palette': ['yellow', 'white', 'green']}
ndwiParams = {'min': -1, 'max': 1, 'palette': ['red', 'green', 'blue']}

for year in range(2018, 2022):
    for month in range(1, 13):
        image = ee.ImageCollection("COPERNICUS/S2_SR")\
                    .filterBounds(aoi)\
                    .filterDate(ee.Date(f'{year}-{month}-01'), ee.Date(f'{year}-{month}-28'))\
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))\
                    .mean()\
                    .clip(aoi)
        try:
            ndvi = image.normalizedDifference(['B8', 'B4'])
            ndwi = image.normalizedDifference(['B3', 'B8'])
            
            Map.addLayer(ndvi, ndviParams, f'NDVI-{year}-{month}')
            Map.addLayer(ndwi, ndwiParams, f'NDWI-{year}-{month}')
        except:
            print(month, year)

print('Finish')
