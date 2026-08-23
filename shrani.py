import csv

def shrani_companies(all_companies_data):
    with open("companies.csv", "w", newline="", encoding="utf-8") as file:
        stolpci = all_companies_data[0].keys()
        pisatelj = csv.DictWriter(file, fieldnames = stolpci)

        pisatelj.writeheader()
        pisatelj.writerows(all_companies_data)

def shrani_history(all_history_data):
    with open("prices.csv", "w", newline="",
              encoding="utf-8") as file:
        stolpci = all_history_data[0].keys()

        pisatelj = csv.DictWriter(file, fieldnames= stolpci)

        pisatelj.writeheader()
        pisatelj.writerows(all_history_data)
        

       



    