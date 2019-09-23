
import itertools
import copy
import networkx as nx
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import utm
class Road:
    def __init__(self, idx, pickup, dropoff,lon, lat):
        self.idx = idx
        self.pickup = pickup
        self.dropoff = dropoff
        self.lon = lon
        self.lat = lat
        self.nb = []
        self.length = 0
        self.density = 0
        self.colored = -1
        self.from_node = -1
        self.to_node = -1
        
    def __str__(self):
        return str(self.idx)

# Create empty graph
g = nx.DiGraph()
lats = set()
longs = set()

roadMap = {}

node_positions = {}
with open("edgeList.txt", mode='r') as edge_info:
    csv_reader = csv.DictReader(edge_info)
    for row in csv_reader:
        roadId = int(row['roadId'])
        roadLength = float(row['length'])
        from_location = [float(row['from_node_lon']),float(row['from_node_lat'])]
        to_location = [float(row['to_node_lon']),float(row['to_node_lat'])]
        default_centroid = [(from_location[0]+to_location[0])/2, (from_location[1]+to_location[1])/2]
        roadMap[roadId]= Road(roadId, 0, 0, default_centroid[0], default_centroid[1])
        r_obj = roadMap[roadId]
        r_obj.length = roadLength
        r_obj.from_node = int(row['from_node'])
        r_obj.to_node = int(row['to_node'])
        #r_obj.colored = process(r_obj.density)

        def project(lon, lat):
            u = utm.from_latlon(lat, lon)
            #print(u)
            lat = u[1]
            lon = u[0]
            return (lon, lat)

        node_positions[int(row['from_node'])] = project(float(row['from_node_lon']),float(row['from_node_lat']))
print([len(Gc) for Gc in sorted(nx.strongly_connected_component_subgraphs(g),key=len, reverse=True)])
print(len(g.edges()))

with open("training_morning_road_pickup_lon_lat.csv") as road_info:
    csv_reader = csv.DictReader(road_info)
    for row in csv_reader:
        
        roadId = int(row['roadId'])
        if roadId not in roadMap:
            continue
        pickup = int(row['pickup_count'])
        dropoff = int(row['dropoff_count'])
        lon = float(row['lon'])
        lat = float(row['lat'])
        # new_road = Road(roadId, pickup, dropoff, lon, lat)
        road_obj = roadMap.get(roadId, None)
        
        if road_obj:
            road_obj.pickup = pickup
            road_obj.dropoff = dropoff
            road_obj.lon = lon
            road_obj.lat = lat

        if road_obj.length!=0:
            
            road_obj.density = road_obj.pickup/road_obj.length
        else:
            print("how many")

with open("bfs_cluster.csv", 'r') as inject_cluster_id:
    csv_reader = csv.DictReader(inject_cluster_id)
    max_id = -1
    for row in csv_reader:
        idx = int(row['road_id'])
        cluster_idx = int(row['cluster_id'])
        if idx in roadMap:
            roadMap[idx].colored = cluster_idx
            
            if max_id<cluster_idx:
                max_id = cluster_idx
    for road in roadMap.values():
        if road.colored==-1:
            road.colored=max_id

for r_obj in roadMap.values():
    if(r_obj.from_node!=-1 and r_obj.to_node!=-1):

        g.add_edge(r_obj.from_node, r_obj.to_node, attr_dict={"idx":r_obj.idx, "density":r_obj.density, "lon":r_obj.lon,"lat":r_obj.lat,"length":r_obj.length, "color":r_obj.colored})


classification = {}
def process(f):
    global classification
    import math
    if f<10:
        res = math.floor(f)
        classification[res] = classification.get(res,0)+1
        return res
    else:
        classification[10] = classification.get(10,0)+1
        return 10
    





        
def plot_cluster():
    import math
    road_colors = [i.colored for i in roadMap.values()]

    min_road_color = min(road_colors)
    max_road_color = max(road_colors)

    edge_colors = []

    jet = cm = plt.get_cmap('brg') 
    print(min_road_color, max_road_color)
    cNorm  = colors.Normalize(vmin=min_road_color, vmax=max_road_color)

    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    def individual_rgba(e):
        n = e[2]['attr_dict']['color']
        if n==10:
            return [0,0,0,0.5]
        else:
            return [0,0,0,0]
    # l = []
    for e in g.edges(data=True):
        colorVal = scalarMap.to_rgba(e[2]['attr_dict']['color']) #individual_rgba(e)#
        edge_colors.append(colorVal)

    plt.figure(figsize=(8, 8))
    nx.draw(g, pos=node_positions, arrowsize=1,edge_color=edge_colors, node_size=0)
    plt.title("Road with density between [0, 1)", size=15)
    sm = plt.cm.ScalarMappable(cmap=jet, norm=plt.Normalize(vmin=min_road_color, vmax=max_road_color))
    sm.set_array([])
    cbar = plt.colorbar(sm,ticks=[1])
    plt.show()


plot_cluster()

def plot_graph():
    import math

    max_density = max([roadMap[r].density for r in roadMap])
    max_density_log = math.log(1000*max_density+1)
    min_density = min([roadMap[r].density for r in roadMap])
    min_density_log = math.log(1000*min_density+1)
    print(min_density, min_density_log, max_density, max_density_log)
    edge_colors = []

    jet = cm = plt.get_cmap('brg_r') #'brg_r'
    cNorm  = colors.Normalize(vmin=0, vmax=1)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    l = []
    with open("021.csv","w") as csv_writer:
        for e in g.edges(data=True):
            d = math.log(1000*roadMap[e[2]['attr_dict']['idx']].density+1)/(max_density_log-min_density_log)
            
            colorVal = scalarMap.to_rgba(d)
            csv_writer.write("{0:.2f}".format(d)+"\n");
            # csv_writer.write(str(roadMap[e[2]['attr_dict']['idx']].density))
            # csv_writer.write(",")
            # csv_writer.write(str(roadMap[e[2]['attr_dict']['idx']].length))
            # csv_writer.write("\n")
            edge_colors.append(colorVal)
    # print(l)
    plt.figure(figsize=(10, 10))
    nx.draw(g, pos=node_positions, arrowsize=2,edge_color=edge_colors, node_size=0)
    plt.title('Drop off Graph Representation, size=15')
    plt.show()

# plot_graph()