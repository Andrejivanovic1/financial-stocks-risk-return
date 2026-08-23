# Finančne delnice – analiza tveganja in donosnosti

Projekt analizira 50 večjih družb iz finančnega sektorja. Podatki so pridobljeni s spletne strani StockAnalysis in vključujejo temeljne finančne kazalnike ter približno šest mesecev zgodovinskih podatkov o cenah delnic.

## Namen projekta

Glavni cilj projekta je analizirati razmerje med donosnostjo in tveganjem finančnih delnic ter primerjati njihovo tržno obnašanje.

Analiza vključuje:
- donosnost delnic,
- volatilnost,
- Sharpejevo razmerje,
- VaR in CVaR,
- korelacije med donosnostmi,
- povezavo med nekaterimi temeljnimi kazalniki in tržnim tveganjem.

## Datoteke

- `pridobi.py` – pridobivanje podatkov s spleta,
- `izlusci.py` – izluščanje podatkov iz HTML datotek,
- `shrani.py` – shranjevanje podatkov v CSV datoteke,
- `main.py` – glavni program,
- `companies.csv` – podatki o podjetjih,
- `prices.csv` – zgodovinske cene delnic,
- `analiza.ipynb` – analiza in vizualizacija podatkov.


## Namestitev

Za izvajanje projekta potrebujete Python 3, Google Chrome in okolje za uporabo
Jupyter Notebooka.

Projekt uporablja naslednje Python knjižnice:

- `requests`,
- `beautifulsoup4`,
- `selenium`,
- `pandas`,
- `numpy`,
- `matplotlib`

Potrebne knjižnice lahko namestite z ukazom:
```bash 
pip install -r requirements.txt
```

## Uporaba

### Analiza že zbranih podatkov

Repozitorij že vsebuje datoteki `companies.csv` in `prices.csv`, zato za ogled
analize ni potrebno ponovno pridobivanje podatkov s spleta.

1. Odprite datoteko `analiza.ipynb`.
2. V Jupyter Notebooku izberite možnost Run All.
3. Vse celice se bodo izvedle po vrsti, rezultati in grafi pa se bodo prikazali tudi.
   
### Ponovno pridobivanje podatkov

Če želite pridobiti nove podatke s spletne strani StockAnalysis, v terminalu
v mapi projekta zaženite:

```bash
python3 main.py pridobi
```

Program pridobi podatke s spleta, jih obdela ter ponovno ustvari datoteki
`companies.csv` in `prices.csv`.

Pri pridobivanju zgodovinskih podatkov program uporablja Selenium, zato se med
izvajanjem samodejno odpre Google Chrome. Postopek lahko traja nekaj časa.

Po končanem pridobivanju podatkov lahko ponovno odprete `analiza.ipynb` in
izberete možnost Run All.


## Uporaba umetne inteligence

Umetno inteligenco sem pri projektu uporabil na nekaj mestih kot pomoč pri razvoju in urejanju projekta.

Uporabil sem jo za:

1. Funkcijo `preuzimanje_history_strani()`. Prvotno različico funkcije sem napisal sam, vendar ni delovala dovolj zanesljivo. Večkrat sem jo poskušal popraviti, nato pa sem za pomoč prosil umetno inteligenco. Moja prvotna različica kode je še vedno na voljo v datoteki `selenium_test.py`.

2. Slovar `important_statistics` v datoteki `izlusci.py`. Sam sem izbral podatke, ki sem jih želel vključiti v analizo, umetni inteligenci pa sem naročil, naj iz njih sestavi slovar in določi ustrezna skrajšana imena (ker jih je bilo okoli 20).

3. Kodo v knjižnici `matplotlib`, s katero sem na grafu razmerja med volatilnostjo in donosnostjo označil deset izbranih točk z njihovimi oznakami delnic oziroma tickerji.

4. Kodo za grafični prikaz korelacijske matrike z uporabo barv.

5. Delno urejanje in izboljšanje besedila v Jupyter Notebooku.