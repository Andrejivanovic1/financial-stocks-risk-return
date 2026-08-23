from bs4 import BeautifulSoup
import re

BASE_URL = "https://stockanalysis.com" # to ni glavna stran, to je samo orodje za posamezne linkove

def pretvori_v_milijarde(value):
    """Funkcija katera sprejme string kot stevilo s crkom na koncu,
    in potem vrne float u milijardama"""
    number = float(value[:-1])
    unit = value[-1]

    if unit == "B":
        return number
    elif unit == "T":
        return number * 1000
    elif unit == "M":
        return number / 1000


def izlusci_companies_basic_data():
    companies_basic_data = []
    with open("htmlji/financials.html", "r", encoding="utf-8") as file:
        vsebina = file.read()

    soup = BeautifulSoup(vsebina, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    companies = rows[1:51]  # ker prvi row ni firma (temvec margina), gledamo od drugega naprej

    for company in companies:
        cells = company.find_all("td")

        ticker = cells[1].text
        link = BASE_URL + cells[1].find("a")["href"]
        company_name = cells[2].text
        market_cap = cells[3].text
        change = cells[4].text
        volume = cells[5].text
        revenue = cells[6].text

        change_decimal = round(float(change[:-1]) / 100, 4)
        volume = int(volume.replace(",", ""))

        basic_data = {
                "ticker": ticker,
                "company_name": company_name,
                "link": link,
                "market_cap_B": pretvori_v_milijarde(market_cap),
                "change": change_decimal,
                "volume": volume,
                "revenue_B": pretvori_v_milijarde(revenue)
            }
        companies_basic_data.append(basic_data)
    return companies_basic_data

def izlusci_vse_statistics(soup):
    """Sprejme juhu in potem iz nje izlusci vse statistike s strani,
    ampak, kasneje mi bomo zbrali samo nekatere"""
    statistics = {}
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2: # Provera, da je to vrstica katero potrebujemo
                name = cells[0].text.strip()
                value = cells[1].text.strip()

                statistics[name] = clean_value(value)
    return statistics

def clean_value(value):
    
    value = value.strip().replace("," , "")
    if value == "n/a" or value == "N/A" or value == "-":
        return None
    elif value.endswith("%"):
        return float(value[:-1]) / 100
    elif "$" in value:
        if value[0] == "$":
            value = value[1:]
        elif value[1] == "$":
            value = value[0] + value[2:]
    if value[-1] in "MBT":
        return pretvori_v_milijarde(value)
    if value[0] in "QWERTYUIOPASDFGHJKLZXCVBNM":
        return value

    try:
        if "." not in value:
            return int(value)
        else:
            return float(value)
    except ValueError:
        return value

def izlusci_company_statistics(ticker):
    with open(f"htmlji/statistics/{ticker}_statistics.html", "r", encoding="utf-8") as file:
        vsebina = file.read()

        soup = BeautifulSoup(vsebina, "html.parser")

        return izlusci_vse_statistics(soup)


important_statistics = {  # od tistih 100 parametrov mi bomo uzeli okoli 20 najbolj
    # pomembnih za naso kasnejso analizo
     
    # Valuation ratios
    "PE Ratio": "pe_ratio",
    "Forward PE": "forward_pe",
    "PB Ratio": "pb_ratio",
    "PEG Ratio": "peg_ratio",
    "Earnings Yield": "earnings_yield",
    # Financial Efficency
    "Return on Equity (ROE)": "roe",
    "Return on Assets (ROA)": "roa",
    "Operating Margin": "operating_margin",
    "Profit Margin": "profit_margin",
    "Earnings Per Share (EPS)": "eps",
    # Stock Price Statistics
    "Beta (5Y)": "beta",
    "52-Week Price Change": "price_change_52w",
    "Relative Strength Index (RSI)": "rsi",
    "Short % of Float": "short_percent_float",
    "Short Ratio (days to cover)": "short_ratio",
    # Balance Sheet
    "Cash & Cash Equivalents": "cash_B",
    "Total Debt": "total_debt_B",
    "Equity (Book Value)": "equity_B",
    "Book Value Per Share": "book_value_per_share",
    # Dividends and Yields
    "Dividend Yield": "dividend_yield",
    "Dividend Growth (YoY)": "dividend_growth",
    "Payout Ratio": "payout_ratio",
    "Buyback Yield": "buyback_yield",
    "Shareholder Yield": "shareholder_yield",
    # Analyst Forecast
    "Price Target Difference": "price_target_difference",
    "Analyst Consensus": "analyst_consensus",
    "Analyst Count": "analyst_count",
    "Revenue Growth Forecast (3Y)": "revenue_growth_forecast_3y",
    "EPS Growth Forecast (3Y)": "eps_growth_forecast_3y"}

def izbrane_statistics(statistics):
    """pravimo nov dict le s pomembnim parametrima in delamo zamenjavo
    imena kljucev v python vibe-u"""
    selected_statistics = {}

    for key in important_statistics:
        selected_statistics[important_statistics[key]] = statistics[key]
    return selected_statistics

def izlusci_vse_companies_data(companies_basic_data):
    """glavna f-ja katera zacne vse iz tistega file-a"""
    all_companies_data = []
    for company in companies_basic_data:
        a = izbrane_statistics(izlusci_company_statistics(company["ticker"]))
        company.update(a)
        all_companies_data.append(company)
    return all_companies_data


def test_history_stran(companies_basic_data): # tu sem videl da se URL ne spreminja ko spreminjamo stran(na "Next"), torej tista funkcija ni vec pomembna
    """Da preveri koliko tabela ima vrstic na prvem history page-u"""
    ticker = companies_basic_data[1]["ticker"]
    history_link = companies_basic_data[1]["link"] + "history/"

    with open(f"htmlji/history/{ticker}_history_1.html", "r", encoding="utf-8") as file:
        vsebina = file.read()
    soup = BeautifulSoup(vsebina, "html.parser")
    tables = soup.find_all("table")
    rows = tables[0].find_all("tr")

    return (len(tables), len(rows))

def izlusci_vse_history(companies_basic_data):
    all_history_data = []
    for company in companies_basic_data:
        ticker = company["ticker"]

        for stran in range(1, 4):
            with open(f"htmlji/history/{ticker}_history_{stran}.html",
                      "r", encoding="utf-8") as file:
                vsebina = file.read()
            soup = BeautifulSoup(vsebina, "html.parser")
            table = soup.find("table")
            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all("td")

                if len(cells) != 8:
                    continue
                date = cells[0].text.strip()
                for i in range(1,len(cells)):
                    cells[i] = clean_value(cells[i].text.strip())

                history_data = {
                    "ticker": ticker,
                    "date": date,
                    "open": cells[1],
                    "high": cells[2],
                    "low": cells[3],
                    "close": cells[4],
                    "adj_close": cells[5],
                    "change": cells[6],
                    "volume": cells[7],
                }
                all_history_data.append(history_data)
    return all_history_data

def test_history(ticker):
    for stran in range(1, 4):
        with open(
            f"htmlji/history/{ticker}_history_{stran}.html",
            "r",
            encoding="utf-8"
        ) as file:
            vsebina = file.read()

        soup = BeautifulSoup(vsebina, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")

        print(stran, len(rows))




    

