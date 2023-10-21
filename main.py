from opportunity_point import PointOfOpportunity
import folium
from folium.plugins import MarkerCluster
from folium.plugins import Search
import pandas
import geopandas
from shapely.geometry import Point

NORTH = 50.17743
SOUTH = 49.9419
WEST = 14.224437
EAST = 14.706788

S1 = 49.9981
N1 = 50.1443
W1 = 14.224437
E1 = 14.706788

#tady si vytvořím objekt moje_mapa, použiju k tomu třidu Map z knihovny folium
moje_mapa = folium.Map(location=(50.07653, 14.40232), zoom_start=10, tiles="openstreetmap")


interest = PointOfOpportunity(filename='souradnice_google_cukrarny.json')

point = interest.grid(step=100)

interest.write_json(point, "grid_point.json")



   
    
# data_points = pandas.DataFrame({'vzdalenost': vzdalenost, 'latitude': latitude, 'longitude': longitude, 'geometry': geometry})
# coords = pandas.DataFrame({'lat':latitude, 'lon':longitude})

# d = {'vzdalenost': vzdalenost, 'latitude': latitude, 'longitude': longitude, 'geometry': geometry}



# #print(data_points)

# data_points.to_csv("grid_point.csv", index=False)
# coords.to_csv("grid_point_coord.csv", index=False)

    

#tady si postupně vykreslím každý bod na mapu jako puntik, barvy jsou odstupnované podle nejmenší vzdálenosti
# for p in point:
#   if p[0] < 1:
#     color = "red"
#   elif p[0] < 3:
#     color = "green"
#   else:
#     color = "blue"
#   radius = 200
#   folium.Circle(
#       location=[p[2], p[1]],
#       radius=radius,
#       color="black",
#       weight=1,
#       fill_opacity=0.6,
#       opacity=1,
#       fill_color=color,
#       fill=False,  # gets overridden by fill_color
#       popup=p[0],
#       tooltip="km",
#   ).add_to(moje_mapa)

# #tady si vykreslím náš dataset
# for c in interest.coordinates:
#   folium.Marker(
#       location=[c[1], c[0]],
#       tooltip="Opravdova cukrarna",
#       popup="Zatim bez popisku",
#       icon=folium.Icon(icon="star"),
#   ).add_to(moje_mapa)

# #zadní souřadnic okraje- může být i polygon
#   trail_coordinates = [
#     (NORTH, EAST),
#     (NORTH, WEST),
#     (SOUTH, WEST),
#     (SOUTH, EAST),
#     (NORTH, EAST),
#   ]

# #tady si vykreslím hranice, dá se využít polygon
# folium.PolyLine(trail_coordinates, tooltip="oblast nahody").add_to(moje_mapa)

# #uložení mapy jako internetové stránky, můžeme otevřít v prohlížeči
# moje_mapa.save("index.html")