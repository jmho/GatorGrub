import json
import random
import math
file_name = 'restaurants.json'

categories = set()
ambience = set()

#with open(file_name, encoding="utf8") as f:
#    for line in f:
#        business = json.loads(line)
#        cat = business["categories"].split(", ")
#        
#        for s in cat:
#            categories.add(s)
#    
#        
#    f.close()
#for s in categories:
    #print(s)


def dist(a,b):
    R = 6371.0
    coord1 = (a["latitude"] , a["longitude"])
    coord2 = (b["latitude"] , b["longitude"])
    latA = math.radians(coord1[0])
    lonA = math.radians(coord1[1])
    
    latB = math.radians(coord2[0])
    lonB = math.radians(coord2[1])
    
    dlon = lonB - lonA
    dlat = latB - latB

    a = math.sin(dlat / 2)**2 + math.cos(latA) * math.cos(latB) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R*c


def similarity(B1,B2):
    cat1 = B1["categories"].split(", ")
    cat2 = B2["categories"].split(", ")


    sum1 = 0
    sum2 = 0
    r = 'Restaurants'
    contR = False
    restP = .2
    if (r in cat1 and r in cat2):
        contR = True
    for s in cat1:
        if s in cat2:
            if (contR):
                if(s==r):
                    sum1 += restP
                else:
                    sum1 += 1 + (1-restP)/len(cat1)
            else:
                sum1 += 1
    for s in cat2:
        if s in cat1:
            if (contR):
                if(s==r):
                    sum2 += restP
                else:
                    sum2 += 1 + (1-restP)/len(cat2)
            else:
                sum1 += 1
    ave = (sum1/len(cat1)+ sum2/len(cat2))/2

    return ave

with open(file_name, encoding="utf8") as f:
    r1 = random.randrange(1,60000)
    for i in range(1,r1):
        first_line = f.readline()
    business1 = json.loads(first_line)

    print(business1["name"] + ": " +business1["categories"])
    for line in f:
        if line!=first_line:
            business2 = json.loads(line)
            sim = similarity(business1,business2)
            d = dist(business1,business2)
            if(sim>.7 and d < 35):
                print()
               
                print(business2["name"] + ": "+ str(sim) + " " +business2["categories"])
                #print(" ")
                #print(" ")

    

    
        
