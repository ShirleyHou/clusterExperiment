
import csv
class Road:
    def __init__(self, idx, pickup, lon, lat):
        self.idx = idx
        self.pickup = pickup
        self.lon = lon
        self.lat = lat
        self.nb = []
        self.colored = -1
    def __str__(self):
        return str(self.idx)

road_graph = {}
map_width = 0
map_height = 0
lats = set()
longs = set()
with open("edgelist.csv", mode='r') as road_info:
    csv_reader = csv.DictReader(road_info)

    for row in csv_reader:
        roadId = int(row['roadId'])
        pickup = int(row['pickup_count'])
        lon = float(row['lon'])
        lat = float(row['lat'])
        
        map_width = max_lon - min_lon
        map_height = max_lat - min_lat
        new_road = Road(roadId, pickup, lon, lat)
        road_graph[roadId] = new_road
    

road_adj = open("Road_adj_map.txt").readlines()[1:]

for r in road_adj:
    r = r.strip().split(',')
    road_id = int(r[0])
    roads_from = r[1].split(' ')
    roads_to = r[2].split(' ')
    for ar in roads_to:
        if int(ar)==road_id:
            continue
        if road_id not in road_graph:
            road_graph[road_id] = Road(road_id, 0, 0, 0)
        road_graph.get(road_id).nb.append(int(ar))

for i in road_graph:
    print(road_graph[i].idx, ":", road_graph[i].nb)

clusters = {}

color = 0
