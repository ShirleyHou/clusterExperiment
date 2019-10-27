class GeoProjector:
    
    EARTH_RADIUS = 6370000.0
    def __init__(self, ref_lat, ref_lon):
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon

        self.metersPerLatDegree = GeoProjector.distanceGreatCircle(ref_lat, ref_lon, ref_lat + 1.0, ref_lon)
        self.metersPerLonDegree = GeoProjector.distanceGreatCircle(ref_lat, ref_lon, ref_lat, ref_lon + 1.0)
    def fromLatLon(self, lat, lon):
        x = (lon - self.ref_lon) * self.metersPerLonDegree
        y = (lat - self.ref_lat) * self.metersPerLatDegree
        return [x, y]

    def toLatLon(self, x, y):
        lon = self.ref_lon + (x / metersPerLonDegree)
        lat = self.ref_lat + (y / metersPerLatDegree)
        return [lat, lon]

    def distanceGreatCircle(lat1, lon1, lat2, lon2):
        import math
        rad_lat1 = math.radians(lat1);
        rad_lon1 = math.radians(lon1);
        rad_lat2 = math.radians(lat2);
        rad_lon2 = math.radians(lon2);
        q1 = math.cos(rad_lat1) * math.cos(rad_lon1) * math.cos(rad_lat2) * math.cos(rad_lon2);
        q2 = math.cos(rad_lat1) * math.sin(rad_lon1) * math.cos(rad_lat2) * math.sin(rad_lon2);
        q3 = math.sin(rad_lat1) * math.sin(rad_lat2);
        q = q1+q2+q3;
        if (q > 1.0):
            q = 1.0
        if (q < -1.0):
            q = -1.0
        return (math.acos(q) *GeoProjector.EARTH_RADIUS)
	
	
