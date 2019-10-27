import csv
roadDic = {}
dropoff = {}
with open('training_morning.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    
    for row in csv_reader:
        roadId = int(row['pickup_roadId'])
        lon = float(row['pickup_lon'])
        lat = float(row['pickup_lat'])
        dropoffId = int(row['dropoff_roadId'])
        if roadId not in roadDic:
            roadDic[roadId] = [lon, lat, 1]
        else:
            old_num = roadDic[roadId][2];
            old_lat = roadDic[roadId][1];
            old_lon = roadDic[roadId][0];
            new_lon = (old_lon*old_num + lon)/(old_num+1)
            new_lat = (old_lat*old_num + lat)/(old_num+1)
            roadDic[roadId] = [new_lon, new_lat, old_num+1]
        dropoff[dropoffId] = dropoff.get(dropoffId,0)+1


with open('training_morning_road_pickup_lon_lat.csv', mode='w') as csv_file:
    fieldnames = ['roadId','pickup_count','dropoff_count', 'lon', 'lat']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for r in sorted(roadDic):
        writer.writerow({'roadId': r, 'lon': roadDic[r][0], 'lat': roadDic[r][1], 'pickup_count':roadDic[r][2],'dropoff_count':dropoff.get(r,0)})

print(sum([roadDic[r][2] for r in roadDic]), sum(dropoff.values()))
print(len(dropoff), len(roadDic))
