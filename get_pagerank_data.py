import csv
import networkx as nx
from collections import defaultdict
d = defaultdict(lambda: defaultdict(int))
with open("training_morning.csv") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        pickup = int(row['pickup_roadId'])
        dropoff = int(row['dropoff_roadId'])
        d[pickup][dropoff]+=1

G = nx.DiGraph()
for pickup in d:
    for dropoff in d[pickup]:
        #G.add_edge(dropoff, pickup, weight=d[pickup][dropoff])
        G.add_edge(dropoff, pickup, weight=d[pickup][dropoff])
print("here 0")
pr = nx.pagerank(G,alpha=1)
pr_2 = nx.pagerank_numpy(G,alpha=0.85)
print("here 1")
with open("pagerank.csv", 'w') as prfile:
    prfile.write("road_id,page_rank\n")
    for i in pr:
        prfile.write("{},{:.8f}\n".format(i, pr[i])); 