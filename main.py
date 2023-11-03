from opportunity_point import PointOfOpportunity
import folium
from folium.plugins import MarkerCluster
from folium.plugins import Search
from shapely.geometry import Point

NORTH = 50.17743
SOUTH = 49.9419
WEST = 14.224437
EAST = 14.706788


# showing the results on the map
moje_mapa = folium.Map(location=(50.07653, 14.40232), zoom_start=10, tiles="openstreetmap")


interest = PointOfOpportunity(filename='cukrarny_union_vz2.csv')


point = interest.grid()


novy_grid = interest.filter_polygon(point,"PRAHA_P.json")

interest.to_csv(novy_grid, "novy_grid.csv")

    

# draw each point of the grid on the map as a rectangle, the colors are graded according to the smallest distance
for index, row in novy_grid.iterrows():
  if row['distance'] < 1:
    color = "#FFB997"
  elif row['distance'] < 3:
    color = "#F67E7D"
  else:
    color = "#843B62"
  # radius = 500
  dx = 0.0025
  folium.Rectangle(
      bounds=[[row['latitude'] + dx, row['longitude'] + dx], [row['latitude'] - dx, row['longitude'] - dx]],
      # radius=radius,
      color=color,
      weight=1,
      fill_opacity=0.6,
      opacity=1,
      fill_color=color,
      fill=False,  # gets overridden by fill_color
      popup=row['distance'],
      tooltip="km",
  ).add_to(moje_mapa)

#draw interest as a circle
for c in interest.dataset:
  c = c.split(",")
  radius = 200
  folium.Circle(
      location=[float(c[4]), float(c[5])],
      radius=radius,
      color="black",
      weight=1,
      fill_opacity=0.8,
      opacity=1,
      fill_color= '#0B032D',
      fill=False,  # gets overridden by fill_color
      popup=c[0].replace('"', ""),
      tooltip="km",
  ).add_to(moje_mapa)

#zadní souřadnic okraje- může být i polygon
  trail_coordinates = [
    (NORTH, EAST),
    (NORTH, WEST),
    (SOUTH, WEST),
    (SOUTH, EAST),
    (NORTH, EAST),
  ]

#tady si vykreslím hranice, dá se využít polygon
folium.PolyLine(trail_coordinates, tooltip="oblast nahody").add_to(moje_mapa)

#uložení mapy jako internetové stránky, můžeme otevřít v prohlížeči
moje_mapa.save("index.html")