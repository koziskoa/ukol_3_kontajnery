import json
from pyproj import Transformer

def open_load (name):
# otevírá soubor typu json 
# do parametru name se zadá název souboru včetně uvozovek např. "soubor.json" 
    try:
        with open(name, encoding="utf-8") as geojsonfile:
            reader = json.load(geojsonfile)
        return reader
    except ValueError:
        print("Soubor je chybný.")
        exit()
    except FileNotFoundError:
        print("Soubor se nepodařilo najít.")
        exit()
    except PermissionError:
        print("Soubor není programu přístupný.")
        exit()

def transfer_coor (x,y):
# převod souřadnicového systému z WGS84 do JTSK
# do paramteru x se uvede zeměpisná délka - např. 14.1564
# do paramteru y se uveede zaměpisná šířka - např. 50.1481
# funkce vrátí dvojici čísel x a y v souřadnicovém systému JTSK
# např. x = -741687.450 a y = -1044981.860
    wgs2jtsk = Transformer.from_crs(4326,5514, always_xy=True)
    return wgs2jtsk.transform(x,y)