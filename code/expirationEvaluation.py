import csv
from BuildRoadMap import getExpiration, getPageRank,getRoadMap

class Road:
    def __init__(self, idx):
        self.idx = idx
        self.pickup= 0
        self.pr = 0
        self.clusterId = -1
        self.expiration1 = 0
        self.randomExpiration = 0
        self.length = 0

def expEva(roadMap, cluster_file, expiration_file, random_destination):
    rd_length = roadMap

    roadMap = {}
    cluster_expiration_count = {}
    with open(cluster_file) as cfile:
        clusterInfo = csv.DictReader(cfile)
        for row in clusterInfo:
            road_id = int(row['road_id'])
            cluster_id = int(row['cluster_id'])
            cluster_expiration_count[cluster_id] = [0,0]
            if road_id not in roadMap:
                roadMap[road_id] = Road(road_id)
                roadMap[road_id].clusterId = cluster_id


    expirationWithExp = getExpiration(expiration_file)
    for r in expirationWithExp:
        if r not in roadMap:
            roadMap[r] = Road(r)
        roadMap[r].expiration1 = expirationWithExp[r]
        if (roadMap[r].clusterId != -1):
            cluster_expiration_count[roadMap[r].clusterId][0]+=roadMap[r].expiration1

    expirationWithRandom = getExpiration(random_destination)
    for r in expirationWithRandom:
        if r not in roadMap:
            roadMap[r] = Road(r)
        roadMap[r].randomExpiration = expirationWithRandom[r]
        if (roadMap[r].clusterId != -1):
            cluster_expiration_count[roadMap[r].clusterId][1] += roadMap[r].randomExpiration


    c = 0
    for r in roadMap:
        if r in rd_length:
            roadMap[r].length = rd_length.get(r).length
            roadMap[r].pr= rd_length.get(r).density*roadMap[r].length
        else:
            c+=1
            roadMap[r].length = 50
    outputClusterFile = expiration_file[:-4] + "_cluster_report.csv"
    with open(outputClusterFile, "w") as oc:
        oc.write(expiration_file + "\n")
        oc.write("cluster_id,expiration,expiration_random\n")
        for c in cluster_expiration_count:
            oc.write(str(c)+','+str(cluster_expiration_count[c][0])+','+str(cluster_expiration_count[c][1])+"\n")

    outputFile = expiration_file[:-4]+"_report.csv"
    with open(outputFile,"w") as er:
        er.write(expiration_file+"\n")
        er.write("road_id,road_pagerank,road_length,road_clusterId,expiration,random_expiration,pickup\n")
        for r in sorted(roadMap.keys()):
            R = roadMap[r]
            er.write(str(R.idx))
            er.write(",")
            er.write("{:.8f}".format(R.pr))
            er.write(",")
            er.write(str(R.length))
            er.write(",")
            er.write(str(R.clusterId))
            er.write(",")
            er.write(str(R.expiration1))
            er.write(",")
            er.write(str(R.randomExpiration))
            er.write(",")
            er.write(str(R.pickup))
            er.write("\n")


