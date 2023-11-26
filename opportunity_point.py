from random import uniform
import json
from math import sqrt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

AMOUNT = 10 #počet náhodných bodů
STEP = 50 #vzálenost bodů od sebe (při MULTI 10000 je 100 ~ 1km)
KM = 111 # převod vzdálenosti dvou bodů na km
MULTI = 10000 # převod souřadnic na celé číslo (pro použití ve for cyklu)

# sloupce v csv souboru
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

    #vytvoření náhodného bodu
    def get_random_point(self):
        x, y = uniform(self.x1, self.x2), uniform(self.y1, self.y2)
        return x, y
    
    #otevření souboru typu json
    def load_json(self, file):
        with open(file, encoding='utf8') as f:
            json_dataset = json.load(f)
        return json_dataset

    #otevření csv souboru
    def load_csv(self, file):
        with open(file, encoding='utf8') as f:
            self.dataset = f.readlines()[1:]

    
    
    # vzdálenost dvou bodů pomocí geopy knihovny (výpočetně náročné)
    # def distance(self,x1,y1,x2,y2):
    #     c = geopy.distance.geodesic([x1, y1], [x2, y2]).km
    #     return c
    
    #uložení souřadnic cukráren do souboru, nakonec tuto funkci nevyužíváme
    # def get_coordinates(self):
    #     data = self.dataset
    #     list = []
    #     for i in data:
    #         x,y = i['longitude'], i['latitude']
    #         list.append([x,y])
    #     return list

    #vzdálenost dvou bodů Pythagorova věta(pro krátké vzdálenosti dostačující)
    def distance(self,x1,y1,x2,y2):
        c = sqrt((x1-x2)**2 + (y1-y2)**2)
        return c
    
    # vytvoření náhodného bodu a zjištění vzdálenosti od nejbližší cukrárny
    # můžeme si zadáním points určit počet bodů a pomocí top vybrat několik nejvzdálenějších bodů
    def monte_carlo(self, points=AMOUNT, top=1):
        final_list = []
        for i in range(points):
            x,y = self.get_random_point()
            min = float("inf")
            result = []
            for c in self.dataset:
                c = c.split(",")
                d = self.distance(x,y, float(c[LONGITUDE].replace('"', '')), float(c[LATITUDE].replace('"', '')))
                if d < min:
                    min = d
                    result = [d*KM, x, y]
            final_list.append(result)
        final_list.sort(reverse=True)
        return final_list[:top]
    
    # vytvoření mřížky bodů a zjištění vzdálenosti od nejbližší cukrárny 
    # můžeme si určit hustotu mřížky pomocí zadání step
    def grid (self, step=STEP):
        final_list = []
        for y in range(int(self.y1*MULTI), int(self.y2*MULTI), step):
            for x in range(int(self.x1*MULTI), int(self.x2*MULTI), step):  
                min = float("inf")
                result = {}
                for c in self.dataset:
                    c = c.split(',')
                    d = self.distance(x/MULTI, y/MULTI, float(c[LONGITUDE].strip('"')), float(c[LATITUDE].strip('"')))
                    if d < min:
                        min = d
                        result['distance'] = d * KM
                        result['latitude'] = y/MULTI
                        result['longitude'] = x/MULTI
                        result['geometry'] = Point([x/MULTI], [y/MULTI])
                        result['id_cukrarna'] = c[0].strip('"')
                final_list.append(result)
        return final_list
    


    #přiřazení k bodům příležitosti nejbližsí zastávku a její vzdálenost
    def distance_mhd(self, result, file_mhd):
        mhd_dataset = self.load_json(file_mhd)
        new_result = []
        for point in result:
            x = point['longitude']
            y = point['latitude']
            min = float('inf')
            for stop in mhd_dataset['stopGroups']:
                name = stop['name']
                x2 = stop['avgLon']
                y2 = stop['avgLat']
                d = self.distance(x, y, x2, y2)
                if d < min:
                    min = d
                    point['distance_mhd'] = d*KM
                    point['name_mhd'] = name.strip('"')
            new_result.append(point)
        return new_result
                

    #omezení výsledků jen na oblast v polygonu
    def filter_polygon(self, result, polygon_file):
        grid = gpd.GeoDataFrame(result, crs="EPSG:4326")
        polys = gpd.read_file(polygon_file)

        mask = grid.within(polys.loc[0, 'geometry'])
        grid['Praha'] = mask

        novy_grid = grid[grid['Praha'] == True]
        novy_grid.drop(columns=['Praha'], inplace=True)
        return novy_grid

    #uložení do csv souboru
    def to_csv(self, gdf, new_file):
        df = pd.DataFrame(gdf)
        df.to_csv(new_file, index=False)
        return new_file
