import pridobi
import izlusci
import shrani
import sys


pridobi_podatke = len(sys.argv) == 2 and sys.argv[1] == "pridobi"

if (len(sys.argv) > 2) or (len(sys.argv) == 2 and sys.argv[1] != "pridobi"):
    print("Uporaba: python3 main.py pridobi")
    sys.exit(1)

if pridobi_podatke:
    pridobi.preuzimanje_glavne_stran()

companies_basic_data = izlusci.izlusci_companies_basic_data()

if pridobi_podatke:
    pridobi.preuzimanje_statistics_strani(companies_basic_data)
    pridobi.preuzimanje_history_strani(companies_basic_data)

all_companies_data = izlusci.izlusci_vse_companies_data(companies_basic_data)
all_history_data = izlusci.izlusci_vse_history(companies_basic_data)

shrani.shrani_companies(all_companies_data)
shrani.shrani_history(all_history_data)


if pridobi_podatke:
    print("Podatki so pridobljeni, obdelani in shranjeni.")
else:
    print("Lokalni podatki so bili obdelani in shranjeni.")












