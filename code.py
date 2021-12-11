import json
from math import sqrt
from pyproj import Transformer

def open_load (name):
# otevírá soubor typu json 
# do parametru name se zadá název souboru včetně uvozovek např. "soubor.json" 
    try:
        with open(name, encoding="utf-8") as geojsonfile:
            reader = json.load(geojsonfile)
        return reader
    except IOError:
        print("Soubor se nepodařilo najít")
        exit()

def transfer_coor (x=0,y=0):
    wgs2jtsk = Transformer.from_crs(4326,5514, always_xy=True)
    return wgs2jtsk.transform(x,y)

chosen = []
counter_public = 0
counter = 0

containers = open_load("kontejnery.geojson")
for cont in containers ["features"]:
        counter += 1
        if (cont ["properties"] ["PRISTUP"] == "volně"):
            chosen.append(cont) 
            counter_public += 1
print(f"Načteno {counter} kontejnerů na tříděný odpad")
print(f"{counter_public} kontejnerů je veřejných")

adress_list = {}
"""
"id":
{
    "housenumber": hodnota,
    "street": hodnota,
    "coordinates": hodnota
}
"""
adress = open_load("adresy.geojson")
for adr in adress ["features"]:
    adress_list[adr["properties"]["@id"]] = {\
        "housenumber": adr["properties"]["addr:housenumber"],\
        "street": adr["properties"]["addr:street"],\
        "coordinates": transfer_coor(adr["geometry"]["coordinates"][0], adr["geometry"]["coordinates"][1])}

print(adress_list)
#print(adress_list["node/290026925"]["coordinates"])

# jen pro ověření správného výběru kontejnerů
'''for i in chosen:
    print(i["properties"]["PRISTUP"])'''
