import requests
import pandas as pd
import schedule
import time
import threading
from datetime import date

today = date.today()
# Define API URL for Nasa Active Fire Data
nasa_url =f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/9799bfce0729259d1fd5f60d816aa38c/MODIS_NRT/world/1/{today}"

# function to fetch and process Nasa Active fire Data
def get_active_fire_data(api_url):
    response = requests.get(api_url)
    data = pd.read_csv(response.url)
    return data


# function to request Nasa Api and update active_fire_data
def request_nasa_api():
    global active_fire_data
    active_fire_data = get_active_fire_data(nasa_url)
    active_fire_data = active_fire_data[active_fire_data['confidence'] > 60] # Filter by Confidence > 65
    # print (active_fire_data)

# Initialise active_fire_Data
active_fire_data = get_active_fire_data(nasa_url)
active_fire_data = active_fire_data[active_fire_data['confidence'] > 60] # Filter by Confidence > 65
print (active_fire_data)

#Schedule Nasa Api request every  30 minutes
schedule.every(30).minutes.do(request_nasa_api)

# define a function to run scheduler
def run_scheduler():
   while True:
      schedule.run_pending()
      time.sleep(1)
 
# start schedule in seperate thread
schedule_thread = threading.Thread(target=run_scheduler)
schedule_thread.start()
