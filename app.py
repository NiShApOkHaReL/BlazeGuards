import streamlit as st
from config import connect_to_database

conn, cursor = connect_to_database()






st.title("BlazeGuards: Fire Management Solutions")
st.map(use_container_width = True)

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
