import csv
class Road:
    def __init__(self, idx, pickup, dropoff,lon, lat):
        self.idx = idx
        self.pickup = pickup
        self.dropoff = dropoff
        self.lon = lon
        self.lat = lat
        self.nb = set()
        self.length = 0
        self.density = 0
        self.color = -1
    def __str__(self):
        return str(self.idx)



roadMap = {}
with open("training_morning_road_pickup_lon_lat.csv") as road_info:
    csv_reader = csv.DictReader(road_info)
    for row in csv_reader:
        roadId = int(row['roadId'])
        pickup = int(row['pickup_count'])
        dropoff = int(row['dropoff_count'])
        lon = float(row['lon'])
        lat = float(row['lat'])
        new_road = Road(roadId, pickup, dropoff, lon, lat)
        roadMap[roadId] = new_road


node_adjm = {}
with open("edgeList.txt", mode='r') as edge_info:

    csv_reader = csv.DictReader(edge_info)
    for row in csv_reader:
        roadId = int(row['roadId'])
        roadLength = float(row['length'])
        roadInfo = roadMap.get(roadId, None)

        if roadInfo==None:
            from_location = [float(row['from_node_lon']),float(row['from_node_lat'])]
            to_location = [float(row['to_node_lon']),float(row['to_node_lat'])]
            default_centroid = [(from_location[0]+to_location[0])/2, (from_location[1]+to_location[1])/2]
            new_road = Road(roadId, 0, 0, default_centroid[0], default_centroid[1])
            roadMap[roadId] = new_road

        r_obj = roadMap[roadId]
        r_obj.length = roadLength
        r_obj.density = r_obj.pickup/roadLength
        from_node = int(row['from_node'])
        to_node = int(row['to_node'])
        key = (from_node, to_node)
        if key in node_adjm:

            node_adjm[key].append(r_obj.density)
        else:
            node_adjm[key] = r_obj.density
print(node_adjm)
c = 0
n = 0
for i in node_adjm:
    f, t = i[0], i[1]
    if (t, f) in node_adjm:
        c+=1
        if abs(node_adjm[(t, f)] - node_adjm[(f, t)])>10:
            print((t, f), (f, t))
            n+=1
print(c)
print(n)
        