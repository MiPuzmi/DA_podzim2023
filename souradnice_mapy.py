import requests
import pandas as pd

url = 'https://api.mapy.cz/v1/rgeocode'

api_klic = 'eyJpIjoyNTcsImMiOjE2Njc0ODU2MjN9.c_UlvdpHGTI_Jb-TNMYlDYuIkCLJaUpi911RdlwPsAY'

lang = 'cs'

headers = {
"Origin": "https://pro.mapy.cz",
"Referer": "https://pro.mapy.cz/",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-site",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def rgeo(lon: float, lat: float) -> tuple[str, str]: 
    r = requests.get(url, headers=headers, params={
        'lang': lang,
    'lon': lon,
    'lat': lat,
    'apikey': api_klic,
    })
    # print(r.status_code, r.reason)
    data = r.json()

    return data

with open ('novy_grid.csv', encoding='utf8') as f:
    dataset = f.readlines()

# print(dataset)

new_dataset = dataset[0].strip().split(',')

for row in dataset[1:10]:
    row = row.strip().split(',')
    lat = float(row[1])
    lon = float(row[2])
    data = rgeo(lon, lat)
    for i in data['items'][0]['regionalStructure']:
        if i['type'] == 'regional.municipality_part':
            row.append(i['name'])
    if 'zip' in data['items'][0]:        
        row.append(data['items'][0]['zip'])
    new_dataset.append(row)

print(new_dataset) 