
from BuildRoadMap import getIntersectionMap, getRoadMap, check_cluster_results, injectClusterInfo, getExpiration
import csv
import statistics
import networkx as nx

def clusterNb(roadMap, cluster_road_map, nb_file, cluster_color_file):

    # expirationRandomDest = getExpiration("expiration_random_destination.csv")
    # expirationIndependent = getExpiration("expiration_8000_independent_exp.csv")
    # betweenessRating = nx.algorithms.betweenness_centrality(edgeNxGraph)
    # with open("betweeness_rating","w") as w:
    #     headers = "roadId,betweeness,expiration_exp,expiration_random\n"
    #     for i in betweenessRating:
    #         w.write(str(i)+","+str(betweenessRating[i])+","+str(expirationIndependent[i])+","+str(expirationRandomDest[i])+"\n")

    # cluster_road_map = injectClusterInfo(roadMap,cluster_file) # inject cluster with info

    # std = []
    # for i in sorted(cluster_road_map.keys()):
    #     road_densities = [roadMap[rd].density for rd in cluster_road_map[i]]
    #     std.append(statistics.pstdev(road_densities))
    # print(std)

    density = check_cluster_results(roadMap,ifprint=False)
    cluster_nbs = {}
    cluster_nearest_nb = {}



    for cluster_id in density.keys():
        cluster_nbs[cluster_id] = set()
        for road_id in cluster_road_map[cluster_id]:
            for nb_idx in roadMap[road_id].nb:
                if (roadMap[nb_idx].cluster_id != cluster_id):
                    cluster_nbs[cluster_id].add(roadMap[nb_idx].cluster_id)

        density_diff = []
        nbs = list(cluster_nbs[cluster_id])
        for nb_idx in nbs:
            density_diff.append(abs(density[nb_idx][0] - density[cluster_id][0]))
        closet_nb = nbs[density_diff.index(min(density_diff))]
        cluster_nearest_nb[cluster_id] = closet_nb

    print(cluster_nbs)
    # def getClusterNbMap(cluster_nbs):

    nb_graph = nx.Graph()
    with open(nb_file,"w") as f:
        f.write("cluster_id,cluster_nbs\n")
        for cluster_id in cluster_nbs:
            f.write("{},{}\n".format(cluster_id, " ".join([str(nb) for nb in cluster_nbs[cluster_id]])))
            for nb_id in cluster_nbs[cluster_id]:
                nb_graph.add_edge(cluster_id, nb_id)
    cluster_color_map = nx.coloring.greedy_color(nb_graph, strategy='largest_first')

    assert len(nb_graph.nodes()) == len(cluster_color_map)

    with open(cluster_color_file,"w") as f:
        f.write("cluster_id,color\n")
        for i in sorted(cluster_color_map.keys()):
            f.write(str(i)+","+str(cluster_color_map[i])+"\n")
    return cluster_nearest_nb, cluster_color_map

"""
Attractiveness_based Silhouette Index
"""
def calculateSilhouetteIndex(roadMap, cluster_road_map, cluster_nearest_nb, out_file_name):
    CLUSTER_SI = []
    OVERALL_SI = []


    for cid in sorted(cluster_nearest_nb):
        nearest_nb = cluster_nearest_nb[cid]
        intraClusterRoad = cluster_road_map[cid]
        interClusterRoad = cluster_road_map[nearest_nb]

        S = []

        for rid in intraClusterRoad:
            intraDiffList = [abs(roadMap[j].density - roadMap[rid].density) for j in intraClusterRoad if j!=rid]
            interDiffList = [abs(roadMap[k].density - roadMap[rid].density) for k in interClusterRoad]


            intraDiff = statistics.mean(intraDiffList)
            interDiff = statistics.mean(interDiffList)
            if (intraDiff==0 and interDiff==0):
                print(intraDiffList, interDiffList, cid, nearest_nb)
            res = (interDiff - intraDiff)/max(interDiff, intraDiff)
            S.append(res)
            OVERALL_SI.append(res)
        res = statistics.mean(S)
        if res==1:
            res = 0
        CLUSTER_SI.append(res)


    with open(out_file_name, "w") as out:
        out.write("cluster_id,SI\n")
        for i, e in enumerate(CLUSTER_SI):
            out.write(str(i)+","+"{:.5f}".format(e)+"\n")
        assert len(CLUSTER_SI) == len(cluster_nearest_nb)
        out.write("average SI {:.5f}".format(statistics.mean(OVERALL_SI)))


# calculateSilhouetteIndex()