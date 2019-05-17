import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
import pandas as pd

result = []

for x in range(1, 10):
    page = requests.get(
        'https://www.euroauctionslive.com/servlet/Search.do?auctionId=475&page=' + str(x) + '&perPage=100&orderBy=')

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find(class_='item-listing')

    table_rows = table.find_all('tr')

    title_result = []
    price_result = []
    link_result = []

    for row in table_rows:
        title = row.find_all('h3')
        price = row.find_all('strong', {'style' : 'color: #00A'})
        for t in title:
            link = t.parent.get('href')
            title_result.append(t.text[33:-33])
            link_result.append('https://www.euroauctionslive.com' + link)
        for p in price:
            price_result.append(
                float(p.text[:-4].replace(',', '')))

    page_result = list(zip(title_result, price_result, link_result))
    result.extend(page_result)

df = pd.DataFrame(result, columns=["Title", "Price", "Link"])
print(df)
df.to_excel('auction.xlsx', engine='xlsxwriter', index=None, header=True)
