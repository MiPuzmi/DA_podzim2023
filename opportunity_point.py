from random import uniform
import json
from math import sqrt
import geopandas
from shapely.geometry import Point

AMOUNT = 10
STEP = 100
KM = 111

NORTH = 50.17743
SOUTH = 49.9419
WEST = 14.224437
EAST = 14.706788

class PointOfOpportunity:
    def __init__(self, x1=WEST, x2=EAST, y1=SOUTH, y2=NORTH, filename = ''):
        self.x1 = x1
        self.x2 = x2 
        self.y1 = y1 
        self.y2 = y2 
        self.dataset = []
        self.coordinates = []
        if len(filename) > 0:
            self.load_json(filename)
            self.coordinates = self.get_coordinates()

    def get_random_point(self):
        x, y = uniform(self.x1, self.x2), uniform(self.y1, self.y2)
        return x, y
    
    def get_point_grid(self, step=STEP):
        point_grid = []
        for y in range(int(self.y1*10000), int(self.y2*10000), step):
            for x in range(int(self.x1*10000), int(self.x2*10000), step):
                point_grid.append([x/10000,y/10000])
        return point_grid
    
    def load_json(self, file):
        with open(file, encoding='utf8') as f:
            self.dataset = json.load(f)

    def distance(self,x1,y1,x2,y2):
        c = sqrt((x1-x2)**2 + (y1-y2)**2)
        return c
        
    def get_coordinates(self):
        data = self.dataset
        list = []
        for i in data:
            x,y = i['longitude'], i['latitude']
            list.append([x,y])
        return list

    def monte_carlo(self, points=AMOUNT, top=1):
        final_list = []
        for i in range(points):
            x,y = self.get_random_point()
            min = self.distance(self.x1, self.y1, self.x2, self.y2)
            result = []
            for c in self.coordinates:
                d = self.distance(x,y, c[0], c[1])
                if d < min:
                    min = d
                    result = [d, x, y]
            final_list.append(result)
        final_list.sort(reverse=True)
        return final_list[:top]
    
    def grid (self, step=STEP):
        final_list = []
        for y in range(int(self.y1*10000), int(self.y2*10000), step):
            for x in range(int(self.x1*10000), int(self.x2*10000), step):  
                min = self.distance(self.x1, self.y1, self.x2, self.y2) 
                result = {}
                for c in self.coordinates:
                    d = self.distance(x/10000, y/10000, c[0], c[1])
                    if d < min:
                        min = d
                        result['distance'] = d * KM
                        result['latitude'] = y/10000
                        result['longitude'] = x/10000
                        result['geometry'] = Point([x/10000], [y/10000])
                final_list.append(result)
        return final_list
    
    def write_json(self,result, filename):
        gdf = geopandas.GeoDataFrame(result, crs="EPSG:4326")
        gdf.to_file(filename, driver="GeoJSON")
