import streamlit as st
import pandas as pd
import numpy as np
import folium as fo
from streamlit_folium import folium_static
import geopandas as gp

st.title('Streamlit with Folium')

"""
## An easy way to create a website using Python
"""

df = pd.read_csv('https://raw.githubusercontent.com/Maplub/MonthlyAirQuality/master/sensorlist.csv')


st.write(df)


crs = "EPSG:4326"
geometry = gp.points_from_xy(df.lon,df.lat)
geo_df  = gp.GeoDataFrame(df,crs=crs,geometry=geometry)

nan_boundary  = gp.read_file('https://github.com/Maplub/AirQualityData/blob/master/nan_shp_wgs84.zip?raw=true')
nanall = nan_boundary.unary_union

nan_sta = geo_df.loc[geo_df.geometry.within(nanall)]


longitude = 100.819200
latitude = 19.331900

station_map = fo.Map(
	location = [latitude, longitude], 
	zoom_start = 10)

latitudes = list(nan_sta.lat)
longitudes = list(nan_sta.lon)
labels = list(nan_sta.name)

for lat, lng, label in zip(latitudes, longitudes, labels):
	fo.Marker(
		location = [lat, lng], 
		popup = label,
		icon = fo.Icon(color='red', icon='heart')
	).add_to(station_map)

folium_static(station_map)
