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

## Uporaba

Za obdelavo že prenesenih podatkov:

```bash
python3 main.py