import requests
import json
import cgi
base_url = 'http://api.zippopotam.us/us/'

form = cgi.FieldStorage()

city =  form.getvalue('city')
state = form.getvalue('state')

r = requests.get(base_url+state.lower()+"/"+city.lower())
j = r.json()
try:
    coords = (float(j["places"][0]["latitude"]), float(j["places"][0]["longitude"]))
    print(coords)
except KeyError:
    print("Enter a real location!")
