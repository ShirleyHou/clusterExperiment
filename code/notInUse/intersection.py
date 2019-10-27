
# import itertools
# import copy
import csv
# import sys
# import networkx as nx
# import matplotlib.pyplot as plt
# OKBLUE = '\033[94m'
# ENDC = '\033[0m'
# OKGREEN = '\033[1m'
# import jenkspy
# from htba import htb

class Road:
    def __init__(self, idx, pickup, dropoff,lon, lat):
        self.idx = idx
        self.pickup = pickup
        self.dropoff = dropoff
        self.lon = lon
        self.lat = lat
        self.nb = set()
        self.length = 0
        self.density = 0.0001
        self.color = -1
    def __str__(self):
        return "{0:.2f}".format(self.density)

class Intersection:
    def __init__(self, idx, lon, lat):
        self.idx = idx
        self.lon = lon
        self.lat = lat
        self.incoming = {}
        self.outgoing = {}
    def __str__(self):
        return str(self.idx)




roadMap = {}
itxMap = {}
with open("intersection_list.csv") as full_road_info:
    csv_reader = csv.DictReader(full_road_info)
    for row in csv_reader:
        idx = int(row['origin'])
        lon = float(row['lon'])
        lat = float(row['lat'])
        intersection = Intersection(idx, lon, lat)
        itxMap[idx] = intersection
with open("intersection_list.csv") as full_road_info:
    csv_reader = csv.DictReader(full_road_info)
    for row in csv_reader:
        idx = int(row['origin'])
        outgoing_str = row['outgoing'].strip().split(' ')
        incoming_str = row['incoming'].strip().split(' ')
        outgoing_intersection_edge = {}

        
        for i in outgoing_str:
            outgoing_list = i.split('-')
            node, edge = int(outgoing_list[0]), int(outgoing_list[1])
            itxMap[idx].outgoing[node] = edge
            default_location=[(itxMap[node].lon+itxMap[idx].lon)/2, (itxMap[node].lat+itxMap[idx].lat)/2]
            if edge not in roadMap:
                roadMap[edge] = Road(edge,0,0, default_location[0], default_location[1])

        for i in incoming_str:
            incoming_list = i.split('-')
            node, edge = int(incoming_list[0]), int(incoming_list[1])
            itxMap[idx].incoming[node] = edge
            default_location=[(itxMap[node].lon+itxMap[idx].lon)/2, (itxMap[node].lat+itxMap[idx].lat)/2]
            if edge not in roadMap:
                roadMap[edge] = Road(edge,0,0, default_location[0], default_location[1])
print(sorted(roadMap))

print(len(roadMap))