import json
from pyproj import Transformer
from math import sqrt
from typing import Final
from json.decoder import JSONDecodeError

wgs2jtsk = Transformer.from_crs(4326,5514, always_xy=True)

def open_load (name):
    """# Otevírá soubor typu json 
    - do parametru se zadá název souboru včetně uvozovek např. "soubor.json"
    - vrací obsah souboru"""
    try:
        with open(name, encoding="utf-8") as geojsonfile:
            reader = json.load(geojsonfile)
        return reader
    
    except FileNotFoundError:
        print(f"Soubor {name} se nepodařilo najít.")
        exit()
    except PermissionError:
        print(f"Soubor {name} není programu přístupný.")
        exit()
    except JSONDecodeError:
        print(f"Soubor {name} je prázdný.")
        exit()

def choose_containers (data_c):
    """# Vytvoření slovníku kontejnerů
    - pokud cyklus narazí v "properties na položku "PRISTUP", 
    ve které je hodnota "volně" -> zapíše vybrané vlastnosti: 
    ID, ulice, souřadnice daného kontejneru do slovníku"""
    chosen_cont = {}        # slovník pro kontejnery
    counter_free = 0
    for cont in data_c ["features"]:
        if len(cont["geometry"]["coordinates"]) != 2:
            print(f"Kontejneru: {cont['properties']['ID']} chybí jedna nebo obě souřadnice. Kontejner přeskakuji.")
            continue
        if (cont ["properties"] ["PRISTUP"] == "volně"):
            chosen_cont[cont["properties"]["ID"]] = {\
            "street_name": cont["properties"]["STATIONNAME"],\
            "type": cont["properties"]["PRISTUP"],\
            "coordinates": [float(cont["geometry"]["coordinates"][0]), 
                            float(cont["geometry"]["coordinates"][1])
                        ]}
            counter_free += 1
    if counter_free == 0:
        print("Soubor s kontejnery nemá ani jeden kontejner veřejný")
        exit()
    return chosen_cont

def choose_address (data_a):
    """# Vytvoření slovníku adres
    - zapíše do slovníku vybrané vlastnosti adresy: ID, číslo domu, ulice, souřadnice
    ## přehled jak vypadá strktura přepsaných adres
    "id":
    {
        "housenumber": hodnota,
        "street": hodnota,
        "coordinates": hodnota
    }
    """
    chosen_adr = {}         # založení slovníku pro adresy
    for adr in data_a ["features"]: 
        try:  
            chosen_adr[adr["properties"]["@id"]] = {\
                "housenumber": adr["properties"]["addr:housenumber"],\
                "street": adr["properties"]["addr:street"],\
                "coordinates": transfer_coor(float(adr["geometry"]["coordinates"][0]), float(adr["geometry"]["coordinates"][1]))}
        except IndexError:
            print(f"Adresnímu bodu: {adr['id']} chybí jedna nebo obě souřadnice. Adresu přeskakuji.")
            continue
    return chosen_adr

def transfer_coor (x,y):
    """# Převod souřadnicového systému z WGS84 do JTSK
    - vrátí dvojici čísel x a y v souřadnicovém systému JTSK"""
    return wgs2jtsk.transform(x,y)
        
MAX_LIMIT: Final = 10000

def load_coor (path, position0 = 0, position1 = 1):
    """## Načtení souřadnic bodu
    - vrátí dvojici čísel"""
    x= path[position0]
    y= path[position1]
    return (x,y)

def distance (point0, point1):
    """# Výpočet vzdálenosti mezi 2 body
    -do parametru vstupují proměnné jakožto dvojice čísel"""
    dist = sqrt((point0[0]-point1[0])**2+(point0[1]-point1[1])**2)
    return dist
