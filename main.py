from opportunity_point import PointOfOpportunity
import folium
from folium.plugins import MarkerCluster
from folium.plugins import Search
from shapely.geometry import Point

NORTH = 50.17743
SOUTH = 49.9419
WEST = 14.224437
EAST = 14.706788


#vytvoření objektu
interest = PointOfOpportunity(n=NORTH, w=WEST, s=SOUTH, e=EAST, filename='soubory/Cukrarny_all_v3_20231111.csv')

#použití metody mřížky
point = interest.grid()

#přidání k výsledkům nejbližší zastávku MHD
point_mhd = interest.distance_mhd(point, 'soubory/stops_MHD_PRAHA.json')

# omezení na oblast Prahy pomocí polygonu
novy_grid = interest.filter_polygon(point_mhd,"soubory/PRAHA_P.json")

# uložení do souboru
interest.to_csv(novy_grid, "soubory/novy_grid.csv")

# zobrazení výsledků na mapě pomocí knihovny Folium
moje_mapa = folium.Map(location=(50.07653, 14.40232), zoom_start=10, tiles="openstreetmap")

# zobrazení každého bodu na mřížce jako obdélníku, body jsou barevně odlišeny podle vzdáleností od nejbližší cukrárny
for index, row in novy_grid.iterrows():
  if row['distance'] < 1:
    color = "#B5F1CC"
  elif row['distance'] < 3:
    color = "#8DDFCB"
  else:
    color = "#5DC7AF"
  # radius = 500
  dx = 0.0025
  folium.Rectangle(
      bounds=[[row['latitude'] + dx, row['longitude'] + dx], [row['latitude'] - dx, row['longitude'] - dx]],
      color=color,
      weight=1,
      fill_opacity=0.6,
      opacity=1,
      fill_color=color,
      fill=False,  
      popup=row['distance'],
      tooltip="km",
  ).add_to(moje_mapa)

#zobrazení cukráren na mapě jako puntík
for c in interest.dataset:
  c = c.split(",")
  radius = 200
  folium.Circle(
      location=[float(c[4].strip('"')), float(c[5].strip('"'))],
      radius=radius,
      color="#EE81CA",
      weight=1,
      fill_opacity=0.8,
      opacity=1,
      fill_color= '#EE81CA',
      fill=False,  
      popup=c[0].replace('"', ""),
      tooltip="km",
  ).add_to(moje_mapa)

#zadání souřadnic okraje (vykreslí obdélník kolem Prahy)
  trail_coordinates = [
    (NORTH, EAST),
    (NORTH, WEST),
    (SOUTH, WEST),
    (SOUTH, EAST),
    (NORTH, EAST),
  ]

#tady si vykreslím hranice
folium.PolyLine(trail_coordinates, tooltip="oblast nahody").add_to(moje_mapa)

#uložení mapy jako internetové stránky, můžeme otevřít v prohlížeči
moje_mapa.save("index.html")