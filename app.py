import streamlit as st
from config import connect_to_database
import pandas as pd
import requests
import plotly.express as px
from data_fetch import active_fire_data 
import folium
from streamlit.components.v1 import html


from config import connect_to_database, get_current_location, manually_select_location, choose_on_map
conn, cursor = connect_to_database()

# Function to get location name from latitude and longitude
def get_location_name(lat, lon):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key=a7b40639e1f84a389ea1a2ea8e0b69c5"
    response = requests.get(url)
    data = response.json()
    
    if 'results' in data and len(data['results']) > 0:
        components = data['results'][0]['components']
        country = components.get('country', '')
        return f"{country}"
    else:
        return "Location information not available"

st.set_page_config(layout="centered")
with st.sidebar:
    st.title("Report a Fire 🔥")
    st.header("Enter the location")
    location_method = st.radio("Choose location method", ["Take current location",  "Choose on map"])
    if location_method == "Take current location":
        lat, lon, address= get_current_location()
    
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
            cursor.execute(query, (lat, lon, address,fire_intensity, population_density, sensitive_areas, "Active"))
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

df = active_fire_data 
# Define a function to assign colors based on brightness
def assign_color(brightness):
    if brightness > 365:
        return 'red'
    elif 250 <= brightness <= 365:
        return 'blue'
    else:
        return 'green'

map_width = 750  
map_height = 600

# Create a base map
m = folium.Map(location=[0, 0], zoom_start=2)



# Iterate through your dataset and add markers to the map
for index, row in df.iterrows():
    lat, lon, brightness = row['latitude'], row['longitude'], row['brightness']
    color = assign_color(brightness)
    folium.Circle(
        location=[lat, lon],
        radius=5,
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)


# Render the map using components
html_string = m.get_root().render()
# html(html_string)
st.components.v1.html(html_string, width=map_width, height=map_height)

# st.map(active_fire_data[['latitude','longitude']],use_container_width = True)

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
                                lat ='latitude', 
                                lon ='longitude', 
                                z = 'brightness', 
                                color_continuous_scale  = 'Viridis',
                                range_color = [200,520],
                                radius = 5,
                                center = dict(lat=28.3949, lon=84.1240), 
                                zoom = 5,
                                mapbox_style = "carto-positron",
                                animation_frame = "acq_date",
                                )
        fig.update_layout(title = 'Time Lapse of 2022')
        st.plotly_chart(fig) #Show Visualization



with tab2:
    # Show "Fatal Zones" (locations with highest brightness) on the right side
    top_fatal_zones = active_fire_data.nlargest(10, 'brightness')
    top_fatal_zones['Location'] = top_fatal_zones.apply(lambda row: get_location_name(row['latitude'], row['longitude']), axis=1)
    
    # Remove index and display unique countries
    top_fatal_zones = top_fatal_zones[['Location', 'brightness','confidence']].reset_index(drop=True)
    # top_fatal_zones = top_fatal_zones.drop_duplicates(subset=['Location'])
    
    st.title('⚠ High Alert Regions')
    st.table(top_fatal_zones[['Location', 'brightness','confidence']])

#Expander to show Educational Content

st.title('📖 Quick informations about fire and how to fight them.')
# Create an accordion to organize content
with st.expander("Types of Fires"):
    st.write("""
    Fires are classified into different types based on the materials that are burning. 
    Here are the main types of fires:
    
    - **Class A Fires:** These involve ordinary combustibles like wood, paper, and cloth.
    
    - **Class B Fires:** These involve flammable liquids or gases like gasoline, oil, and propane.
    
    - **Class C Fires:** These involve electrical equipment and should not be extinguished with water.
    
    - **Class D Fires:** These involve combustible metals like magnesium, sodium, or potassium.
    
    - **Class K Fires:** These involve cooking oils or fats in commercial kitchens.
    """)

with st.expander("Ways to Fight Fires"):
    st.write("""
    The appropriate method to fight a fire depends on its type. Here are some common ways to combat fires:

    - **Water:** Effective for Class A fires, but should not be used on electrical or grease fires.
    
    - **Fire Extinguishers:** Each type of fire has a specific extinguisher type (A, B, C, D, or K).
    
    - **Carbon Dioxide (CO2):** Suitable for Class B and C fires, as it doesn't leave residue.
    
    - **Dry Chemical Powder:** Versatile and can be used on Class A, B, and C fires.
    
    - **Wet Chemical:** Designed for Class K fires, often found in commercial kitchens.
    
    - **Fire Blankets:** Used to smother small fires, particularly in kitchens.
    
    - **Sand or Dirt:** Can be used in the absence of an extinguisher for Class A fires.
    """)
cursor.close()
conn.close()