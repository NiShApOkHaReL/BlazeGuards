import streamlit as st

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
            
        







st.title("BlazeGuards: Fire Management Solutions")
st.map(use_container_width = True)

active_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'Active';"
operation_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'In-Operation';"
control_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'Controlled';"


