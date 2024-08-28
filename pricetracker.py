from bs4 import BeautifulSoup
import requests 
import numpy as np
import csv
from datetime import datetime


LINK = "https://www.amazon.se/s?k=speaker&crid=1Q140QSPCRC28&sprefix=speaker%2Caps%2C122&ref=nb_sb_ss_pltr-data-refreshed_1_7"

def get_prices_by_link(link):
    # Sending request To amazaon
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    r = requests.get(link, headers=headers)
    
    # Parsring the sourceCode
    page_parse = BeautifulSoup(r.text, 'html.parser')
    
    # getting all the prices 
    item_prices = []
    

    price_tags = page_parse.find_all("span", {"class": "a-price-whole"})
    
    for price_tag in price_tags:
        whole_price = price_tag.text.strip().replace(",", "")
        fraction_price = price_tag.find_next("span", {"class": "a-price-fraction"}).text.strip()
        price_as_text = whole_price + "." + fraction_price
        try:
            price = float(price_as_text)
            item_prices.append(price)
        except ValueError:
            continue
    
    return item_prices

def remove_outliers(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def get_average(prices):
    return np.mean(prices)

def save_to_file(prices):
    fields = [datetime.today().strftime("%B-%d-%Y"), np.around(get_average(prices), 2)]
    with open('prices_amazon.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == "__main__":
    prices = get_prices_by_link(LINK)
    prices_without_outliers = remove_outliers(prices)
    print(get_average(prices_without_outliers))
    save_to_file(prices)