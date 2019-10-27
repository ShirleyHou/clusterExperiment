import csv
import networkx as nx
from collections import defaultdict
d = defaultdict(lambda: defaultdict(int))

def get_pagerank(TRANING_DATA, PAGERANK_OUTPUT):
    pickupD = defaultdict(int)
    dropoffD = defaultdict(int)

    with open(TRANING_DATA) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            pickup_id = int(row['pickup_roadId'])
            pickupD[pickup_id] += 1
            dropoff_id = int(row['dropoff_roadId'])
            dropoffD[dropoff_id] += 1
            d[pickup_id][dropoff_id]+=1

    G = nx.DiGraph()
    for pickup in d:
        for dropoff in d[pickup]:
            #G.add_edge(dropoff, pickup, weight=d[pickup][dropoff])
            G.add_edge(dropoff, pickup, weight=d[pickup][dropoff])

    pr = nx.pagerank(G,alpha=1)

    with open(PAGERANK_OUTPUT, 'w') as prfile:
        prfile.write("road_id,page_rank,pickup,dropoff\n")
        for i in pr:
            prfile.write("{},{:.8f},{},{}\n".format(i, pr[i],pickupD[i], dropoffD[i]));