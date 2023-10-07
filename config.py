import streamlit as st
import mysql.connector
import requests

def connect_to_database():
    conn = mysql.connector.connect(
        host = "localhost",
        database = "blazeguards",
        user = "root",
        password = ""
    )
    cursor = conn.cursor()
    return conn, cursor

def choose_on_map():
    st.write("Click on the map to Choose a Location")  
       # Initialize latitude and longitude with default values
    lat = 0.0
    lon = 0.0

    iframe_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Current Location Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
            crossorigin=""/>
        <!-- Make sure you put this AFTER Leaflet's CSS -->
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
            integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
            crossorigin=""></script>
        <style>
            #map {
                height: 400px;
            }
        </style>
    </head>
    <body>
        <h1 class="text-center">Current Location Map</h1>
        
        <div id="map"></div>

        <script>
            var map = L.map('map').setView([28.6139, 84.2096], 7);

            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            var popup = L.popup();

            function onMapClick(e) {
                popup
                    .setLatLng(e.latlng)
                    .setContent("You clicked the map at " + e.latlng.toString())
                    .openOn(map);

                // Update the hidden input fields with new values
                var lat = e.latlng.lat;
                var lon = e.latlng.lng;               
                
            }

            map.on('click', onMapClick);
        </script>
    </body>
    </html>
    """

    st.components.v1.html(iframe_html, width=800, height=600)

    # Display text input fields for latitude and longitude
    lat = st.text_input("Latitude", value=str(lat), key="latitude")
    lon = st.text_input("Longitude", value=str(lon), key="longitude")

    return lat, lon
             

# Function to handle "Manually" method

def manually_select_location():
    st.write("You chose 'Manually'")
    location_name = st.text_input("Enter a location:")

    latitude = None
    longitude = None
    
    if st.button("Geocode"):
        if location_name:
            # Geocode the entered location
            base_url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": location_name,
                "format": "json",
            }

            response = requests.get(base_url, params=params)
            data = response.json()

            if data:
                first_result = data[0]  # Take the first result (most relevant)
                latitude = float(first_result["lat"])
                longitude = float(first_result["lon"])
                
            else:
                st.write("Unable to geocode the address.")
        else:
            st.write("Please enter a location.")

    return latitude, longitude
 

# Function to handle "Current Location" method

def get_current_location():    
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        if 'loc' in data:
            latitude, longitude = data['loc'].split(',')            
            return float(latitude), float(longitude)
    except Exception as e:
        print(f"An error occurred: {e}")

