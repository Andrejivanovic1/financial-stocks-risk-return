import requests
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://stockanalysis.com/stocks/sector/financials/"

HEADERS = {"User-Agent": "Mozilla/5.0"}


def preuzimanje_glavne_stran():
    response = requests.get(URL, headers=HEADERS)

    if response.status_code != 200:
        print("Napaka:", response.status_code)
        return

    response.encoding = "utf-8"

    with open("htmlji/financials.html", "w", encoding="utf-8") as file:
        file.write(response.text)

def preuzimanje_statistics_strani(companies_basic_data):
    for company in companies_basic_data:
        statistics_url = company["link"] + "statistics/"
        ticker = company["ticker"]

        response = requests.get(statistics_url, headers=HEADERS)
        if response.status_code != 200:
            print("Napaka:", response.status_code)
            continue
        response.encoding = "utf-8"

        with open(f"htmlji/statistics/{ticker}_statistics.html", "w", encoding="utf-8") as file:
            file.write(response.text)

        time.sleep(0.5)

def preuzimanje_history_strani(companies_basic_data):

    def prvi_datum(driver):
        return driver.execute_script("""
            const rows = document.querySelectorAll("table tr");

            for (const row of rows) {
                const cells = row.querySelectorAll("td");

                if (cells.length === 8) {
                    return cells[0].innerText.trim();
                }
            }

            return null;
        """)


    for company in companies_basic_data:
        ticker = company["ticker"]
        history_url = company["link"] + "history/"

        driver = webdriver.Chrome()

        try:
            driver.get(history_url)

            # Cekamo da se prva tabela ucita
            datum = prvi_datum(driver)
            pokusaji = 0

            while datum is None and pokusaji < 20:
                time.sleep(1)
                datum = prvi_datum(driver)
                pokusaji += 1

            if datum is None:
                print("Tabela se ni nalozila:", ticker)
                continue


            for stran in range(1, 4):

                html = driver.execute_script(
                    "return document.documentElement.outerHTML;"
                )

                with open(
                    f"htmlji/history/{ticker}_history_{stran}.html",
                    "w",
                    encoding="utf-8"
                ) as file:
                    file.write(html)


                if stran == 3:
                    break


                stari_datum = prvi_datum(driver)


                klik = driver.execute_script("""
                    const elements = document.querySelectorAll(
                        'button, a, [role="button"]'
                    );

                    for (const element of elements) {

                        const label =
                            (element.getAttribute("aria-label") || "")
                            .trim()
                            .toLowerCase();

                        const title =
                            (element.getAttribute("title") || "")
                            .trim()
                            .toLowerCase();

                        const text =
                            (element.innerText || "")
                            .trim()
                            .toLowerCase();

                        if (
                            label === "next" ||
                            title === "next" ||
                            text === "next"
                        ) {
                            element.click();
                            return true;
                        }
                    }

                    return false;
                """)


                if not klik:
                    print("Next ni najden:", ticker, stran)
                    break


                # Cekamo da se prvi datum promeni
                novi_datum = prvi_datum(driver)
                pokusaji = 0

                while (
                    (novi_datum is None or novi_datum == stari_datum)
                    and pokusaji < 20
                ):
                    time.sleep(1)
                    novi_datum = prvi_datum(driver)
                    pokusaji += 1


                if novi_datum is None or novi_datum == stari_datum:
                    print("Stran se ni spremenila:", ticker, stran)
                    break


            print("Preuzet history za:", ticker)

        finally:
            driver.quit()

        time.sleep(1)