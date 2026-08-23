import pridobi
import izlusci
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def prvi_datum(driver):
    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    cells = rows[1].find_elements(By.TAG_NAME, "td")
    return cells[0].text.strip()

def preuzimanje_history_strani_2(companies_basic_data):

    for company in companies_basic_data:
        ticker = company["ticker"]
        history_url = company["link"] + "history/"

        driver = webdriver.Chrome()

        driver.get(history_url)
        time.sleep(5)

        for stran in range(1,4):
            stari_datum = prvi_datum(driver)
            html = driver.execute_script("return document.documentElement.outerHTML;")
            with open(f"selenijum_test/{ticker}_{stran}.html", "w", encoding="utf-8") as file:
                file.write(html)

                if stran == 3:
                    break
                next_buttons = driver.find_elements(By.CSS_SELECTOR,'button[aria-label="Next"]')

                for button in next_buttons:
                     if button.is_displayed() and button.is_enabled():
                            button.click()
                            break
                poskusi = 0

                while stari_datum == prvi_datum(driver) and poskusi < 30:
                    time.sleep(1)
                    poskusi += 1
                
        driver.quit()

companies_basic_data = izlusci.izlusci_companies_basic_data()

#preuzimanje_history_strani_2(companies_basic_data[:5])






        




        


