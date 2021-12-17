# Vzdálenost ke kontejnerům na tříděný odpad

Program zjistí průměrnou a maximální vzdálenost z adresního bodu ke kontejneru na tříděný odpad. Pro maximální vzdálenost vypíše název ulice, číslo domu a vzdálenost, ze které adresy je to ke kontejneru nejdále.

Funkčnost programu je podmíněna 2 vstupními soubory typu GEOJSON. Jeden s adresními body, které lze získat na následujícím odkazu: http://overpass-turbo.eu/. Druhý soubor musí nést informace o kontejnerech na tříděný odpad, pro Prahu dostupný zde: https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB.

## Stručný popis chodu programu
Program projde postupně všechny adresy, ke kterým najde vdálenost k nejbližšímu kontejneru. Pro každou adresu se tak najde nejbližší kontejner. Vzdálenost každé adresy k jejímu nejbližšímu kontejneru je průběžně načítána. Po načtení všech minimálních vzdáleností se výsledek zprůměruje a je vypsán do konzole.
Během chodu pogramu se minimální vzdálenosti mezi sebou porovnávají, ze kterých vzejde nejdelší vzdálenost ke kontejneru. Spolu s touto nejdelší vzdáleností program vypíše i název ulice a číslo popisné adresního bodu, pro který je ona vzdálenost nejdelší. 
