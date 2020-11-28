import requests
import json

base_url = 'http://api.zippopotam.us/us/'

city = input("Enter a City:  ")
state = input("Enter a State: ")



r = requests.get(base_url+state.lower()+"/"+city.lower())
j = r.json()
try:
    coords = (float(j["places"][0]["latitude"]), float(j["places"][0]["longitude"]))
    print(coords)
except KeyError:
    print("Enter a real location!")


