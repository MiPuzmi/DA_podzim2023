import json

with open ("dataset_crawler-google-places_2023-10-01_17-02-30-942.json", encoding='utf8') as file:
    cukrarny = json.load(file)

for data in cukrarny:
    adresa = data['url'].split('@')
    adresa = adresa[1].split(',')
    latitude = float(adresa[0])
    longitude = float(adresa[1])
    data['latitude'] = latitude
    data['longitude'] = longitude
    

with open('souradnice_google_cukrarny.json', mode= 'w', encoding='utf8') as f:
    json.dump(cukrarny, f, indent=4, ensure_ascii=False)