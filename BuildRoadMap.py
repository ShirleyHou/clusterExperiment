
import itertools
import copy
import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt
import jenkspy
import math
from htba import htb
from Road import Road, Intersection

def getIntersectionMap():
    itxMap = {}
    with open("intersection_list.csv") as full_road_info:
        csv_reader = csv.DictReader(full_road_info)
        for row in csv_reader:
            idx = int(row['origin'])
            lon = float(row['lon'])
            lat = float(row['lat'])
            intersection = Intersection(idx,lon, lat)
            itxMap[idx] = intersection
    return itxMap
    
def getRoadMap():
    roadMap = {}
    with open("training_morning_road_pickup_lon_lat.csv") as road_info:
        csv_reader = csv.DictReader(road_info)
        for row in csv_reader:
            roadId = int(row['roadId'])
            pickup = int(row['pickup_count'])
            dropoff = int(row['dropoff_count'])
            lon = float(row['lon'])
            lat = float(row['lat'])
            new_road = Road(roadId, pickup, dropoff, lon, lat)
            roadMap[roadId] = new_road

    with open("edgeList.txt", mode='r') as edge_info:
        with open("density_test_modified.txt", mode='w') as out:
            csv_reader = csv.DictReader(edge_info)
            for row in csv_reader:
                roadId = int(row['roadId'])
                roadLength = float(row['length'])
                roadInfo = roadMap.get(roadId, None)

                if roadInfo==None:
                    from_location = [float(row['from_node_lon']),float(row['from_node_lat'])]
                    to_location = [float(row['to_node_lon']),float(row['to_node_lat'])]
                    default_centroid = [(from_location[0]+to_location[0])/2, (from_location[1]+to_location[1])/2]
                    new_road = Road(roadId, 0, 0, default_centroid[0], default_centroid[1])
                    roadMap[roadId] = new_road
                r_obj = roadMap[roadId]
                r_obj.length = roadLength
                r_obj.density = max(r_obj.density, r_obj.pickup/roadLength)
                out.write(str(roadId)+","+str(r_obj.density)+"\n")
            
    # Create empty graph
    g = nx.DiGraph()

    with open("Road_adj_map.csv") as road_adj:
        csv_reader = csv.DictReader(road_adj)
        own_id_set = set()
        for row in csv_reader:
            own_id = int(row['roadId'])
            own_id_set.add(own_id)
            to_ids = [int(i) for i in row['downstream'].split(' ') if i != own_id and i!='']
            from_ids = [int(i) for i in row['upstream'].split(' ') if i != own_id and i!='']

            key = own_id
            for i in set(from_ids+to_ids):
                roadMap[own_id].nb.add(i)
                roadMap[i].nb.add(own_id)

            for i in set(from_ids):
                
                g.add_edge(i, own_id)
                
            for i in set(to_ids):
                g.add_edge(own_id, i)
        diff_set = set()
        for i in roadMap:
            if i not in own_id_set:
                diff_set.add(i)
        for i in diff_set:
            roadMap.pop(i, None)

    connected_component = [len(Gc) for Gc in sorted(nx.strongly_connected_component_subgraphs(g),key=len, reverse=True)]
    assert(len(connected_component) == 1)
    assert(connected_component[0] == len(roadMap))
    return roadMap

def check_cluster_results(roadMap):
    D = {}
    for i in roadMap.values():
        if i.cluster_id not in D:
            D[i.cluster_id]=1
        else:
            D[i.cluster_id]+=1

    density = {}

    for v in roadMap.values():
        if v.cluster_id not in density:
            density[v.cluster_id]=v.density
        else:
            density[v.cluster_id]+=v.density

    for v in density.keys():
        density[v] = float(density[v])/D[v]
        
    for i in sorted(density):
        print("{} {:.3f} {}".format(i, density[i], D[i]))
    print(len(density))