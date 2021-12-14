from math import sqrt
from functions import open_load, transfer_coor

# založení proměnných pro počet kontejnerů
# založení slovníku pro zapsání veřejných kontejnerů
counter = 0             # všechny kontejnery
counter_public = 0      # kontejnery s veřejným přístupem
chosen_cont = {}        # slovník pro veřejné kontejnery

containers = open_load("kontejnery.geojson")
#otevření a načtení souboru s kontejnery do proměnné containers
for cont in containers ["features"]:
# procházení proměnné containers ve "features"    
    counter += 1
    # při každém novém "features" přičte 1 do proměnné counter
    # načítá počet VŠECH kontejnerů
    if (cont ["properties"] ["PRISTUP"] == "volně"):
    # pokud cyklus narazí v "properties na položku "PRISTUP", 
    # ve které je hodnota "volně" -> zapíše vybrané vlastnosti: 
    # ID, ulice, souřadnice daného kontejneru do slovníku chosen_cont
        chosen_cont[cont["properties"]["ID"]] = {\
        "Street name": cont["properties"]["STATIONNAME"],\
        "Type": cont["properties"]["PRISTUP"],\
        "coordinates": [float(cont["geometry"]["coordinates"][0]), 
                        float(cont["geometry"]["coordinates"][1])
                       ]} 
        counter_public += 1
        # načítá počet VEŘEJNÝCH kontejnerů
# tisk počtu načtených kontejnerů    
print(f"Načteno {counter} kontejnerů na tříděný odpad")
print(f"        {counter_public} kontejnerů je veřejných\n")

# založení proměnnéh pro počet adresních bodů
# založení slovníku pro zapsání adres
counter_adr = 0
chosen_adr = {}

address = open_load("adresy.geojson")
#otevření a načtení souboru s adresními body do proměnné address
for adr in address ["features"]:
# procházení proměnné address ve "features"
# pro každou novou položku ve "features" uloží do slovníku chosen_adr 
# vybrané vlastnosti adresy: ID, číslo domu, ulice, souřadnice 
    chosen_adr[adr["properties"]["@id"]] = {\
        "housenumber": adr["properties"]["addr:housenumber"],\
        "street": adr["properties"]["addr:street"],\
        "coordinates": transfer_coor(float(adr["geometry"]["coordinates"][0]), float(adr["geometry"]["coordinates"][1]))}
    if adr["properties"]:
        counter_adr += 1
        # načítá počet adres
#přehled jak vypadá strktura přepsaných adres
"""
"id":
{
    "housenumber": hodnota,
    "street": hodnota,
    "coordinates": hodnota
}
"""
# tisk počtu adresních bodů
print(f"počet adresních bodů: {counter_adr}\n")

# založení proměnných pro zjistění nejkratší vzdálenosti (min_dist),
# nejdelší vzdálenosti (max_dist) a součet nejkratších vzdáleností(sum_dist)
min_dist = 100000
max_dist = 0
sum_dist = 0
for coor_adresa in chosen_adr:
    #procházení slovníku adres pro uložení polohy adresy
    X=chosen_adr[coor_adresa]["coordinates"][0]
    Y=chosen_adr[coor_adresa]["coordinates"][1]
    for kont in chosen_cont:
        #peocházení slovníku kontejnerů pro uložení polohy
        X2=chosen_cont[kont]["coordinates"][0]
        Y2=chosen_cont[kont]["coordinates"][1]
        cal_dist = sqrt((X-X2)**2+(Y-Y2)**2)
        # výpočet vzdálenosti mezi adresním bodem a kontejnerem
        if cal_dist < min_dist:
            # pokud je vypočtená vzdálenost menší než dosavadní minimální vzdálenost,
            # přeuloží se aktuální vypočtená vzdálenost do proměnné min_dist,
            # která reperezentuje nejkratší vzdálenost pro danou adresu ke kontejneru
            min_dist = cal_dist
    # poté, co se projde celý slovník kontejnerů
    sum_dist += min_dist
    # načítá nejmenší nalezenou vzdálenost z dané adresy ke kontejneru

    if min_dist > max_dist:
        # pokud je aktuální minimální vzdálenost větší než největší 
        # uložená maximální vzdálenost, uloží se do proměnné max_dist nová největší vzdálenost
        max_dist = min_dist
        # do proměnných níže se uloží jméno ulice a číslo domu
        max_street = chosen_adr[coor_adresa]["street"]
        max_hnumber = chosen_adr[coor_adresa]["housenumber"]

# v proměnné result se uloží průměrná vzdálenost k nejbližšímu kontejneru
result = int(sum_dist/counter_adr)
print(f"Průměrná vzdálenost ke kontejneru je {result} m.")
print(f"Nejdale ke kontejneru je z adresy {max_street} {max_hnumber} a to {max_dist:.0f} m.\n")
