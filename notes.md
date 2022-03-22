# QGIS
### Importing GeoJson Layer in QGIS
- Layer -> Add Layer -> Add Vector Layer

### Filtering for District
- Right Click GeoJson Layer -> Properties -> Query Builder -> Paste `DISTRICT = 'East Godavari'` in Provide Specific Filter Expression -> Ok -> Apply

# Content
### NDVI
- Is used for vegetation.
- `NDVI = (NIR-RED)/(NIR+RED)`
- For Sentinel-2, `NDVI = (B8-B4)/(B8+B4)`
### NDWI
- Is used for Water.
- `NDVI = (NIR-SWIR)/(NIR+SWIR)`
- For Sentinel-2, `NDVI = (B3-B8)/(B3+B8)`

# Error info
> If ipyleaflet maps are not working in Jupyterlab try [link](https://ipywidgets.readthedocs.io/en/stable/user_install.html)

# Keywords
- Remote sensing
- Google Earth Engine
- QGIS
- NDVI
- NDWI
- Mineral index
- Vegetation/Deforestation
- Groundwater
- QGIS Python