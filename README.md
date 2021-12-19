# Vzdálenost ke kontejnerům na tříděný odpad

## Využití programu
Program slouží jako jednoduchá analýza dostupnosti kontejnerů pro obyvatelstvo.
## Základní popis
Program zjistí průměrnou a maximální vzdálenost a medián z adresního bodu ke kontejneru na tříděný odpad. Pro maximální vzdálenost vypíše název ulice, číslo domu a vzdálenost, ze které adresy je to ke kontejneru nejdále.

### Otevření vstupních dat a načtení do slovníků
Funkčnost programu je podmíněna 2 vstupními soubory. Jeden s adresními body, které lze získat na následujícím [odkazu](http://overpass-turbo.eu/). Druhý soubor musí nést informace o kontejnerech na tříděný odpad. Data pro Prahu jsou dostupná na stránkách [pražského geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB). Po stažení souborů je dobré se ujistit, že oba mají koncovku typu `.geojson` a jsou oba uloženy ve stejné složce, kde bude uložen kód programu. Vhodné je také přejmenovat soubor s adresami jako `adresy.geojson` a soubor s kontejnery jako `kontejnery.geojson`. Pokud se budou soubory jmenovat jinak, je nutné přepsat v kódu na řádku 5, nebo 6 ve funkci "*open_load*" jméno souboru.

  **Příklad**: `containers = open_load("soubor_adresy.geojson")`
  
Po otevření a načtení souborů pomocí funkce "*open_load()*" následuje uložení dat do slovníků, aby nemusely být vstupní programy otevřené po celou dobu běhu programu. K tomu slouží **funkce "*dict_address*" a "*dict_containers()*"**, které si z původních souborů berou jen některé atributy. Pro adresy se ukládá ID: `@id`, jméno ulice: `addr:street`, číslo popisné: `addr:housenumber` a souřadnice: `"coordinates"`. Pro kontejnery se ukládá ID: `ID`, jméno ulice: `"STATIONNAME"`, typ přístupu: `PRISTUP` a souřadnice: `"coordinates"`. V tomto kroku dochází také u adres k převedení souřadnicového systému z WGS-84 do S-JTSK pomocí funkce "*transfer_coor()*", která vrací dvojici čísel. Souřadnice kontejnerů jsou již ve vstupním souboru v systému S-JTSK.

Všechny funkce a jejich popis jsou v souboru **"*functions.py*"**.

### Stručný popis chodu programu
Program projde postupně všechny adresy, ke kterým najde vzdálenost k nejbližšímu kontejneru. Vzdálenost je vypočítána pomocí funkce "*distance()*", která počítá vzdálenost pomocí Pythagorovy věty.
Pro každou adresu se tak najde nejbližší kontejner. Vzdálenosti z každé adresy k jejímu nejbližšímu kontejneru jsou průběžně načítány. Jednotlivé nejmenší vzdálenosti pro každou adresu jsou také ukládány do seznamu pro výpočet mediánu. Po načtení všech minimálních vzdáleností se výsledek zprůměruje a je vypsán do konzole.
Během chodu pogramu se minimální vzdálenosti mezi sebou porovnávají, ze kterých vzejde nejdelší vzdálenost ke kontejneru. Spolu s touto nejdelší vzdáleností program vypíše i název ulice a číslo popisné adresního bodu, pro který je ona vzdálenost nejdelší. Program také na konci vytvoří nový soubor `adresy_kontejnery.geojson`, který nese vybrané atributy o všech vstupních adresách a navíc je k nim přidaný atribut `kontejner`, který nese informaci o ID nejbližšího kontejneru z dané adresy.

## Příklad vypsání výsledků
```
Načteno 5813 kontejnerů na tříděný odpad
        3438 kontejnerů je veřejných

Počet adresních bodů: 1899

Průměrná vzdálenost ke kontejneru je 135 m.
Nejdále ke kontejneru je z adresy Křižovnické náměstí 191/3 a to 330 m.
Medián vzdálenosti ke kontejnerům: 128 m.
```
