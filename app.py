import streamlit as st
from config import connect_to_database
import pandas as pd
import plotly.express as px
from data_fetch import active_fire_data

from config import connect_to_database, get_current_location, manually_select_location, choose_on_map
conn, cursor = connect_to_database()



st.set_page_config(layout="centered")
with st.sidebar:
    st.title("Report a Fire 🔥")
    st.header("Enter the location")
    location_method = st.radio("Choose location method", ["Take current location", "Enter address manually", "Choose on map"])
    if location_method == "Take current location":
        lat, lon = get_current_location()
    if location_method == "Enter address manually":
        lat,lon = manually_select_location()
    if location_method == "Choose on map":
        lat, lon = choose_on_map()
    
    fire_intensity = st.selectbox("Fire Intensity ", ["High", "Medium", "Low"])
    population_density = st.selectbox("Population Density", ["High", "Medium", "Low"])
    sensitive_areas = st.text_area("Sensitive Areas ")

    fire_image = st.file_uploader("Fire Image", type=["jpg","png"])
    

    if st.button("Submit"):
        if fire_intensity and population_density and fire_image and lat and lon:
            st.write("Submitted Data:")
            st.write(f"Fire Intensity: {fire_intensity}")
            st.write(f"Population Density: {population_density}")
            st.write(f"Sensitive Areas: {sensitive_areas}")

            # Save data to MySQL
            query = "INSERT INTO submissions (latitude,longitude,address, fire_intensity, population_density, sensitive_areas, status) VALUES (%s,%s,%s, %s, %s, %s, %s)"
            cursor.execute(query, (lat, lon, "Adress to be defined",fire_intensity, population_density, sensitive_areas, "Active"))
            conn.commit()

            # Display success message
            st.success("Submission successful!")

            # Save image (if uploaded)
            if fire_image is not None:
                image_path = f"uploaded_images/{fire_image.name}"
                with open(image_path, 'wb') as image_file:
                    image_file.write(fire_image.read())
                st.image(fire_image, caption="Uploaded Fire Image", use_column_width=True)
                st.success("Image saved successfully!")

            else:
                st.warning("Please fill out all fields.")


        
            
        


st.title("BlazeGuards: Fire Management Solutions")
st.map(active_fire_data[['latitude','longitude']],use_container_width = True)

active_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'Active';"
operation_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'In-Operation';"
control_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'Controlled';"

col1, col2 = st.columns(2)
with col1:
    st.header("Fire Reports 🔔")
with col2:
     status = st.selectbox('Select Status',("Active","In-Operation","Controlled"))
if status == 'Active':
    cursor.execute(active_query)
    submissions = cursor.fetchall()
    # Create a list of dictionaries for the data
    data = []
    for submission in submissions:
        data.append({
            "Address": submission[0],
            "Fire Intensity": submission[1],
            "Population Density": submission[2],
            "Sensitive Areas": submission[3],
            "Status": submission[4]
        })
    # Display the data in a table
    st.table(data)

if status == 'In-Operation':
    cursor.execute(operation_query)
    submissions = cursor.fetchall()
    # Create a list of dictionaries for the data
    data = []
    for submission in submissions:
        data.append({
            "Address": submission[0],
            "Fire Intensity": submission[1],
            "Population Density": submission[2],
            "Sensitive Areas": submission[3],
            "Status": submission[4]
        })
    # Display the data in a table
    st.table(data)

if status == 'Controlled':
    cursor.execute(control_query)
    submissions = cursor.fetchall()
    # Create a list of dictionaries for the data
    data = []
    for submission in submissions:
        data.append({
            "Address": submission[0],
            "Fire Intensity": submission[1],
            "Population Density": submission[2],
            "Sensitive Areas": submission[3],
            "Status": submission[4]
        })
    # Display the data in a table
    st.table(data)

# Creating tabs
tab1, tab2 = st.tabs(['Past Fires','High Alerts'])

with tab1:
    past_data = pd.read_csv("2022_Nepal.csv")
    with st.container():
        st.title("🗺 Map View")

        fig = px.density_mapbox(past_data,
                                lat = 'latitude',
                                lon = 'longitude'
                                )
        fig.update_layout(title = 'Time Lapse of 2022')
        st.plotly_chart(fig) #Show Visualization