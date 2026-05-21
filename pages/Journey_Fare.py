import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 1.loading the trained model
model = pickle.load(open("flight_rf.pkl", "rb"))

st.set_page_config(page_title="Journey Fare", layout="centered")
st.title("AIR FARE")
st.write("Know your Journey Price....")

# For UI Inputs
col1, col2 = st.columns(2)

with col1:
    # Date of Journey
    date_dep = st.date_input("Date of Journey", min_value=datetime.today())
    journey_day = date_dep.day
    journey_month = date_dep.month

    # Set default times only once using session_state
    if "default_dep" not in st.session_state:
        st.session_state.default_dep = datetime.now().time()
    if "default_arr" not in st.session_state:
        st.session_state.default_arr = (datetime.now() + timedelta(hours=2)).time()

    # Time inputs
    dep_time = st.time_input("Departure Time", value=st.session_state.default_dep)
    arrival_time = st.time_input("Arrival Time", value=st.session_state.default_arr)
    dep_hour = dep_time.hour
    dep_minute = dep_time.minute
    arrival_hour = arrival_time.hour
    arrival_minute = arrival_time.minute


with col2:
    # Duration handling with proper time difference
    dep_datetime = datetime.combine(date_dep, dep_time)
    arr_datetime = datetime.combine(date_dep, arrival_time)

    if arr_datetime < dep_datetime:
        arr_datetime += timedelta(days=1)  # Assume arrival is next day

    duration = arr_datetime - dep_datetime
    duration_hour = duration.seconds // 3600
    duration_minute = (duration.seconds % 3600) // 60

    st.write(f"Your Calculated Duration is: {duration_hour}h {duration_minute}m")

    if arr_datetime < dep_datetime:
        st.warning("⚠️ Arrival time is before departure! Adjusted to next day ⚠️")

    total_stops = st.selectbox("Number of Stops", ["Non-stop", "1 stop", "2 stops", "3 stops", "4 stops"])
    stops_mapping = {
        "Non-stop": 0,
        "1 stop": 1,
        "2 stops": 2,
        "3 stops": 3,
        "4 stops": 4
    }
    stops = stops_mapping[total_stops]

    airline = st.selectbox("Airline", [
        'IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara',
        'GoAir', 'Multiple carriers', 'Jet Airways Business',
        'Vistara Premium economy', 'Trujet', 'Multiple carriers Premium economy'
    ])

    source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai', 'Banglore'])
    destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata', 'Banglore'])


# One-hot encoding for categorical values
def encode_features(airline, source, destination):
    airline_list = ['Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
                    'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
                    'Trujet', 'Vistara', 'Vistara Premium economy']
    source_list = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
    destination_list = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']

    airline_encoded = [1 if a == airline else 0 for a in airline_list]
    source_encoded = [1 if s == source else 0 for s in source_list]
    destination_encoded = [1 if d == destination else 0 for d in destination_list]

    return airline_encoded + source_encoded + destination_encoded

# Predict button
if st.button("Get my Jorney Fare 💰"):
    input_features = [
        stops,
        journey_day,
        journey_month,
        dep_hour,
        dep_minute,
        arrival_hour,
        arrival_minute,
        duration_hour,
        duration_minute
    ] + encode_features(airline, source, destination)

    final_input = np.array([input_features])
    prediction = model.predict(final_input)

    st.success(f" Estimated Fare (Rounded off): ₹ {round(prediction[0], 2)}")

