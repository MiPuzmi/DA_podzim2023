from random import uniform
import json
from math import sqrt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

AMOUNT = 10 #number of random points
STEP = 50 #distance of points in grid 100 ~ 1KM
KM = 111 # conversion to km
MULTI = 10000 # conversion coordinates to integer (for loop)

# columns in csv file
LATITUDE = 4
LONGITUDE = 5
ID = 0
SCORE = 3
ZIPCODE = 10

# entry coordinates
NORTH = 50.17743
SOUTH = 49.9419
WEST = 14.224437
EAST = 14.706788

class PointOfOpportunity:
    def __init__(self, w=WEST, e=EAST, s=SOUTH, n=NORTH, filename = ''):
        self.x1 = w
        self.x2 = e 
        self.y1 = s 
        self.y2 = n 
        self.dataset = []
        self.coordinates = []
        if len(filename) > 0:
            self.load_csv(filename)
            # self.coordinates = self.get_coordinates()

    def get_random_point(self):
        x, y = uniform(self.x1, self.x2), uniform(self.y1, self.y2)
        return x, y
    
    # def get_point_grid(self, step=STEP):
    #     point_grid = []
    #     for y in range(int(self.y1*MULTI), int(self.y2*MULTI), step):
    #         for x in range(int(self.x1*MULTI), int(self.x2*MULTI), step):
    #             point_grid.append([x/MULTI,y/MULTI])
    #     return point_grid
    
    # def load_json(self, file):
    #     with open(file, encoding='utf8') as f:
    #         self.dataset = json.load(f)

    #read csv file
    def load_csv(self, file):
        with open(file, encoding='utf8') as f:
            self.dataset = f.readlines()[1:]

    #distance of two points
    def distance(self,x1,y1,x2,y2):
        c = sqrt((x1-x2)**2 + (y1-y2)**2)
        return c
    
    #distance of two points in km
    # def distance(self,x1,y1,x2,y2):
    #     c = geopy.distance.geodesic([x1, y1], [x2, y2]).km
    #     return c
    
    # def get_coordinates(self):
    #     data = self.dataset
    #     list = []
    #     for i in data:
    #         x,y = i['longitude'], i['latitude']
    #         list.append([x,y])
    #     return list

    # create random points and calculation of the shortest distance from our object
    def monte_carlo(self, points=AMOUNT, top=1):
        final_list = []
        for i in range(points):
            x,y = self.get_random_point()
            min = float("inf")
            result = []
            for c in self.dataset:
                c = c.split(",")
                d = self.distance(x,y, float(c[LONGITUDE]), float(c[LATITUDE]))
                if d < min:
                    min = d
                    result = [d, x, y]
            final_list.append(result)
        final_list.sort(reverse=True)
        return final_list[:top]
    
    # create points in the grid and calculation of the shortest distance from our object
    def grid (self, step=STEP):
        final_list = []
        for y in range(int(self.y1*MULTI), int(self.y2*MULTI), step):
            for x in range(int(self.x1*MULTI), int(self.x2*MULTI), step):  
                min = float("inf")
                result = {}
                for c in self.dataset:
                    c = c.split(',')
                    d = self.distance(x/MULTI, y/MULTI, float(c[LONGITUDE]), float(c[LATITUDE]))
                    if d < min:
                        min = d
                        result['distance'] = d * KM
                        result['latitude'] = y/MULTI
                        result['longitude'] = x/MULTI
                        result['geometry'] = Point([x/MULTI], [y/MULTI])
                        result['id_cukrarna'] = c[0]
                final_list.append(result)
        return final_list
    
    # def write_json(self,result, filename):
    #     gdf = geopandas.GeoDataFrame(result, crs="EPSG:4326")
    #     gdf.to_file(filename, driver="GeoJSON")

    #filter point only in polygon(Prague)
    def filter_polygon(self, result, polygon_file):
        grid = gpd.GeoDataFrame(result, crs="EPSG:4326")
        polys = gpd.read_file(polygon_file)

        mask = grid.within(polys.loc[0, 'geometry'])
        grid['Praha'] = mask

        novy_grid = grid[grid['Praha'] == True]
        return novy_grid

    #save to csv
    def to_csv(self, gdf, new_file):
        df = pd.DataFrame(gdf)
        df.to_csv(new_file, index=False)
        return new_file
