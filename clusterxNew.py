
import copy
import csv
import math
from Road import Road, Intersection
from BuildRoadMap import getIntersectionMap, getRoadMap, check_cluster_results

OKBLUE = '\033[94m'
ENDC = '\033[0m'
OKGREEN = '\033[1m'


roadMap = getRoadMap()
road_id_sorted = [r.idx for r in sorted(roadMap.values(), key = lambda x:-x.density)]
road_density = [r.density for r in sorted(roadMap.values(), key = lambda x:-x.density)]



def updatek(k,road_id,x_average_k, segma_k):
    
    new_x_k = roadMap[road_id].density
    new_x_avg_k = ((k-1)*x_average_k+new_x_k)/(k)
    new_segma_k = ((k-1)*(segma_k)+(new_x_k-new_x_avg_k)*(new_x_k-x_average_k))/k
    if math.sqrt(abs(new_segma_k))/new_x_avg_k > 1.5:
        return -1, k+1, new_x_avg_k, new_segma_k
    return 1, k+1, new_x_avg_k, new_segma_k



"""
d: stores each known cluster's information as it goes.
key: road_id
value: [known_average_densiy, known_road_count]
"""
d = {} 


def merge_current_cluster_with_neighbours(current_cluster_rds, current_cluster_nbs):
    """
    let known_road_count = N, known_average_densiy = D
    when adding a new road to current cluster that has density d, 
    update the entry by [(D*N+d)/(N+1), N+1]
    """
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
        road.setCluster(closest_cluster_id)

def find_next_qualified_candidate_index(q, k, avg, seg):
    """
    q: candidate queue
    k: current cluster size
    avg: current cluster average density
    seg: current 
    find the next candidate to pop that lowest current cluster standard deviation (variance)
    """
    assert len(q)>0
    candidate_sd = [float('inf') for i in q]
    for i, candidate in enumerate(q):
        _, _, _, seg_temp = updatek(k, candidate.idx, avg, seg)
        candidate_sd[i] = seg_temp
    min_sd_idx = candidate_sd.index(min(candidate_sd))
    return min_sd_idx

import heapq

cluster_id = 0 #cluster_id starts with 0

for idx, road_id in enumerate(road_id_sorted):
    road = roadMap[road_id]
    
    if not road.isClustered():

        q = [road]
        
        k = 1
        avg = road.density
        seg = 0

        current_cluster_roads = [] 
        current_cluster_neighbours = set()
        visited = set() #garantees for each cluster no road is repeatedly added into the consider queue.
        visited.add(road)

        while(q):
            
            
            candidate_index = find_next_qualified_candidate_index(q, k, avg, seg)

            current_road = q.pop(candidate_index)

            res, k_temp, avg_temp, seg_temp = updatek(k, current_road.idx, avg, seg)

            if res!=-1 or len(current_cluster_roads)<10:
                    
                current_cluster_roads.append(current_road)
                current_road.setCluster(cluster_id)
                k, avg, seg= k_temp, avg_temp, seg_temp
                
                neighbour_roads = [roadMap[n] for n in current_road.nb]
                
                for nb_road in neighbour_roads:
                    if not nb_road.isClustered() and nb_road not in visited:
                        q.append(nb_road)
                        visited.add(nb_road)

                    elif nb_road.isClustered() and not nb_road.isSameCluster(current_road): 
                        #neighbour branch
                        current_cluster_neighbours.add(nb_road.cluster_id)
            

        current_sum_density = sum([r.density for r in current_cluster_roads])
        current_average_density = current_sum_density/len(current_cluster_roads)

        
        if len(current_cluster_roads)< 10 and len(current_cluster_neighbours)>0:
            #current cluster jas < 10 elemnents. merge.
            merge_current_cluster_with_neighbours(current_cluster_roads, current_cluster_neighbours)
            
        else: 
            d[cluster_id] = [current_average_density, len(current_cluster_roads)]
            cluster_id +=1

total_road_number_check = 0
for i in d:
    print(d[i])
    total_road_number_check +=d[i][1]
assert total_road_number_check == len(roadMap)

check_cluster_results(roadMap)
with open("bfs_cluster.csv", 'w') as out:
    out.write("road_id,cluster_id\n")
    for i in roadMap.keys():
        out.write(str(i)+","+str(roadMap[i].cluster_id)+"\n")
    
