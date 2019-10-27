class Road:
    def __init__(self, idx, lon, lat):
        self.idx = idx
        self.pickup = 0
        self.dropoff = 0
        self.lon = lon
        self.lat = lat
        self.nb = set()
        self.length = 0
        self.density = 0
        self.cluster_id = -1
        self.from_node = -1
        self.to_node = -1
        self.no_pickup = 0
        self.no_expiration = 0
        self.ineffective_search = 0
        self.pr = 0
        self.travel_time = 2

        
    def setCluster(self, n):
        assert n>=0
        self.cluster_id = n
    def isClustered(self):
        return self.cluster_id != -1
    def isSameCluster(self, roadB):
        return self.cluster_id == roadB.cluster_id
    def __str__(self):
        return "{0:.2f}".format(self.density)

class Intersection:
    def __init__(self, idx, lon, lat):
        self.idx = idx
        self.lon = lon
        self.lat = lat
        self.incoming = {}
        self.outgoing = {}