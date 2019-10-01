

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from BuildRoadMap import getRoadMap, getNodeGraph, injectClusterInfo

        
def plot_cluster(colormap_name):
    roadMap, eGraph = getRoadMap(PR=True)
    nGraph, node_positions = getNodeGraph(PR=True)
    _ = injectClusterInfo(roadMap)
    road_colors = [i.cluster_id for i in roadMap.values()]

    min_road_color = min(road_colors)
    max_road_color = max(road_colors)

    edge_colors = []

    jet = plt.get_cmap(colormap_name)
    print(min_road_color, max_road_color)
    cNorm  = colors.Normalize(vmin=min_road_color, vmax=max_road_color)

    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)


    for e in nGraph.edges(data=True):
        colorVal = scalarMap.to_rgba(e[2]['attr_dict']['color']) #individual_rgba(e)#
        edge_colors.append(colorVal)

    plt.figure(figsize=(8, 8))
    nx.draw(nGraph, pos=node_positions, arrowsize=1,edge_color=edge_colors, node_size=0)
    plt.title("Road with density between [0, 1)", size=15)
    sm = plt.cm.ScalarMappable(cmap=jet, norm=plt.Normalize(vmin=min_road_color, vmax=max_road_color))
    sm.set_array([])
    plt.colorbar(sm,ticks=[i for i in range(0,max_road_color+1,1)])
    plt.show()


plot_cluster('tab20')

def plot_graph():
    import math
    roadMap, _ = getRoadMap(PR=True)
    ng, node_positions = getNodeGraph(PR=True)
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
    
    for e in ng.edges(data=True):
        d = math.log(1000*roadMap[e[2]['attr_dict']['idx']].density+1)/(max_density_log-min_density_log)
        colorVal = scalarMap.to_rgba(d)
        edge_colors.append(colorVal)
    # print(l)
    plt.figure(figsize=(10, 10))
    nx.draw(ng, pos=node_positions, arrowsize=2,edge_color=edge_colors, node_size=0)
    sm = plt.cm.ScalarMappable(cmap=jet
                               )
    sm.set_array([])
    plt.colorbar(sm)
    plt.title('Drop off Graph Representation, size=15')
    plt.show()
#plot_graph()