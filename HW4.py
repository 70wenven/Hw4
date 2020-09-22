#Kan Tuekthaew 6030802621
#GeoDataSci
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import folium as fo
from streamlit_folium import folium_static
import geopandas as gp


select_date = st.sidebar.selectbox('Date :' , ['2019/01/01','2019/01/02','2019/01/03','2019/01/04','2019/01/05'])

if select_date=='2019/01/01' :
    DATA_URL = ( "https://raw.githubusercontent.com/70wenven/Hw4/master/20190101.csv")
elif select_date=='2019/01/02':
    DATA_URL =  ( "https://raw.githubusercontent.com/70wenven/Hw4/master/20190102.csv")
elif select_date=='2019/01/03':
    DATA_URL =( "https://raw.githubusercontent.com/70wenven/Hw4/master/20190103.csv")
elif select_date=='2019/01/04':
    DATA_URL =( "https://raw.githubusercontent.com/70wenven/Hw4/master/20190104.csv")
elif select_date=='2019/01/05':
    DATA_URL =( "https://raw.githubusercontent.com/70wenven/Hw4/master/20190105.csv")
st.title("Hw4_GeoDataSci")
st.markdown("Uber in Bangkok")


# import data
DATE_TIME = "timestart"
st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME],format='%d/%m/%Y %H:%M')
    return data
data = load_data(100000)
################## Set GEOMETRY ####################

hour = st.sidebar.slider("Hour to look at", 0, 23,step=2)
data = data[data[DATE_TIME].dt.hour == hour]


if st.checkbox("Show raw data", False):
    '## Raw data at %sh' % hour,data


crs = "EPSG:4326"
geometry = gp.points_from_xy(data.lonstartl,data.latstartl)
geo_df  = gp.GeoDataFrame(data,crs=crs,geometry=geometry)

#################### Create MAP ##########################
st.subheader("Map at %i:00" %hour)
longitude = 100.524186 #longitude TH
latitude = 13.736417 #latitude TH
station_map = fo.Map(
                location = [latitude, longitude], 
                zoom_start = 10)

latitudes = list(data.latstartl)
longitudes = list(data.lonstartl)
time = list(data.timestart)
labels = list(data.n)


for lat, lon,t, label in zip(latitudes, longitudes,time, labels):
    if data.timestart[label].hour==hour and data.timestart[label].year!=2018:
        fo.Marker(
          location = [lat, lon], 
          popup = [label,lat,lon,t],
          icon = fo.Icon(color='pink', icon='map-marker')
         ).add_to(station_map)
folium_static(station_map)

#################### Create GEO DATA ########################
st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data["latstartl"]), np.average(data["lonstartl"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lonstartl", "latstartl"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

################## create GRAPH ###########################
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)
