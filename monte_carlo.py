import random
from math import sqrt
from PIL import Image, ImageDraw #knihovna na obrazky a kresleni


# DEFINICE KONSTANT
POCET_CUKRAREN = 30 #kolik je na zacatku skutecnych cukraren
POKUSY = 150 # kolik nahodnych bodu budu zkouset
LAT_MAX = 300 #sirka a vyska mapy/obrazku


# definice funkce, ktera pocita vzdalenost podle Pythagorovy vety
def vzdalenost(x1,y1,x2,y2):
  c = sqrt((x1-x2)**2 + (y1-y2)**2)
  return c

# funkce, ktera pripravi seznam souradnic cukraren, v tuto chvili nahodne, pozdeji skutecne
def priprav_cukrarny(kolik):
  seznam_cukraren = []
  for i in range(kolik):
    x,y = random.randint(0,LAT_MAX), random.randint(0,LAT_MAX)
    seznam_cukraren.append([x,y])
  return seznam_cukraren

#vytvorim si platno na kresleni
obrazek = Image.new('RGBA', (LAT_MAX, LAT_MAX))
platno = ImageDraw.Draw(obrazek)

# vytvorim seznam cukraren
seznam_cukraren = priprav_cukrarny(POCET_CUKRAREN)
print("Skutecne cukrarny:", seznam_cukraren)

# ted jsem v situaci, kdy mam pripravena data a chystam se resit muj problem
#Co dal? Potrebujeme spoustu nahodnych potencialnich cukraren a z nich vybrat tu, ktera bude mit nejvetsi vzdalenost od ostatnich
################################################
########        MONTE CARLO       ##############
################################################

#vytvarim si novy seznam, kam budu ukladat nejkratsi vzdalenost nahodne cukrarny od ostatnich cukraren
nejblizsi_cukrarny = []

for pokus in range(POKUSY): #kolik mam v konstante POKUSY, tolik se mi vytvori nahodnych cukraren
  # vyvtorim si nahodny bod pro potencialni cukrarnu
  x,y = random.randint(0,LAT_MAX), random.randint(0,LAT_MAX)

  #pridam nahodny bod na platno, jako hypotetickou cukrarnu
  platno.ellipse((x-3, y-3, x+3, y+3), fill = 'yellow', outline ='blue')

  # zmerim jeho vzdalenost od vsech cukraren
  # pripravim si na to prazdny seznam, kam budu ukladat vzdalenosti od opravdovych cukraren
  seznam_vzdalenosti = []

  # a do nej pridam cukrarnu a jeji vzdalenost od meho bodu
  for i in range(POCET_CUKRAREN):
    x2 = seznam_cukraren[i][0]
    y2 = seznam_cukraren[i][1]
    v = vzdalenost(x,y, x2,y2)
    seznam_vzdalenosti.append([v  ,    seznam_cukraren[i]      ])
    # po vypoctu seznam setridim, probehne setrideni sestupne podle prvni polozky a to ted chci
  seznam_vzdalenosti.sort()
  #print(seznam_vzdalenosti)
  print("Nejkratsi vzdalenost pro Novou cukrarnu c.", pokus, " na souradnicich ", x, y,":", seznam_vzdalenosti[0][0])
  # a protoze je vitezna, ulozim si ji do seznamu nejblizsich cukraren
  nejblizsi_cukrarny.append([seznam_vzdalenosti[0][0], x,y])

#uz se mi provedly vsechny pokusy
#ted ze seznamu tech nejblizsich cukraren, vyberu tu nejvzdalenejsi :)

#nejdriv si je setridim
nejblizsi_cukrarny.sort()

#pak ten seznam otocim
nejblizsi_cukrarny.reverse()

#a z tohoto seznamu je to ten nulty prvek, tedy ten s nejvetsi vzdalenosti od vseho
print(nejblizsi_cukrarny[0])

#pridam na platno puvodni cukrarny
for c in seznam_cukraren:
  x = c[0]
  y = c[1]
  platno.ellipse((x-5, y-5, x+5, y+5), fill = 'red', outline ='black')

#pridam na platno viteznou nahodnou cukrarnu
x = nejblizsi_cukrarny[0][1]
y = nejblizsi_cukrarny[0][2]
platno.ellipse((x-5, y-5, x+5, y+5), fill = 'blue', outline ='blue')

#vykreslim samotny obrazek na obrazovku
print("Modra - vitezna, Zluta - nahodna, Cervena - opravdova")
obrazek.show() #pokud chcete obrazek ulozit: obrazek.save("obrazek.jpg") pokud jen ukazat obrazek.show()
