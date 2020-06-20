import requests
import os

# https://pypi.org/project/geolocation-python/

def generate_map_png(lat, long):
    dir_name = 'temporal'
    try:
        # Create target Directory
        os.mkdir(dir_name)
        print("Directory ", dir_name, " Created ")
    except FileExistsError:
        print("Directory ", dir_name, " already exists")
    # gmaps_api_url = 'https://maps.googleapis.com/maps/api/staticmap?'
    # url = f'{gmaps_api_url}center={lat},{long}&zoom=12&size=400x400&key={API_key}'
    # urllib.request.urlretrieve(url, 'temporal/map.png')

