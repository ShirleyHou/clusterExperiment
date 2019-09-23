
import itertools
import copy
import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt
OKBLUE = '\033[94m'
ENDC = '\033[0m'
OKGREEN = '\033[1m'
import jenkspy
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
# with open("intersection_list.csv") as full_road_info:
#     csv_reader = csv.DictReader(full_road_info)
#     for row in csv_reader:
        # outgoing_str = row['outgoing'].split(' ')
        # incoming_str = row['incoming'].split(' ')
        # outgoing_intersection_edge = {}
        # for i in outgoing_str:
        #     outgoing_list = i.split('-')
        #     node, edge = int(outgoing_list[0]), int(outgoing_list[1])
        #     origin[]
        # incoming_intersection_edge = {}
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
print(l)
print(len(roadMap))
road_id_sorted = [r.idx for r in sorted(roadMap.values(), key = lambda x:-x.density)]
road_density = [r.density for r in sorted(roadMap.values(), key = lambda x:-x.density)]

breaks = jenkspy.jenks_breaks(road_density, nb_class=4)
#breaks = [0]+htb(road_density)
#print(breaks)
def process(value):
    global breaks
    n = len(breaks)-1
    while(value<breaks[n] and n>0):
        n-=1
    return n
# processed = {}
# for i in road_density:
#     val = process(i)
#     print(i, val)
#     processed[val] = processed.get(val,0)+1
# print(processed)
# print(breaks)
# plt.figure(figsize = (10,8))
# hist = plt.hist(road_density, bins=100, align='left', color='g')
# for b in breaks:
#     plt.vlines(b, ymin=0, ymax = max(hist[0]))
# plt.show()


def updatek(k,road_id,x_average_k, segma_k):
    
    new_x_k = roadMap[road_id].density
    new_x_avg_k = ((k-1)*x_average_k+new_x_k)/(k)
    new_segma_k = ((k-1)*(segma_k)+(new_x_k-new_x_avg_k)*(new_x_k-x_average_k))/k
    #print("segma ",k,x_k, new_x_k, new_x_avg_k,new_segma_k)
    # diff = (new_segma_k - segma_k)/(new_x_k - x_k)
    # print(diff)   
    # print(math.sqrt(abs(new_segma_k)), new_x_avg_k)              
    if abs(math.sqrt(abs(new_segma_k)) - math.sqrt(abs(segma_k)))> 1:
        return -1, k+1, new_x_avg_k, new_segma_k
    return 1, k+1, new_x_avg_k, new_segma_k

color = 0
d = {}


import heapq
for idx, road_id in enumerate(road_id_sorted):
    road = roadMap[road_id]
    
    if road.color==-1:

        q = [(-road.density, road.idx, road)]
        heapq.heapify(q)
        #road.color = color
        
        k = 1
        avg = road.density
        seg = 0

        #origin_density_level = process(road.density)
        counter = 0
        current_cluster_rds = []
        current_cluster_nbs = set()
        visited = set()
        visited.add(road)
        while(q):
            
            current_road = heapq.heappop(q)[2]

            res, k_temp, avg_temp, seg_temp = updatek(k, current_road.idx, avg, seg)
            
            if res!=-1 or counter<10:
                    
                current_cluster_rds.append(current_road)
                counter+=1
                k, avg, seg= k_temp, avg_temp, seg_temp
                
                nbs = [roadMap[n] for n in current_road.nb]
                nbs = sorted(nbs, key=lambda x: -x.density)
                nbs_index = [z.idx for z in nbs]
                
                
                for n in nbs_index:#current_road.nb:
                    nb_road = roadMap[n]
                    if nb_road.color==-1 and nb_road not in visited: #and process(nb_road.density) == origin_density_level:
                        heapq.heappush(q, (-nb_road.density,nb_road.idx, nb_road))
                        visited.add(nb_road)
                    elif nb_road.color!=-1 and nb_road.color!=color:
                        current_cluster_nbs.add(nb_road.color)
            

        current_sum_density = sum([r.density for r in current_cluster_rds])
        current_average_density = current_sum_density/len(current_cluster_rds)

        
        if len(current_cluster_rds)< 10 and len(current_cluster_nbs)>0:
            #current cluster jas < 10 elemnents. merge.
            closest_cluster_id = list(current_cluster_nbs)[0]
            min_density_diff = float('inf')
            
            for cluster_id in current_cluster_nbs:
                nb_density = d[cluster_id][0]
                if abs(nb_density-current_average_density)<min_density_diff:
                    min_density_diff = abs(nb_density-current_average_density)
                    closest_cluster_id = cluster_id
            
            
            d[closest_cluster_id][0] = (d[closest_cluster_id][0] * d[closest_cluster_id][1] + current_sum_density) / (d[closest_cluster_id][1] + len(current_cluster_rds))
            d[closest_cluster_id][1] += len(current_cluster_rds)
            for road in current_cluster_rds:
                road.color = closest_cluster_id
        else: 
            d[color] = [current_average_density, len(current_cluster_rds)]
            color+=1
sum_ = 0
for i in d:
    print(d[i])
    sum_+=d[i][1]
print(sum)
D = {}
for i in roadMap.values():
    if i.color not in D:
        D[i.color]=1
    else:
        D[i.color]+=1


density = {}

for v in roadMap.values():
    if v.color not in density:
        density[v.color]=v.density
    else:
        density[v.color]+=v.density


for v in density.keys():
    density[v] = float(density[v])/D[v]
    
for i in sorted(density):
    print(i, density[i], D[i])
print(len(density))

with open("bfs_cluster.csv", 'w') as out:
    out.write("road_id,cluster_id\n")
    for i in roadMap.keys():
        out.write(str(i)+","+str(roadMap[i].color)+"\n")
    
