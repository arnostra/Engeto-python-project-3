# Enegto project 3

# Popis projektu

Tento projekt slouží k vyscrapování výsledků z parlamentních voleb v roce 2017. 

# Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít virtuální prostředí a s nainstalovaným manažerem

```commandline
$ pip install -r requirements.txt  # nainstalujeme knihovny
```

# Spuštění projektu

Spuštěním souboru election_scraper.py v rámci příkazového řádku požaduje dva povinné argumenty.

```commandline
python election_scraper.py <odkaz-na-uzemní-celek> <název-města>
```

Následně se vám stáhnou výsledky jako soubor s příponou `.csv`

# Ukázka projektu

Výsledky hlasování pro okres Benešov:
    
1. argument: 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101'
2. argument: `benesov`

Spuštění programu:

python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" benesov


Průběh stahování:

```commandline
Downloading data from selected URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
Saving data to file: vysledky_benesov.csv
All done, closing...
```

Částečný výstup:

```commandline
Code,Location,Registered,Envelopes,Valid,...
529303,Benešov,13104,8476,8437,1052,10,2,624,3,802,597,109,35,112,6,11,948,3,6,414,2577,3,21,314,5,58,17,16,682,10
532568,Bernartice,191,148,148,4,0,0,17,0,6,7,1,4,0,0,0,7,0,0,3,39,0,0,37,0,3,0,0,20,0
532380,Blažejovice,96,80,77,6,0,0,5,0,3,11,0,0,3,0,0,5,1,0,0,29,0,0,6,0,0,0,0,8,0
...
```
