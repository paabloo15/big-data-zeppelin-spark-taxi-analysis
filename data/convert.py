import geopandas as gpd
import pandas as pd

gdf = gpd.read_file('/data/taxi_zones.shp')
gdf = gdf.to_crs(epsg=4326)

lookup = pd.read_csv('/data/taxi_zone_lookup.csv')
gdf = gdf.merge(lookup[['LocationID', 'service_zone']], on='LocationID', how='left')

gdf.to_file('/data/nyc_taxi_zones.geojson', driver='GeoJSON')
print('Convertido correctamente')
print(gdf.columns.tolist())