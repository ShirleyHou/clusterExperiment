

from __future__ import absolute_import

TRAINING_DATA_NAME = "training_morning"
TRAINING_DATA = "../rawData/"+TRAINING_DATA_NAME+".csv"
PAGERANK_OUTPUT = "../RunningData/pagerank_{}.csv".format(TRAINING_DATA_NAME)


# from get_pagerank_data import get_pagerank
# get_pagerank(TRAINING_DATA, PAGERANK_OUTPUT)
from BuildRoadMap import getRoadMap, injectClusterInfo, getNodeGraph
roadMap, edgeNxGraph = getRoadMap(PAGERANK_OUTPUT)


from clusterxNew import BFSCluster
MINCSIZE = 20
MAXCSIZE = 400
AlphaInitial = -0.001
cluster_result_name = "cluster_min={}_max={}_alpha={}".format(MINCSIZE, MAXCSIZE, AlphaInitial)
cluster_attr_file = "../clusterResult/"+cluster_result_name+"_attractiveness.csv"
cluster_result_output = "../clusterResult/"+cluster_result_name+".csv"
normalized_cluster_attr = BFSCluster(roadMap,
           cluster_result_output,
           cluster_attr_file,
           MinimumClusterSize=MINCSIZE,
           MaximumClusterSize=MAXCSIZE,
           AlphaInitial=AlphaInitial)

nodeGraph, node_positions = getNodeGraph(roadMap)
cluster_road_mapping = injectClusterInfo(roadMap = roadMap, file=cluster_result_output)
from ClusterQualityEvaluation import clusterNb, calculateSilhouetteIndex

cluster_nb_file = "../clusterResult/"+cluster_result_name+"_nb.csv"
cluster_color_file = "../clusterResult/"+cluster_result_name+"_color.csv"
cluster_nearest_neighbour, cluster_color_map = clusterNb(roadMap, cluster_road_mapping, cluster_nb_file, cluster_color_file)
#calculateSilhouetteIndex(roadMap, cluster_road_mapping, cluster_nearest_neighbour,"../evaluationResult/SI_"+cluster_result_name+"t.csv")

# from expirationEvaluation import expEva
# expEva(roadMap,
#        "../clusterResult/cluster_min=10_max=10000_alpha=-5e-06.csv",
#        "../Expiration_WithCompetition/Expiration_10000_Independent_cluster_min=20_max=400_alpha=-0.001_manual_attr_t=50.csv",
#        "../Expiration_WithCompetition/Expiration_10000_RandomDest_cluster_min=20_max=400_alpha=-0.001.csv")


from graphx import plot_cluster, plot_graph
#plot_cluster(nodeGraph, node_positions, cluster_color_map, roadMap)
print(normalized_cluster_attr)
# plot_graph(roadMap, normalized_cluster_attr, 'cluster_attr')
#plot_graph(roadMap, "../Expiration_WithCompetition/Search_10000_Independent_cluster_min=20_max=400_alpha=-0.001_maual_attr_t=50.csv", 'ineffectivesearch')

plot_graph(roadMap, "../Expiration_WithCompetition/Expiration_10000_Independent_cluster_min=20_max=400_alpha=-0.001_linearexp_t=inf.csv", 'expiration')