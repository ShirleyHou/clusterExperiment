

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import csv
from BuildRoadMap import getRoadMap, getNodeGraph, injectClusterInfo, getExpiration


def plot_cluster(nGraph, node_positions, cluster_color_mapping, roadMap):


    #road_colors = [cluster_color_mapping[i.cluster_id] for i in roadMap.values()]

    #min_road_color = min(road_colors)
    #max_road_color = max(road_colors)

    edge_colors = []

    #jet = plt.get_cmap(colormap_name)
    #print(min_road_color, max_road_color)
    #cNorm  = colors.Normalize(vmin=min_road_color, vmax=max_road_color)

    #scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for e in nGraph.edges(data=True):
        colorVal = cluster_color_mapping[roadMap[e[2]['attr_dict']['idx']].cluster_id]


        edge_colors.append(color[colorVal])

    plt.figure(figsize=(8, 8))
    nx.draw(nGraph, pos=node_positions, arrowsize=1,edge_color=edge_colors, node_size=0)
    # plt.title("Road with density between [0, 1)", size=15)
    # sm = plt.cm.ScalarMappable(cmap=jet, norm=plt.Normalize(vmin=min_road_color, vmax=max_road_color))
    # sm.set_array([])
    # plt.colorbar(sm,ticks=[i for i in range(0,max_road_color+1,1)])
    plt.show()

#plot_cluster('tab20')

def plot_graph(roadMap, inputmap=None, method='density'):
    print(method)
    import math
    if method == 'expiration':
        exp = getExpiration(inputmap)
        print(sum(exp.values()))
        for r in roadMap:
            roadMap[r].no_expiration = exp[r]
    elif method=='ineffectivesearch':
        exp = getExpiration(inputmap)
        print(sum(exp.values()))
        for r in roadMap:
            roadMap[r].ineffective_search = exp[r]
    elif method=='cluster_attr':
        for r in roadMap:
            roadMap[r].dropoff = math.log(10*inputmap[roadMap[r].cluster_id]+1)


    ng, node_positions = getNodeGraph(roadMap)
    max_density = 0
    min_density = 0

    if method == 'density' or method == 'cluster_attr':
        max_density = max([roadMap[r].dropoff for r in roadMap])
        min_density = min([roadMap[r].dropoff for r in roadMap])

    elif method == 'expiration':
        max_density = max([roadMap[r].no_expiration for r in roadMap])
        min_density = min([roadMap[r].no_expiration for r in roadMap])
    elif method == 'ineffectivesearch':
        max_density = max([roadMap[r].ineffective_search for r in roadMap])
        min_density = min([roadMap[r].ineffective_search for r in roadMap])

    max_density_log = math.log(max_density + 1)
    min_density_log = math.log(min_density + 1)

    print(max_density, min_density)
    edge_colors = []

    jet = plt.get_cmap('YlOrRd') #'brg_r'
    cNorm  = colors.Normalize(vmin=min_density_log, vmax=max_density_log)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    for e in ng.edges(data=True):
        d = 0
        if method == 'density' or method == 'cluster_attr':
            d = roadMap[e[2]['attr_dict']['idx']].dropoff
        elif method == 'expiration':
            d = math.log(roadMap[e[2]['attr_dict']['idx']].no_expiration + 1)
        elif method == 'ineffectivesearch':
            d = math.log(roadMap[e[2]['attr_dict']['idx']].ineffective_search + 1)

        #d = roadMap[e[2]['attr_dict']['idx']].density#/(max_density - min_density)
        colorVal = scalarMap.to_rgba(d)
        edge_colors.append(colorVal)

    plt.figure(figsize=(10, 10))
    nx.draw(ng, pos=node_positions, arrowsize=2,edge_color=edge_colors, node_size=0)
    sm = plt.cm.ScalarMappable(cmap=jet)
    sm.set_array([])
    #plt.colorbar(sm)
    plt.title('Drop off Graph Representation, size=15')
    plt.show()
