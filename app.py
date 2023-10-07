import streamlit as st








st.title("BlazeGuards: Fire Management Solutions")
st.map(use_container_width = True)

active_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'Active';"
operation_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'In-Operation';"
control_query = "SELECT address, fire_intensity, population_density, sensitive_areas, status FROM blazeguards.submissions where status = 'Controlled';"


