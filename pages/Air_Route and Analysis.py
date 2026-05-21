import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Shortest Route Visualizer", layout="wide")
st.title(" Real-Time Shortest Air route Visualizer")

# Cities list
city_list = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Kochi", "Jaipur"]
col1, col2 = st.columns(2)
source_city = col1.selectbox("🛫 Source City", city_list)
destination_city = col2.selectbox("🛬 Destination City", [c for c in city_list if c != source_city])

# Getting coordinates for map
geolocator = Nominatim(user_agent="flight_route_app")
source_loc = geolocator.geocode(source_city)
dest_loc = geolocator.geocode(destination_city)

source_coords = (source_loc.latitude, source_loc.longitude)
dest_coords = (dest_loc.latitude, dest_loc.longitude)

# Function for fetching APIs 
def get_weather(city):
    api_key = "a491d8b513c19f0528187218f0fa28e1" # From openweathermap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    resp = requests.get(url).json()
    # st.write(resp) (If you want to see exact response or error in fetching APIs)
    weather = {
        "temp": resp["main"]["temp"],
        "desc": resp["weather"][0]["description"],
        "wind": resp["wind"]["speed"]
    }
    return weather

source_weather = get_weather(source_city)
dest_weather = get_weather(destination_city)

# Map Plotting
m = folium.Map(location=[(source_coords[0] + dest_coords[0]) / 2,
                         (source_coords[1] + dest_coords[1]) / 2],
               zoom_start=5)

# Add markers
folium.Marker(source_coords, tooltip=f"Source: {source_city}",
              popup=f"{source_city}\n🌡️ {source_weather['temp']}°C, 🌬️ {source_weather['wind']} m/s").add_to(m)

folium.Marker(dest_coords, tooltip=f"Destination: {destination_city}",
              popup=f"{destination_city}\n🌡️ {dest_weather['temp']}°C, 🌬️ {dest_weather['wind']} m/s").add_to(m)

# Draw line
folium.PolyLine([source_coords, dest_coords], color="blue", weight=3, tooltip="Shortest Route").add_to(m)

# Show map
st.subheader("🗺️ Route Visualization")
st_data = st_folium(m, width=800)

# Weather Information
col3, col4 = st.columns(2)
with col3:
    st.metric(label=f"{source_city} Temperature", value=f"{source_weather['temp']}°C")
    st.write(f"Condition: {source_weather['desc'].title()}")
    st.write(f"Wind Speed: {source_weather['wind']} m/s")

with col4:
    st.metric(label=f"{destination_city} Temperature", value=f"{dest_weather['temp']}°C")
    st.write(f"Condition: {dest_weather['desc'].title()}")
    st.write(f"Wind Speed: {dest_weather['wind']} m/s")

