import json
import random
import math
import numpy as np
from heapq import heapify, heappush, heappop
import networkx as nx
import matplotlib
matplotlib.rcParams['interactive'] == True
import matplotlib.pyplot as plt

import time

dataset_file = 'RESTAURANTS.FINAL.final.json'
param_file_name = 'params.json'
STAR_THRESHOLD = 3.0
SCALER = 20
REVIEW_THRESHOLD = 30
param_f = open(param_file_name,encoding='utf8')

p_json = json.loads(param_f.readline())

data_f = open(dataset_file,encoding='utf8')

d_json = json.loads(data_f.readline())


def dist(b1,b2):
    R = 6371.0
    latA = math.radians(b1["latitude"])
    lonA = math.radians(b1["longitude"])
    
    latB = math.radians(b2["latitude"])
    lonB = math.radians(b2["longitude"])
    
    dlon = lonB - lonA
    dlat = latB - latA
    
    a = math.sin(dlat / 2)**2 + math.cos(latA) * math.cos(latB) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R*c
def sigmoid(x):
    return 1/(1+np.exp(-x/SCALER))
def scaleFactor(nor,star):
    revdef = nor-REVIEW_THRESHOLD
    stardef = star - STAR_THRESHOLD
    mult = 1
    if(stardef<0):
        mult = -1
    return mult*(2*sigmoid(nor-REVIEW_THRESHOLD)-1)
def likeability(quizR,business):
    
   
    #RATING SCORE
    busRating = business["stars"]
    busRevCount = business["review_count"]
    scale = scaleFactor(busRevCount,busRating)
    rating = (busRating + scale)/6

    #CATEGORY SCORE
    buscat = business["categories"]
    quizcat = quizR["categories"]
    
    sum1 = 0
    sum2 = 0
    r = 'Restaurants'
    f = 'Food'
    contR = False
    l1 = len(buscat)
    l2 = len(quizcat)

    if(f in buscat and len(buscat) > 1):
        l1 = l1 -1
    if(f in quizcat and len(quizcat)> 1):
        l2 = l2 -1
    restP = .2
    if (r in buscat and r in quizcat):
        contR = True

    
    for s in buscat:
        if(s!=f):
            if s in quizcat:
                if (contR):
                    if(s==r):
                        sum1 += restP
                    else:
                        sum1 += 1 + (1-restP)/(l1-1)
                else:
                    sum1 += 1
    for s in quizcat:
        if(s!=f):
            if s in buscat:
                if (contR):
                    if(s==r):
                        sum2 += restP
                    else:
                        sum2 += 1 + (1-restP)/(l2-1)
                else:
                    sum1 += 1
    catScore = (sum1/l1+ sum2/l2)/2

    #ATTRIBUTES SCORE
    busatb = business["attributes"]
    quizatb = quizR["attributes"]
    atbScore = 0
    for line in quizatb:
        if line in busatb:
            if quizatb[line] == busatb[line]:
                atbScore += 1
    atbScore = atbScore/len(quizatb)
        
    #DIST SCORE

    d = dist(quizR,business)

    distScore = 2*sigmoid(-1*d/2)
    

    return .7*(.2*rating+.5*catScore+.3*atbScore)+.3*distScore
def findRest(params,dat,n,family):
    rest = dict()
    heap = []
    scores = set()
    parentName = ""
    try:
        parentName = params["name"]
    except KeyError:
        pass

    #use this to make sure we avoid adding two restaurants of the same name unless one is better than the other
    #limits the likelyhood of duplicates
    nameMap = dict()
    for business in dat:
        if business["name"] not in family:
            score = likeability(params,business)
            if (score not in scores) and (business["name"] != parentName) and (business['name'] not in nameMap or nameMap[business["name"]] < score):
                scores.add(score)
                heappush(heap, (score,business))
                nameMap[business["name"]] = score
                if len(heap) > n:
                    heappop(heap)
    family.clear()
    for h in heap:
        family.add(h[1]["name"])
    return heap
        
def makeGraph(param,dat):
    print(param["categories"])
    adjMap = dict()
    nodes = dict()
    family = set()
    initSet = findRest(param,dat,1,family)
    
    for suggestion in initSet:
        p1 = suggestion[1]["business_id"]
        nodes[p1] = suggestion
        adjMap[p1] = []
        set2 = findRest(suggestion[1],dat,4,family)
        for suggestion2 in set2:
            p2 = suggestion2[1]["business_id"]
            nodes[p2] = suggestion2
            adjMap[p1].append(p2)
            if p2 not in adjMap:
                adjMap[p2] = [] 
            set3 = findRest(suggestion2[1],dat,4,family)
            for suggestion3 in set3:
                p3 = suggestion3[1]["business_id"]
                nodes[p3] = suggestion3
                adjMap[p2].append(p3)
                if p3 not in adjMap:
                    adjMap[p3] = []
                set4 = findRest(suggestion3[1],dat,4,family)
                for suggestion4 in set4:
                    p4 = suggestion4[1]["business_id"]
                    nodes[p4] = suggestion4
                    adjMap[p3].append(p4)
                    #if p4 not in adjMap:
                        #adjMap[p4] = []
    return (adjMap,nodes)
        
def drawGraph(raw_graph_data):

    vertices = raw_graph_data[1]
    adjMap = raw_graph_data[0]

    graph_data = dict()
    names = set()
    nameMap = dict()

    for v in vertices:
        name = vertices[v][1]["name"]
        if name in names: #add to set and add as normal
            i = 2
            newname = str(name)
            while newname in names:
                newname = name + " " +  str(i)
                i +=1
            name = newname
        
        names.add(name)
        nameMap[v] = name

    for f in adjMap:
        from_name = nameMap[f]
        graph_data[from_name] = []
        for t in adjMap[f]:
            to_name = nameMap[t]
            graph_data[from_name].append(to_name)

    G = nx.Graph(graph_data)
    nx.draw_networkx(G, with_labels = True, node_color = "c", edge_color = "k", font_size = 2)

    plt.axis('off')
    plt.draw()
    plt.show()



drawGraph(makeGraph(p_json,d_json))
