from math import inf
from functions import choose_address, choose_containers, distance, load_coor, new_geojson, open_load, new_geojson, MAX_LIMIT
from statistics import median
# načtení souborů a uložení do slovníků
containers = open_load("kontejnery.geojson") 
address = open_load("adresy.geojson")
dict_containers = choose_containers(containers)
dict_address = choose_address(address)

# počet kontejnerů a adresních bodů
counter = len(containers["features"])
counter_public = len(dict_containers)
counter_adr = len(dict_address)

# založení proměnných pro: 
short_dist = float(inf)     #nejkratší vzdálenosti
long_dist = 0               #nejdelší vzdálenosti
sum_dist = 0                #součet nejkratších vzdáleností
short_list = []             #seznam nejkratších vzdáleností
dict_adr_cont = {}
for coor_adresa in dict_address:
    #procházení slovníku adres pro uložení polohy adresy
    adr_point = load_coor(dict_address[coor_adresa]["coordinates"])
    for kont in dict_containers.keys():
        #procházení slovníku kontejnerů pro aktuální uložení polohy a id
        id = kont
        cont_point = load_coor(dict_containers[kont]["coordinates"])
        cal_dist = distance(adr_point,cont_point)
        if cal_dist < short_dist:
            short_dist = cal_dist     # reperezentuje nejkratší vzdálenost pro danou adresu ke kontejneru
            id_kont = id

    sum_dist += short_dist
    short_list.append(short_dist)
    dict_adr_cont[coor_adresa] = {\
        "hnumber": dict_address[coor_adresa]["housenumber"],\
        "street": dict_address[coor_adresa]["street"],\
        "coor": dict_address[coor_adresa]["coordinates"],\
        "kontejner": id_kont,\
            }
    if short_dist > long_dist:
        # pokud je aktuální minimální vzdálenost větší než největší 
        # uložená maximální vzdálenost, uloží se do proměnné max_dist nová největší vzdálenost
        long_dist = short_dist
        max_street = dict_address[coor_adresa]["street"]
        max_hnumber = dict_address[coor_adresa]["housenumber"]
    if short_dist > MAX_LIMIT:
        print("Vzdálenost k nejbližšímu kontejneru je větší než 10 km")
        quit()
    short_dist = float(inf)
    
result = int(sum_dist/counter_adr)      # průměrná vzdálenost       
med = median(short_list)
print(f"Načteno {counter} kontejnerů na tříděný odpad")
print(f"        {counter_public} kontejnerů je veřejných\n")
print(f"Počet adresních bodů: {counter_adr}\n")
print(f"Průměrná vzdálenost ke kontejneru je {result} m.")
print(f"Nejdale ke kontejneru je z adresy {max_street} {max_hnumber} a to {long_dist:.0f} m.")
print(f"Medián vzdálenosti ke kontejnerům: {med:.0f} m.\n")
print(dict_adr_cont)
new_geojson(dict_adr_cont)