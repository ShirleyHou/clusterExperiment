
import itertools
import copy
import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt
OKBLUE = '\033[94m'
ENDC = '\033[0m'
OKGREEN = '\033[1m'

from htba import htb

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



roadMap = {}
itxMap = {}
with open("intersection_list.csv") as full_road_info:
    csv_reader = csv.DictReader(full_road_info)
    for row in csv_reader:
        idx = int(row['origin'])
        lon = float(row['lon'])
        lat = float(row['lat'])
        intersection = Intersection(idx,lon, lat)
        itxMap[idx] = intersection

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
import math
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

l = [len(Gc) for Gc in sorted(nx.strongly_connected_component_subgraphs(g),key=len, reverse=True)]

road_id_sorted = [r.idx for r in sorted(roadMap.values(), key = lambda x:-x.density)]
road_density = [r.density for r in sorted(roadMap.values(), key = lambda x:-x.density)]


color = 0
d = {}
COUNTER= 0
import heapq

visited = set()
for idx, road_id in enumerate(road_id_sorted):
    if road_id not in visited:

        q = [road_id]
        counter = 0
        current_cluster_rds = []
        current_cluster_nbs = set()
        visited.add(road_id)
        while len(q)>0:
            
            current_road_idx = q.pop(0)
            # if(current_road_idx in visited):
            #     print("WTF")
            visited.add(current_road_idx)
            for n in roadMap[current_road_idx].nb:
                if n not in visited: 
                    q.append(n)
                    # visited.add(n)
                
        color+=1

print("End")
        # current_sum_density = sum([r.density for r in current_cluster_rds])
        # current_average_density = current_sum_density/len(current_cluster_rds)


        # if counter<10 and len(current_cluster_nbs)>0:
            
        #     #current cluster jas < 10 elemnents. merge.
        #     closest_cluster_id = list(current_cluster_nbs)[0]
        #     min_density_diff = float('inf')
            
        #     for cluster_id in current_cluster_nbs:
        #         nb_density = d[cluster_id][0]
        #         if abs(nb_density-current_average_density)<min_density_diff:
        #             min_density_diff = abs(nb_density-current_average_density)
        #             closest_cluster_id = cluster_id
            
            
        #     d[closest_cluster_id][0] = (d[closest_cluster_id][0] * d[closest_cluster_id][1] + current_sum_density) / (d[closest_cluster_id][1] + len(current_cluster_rds))
        #     d[closest_cluster_id][1] += len(current_cluster_rds)
            
        #     for road in current_cluster_rds:
        #         road.color = closest_cluster_id
        # else: 
            
        #     d[color] = [current_average_density, len(current_cluster_rds)]

        #     color+=1
# sum_= 0
# for i in d:
#     print(d[i])
#     sum_+=d[i][1]
# print(sum_)
# D = {}
# for i in roadMap.values():
#     if i.color not in D:
#         D[i.color]=1
#     else:
#         D[i.color]+=1


# density = {}

# for v in roadMap.values():
#     if v.color not in density:
#         density[v.color]=v.density
#     else:
#         density[v.color]+=v.density


# for v in density.keys():
#     density[v] = float(density[v])/D[v]

# # for i in sorted(density):
# #     print(i, density[i], D[i])
# # print(len(density)) 


# with open("bfs_cluster.csv", 'w') as out:
#     out.write("road_id,cluster_id\n")
#     for i in roadMap.keys():
#         out.write(str(i)+","+str(roadMap[i].color)+"\n")
    
