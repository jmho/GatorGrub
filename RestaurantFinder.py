import requests
import json
import urllib
import math
import random
base_url = 'http://api.zippopotam.us/us/'
file_name = 'restaurants.json'


DISTANCE_LIMIT = 35
SIZE_LIMIT = 100

def convertToDist(coord1,coord2):
    R = 6371.0
    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R*c


    
def getEntries(coords):
    returnList = []
    with open(file_name, encoding='utf8') as infile:
        for line in infile:
            business = json.loads(line)
            buscoords = (business["latitude"] , business["longitude"])
            dist = convertToDist(coords,buscoords)
            if(dist<DISTANCE_LIMIT):
                returnList.append(business)
    infile.close()
    random.shuffle(returnList)
    if(len(returnList)>SIZE_LIMIT):
        del returnList[SIZE_LIMIT:]
    return returnList
            

def printResults(r,coord):
    for business in r:
        buscoords = (business["latitude"] , business["longitude"])
        dist = convertToDist(coord,buscoords)
        name = business["name"]
        print(name + ": " + str(dist) + " kms away")
def startProg():
    inp = ""
    address = ()
    inpCheck = False
    coords = ()
    while(inpCheck == False) or (len(address)!=2):
        
        inp = input("Enter an adress (City, State): ")
        try:
            address = inp.split(", ")
            r = requests.get(base_url+address[1].lower()+"/"+address[0].lower())
            j = r.json()
            try:
                coords = (float(j["places"][0]["latitude"]), float(j["places"][0]["longitude"]))
                inpCheck = True
            except KeyError:
                print("Enter a real location!")

        except IndexError:
            print("Make sure to use the correct format!")
    
    print("Searching for restaurants near " + inp)
    print(coords)
    printResults(getEntries(coords),coords)
startProg()
