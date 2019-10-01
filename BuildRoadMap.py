

import csv
import networkx as nx
import utm
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

def getPageRank():
    pr = {}
    with open("pagerank.csv") as prfile:
        csv_reader = csv.DictReader(prfile)
        for row in csv_reader:
            roadId = int(row['road_id'])
            rank = float(row['page_rank'])
            pr[roadId] = rank
    return pr

def project(lon, lat):
    u = utm.from_latlon(lat, lon)
    lat = u[1]
    lon = u[0]
    return (lon, lat)

        
def getRoadMap(**kwargs):
    pr = getPageRank()
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
            r_obj.from_node = int(row['from_node'])
            r_obj.to_node = int(row['to_node'])
            r_obj.length = roadLength
            
            if kwargs['PR']:
                r_obj.density = max(r_obj.density, pr.get(r_obj.idx, 0)*1000)
            else:
                r_obj.density = max(r_obj.density, r_obj.pickup/roadLength*1000)
    
            
    # Create empty graph
    egraph = nx.DiGraph()

    with open("Road_adj_map.csv") as road_adj:
        csv_reader = csv.DictReader(road_adj)
        own_id_set = set()
        for row in csv_reader:
            own_id = int(row['roadId'])
            own_id_set.add(own_id)
            to_ids = [int(i) for i in row['downstream'].split(' ') if i != own_id and i!='']
            from_ids = [int(i) for i in row['upstream'].split(' ') if i != own_id and i!='']

            for i in set(from_ids+to_ids):
                roadMap[own_id].nb.add(i)
                roadMap[i].nb.add(own_id)

            for i in set(from_ids):
                
                egraph.add_edge(i, own_id)
                
            for i in set(to_ids):
                egraph.add_edge(own_id, i)
        diff_set = set()
        for i in roadMap:
            if i not in own_id_set:
                diff_set.add(i)
        for i in diff_set:
            roadMap.pop(i, None)

    connected_component = [len(Gc) for Gc in sorted(nx.strongly_connected_component_subgraphs(egraph),key=len, reverse=True)]
    assert(len(connected_component) == 1)
    assert(connected_component[0] == len(roadMap))
    return roadMap, egraph


def project(lon, lat):
    u = utm.from_latlon(lat, lon)
    lat = u[1]
    lon = u[0]
    return lon, lat


def getNodeGraph(**kwargs):
    
    node_positions = {}
    roadMap, _ = getRoadMap(PR=kwargs['PR'])
    injectClusterInfo(roadMap)
    ngraph = nx.DiGraph()

    with open("edgeList.txt", mode='r') as edge_info:
        csv_reader = csv.DictReader(edge_info)
        for row in csv_reader:
            r_obj = roadMap[int(row['roadId'])]
            node_positions[int(row['from_node'])] = project(float(row['from_node_lon']), float(row['from_node_lat']))
            if r_obj.from_node != -1 and r_obj.to_node != -1:
                ngraph.add_edge(
                            r_obj.from_node, 
                            r_obj.to_node, 
                            attr_dict={
                                "idx": r_obj.idx,
                                "density": r_obj.density,
                                "lon": r_obj.lon,
                                "lat": r_obj.lat,
                                "length": r_obj.length,
                                "color": r_obj.cluster_id
                                }
                            )
    return ngraph, node_positions
    
def check_cluster_results(coloredRoadMap, ifprint=False):
    roadMap = coloredRoadMap #rename
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
        density[v] = [float(density[v])/D[v], D[v]]
        
    for i in sorted(density):
        print("{} {:.3f} {}".format(i, density[i][0], density[i][1]))
    if ifprint:
        print(len(density))
    return density


def injectClusterInfo(roadMap):
    cluster_road_map = {}
    with open("bfs_cluster.csv", 'r') as cluster_info_file:
        cluster_info = csv.DictReader(cluster_info_file)
        for row in cluster_info:
            road_id = int(row['road_id'])
            cluster_id = int(row['cluster_id'])
            roadMap[road_id].setCluster(cluster_id)

            if cluster_id not in cluster_road_map:
                cluster_road_map[cluster_id] = set()
            cluster_road_map[cluster_id].add(road_id)
    return cluster_road_map
