
import copy
import csv
import math
from Road import Road, Intersection
from BuildRoadMap import getIntersectionMap, getRoadMap, check_cluster_results
import heapq

OKBLUE = '\033[94m'
ENDC = '\033[0m'
OKGREEN = '\033[1m'


roadMap, eGraph = getRoadMap(PR=True)
road_id_sorted = [r.idx for r in sorted(roadMap.values(), key = lambda x:-x.density)]
road_density = [r.density for r in sorted(roadMap.values(), key = lambda x:-x.density)]

LEN = 10

def updatek(k,road_id,x_average_k, segma_k,C=0):

    new_x_k = roadMap[road_id].density
    new_x_avg_k = ((k-1)*x_average_k+new_x_k)/(k)
    new_segma_k = ((k-1)*(segma_k)+(new_x_k-new_x_avg_k)*(new_x_k-x_average_k))/k

    threshold = min( -0.005+0.00001*(C**2), 0)#-0.005*(1/2)**(C)
    if math.sqrt(new_segma_k) - math.sqrt(segma_k)> threshold:#0.00002: #math.sqrt(new_segma_k)/new_x_avg_k > 1.5: 0.00001
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
        candidate_sd[i] = math.sqrt(seg_temp)
    min_sd_idx = candidate_sd.index(min(candidate_sd))
    return min_sd_idx



cluster_id = 0 #cluster_id starts with 0

for idx, road_id in enumerate(road_id_sorted):
    road = roadMap[road_id]
    
    if not road.isClustered():

        #q = [road]
        q = [(-road.density, road.idx, road)]
        heapq.heapify(q)

        k = 1
        avg = road.density
        seg = 0

        current_cluster_roads = [] 
        current_cluster_neighbours = set()
        visited = set() #garantees for each cluster no road is repeatedly added into the consider queue.
        visited.add(road)

        while(q):
            
            
            #candidate_index = find_next_qualified_candidate_index(q, k, avg, seg)

            current_road = heapq.heappop(q)[2] #q.pop(candidate_index)

            res, k_temp, avg_temp, seg_temp = updatek(k, current_road.idx, avg, seg, cluster_id)

            """test"""
            # if len(current_cluster_roads) > 9:
            #     #print("test -")
            #     print(math.sqrt(seg_temp) - math.sqrt(seg))
            """test"""
            if res!=-1 or len(current_cluster_roads) < LEN:
                    
                current_cluster_roads.append(current_road)
                current_road.setCluster(cluster_id)
                k, avg, seg = k_temp, avg_temp, seg_temp
                
                neighbour_roads = [roadMap[n] for n in current_road.nb]
                
                for nb_road in neighbour_roads:
                    if not nb_road.isClustered() and nb_road not in visited:
                        #q.append(nb_road)
                        heapq.heappush(q, (-nb_road.density, nb_road.idx, nb_road))
                        visited.add(nb_road)

                    elif nb_road.isClustered() and not nb_road.isSameCluster(current_road): 
                        #neighbour branch
                        current_cluster_neighbours.add(nb_road.cluster_id)
            

        current_sum_density = sum([r.density for r in current_cluster_roads])
        current_average_density = current_sum_density/len(current_cluster_roads)

        
        if len(current_cluster_roads)< LEN and len(current_cluster_neighbours)>0:
            #current cluster jas < 10 elemnents. merge.
            merge_current_cluster_with_neighbours(current_cluster_roads, current_cluster_neighbours)
            
        else: 
            d[cluster_id] = [current_average_density, len(current_cluster_roads)]
            cluster_id +=1



density = check_cluster_results(roadMap) #key_id: density, road_number.

cluster_road_map = {}
cluster_density_map = {}
for r in roadMap.values():
    if r.cluster_id not in cluster_road_map:
        cluster_road_map[r.cluster_id] = [r]
        cluster_density_map[r.cluster_id] = set([r.density])
    else:
        cluster_road_map[r.cluster_id].append(r)
        cluster_density_map[r.cluster_id].add(r.density)

sdc_roads = {}
sdc_density ={}
for i in cluster_density_map:
    if len(cluster_density_map[i])==1:
        sdc_density[i] = cluster_density_map[i]
        sdc_roads[i] = cluster_road_map[i]
#only left with single value clusters.


sdc_nbs = {}

for cluster_id in sdc_density.keys():
    sdc_nbs[cluster_id] = set()
    for road in sdc_roads[cluster_id]:
        road_id = road.idx
        for nb_idx in roadMap[road_id].nb:
            nb_id = roadMap[nb_idx].cluster_id
            if nb_id not in sdc_nbs and nb_id != cluster_id and nb_id in sdc_density.keys() and list(sdc_density[nb_id])[0] == list(sdc_density[cluster_id])[0]:
                sdc_nbs[cluster_id].add(roadMap[nb_idx].cluster_id)
print(sdc_nbs)

def merge_same_nbs(sdc_roads, i, nbs):
    for nb_id in nbs:
        for r in sdc_roads[nb_id]:
            r.setCluster(i)

for i in sdc_nbs:
    if len(sdc_nbs[i]):
        merge_same_nbs(sdc_roads, i, sdc_nbs[i])

check_cluster_results(roadMap, True)
with open("bfs_cluster.csv", 'w') as out:
    out.write("road_id,cluster_id\n")
    for i in roadMap.keys():
        out.write(str(i)+","+str(roadMap[i].cluster_id)+"\n")
    
